# JSON Output Generator
"""
willbe used for 
This is the foundation for:

agents
tool calling
RAG pipelines
APIs
structured workflows
"""

import json
from prompts import get_json_extractor_prompt
from llm import llm_creation

# text_data = """ollama llm ,
# Ollama is a tool that allows running large language models locally.
# It supports models like Llama 3 and Mistral.
# It is widely used for offline AI development and experimentation.
# """

text_data = """
Cloud computing is the delivery of computing services over the internet, allowing users to access and use resources such as servers, storage, databases, networking, software, and analytics without having to manage physical hardware. It offers scalability, flexibility, and cost-efficiency, enabling businesses and individuals to leverage powerful computing capabilities on demand.
Application: Amazon Web Services (AWS) is a leading cloud computing platform that provides a wide range of services, including computing power, storage, and databases, to businesses and developers worldwide.
"""


get_llm = llm_creation()
json_extractor_prompt = get_json_extractor_prompt()
prompt = json_extractor_prompt.format(text=text_data)
response = get_llm.invoke(prompt)
print(response)
print(type(response))  # response is a string <class 'langchain_core.messages.ai.AIMessage'>
