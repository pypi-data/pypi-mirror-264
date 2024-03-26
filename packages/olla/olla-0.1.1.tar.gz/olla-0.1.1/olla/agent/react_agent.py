import json_repair

from olla.core.function import Function, NoFunction
from olla.prompt.react import react_prompt
from olla.core.llm import OpenAI
from olla.core.utils import ReActOutputParser


class ReActAgent:
    def __init__(self, llm: OpenAI, tools: "list[Function]"):
        tools = tools + [NoFunction()]
        tools_desc = "".join(tool.help for tool in tools)
        tools_name = "".join(tool.name for tool in tools)
        self.tools = { tool.name: tool for tool in tools }
        self.system_message = react_prompt.format(tools_desc=tools_desc, tools_name=tools_name)
        self.llm = llm
        self.output_parser = ReActOutputParser()

    def _call_tool_or_get_answer(self, response):
        try:
            result = self.output_parser.parse(response)
            if "Action" in result:
                action = result["Action"]
                action = json_repair.loads(action)
                if action.get("action", None) in self.tools:
                    output = self.tools[action["action"]](action["action_input"])
                    return { "ToolResult": output }
            else:
                return result
        except Exception as e:
            print(type(e), e)
        return None

    def run(self, prompt: str, max_retries=3):
        while True:
            messages = [
                {
                    "role": "system",
                    "content": self.system_message
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            for i in range(max_retries):
                if i > 0:
                    print(f"Retrying... {i}/{max_retries}")
                response = self.llm.generate(messages, ["Observation:"])
                output = self._call_tool_or_get_answer(response)
                if output is not None:
                    break

            if output is None:
                raise ValueError("Agent run error")
            if "FinalAnswer" in output:
                return output["FinalAnswer"]
            else:
                prompt += response + "\n" \
                           + f"Observation: Answer from tool: {output['ToolResult']}\nThought:"
