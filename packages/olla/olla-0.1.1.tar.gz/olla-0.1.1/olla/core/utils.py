import re

class LLMOutputParser:
    def parse(self, output):
        raise NotImplementedError()


class ReActOutputParser(LLMOutputParser):
    def __init__(self):
        self.action_regex = re.compile("Action:\s*(\{.*\})", re.DOTALL)
        self.final_answer_regex = re.compile("Final Answer:\s*(.*)", re.DOTALL)

    def parse(self, output):
        try:
            result = self.action_regex.search(output).groups()[-1]
            result = {
                "Action": result
            }
        except Exception:
            result = self.final_answer_regex.search(output).groups()
            if result is None:
                raise ValueError("Don't find any valid action or final answer")
            else:
                result = {
                    "FinalAnswer": result[0]
                }
        return result
