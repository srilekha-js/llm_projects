from langchain_core.prompts import PromptTemplate


def get_summary_prompt():
    summary_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
    You are a helpful assistant.
    Summarize the following text in simple bullet points:

    Text:
    {text}

    Summary:
    """
    )
    return summary_prompt