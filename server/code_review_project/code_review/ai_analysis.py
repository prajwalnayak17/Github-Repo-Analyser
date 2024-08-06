import os
import pdb

import openai
import json
from groq import Groq
import black


def split_code_into_chunks(code, max_tokens):
    """
    Splits the given code into chunks that each have a maximum of max_tokens tokens.
    Assumes that each word is a token.
    """

    words = code.split()
    chunks = []
    current_chunk = []
    current_token_count = 0

    for word in words:
        if current_token_count + 1 > max_tokens:  # Each word is one token
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_token_count = 1
        else:
            current_chunk.append(word)
            current_token_count += 1

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


def analyze_code(code):
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    lite_base_url = os.environ.get('LITE_BASE_URL')
    groq_api_key=os.environ.get('GROQ_API_KEY_PERSONAL')

    client = openai.OpenAI(api_key=openai_api_key, base_url=lite_base_url)
    # client = Groq(api_key=groq_api_key)

    # Use black to format the code
    # formatted_code = black.format_str(code, mode=black.FileMode())

    # Store the result in a variable
    # code = formatted_code

    max_tokens = 6000  # Max tokens for each request
    threshold_tokens = 5000  # Threshold for deciding whether to split the code
    words = code.split()

    if len(words) > threshold_tokens:
        chunks = split_code_into_chunks(code, max_tokens)
        all_feedback = {}
        for i, chunk in enumerate(chunks):
            # Create a prompt for each chunk
            prompt = f"""You are a code review assistant. Please review the following code and provide feedback line by line. 
            If there are functions or a group of lines that should be reviewed together, group them accordingly in the 
            response. The output should be in the form of a JSON object where keys are line numbers and values are the 
            comments or improvements for those lines.

            Here is the code:

            {chunk}

            Provide the feedback in the following JSON format:
            {{
                "1": "Comment or improvement for line 1",
                "2": "Comment or improvement for line 2",
                "3-5": "Comment or improvement for lines 3 to 5",
                ...
            }}

            Don't add any introduction lines like 'Here is the feedback' and so on and make the entire response a json without 
            any sentence in the starting or ending.

            Make sure to cover the whole code line by line and  stick to the line number properly including all the '\n',
             and provide comments for only the \
            important suggestions/fixes and 
            not for every line. 
            """

            response = client.chat.completions.create(
                model="4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract the content from the response
            content = response.choices[0].message.content.strip()
            try:
                # Parse the response content as JSON
                feedback_json = json.loads(content)
                for key, value in feedback_json.items():
                    all_feedback[f"{i}-{key}"] = value  # Prefix chunk number to avoid duplicate keys
            except json.JSONDecodeError as e:
                all_feedback[f"error-{i}"] = f"Failed to parse JSON response: {str(e)}"

        return all_feedback

    else:
        # Creating the prompt for the LLM
        prompt = f"""You are a code review assistant. Please review the following code and provide feedback line by line. 
        If there are functions or a group of lines that should be reviewed together, group them accordingly in the 
        response. The output should be in the form of a JSON object where keys are line numbers and values are the 
        comments or improvements for those lines.

        Here is the code:

        {code}

        Provide the feedback in the following JSON format:
        {{
            "1": "Comment or improvement for line 1",
            "2": "Comment or improvement for line 2",
            "3-5": "Comment or improvement for lines 3 to 5",
            ...
        }}

        Don't add any introduction lines like 'Here is the feedback in the JSON Format' 
        and so on and make the entire response a json 
        without any sentence in the starting or ending. I don't want any additional lines apart from the json.
         
        Also, provide comments for only the important suggestions/fixes and not for every line. Skip the lines for which
        you do not have any comments.
        """

        response = client.chat.completions.create(
            model="4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Extracting the content from the response
        content = response.choices[0].message.content.strip()
        try:
            # Parse the response content as JSON
            print(content)
            feedback_json = json.loads(content)
        except json.JSONDecodeError as e:
            feedback_json = {"error": f"Failed to parse JSON response: {str(e)}"}

        return feedback_json
