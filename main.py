import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types as genai_types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

function_dict = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

def call_function(function_call_part):
    function_name = function_call_part.name
    function_args = function_call_part.args
    
    # Add the working directory as the first argument for all functions
    working_directory = "./calculator"
    
    if function_name in function_dict:
        function_result = function_dict[function_name](working_directory, **function_args)
        return genai_types.Content(
            role="tool",
            parts=[
                genai_types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return genai_types.Content(
            role="tool",
            parts=[
                genai_types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

if (len(sys.argv) < 2):
    print("Usage: python main.py <prompt>")
    sys.exit(1)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, answer their questions assuming that the user's question is related to the files in the 'calculator' directory, which is your working directory.
Don't return the calls to the user, just execute them and return the results within a few paragraphs of natural language. 
Deeply explore the user's request before returning an answer and summarize so that it's easily understandable.
When answering in multiple parts use numbered lists and when breaking down an answer into parts use a bulleted list.

You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

prompt = sys.argv[1]
verbose = "--verbose" in sys.argv
messages = [
    genai_types.Content(
        role="user", 
        parts=[genai_types.Part(text=prompt)]
    ),
]

available_functions = genai_types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

for i in range(20):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=messages,
            config=genai_types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            ),
        )
        if response.candidates is None or len(response.candidates) == 0:
            raise Exception("Error: No candidates returned in response")

        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

        if verbose or True:
            print(f"User prompt: {prompt}")
            if response.usage_metadata is None:
                raise Exception("Error: No usage metadata returned in response")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.function_calls and len(response.function_calls):
            for function_call_part in response.function_calls:
                if verbose:
                    print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                else:
                    print(f" - Calling function: {function_call_part.name}")
                # Execute the function call
                function_call_result = call_function(function_call_part)
                messages.append(function_call_result)
                if function_call_result.parts and len(function_call_result.parts) > 0 and function_call_result.parts[0].function_response and function_call_result.parts[0].function_response.response:
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                else:
                    raise Exception("Error: Function call did not return a valid response")
        elif response.text:
            print(f"Final response: {response.text}")
            break

    except:
        print("Error: An error occurred while processing the request.")
        import traceback
        traceback.print_exc()

