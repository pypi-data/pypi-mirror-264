# Open Local LLM Agent(Olla)

Build your own AI agent with open LLM.

```python
from olla.agent.react_agent import ReActAgent
from olla.core.llm import OpenAI
from olla.core.function import CurrTime

if __name__ == "__main__":
    llm = OpenAI(
        base_url="http://localhost:11434/v1",
        model="openchat",
        api_key="sk-none",
    )
    agent = ReActAgent(
        llm=llm,
        tools=[CurrTime()]
    )
    agent.run("what time is now in Shanghai")
```
