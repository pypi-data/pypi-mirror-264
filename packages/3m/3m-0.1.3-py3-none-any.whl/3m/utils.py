import os
import sys
import numpy as np
from typing import Union

import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
from langchain.text_splitter import CharacterTextSplitter
import faiss
from PIL import Image
import openai
from dataclasses import dataclass, asdict
from stqdm import stqdm
import re
import base64
from pathlib import Path

import concurrent.futures
import time

liqa_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(liqa_dir)


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text,chunk_size,chunk_overlap):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks,e_model):
    
    if type(e_model)==str: # 判断本地模型还是在线
        if type(text_chunks)!=str: #判断单个还是一组 如果是多个
            embeddings=[]
            for text_chunk in stqdm(text_chunks):
                response=openai.Embedding.create(
                        input=text_chunk,
                        model="text-embedding-ada-002")
                embeddings.append(response['data'][0]['embedding'])
            embeddings = np.vstack(embeddings).astype('float32')
        else:
            response=openai.Embedding.create(
                        input=text_chunks,
                        model="text-embedding-ada-002")
            embeddings=response['data'][0]['embedding']
            embeddings = np.vstack(embeddings).astype('float32').T
        print('embedding/',embeddings.shape)
    else:
        embeddings= e_model.encode(list(text_chunks)) 
    
    return embeddings


def retriver_prompt(dataset_name,content,e_model,K=3):
    """
    生成数据库search
    添加prompt
    """
    print('content',content)
    index = faiss.read_index(f'dataset/{dataset_name[0]}/index.faiss')
    assistant = ChatAssistant(config.API_KEYS)
    search = assistant.generate_embeddings(content,e_model)
    print('search',search)
    D,I = index.search(search,K)  
    

    # 使用 Pandas 一行代码读取 CSV 文件
    text_chunk = pd.read_csv(f"dataset/{dataset_name[0]}/index.csv")["text_chunks"].tolist()
    print('I:',I)
    
    search_txt=[text_chunk[i] for i in I.ravel()]
    
    full_content = f'''您是位帮助中心客服。如果提问和文档内容无关信息，请提醒围绕内容提问，请自信一点，给您的文档片段都是可靠的，您负责从中提取信息，用以分条回答用户问题，要求回答简洁干练。可用markdown表达内容
问题是"{content}
以下是可参考的部分文档片段
'''+"".join([f"{j} \n" for i,j in enumerate(search_txt)])
        
    # full_content = f'根据文档内容来回答问题，问题是"{content}"，文档内容片段1：\n {i for i in search_txt}'
    print(full_content)
    return full_content,search_txt[0:K]




def markdown_images(markdown):
    # example image markdown:
    # ![Test image](images/test.png "Alternate text")
    images = re.findall(r'(!\[(?P<image_title>[^\]]+)\]\((?P<image_path>[^\)"\s]+)\s*([^\)]*)\))', markdown)
    return images


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def img_to_html(img_path, img_alt):
    img_format = img_path.split(".")[-1]
    img_html = f'<img src="data:image/{img_format.lower()};base64,{img_to_bytes(img_path)}" alt="{img_alt}" style="max-width: 100%;">'

    return img_html

def markdown_insert_images(markdown):
    images = markdown_images(markdown)

    for image in images:
        image_markdown = image[0]
        image_alt = image[1]
        image_path = image[2]
        if os.path.exists(image_path):
            markdown = markdown.replace(image_markdown, img_to_html(image_path, image_alt))
    return markdown

class ChatAssistant:
    """
    输入不太对，现在是列表，应该是字典式输入输出
    """
    def __init__(self, api_key):
      
        openai.api_key = api_key

    def send_chat_request(self, messages):
        return openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            stream=False,
        )


    def wrap_chunks_q(self, chunk):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"请根据下面的文本生成多个问题：\n {chunk}"},
        ]
        return messages

    def generate_embeddings(self, text_chunks, e_model):
        if type(text_chunks) != str:
            print('执行批embedding')
            embeddings = {}
            with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
                futures = {executor.submit(self.generate_embedding_online, chunk): i for i, chunk in enumerate(text_chunks)}
                with stqdm(total=len(futures)) as pbar:  # 创建进度条对象
                    for future in concurrent.futures.as_completed(futures):
                        try:
                            index = futures[future]  # 获取对应的索引
                            embedding = future.result()
                            embeddings[index] = embedding
                        except Exception as e:
                            print(f"Failed to generate embedding, Error: {e}")
                        pbar.update(1)  # 更新进度条

            ordered_embeddings = [embeddings[i] for i in range(len(embeddings))]  # 按照索引顺序获取嵌入向量
            embeddings = np.vstack(ordered_embeddings).astype('float32')
        else:
            print('执行单次embedding')
            embeddings = self.generate_embedding_online(text_chunks)
            embeddings = np.vstack(embeddings).astype('float32').T
        print('embedding/', embeddings.shape)

        return embeddings


    def generate_embedding_online(self, text_chunk):
        response = openai.Embedding.create(
            input=text_chunk,
            model="text-embedding-ada-002"
        )
        return response['data'][0]['embedding']
    
    def process_responses(self, chunks_list):
        num_requests = len(chunks_list)
        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
            future_to_request = {
                executor.submit(
                    self.send_chat_request, self.wrap_chunks_q(chunks)
                ): self.wrap_chunks_q(chunks)
                for chunks in chunks_list
            }

            for future in concurrent.futures.as_completed(future_to_request):
                request_data = future_to_request[future]
                try:
                    response = future.result()
                    # Process response here
                    
                    print(
                        "Response_data:",
                        request_data[1]["content"],
                        "Response:",
                        response["choices"][0]["message"]["content"],
                    )
                except Exception as e:
                    print(f"Request failed for messages: {request_data}, Error: {e}")
                    return 0
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Total time:", elapsed_time, "seconds")


def convert_path_to_abspath(input_path: Union[str, list]):
    def _to_abspath(file_path:str) -> str:
        return os.path.join(liqa_dir, file_path) if not os.path.isabs(file_path) else file_path
    
    if isinstance(input_path, str):
        return _to_abspath(input_path)
    else:
        return [_to_abspath(path) for path in input_path]
    


import logging
from typing import Dict, List, Optional, cast,Any

from llama_index.core.bridge.pydantic import Field, validator
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core import get_response_synthesizer
from llama_index.core.schema import NodeRelationship, NodeWithScore
from llama_index.core import QueryBundle
from llama_index.core.storage.docstore import BaseDocumentStore


from llama_index.core.retrievers import BaseRetriever

class HybridRetriever(BaseRetriever):
    def __init__(self, vector_retriever, bm25_retriever):
        self.vector_retriever = vector_retriever
        self.bm25_retriever = bm25_retriever

    def _retrieve(self, query, **kwargs):
        bm25_nodes = self.bm25_retriever.retrieve(query, **kwargs)
        vector_nodes = self.vector_retriever.retrieve(query, **kwargs)

        # combine the two lists of nodes
        all_nodes = []
        node_ids = set()
        for n in bm25_nodes + vector_nodes:
            if n.node.node_id not in node_ids:
                all_nodes.append(n)
                node_ids.add(n.node.node_id)
        return all_nodes


class ParentChildNodePostprocessor(BaseNodePostprocessor):
    """Parent/Child Node post-processor.

    Allows users to fetch additional nodes from the document store,
    based on the parent-child relationships of the nodes.

    NOTE: this is a beta feature.

    Args:
        docstore (BaseDocumentStore): The document store.
        num_nodes (int): The number of child nodes to return (default: 1)
        mode (str): The mode of the post-processor.
            Can be "parent", "child", or "both".
    """

    docstore: BaseDocumentStore
    num_nodes: int = Field(default=1)
    mode: str = Field(default="child")

    @validator("mode",allow_reuse=True)
    def _validate_mode(cls, v: str) -> str:
        """Validate mode."""
        if v not in ["parent", "child", "both"]:
            raise ValueError(f"Invalid mode: {v}")
        return v

    @classmethod
    def class_name(cls) -> str:
        return "ParentChildNodePostprocessor"

    def _postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[Any] = None,
    ) -> List[NodeWithScore]:
        all_nodes: Dict[str, NodeWithScore] = {}
        for node_with_score in nodes:
            all_nodes[node_with_score.node.node_id] = node_with_score
            if self.mode in ["child", "both"]:
                child_nodes = self.get_child_nodes(node_with_score, self.docstore)
                # for child_node in child_nodes:
                all_nodes.update(child_nodes)
            if self.mode in ["parent", "both"]:
                parent_nodes = self.get_parent_nodes(node_with_score, self.docstore)
                # for parent_node in parent_nodes:
                all_nodes.update(parent_nodes)
        return list(all_nodes.values())
    
    def get_child_nodes(self,node_with_score: NodeWithScore, docstore: BaseDocumentStore) -> Dict[str, NodeWithScore]:
        child_nodes_info = node_with_score.node.relationships.get(NodeRelationship.CHILD, [])
        child_nodes: Dict[str, NodeWithScore] = {}
        if isinstance(child_nodes_info, list):
            for child_info in child_nodes_info:
                child_node = docstore.get_node(child_info.node_id)
                if child_node:
                    child_nodes[child_node.node_id] = NodeWithScore(node=child_node)
        else:  # 单个元素
            child_node = docstore.get_node(child_nodes_info.node_id)
            if child_node:
                child_nodes[child_node.node_id] = NodeWithScore(node=child_node)
        return child_nodes

    def get_parent_nodes(self,node_with_score: NodeWithScore, docstore: BaseDocumentStore) -> Dict[str, NodeWithScore]:
        parent_nodes_info = node_with_score.node.relationships.get(NodeRelationship.PARENT, [])
        parent_nodes: Dict[str, NodeWithScore] = {}
        if isinstance(parent_nodes_info, list):
            for parent_info in parent_nodes_info:
                parent_node = docstore.get_node(parent_info.node_id)
                if parent_node:
                    parent_nodes[parent_node.node_id] = NodeWithScore(node=parent_node)
        else:  # 单个元素
            parent_node = docstore.get_node(parent_nodes_info.node_id)
            if parent_node:
                parent_nodes[parent_node.node_id] = NodeWithScore(node=parent_node)
        return parent_nodes