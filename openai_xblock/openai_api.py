import openai

openai.api_key = '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'

class OpenaiClient:
    model = 'text-davinci-003'

    def ask(self, text):
        response = openai.Completion.create(
            model=self.model,
            prompt=text,
        )

        return response['choices'][0]['text']
