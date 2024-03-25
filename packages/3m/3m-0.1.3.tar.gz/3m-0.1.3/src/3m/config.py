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