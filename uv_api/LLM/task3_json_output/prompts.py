from langchain_core.prompts import PromptTemplate

def get_json_extractor_prompt():
    json_extractor_prompt = PromptTemplate(
    input_variables=["text"], #will be filled at runtime
    template="""
    You are a information extraction system
    you need to generate title if not present in the text
    Extract the structured data from the text below
    Return ONLY valid JSON (no explanations, no extra text, no comments, no markdown, no code blocks):
    Return valid JSON with:
    - title (string)
    - summary (string)
    - key_points (list of strings)

    Rules:
    - key_points must be 3 to 6 items
    - summary must be 2-3 lines max
    - do not include any extra text

    TEXT:
    {text}

    OUTPUT:
    
    """
    )

    return json_extractor_prompt

