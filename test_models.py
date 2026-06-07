from google import genai

client = genai.Client(api_key="AQ.Ab8RN6KczDNCtfmCIUsGeFTYS2uwj2jwZ8BUH8FQiuUTtu-h1Q")

models = client.models.list()

for m in models:
    print(m.name)