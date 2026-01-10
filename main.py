import os
from dotenv import load_dotenv
import argparse
from google.genai import types
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("GEMINI_API_KEY is not set in environment variables.")

from google import genai

client = genai.Client(api_key=api_key)

model = "gemini-2.5-flash"

# replacing hardcoded prompt with command-line argument
# contents = "Tell me the virtues of learning with Boot.dev. Use one paragraph maximum."

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output") # Optional verbose flag
args = parser.parse_args()
# Now we can access `args.user_prompt`
contents = args.user_prompt

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]


response = client.models.generate_content(
    model=model, 
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt, temperature = 0),
    )
# used contents from the hardcode and args.user_prompt in previous iterations

if response.usage_metadata is None:
    raise RuntimeError("Usage metadata is missing in the response. Doesn't look like the request was processed correctly.")

if response.usage_metadata is not None:
    if args.verbose:  # Check if verbose flag is set
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)

def main():
    print("Hello from ai-agent!")


if __name__ == "__main__":
    main()
