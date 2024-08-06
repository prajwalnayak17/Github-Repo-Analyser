import os
import pdb

import openai  # openai v1.0.0+
from groq import Groq

def repo_analysis(repo_structure):
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    # groq_api_key= os.environ.get('GROQ_API_KEY_PERSONAL')
    lite_base_url = os.environ.get('LITE_BASE_URL')

    prompt = f"""I have a JSON representation of a GitHub repository's file structure. Please analyze the repository 
    based on the following criteria and provide feedback:

        1. Check if good naming conventions are followed for both folders and files. 2. Ensure that .env files or 
        other sensitive configuration files are not pushed to the repository. 3. Verify if there are any large binary 
        files (like images, videos, etc.) that could be better handled by a dedicated storage service. 4. Identify if 
        the repository contains documentation files (e.g., README.md, CONTRIBUTING.md). 5. Assess if there are test 
        files or directories indicating the presence of automated tests. 6. Confirm the presence of configuration 
        files for code linters or formatters (e.g., .eslintrc, .prettierrc). 7. Detect any obsolete or unnecessary 
        files that can be removed. 8. Identify if there are any deeply nested directories that can be flattened. 9. 
        Evaluate if the repository follows best practices for code organization and file structure. 10. Grade the 
        repository out of 10 based on its production readiness, with 10 being highly production-ready and 1 being 
        intern-level quality. 11. Consider the length and complexity of files, ensuring they are manageable and 
        adhere to best practices.

    Please provide feedback based on these criteria and modify the JSON to keep only the most important files and 
    directories that are critical for a production-level repository. The JSON should maintain its structure but only 
    include the essential files and directories based on your analysis.

    Your response should not contain any text whatsoever outside the '{' '}' brackets. 
    There should not be an introduction or a conclusion text. 
    Make it purely in a json format. 
    I should not need to convert your response to a json file. Format it as a proper json file. Make 
    sure to initialise the empty values as null and not None.
    
    Your entire response should be in .JSON format in key,value pairs so that I can parse this response later, 
    with the following keys. Add the appropriate values to each:
    
        - "feedback": A detailed feedback on the repository in the format of a string. 
        - "score": A score out of 10 
        based on the production readiness of the repository, judge on everything. A score of 10 would be a repository 
        that complete in all senses, like ones in Meta or Google. So judge accordingly. 
        Make sure to not give a repetitive score of 7 everytime, like if the feedback is medium, rotate between 5, 6 
        and 7 based on how bad or good it is, and if it is really better than average, then give a 8 and so on.
        - "updated_file_structure": 
        The modified JSON structure keeping only the most important files and directories. Here, make sure to not skip
        important files like views.py or any services files in Django. Do not change the original file structure, or 
        file paths. Take extra care while handling nested folders as missing them would be critical.
        
    If these keys are not enough, add other keys to contain the rest of your response. Your entire response should be in 
    JSON format between '{' '}' brackets with no texts and comments like ```json above or below the starting and ending 
    brackets.

    Here is the JSON representation of the repository:

    {repo_structure}
    """

    client = openai.OpenAI(api_key=openai_api_key,base_url=lite_base_url)
    # set proxy to base_url
    # request sent to model set on litellm proxy, `litellm --model`

    # client = Groq(api_key=groq_api_key)

    response = client.chat.completions.create(model="4o-mini", messages=[
        {
            "role": "user",
            "content": prompt
        }
    ])

    return response.choices[0].message.content
