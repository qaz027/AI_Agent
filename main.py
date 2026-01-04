import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("GEMINI_API_KEY is not set in environment variables.")

from google import genai

client = genai.Client(api_key=api_key)

model = "gemini-2.5-flash"
contents = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

response = client.models.generate_content(
    model=model, contents=contents)
print(response.text)

def main():
    print("Hello from ai-agent!")


if __name__ == "__main__":
    main()
