import streamlit as st
import os
import pandas as pd
from streamlit_option_menu import option_menu
import streamlit_antd_components as sac
from utils import retriver_prompt,markdown_insert_images,ParentChildNodePostprocessor,HybridRetriever
import pandas as pd
from dataclasses import dataclass, asdict
import streamlit_antd_components as sac
from streamlit_antd_components.utils.data_class import BsIcon
from llama_index.core import StorageContext  #定义了存储文档、嵌入和索引的存储后端
from llama_index.core.postprocessor import SimilarityPostprocessor

from llama_index.core import PromptTemplate
from llama_index.core.prompts import PromptType

import logging

logging.basicConfig(level=logging.INFO)

# 删除streamlit的页脚，隐藏右上角菜单栏
st.set_page_config(
    page_title="Sensetime Dqa demo App",
    layout="wide",
    initial_sidebar_state="expanded"
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

#用st实现页面布局
with st.sidebar:
    selected2 = option_menu(None, [ "问答", "配置项"],
                                icons=['gear', 'cloud-upload',] ,
                                menu_icon="cast", default_index=0)



# 除了侧边栏的部分分为两页，一页展示数据，一页展示交互
# 交互部分分为两栏，左栏展示问题，右栏展示答案
import httpx
from llama_index.core import ServiceContext
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core.query_engine import RetrieverQueryEngine
LLM = OpenAILike(
            model="internlm/internlm2-chat-20b",
            api_key='sd-66C45asdas8',
            is_chat_model=True,
            api_base='http://103.177.28.196:8003/v1',
            http_client=httpx.Client(trust_env=True),
            max_tokens=2000,
            additional_kwargs={"stop":["<|im_end|>"]}
        )
        
EMBEDDING=OpenAIEmbedding(api_base='http://103.177.28.196:8003/v1',api_key='sd-66C45asdas8',embed_batch_size=2)

service_context=ServiceContext.from_defaults(embed_model=EMBEDDING,llm=LLM)
def on_btn_click():
    del st.session_state.messages
    del st.session_state.messages_latent

@st.cache_resource
def load_index():
    # 加载索引的代码
    # if selected_file:
    storage_context = StorageContext.from_defaults(persist_dir="liqa/dataset"+"/"+'3M'+'/'+'storage')
    # load index
    index = load_index_from_storage(storage_context,service_context=service_context)  
    return index

@st.cache_resource
def load_reranker():
from llama_index.postprocessor.flag_embedding_reranker import FlagEmbeddingReranker
    reranker=FlagEmbeddingReranker(model='BAAI/bge-reranker-v2-m3')
    return reranker


    
if selected2 == '问答':
    #载入可选的数据库，单选，先查询本地dataset文件夹下的文件目录
    # 读取文件夹下的文件名
    file_list = [item for item in os.listdir('liqa/dataset') if  '.' not in item]
    #查询当前路径下的文件夹都有哪些
    
    with st.sidebar:    
        
        st.divider()
        

        st.button("清空对话", on_click=on_btn_click,use_container_width=True) 
        st.button("导出对话",use_container_width=True)  
    user_avator = "liqa/images/user.png"
    assistant_avator = "liqa/images/robot.png"
    ## TODO初始化对话配置
    st.session_state.max_length=2048
    st.session_state.top_p=  0.8
    st.session_state.temperature = 0.7
    a,c=st.columns([1,3])
    
    with a:
        a1,c1=st.columns([1,1])
        with a1:
            sac_web=sac.switch(label='**联网功能**', value=False, checked=BsIcon(name='wifi'), unchecked=BsIcon(name='wifi-off'), align='center', position='top', size='large', disabled=True)
        with c1:
            sac_memory=sac.switch(label='**记忆**', value=False, checked=BsIcon(name='memory'), unchecked=BsIcon(name='x'), align='center', position='top', size='large', disabled=True)
    with c:
        a,b,c=st.columns([1,3,1])
        with a:
            sac_file=sac.switch(label='**数据库功能**', value=True, checked=BsIcon(name='database-fill-check'), unchecked=BsIcon(name='database-fill-slash'), align='center', position='top', size='large', disabled=False)
        with b:
            st.multiselect('**选择要对话的数据库**',['3M'],default='3M',disabled=not sac_file)
        with c:
            K_text_chunks=int(st.number_input('**片段数量**',value=2,disabled=not sac_file))
    st.title("对话助手")
    index=load_index()
    reranker=load_reranker()

    

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": '你好，有什么可以帮您的'}]
    if "messages_latent" not in st.session_state:
        st.session_state.messages_latent = [{"role": "assistant", "content": '你好，有什么可以帮您的'}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"],avatar=assistant_avator):
            st.markdown(message["content"])

    if prompt := st.chat_input("想咨询什么?"):
        
        # 如果开启数据库查询式问答
        with st.chat_message("user",avatar=user_avator):
            st.markdown(markdown_insert_images(prompt),unsafe_allow_html=True)
            st.session_state.messages.append({"role": "user", "content": prompt})
            if sac_file:
                print(sac_file,"sac_file当前状态")
                
            st.session_state.messages_latent.append({"role": "user", "content": prompt})

        with st.chat_message("assistant",avatar=assistant_avator):
            
            message_placeholder = st.empty()
            full_response = ""

            
            TEXT_QA_PROMPT_TMPL = (
            "以下是供参考的上下文信息：\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "请根据上述上下文信息，扮演一个专业的的问答助手，回答接下来的查询。"
            "回答应详尽、忠实于原文，需要markdown格式分条分点做答。"
            "最大化的利用参考文本，当你分条分点做答完之后，可以在最后部分自然而然的做一下给一些总结\n，给我中文回答"
            "查询：{query_str}\n"
            "回答："
            )
            TEXT_QA_PROMPT = PromptTemplate(
                TEXT_QA_PROMPT_TMPL, prompt_type=PromptType.QUESTION_ANSWER
            )
            

            # REFINE_PROMPT = PromptTemplate(
            #     REFINE_PROMPT_TMPL, prompt_type=PromptType.REFINE
            # )

            reranker.top_n=K_text_chunks
            
            hybrid_retriever = HybridRetriever(index.as_retriever(similarity_top_k=12), bm25_retriever)

            query_engine = RetrieverQueryEngine.from_args(
            response_mode=ResponseMode.SIMPLE_SUMMARIZE,
            retriever=hybrid_retriever,
            streaming=True,
            service_context=service_context,
            node_postprocessors=[
                    reranker,
                    SimilarityPostprocessor(similarity_cutoff=0.0)
                    ],
            text_qa_template=TEXT_QA_PROMPT,
         
            )

            responses=query_engine.query(st.session_state.messages_latent[-1]['content'])
            # if not responses:

            # else:
            for response in responses.response_gen:
                full_response += response
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(markdown_insert_images(full_response),unsafe_allow_html=True)
            source_nodes=ParentChildNodePostprocessor(docstore=index.docstore).postprocess_nodes(responses.source_nodes)#[1].node.relationships
            from collections import defaultdict
    
            modal_nodes = defaultdict(list)
            for node in source_nodes:
                modal_nodes[node.node.class_name()].append(node.node)
            
            table_nodes=[node.node for node in source_nodes if 'table_number' in node.node.metadata]
            
            
            with st.expander("参考展示"):
                for node in modal_nodes['ImageNode']:
                    st.image(node.resolve_image())
                # for node in table_nodes:
                #     st.markdown(node.text)
                # st.markdown(markdown_insert_images(responses.get_formatted_sources()))
    
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.session_state.messages_latent.append({"role": "assistant", "content": full_response})
        rating = st.radio("打分回复:",help='help', options=[1, 2, 3], index=1,horizontal=True)



if selected2=='配置项':
    with st.expander("对话配置",expanded=True):
        max_length = st.slider("Max Length", min_value=32, max_value=2048, value=2048)
        top_p = st.slider(
            'Top P', 0.0, 1.0, 0.8, step=0.01
        )
        temperature = st.slider(
            'Temperature', 0.0, 1.0, 0.7, step=0.01
        )