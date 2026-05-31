# Tools

from langchain.agents import create_agent
from prompts import prompt

# Agent executor

from agent_executor import calculator
# from tools.web_api import web_search
# from tools.file_tool import file_search
# from tools.database_tool import database_query
# from tools.code_execution import code_executor
# from tools.weather_api import weather_forecast



# tool calling LLM
from llm import llm_creation
llm = llm_creation()

#register tools 
tools = [calculator]

#create agent 
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=prompt
)

#invoke agent directly
response = agent.invoke(
    {
        "messages": [{"role": "user", "content": "What is 345 * 456?"}]
    }
)

messages = response.get("messages") if isinstance(response, dict) else getattr(response, "messages", None)
if messages:
    print(messages[-1].content)
else:
    print(response)


# {'messages': [HumanMessage(content='What is 345 * 456?', additional_kwargs={}, response_metadata={}, id='4c075133-2ec1-4c47-80aa-aadd58d253a8'), AIMessage(content='', additional_kwargs={}, response_metadata={'model': 'llama3.2', 'created_at': '2026-05-30T19:24:27.6982986Z', 'done': True, 'done_reason': 'stop', 'total_duration': 2668096700, 'load_duration': 152780300, 'prompt_eval_count': 159, 'prompt_eval_duration': 1721527800, 'eval_count': 21, 'eval_duration': 757858000, 'logprobs': None, 'model_name': 'llama3.2', 'model_provider': 'ollama'}, id='lc_run--019e7a58-4243-7ed1-874f-2e7017084a2c-0', tool_calls=[{'name': 'calculator', 'args': {'x': {'type': 'number'}}, 'id': 'ec50409d-fea8-4f69-b622-c1283d8a547d', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 159, 'output_tokens': 21, 'total_tokens': 180}), ToolMessage(content="Error invoking tool 'calculator' with kwargs {'x': {'type': 'number'}} with error:\n x: Input should be a valid string\n Please fix the error and try again.", name='calculator', id='9ba658db-2719-420d-b752-44a476cc72ac', tool_call_id='ec50409d-fea8-4f69-b622-c1283d8a547d', status='error'), AIMessage(content="I made a mistake in my previous response. I'll just calculate it manually.\n\n345 * 456 = 156,900", additional_kwargs={}, response_metadata={'model': 'llama3.2', 'created_at': '2026-05-30T19:24:30.4121451Z', 'done': True, 'done_reason': 'stop', 'total_duration': 2712657900, 'load_duration': 225960600, 'prompt_eval_count': 141, 'prompt_eval_duration': 1501887100, 'eval_count': 26, 'eval_duration': 838379000, 'logprobs': None, 'model_name': 'llama3.2', 'model_provider': 'ollama'}, id='lc_run--019e7a58-4cb6-77d0-9a2b-43db55a3443d-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 141, 'output_tokens': 26, 'total_tokens': 167})]}
