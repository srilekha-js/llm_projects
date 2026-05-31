from langchain_ollama.chat_models import ChatOllama

def llm_creation():
    # Create a ChatOllama instance
    llm = ChatOllama(
        model="llama3.2",
        temperature=0,
        max_tokens=1000,
    )
    return llm

llm = llm_creation()


summary_prompt ="""
You are a helpful assistant for summarizing text.
Summarize the following text in a concise manner, capturing the main points and key information.
Instructions:
- Provide a clear and concise summary of the text.
- Focus on the main ideas and important details.
- Do not include any personal opinions or interpretations.
- Ensure the summary is coherent and easy to understand.
- Avoid unnecessary repetition and keep it brief.
- Do not include any harmful content or sensitive information. which induces vulgarity, hate, violence, or any form of discrimination.
TEXT:
{text}
SUMMARY:
"""


keyword_extraction_prompt = """
You are a helpful assistant for extracting keywords from text.
Extract the most relevant keywords from the following text.
Instructions:
- Identify and extract the most important keywords that represent the main topics and themes of the text.
- Focus on nouns, proper nouns, and significant phrases.
- Avoid common stop words and less relevant terms.
- Ensure the keywords are concise and accurately reflect the content of the text.
- Do not include any harmful content or sensitive information. which induces vulgarity, hate, violence
, or any form of discrimination.
TEXT:
{text}
KEYWORDS:
"""

title_generation_prompt = """
You are a helpful assistant for generating a title for a given text.
Generate a concise and descriptive title for the following text.
Instructions:
- Create a title that accurately reflects the main theme and content of the text.
- Keep the title concise, ideally between 5 to 10 words.
- Use clear and descriptive language to capture the essence of the text.
- Avoid using clickbait or misleading language.
- Do not include any harmful content or sensitive information. which induces vulgarity, hate, violence, or any form of discrimination.
TEXT:
{text}
TITLE:
"""

from langgraph.prebuilt import create_react_agent
from langchain.tools import tool

# return direct means the output of the tool will be returned directly without any additional processing or formatting. This is useful when you want to get the raw output from the tool without any modifications.
# If this tool is called, stop the agent loop and return the tool's output immediately."
# without return_direct, the agent output may be sent as input to the next tool or may be processed further by the agent before being returned to the user. 
# With return_direct=True, the output of the tool is returned directly to the user without any further processing by the agent. This can be useful when you want to get the raw output from the tool without any modifications or when you want to ensure that the output is returned immediately without any additional steps.
# So for multi-step agent workflows, don't use return_direct=True unless you intentionally want that tool's result to be the final answer

@tool("summarize_text")
def summarize_text(text: str) -> str:
    "Summarize the given text. or summarize the article"
    prompt = summary_prompt.format(text=text)
    response = llm.invoke(prompt)
    return response.content

@tool("extract_keywords")
def extract_keywords(text: str) -> str:
    "Extract keywords from the given text"
    prompt = keyword_extraction_prompt.format(text=text)
    response = llm.invoke(prompt)
    return response.content

@tool("generate_title")
def generate_title(text: str) -> str:
    "Generate a title for the given text"
    prompt = title_generation_prompt.format(text=text)
    response = llm.invoke(prompt)
    return response.content


#register the tool
tools = [
    summarize_text,
    extract_keywords,
    generate_title
]


agent = create_react_agent(
    model=llm,
    tools=tools,
)


################################################### Summarize Agent invocation##############################
print("---------------Summarize Agent invocation-----------------")
response = agent.invoke(
    {
        "messages":
        [
            {
                "role": "user",
                "content":"Summarize the following article: The COVID-19 pandemic has had a profound impact on global health, economies, and societies. It originated in late 2019 and quickly spread worldwide, leading to widespread illness and death. Governments implemented various measures such as lockdowns, social distancing, and mask mandates to curb the spread of the virus. The pandemic also accelerated the development and deployment of vaccines, which have been crucial in controlling the outbreak. However, it has also exposed and exacerbated existing inequalities in healthcare access and economic stability. The long-term effects of the pandemic are still unfolding, but it has undoubtedly reshaped the way we live and work, highlighting the importance of preparedness and resilience in the face of global health crises."
            }
        ]
    }
)
print(response['messages'][-1].content)
print(type(response))  # response is a string <class 'langchain_core.messages.ai.AIMessage'>

# response dictionary key is messages
# inside list access from last so  -1 
# inside that tuple content is the actual response content

################################################### Keyword Extraction Agent invocation##############################
print("---------------Keyword Extraction Agent invocation-----------------")
response = agent.invoke(
    {
        "messages":
        [
            {
                "role": "user",
                "content":"Extract keywords from the following text: The COVID-19 pandemic has had a profound impact on global health, economies, and societies. It originated in late 2019 and quickly spread worldwide, leading to widespread illness and death. Governments implemented various measures such as lockdowns, social distancing, and mask mandates to curb the spread of the virus. The pandemic also accelerated the development and deployment of vaccines, which have been crucial in controlling the outbreak. However, it has also exposed and exacerbated existing inequalities in healthcare access and economic stability. The long-term effects of the pandemic are still unfolding, but it has undoubtedly reshaped the way we live and work, highlighting the importance of preparedness and resilience in the face of global health crises."
            }
        ]
    }

)
print(response['messages'][-1].content)

################################################### Title Generation Agent invocation##############################
print("---------------Title Generation Agent invocation-----------------")
response = agent.invoke(
    {
        "messages":
        [
            {
                "role": "user",
                "content":"Generate a title for the following text: The COVID-19 pandemic has had a profound impact on global health, economies, and societies. It originated in late 2019 and quickly spread worldwide, leading to widespread illness and death. Governments implemented various measures such as lockdowns, social distancing, and mask mandates to curb the spread of the virus. The pandemic also accelerated the development and deployment of vaccines, which have been crucial in controlling the outbreak. However, it has also exposed and exacerbated existing inequalities in healthcare access and economic stability. The long-term effects of the pandemic are still unfolding, but it has undoubtedly reshaped the way we live and work, highlighting the importance of preparedness and resilience in the face of global health crises."
            }
        ]
    }
)
print(response['messages'][-1].content)