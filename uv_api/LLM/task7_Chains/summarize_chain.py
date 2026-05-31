from llm import llm_creation

llm = llm_creation()

from prompts import summary_prompt

# article = "https://www.bbc.com/news/world-us-canada-66231719"

article = """The COVID-19 pandemic has had a profound impact on global health, economies, and societies. It
originated in late 2019 and quickly spread worldwide, leading to widespread illness and death. Governments implemented various measures such as lockdowns, social distancing, and mask mandates to curb the spread of the virus. The pandemic also accelerated the development and deployment of vaccines, which have been crucial in controlling the outbreak. However, it has also exposed and exacerbated existing inequalities in healthcare access and economic stability. The long-term effects of the pandemic are still unfolding, but it has undoubtedly reshaped the way we live and work, highlighting the importance of preparedness and resilience in the face of global health crises.
"""

#extracting summary from the article
prompt = summary_prompt.format(text=article)
response = llm.invoke(prompt)

summarized_text = response.content
print(response)
print("SUMMARY:\n", summarized_text)

#extracting keywords from the summary
from prompts import keyword_extraction_prompt
keyword_prompt = keyword_extraction_prompt.format(text=summarized_text)
response = llm.invoke(keyword_prompt)
keywords = response.content
print("KEYWORDS:\n", keywords)

#title generation from the summary
from prompts import title_generation_prompt
title_prompt = title_generation_prompt.format(text=summarized_text)

response = llm.invoke(title_prompt)
title = response.content
print("TITLE:\n", title)


