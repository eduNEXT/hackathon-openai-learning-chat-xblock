import openai

openai.api_key = '' # do NOT commit

class OpenaiClient:
    model = 'text-davinci-003'

    def ask(self, text):
        response = openai.Completion.create(
            model=self.model,
            prompt=text,
            max_tokens=1024,
        )

        return response['choices'][0]['text']
