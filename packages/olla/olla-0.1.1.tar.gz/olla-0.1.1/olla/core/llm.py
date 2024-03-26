import openai


class OpenAI:
    def __init__(self,
                 base_url: str,
                 api_key: str,
                 model: str,
                 temperature: float = 1,
                 max_tokens: int = 1024):
        self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(self, messages: "list[dict]", stop: "list[str]"):
        response = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stop=stop,
            stream=True
        )
        result = ""
        for chunk in response:
            if chunk.choices[0].delta is not None and chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")
                result += chunk.choices[0].delta.content
        print()
        return result
