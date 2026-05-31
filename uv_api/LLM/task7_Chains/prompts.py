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