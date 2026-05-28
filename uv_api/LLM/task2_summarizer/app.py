from prompts import get_summary_prompt
from llm import llm_creation


text_data = """
Text Generation
Text Generation involves using machine learning models to generate new text based on patterns learned from existing text data. The models used for text generation can be Markov Chains, Recurrent Neural Networks (RNNs), and more recently, Transformers, which have revolutionized the field due to their extended attention span. Text generation has numerous applications in the realm of natural language processing, chatbots, and content creation.

Application: ChatGPT, developed by OpenAI, is a successful platform that uses Text Generation to generate human-like responses in chat conversations. 

"""
#calling function from llm.py and prompts.py
get_llm= llm_creation()
summary_prompt = get_summary_prompt()

prompt = summary_prompt.format(text=text_data)
response = get_llm.invoke(prompt)
print(response)