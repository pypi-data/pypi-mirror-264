# flake8: noqa
from openfinance.agentflow.prompt.base import PromptTemplate

ROLE_PROMPT = PromptTemplate(
    prompt="""
You are {role}.
Your personal goal is: {goal}
""", 
    variables=["role", "goal"]
)

TOOL_PROMPT = PromptTemplate(
    prompt = """
TOOLS:
------
You only have access to the following tools:

{tools}

To use a tool, please use the exact following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}], just the name.
Action Input: the input to the action
Observation: the result of the action
```

When you have a response for your task, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```
""",
    variables=["tools", "tool_names"]
)

POST_PROMPT = PromptTemplate(
    prompt="""
Begin! This is VERY important to you, your job depends on it!

Current Task: {content}
""",
    variables=["content"]
)

MEM_PROMPT = PromptTemplate(
    prompt="""
This is the summary of your work so far:\n{chat_history}
""",
    variables=["chat_history"]
)