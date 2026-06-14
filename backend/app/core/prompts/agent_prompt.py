agent_prompt="""

<Inputs>
{prompt}
</Inputs>
<Instructions Structure>
1. Explain the task.
2. Provide the prompt inside <prompt></prompt> XML tags.
3. Instruct the AI to think step by step and write down its chain of thought inside <thinking></thinking> XML tags.
4. Instruct the AI to provide the agent prompt inside <agent_prompt></agent_prompt> XML tags.
</Instructions Structure>
<Instructions>
You will be converting a basic prompt into a prompt that can be used with an AI agent.
Agentic AI prompt is for AI systems that can autonomously pursue goals and complete tasks without direct human supervision,
Able to learn from interactions, plan, and execute strategies to achieve specified objectives and make decisions based on dynamic environments.

Here is the basic prompt:
<prompt>
{prompt}
</prompt>

Think step by step about how to convert this prompt to a prompt that can be used with an AI agent. Write down your chain of thought inside <thinking></thinking> XML tags.

Provide the agent prompt inside <agent_prompt></agent_prompt> XML tags.
</Instructions>

"""