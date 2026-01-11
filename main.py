import os
from dotenv import load_dotenv
import argparse
from google import genai
from google.genai import types

from prompts import system_prompt
from call_functions import available_functions


# replacing hardcoded prompt with command-line argument
# contents = "Tell me the virtues of learning with Boot.dev. Use one paragraph maximum."

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output") # Optional verbose flag
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY is not set in environment variables.")
    
    client = genai.Client(api_key=api_key)
    model = "gemini-2.5-flash"
    contents = args.user_prompt
    messages = [types.Content(role="user", parts=[types.Part(text=contents)])]

    generate_content(client, messages, model, args.verbose)


def generate_content(client, messages, model, verbose):

    response = client.models.generate_content(
        model=model, 
        contents=messages,
        config=types.GenerateContentConfig(
            tools = [available_functions],system_instruction=system_prompt, temperature = 0),
        )
    # used contents from the hardcode and args.user_prompt in previous iterations

    if response.usage_metadata is None:
        raise RuntimeError("Usage metadata is missing in the response. Doesn't look like the request was processed correctly.")

    if verbose:  # Check if verbose flag is set
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    

    if not response.function_calls:
        print(response.text)
        return
    

    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")





if __name__ == "__main__":
    main()
