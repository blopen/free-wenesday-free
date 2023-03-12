import openai
openai.api_key = "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"
response = openai.Completion.create(
    engine="davinci",
    prompt="Hello, world!",
    max_tokens=3333
)
print(response.choices[0].text)

