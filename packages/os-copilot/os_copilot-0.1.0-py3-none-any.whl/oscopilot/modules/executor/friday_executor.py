from oscopilot.modules.base_module import BaseModule
from oscopilot.tool_repository.manager.tool_manager import get_open_api_doc_path
import re
import json
from pathlib import Path
from oscopilot.utils.utils import send_chat_prompts



class FridayExecutor(BaseModule):
    """
    A modules within the system responsible for executing tools based on prompts and maintaining the tool library.

    The ExecutionModule extends the BaseAgent class, focusing on the practical execution of tools determined
    by the system. It utilizes a language learning model (LLM) in conjunction with an execution environments and
    an tool library to carry out tools. Additionally, it manages system versioning and prompts initialization
    for tool execution guidance.
    """

    def __init__(self, prompt, tool_manager, max_iter=3):
        super().__init__()
        self.prompt = prompt
        self.tool_manager = tool_manager
        self.max_iter = max_iter
        self.open_api_doc_path = get_open_api_doc_path()
        self.open_api_doc = {}
        with open(self.open_api_doc_path) as f:
            self.open_api_doc = json.load(f) 
    
    def generate_tool(self, task_name, task_description, pre_tasks_info, relevant_code):
        """
        Generates executable code and invocation logic for a specified tool.

        This method constructs a message to generate tool code capable of completing the specified task,
        taking into account any prerequisite task information and relevant code snippets. It then formats
        this message for processing by the language learning model (LLM) to generate the tool code. The
        method extracts the executable Python code and the specific invocation logic from the LLM's response.

        Args:
            task_name (str): The name of the task for which tool code is being generated.
            task_description (str): A description of the task, detailing what the tool aims to accomplish.
            pre_tasks_info (dict): Information about tasks that are prerequisites for the current task, including their descriptions and return values.
            relevant_code (dict): A dictionary of code snippets relevant to the current task, possibly including code from prerequisite tasks.

        Returns:
            tuple: A tuple containing two elements:
                - code (str): The generated Python code for the tool.
                - invoke (str): The specific logic or command to invoke the generated tool.
        """
        relevant_code = json.dumps(relevant_code)

        sys_prompt = self.prompt['_SYSTEM_SKILL_CREATE_AND_INVOKE_PROMPT']
        user_prompt = self.prompt['_USER_SKILL_CREATE_AND_INVOKE_PROMPT'].format(
            system_version=self.system_version,
            task_description=task_description,
            working_dir= self.environment.working_dir,
            task_name=task_name,
            pre_tasks_info=pre_tasks_info,
            relevant_code=relevant_code
        )

        create_msg = send_chat_prompts(sys_prompt, user_prompt, self.llm)
        code = self.extract_python_code(create_msg)
        invoke = self.extract_information(create_msg, begin_str='<invoke>', end_str='</invoke>')[0]
        return code, invoke

    def execute_tool(self, code, invoke, node_type):
        """
        Executes a given tool code and returns the execution state.

        This method handles the execution of tool code based on its node_type. For code tools, it appends
        additional instructions to print the execution result within designated markers. It then passes
        the modified code for execution in the environments. The method captures and prints the execution
        state, including any results or errors, and returns this state.

        Args:
            code (str): The Python code to be executed as part of the tool.
            invoke (str): The specific command or function call that triggers the tool within the code.
            node_type (str): The type of the tool, determining how the tool is executed. Currently supports 'Code' type.

        Returns:
            state: The state object returned by the environments after executing the tool. This object contains
                   details about the execution's outcome, including any results or errors.

        Note:
            The execution logic is currently tailored for tools of type 'Code', where the code is directly executable
            Python code. The method is designed to be extensible for other tool types as needed.
        """
        # print result info
        if node_type == 'Code':
            info = "\n" + '''print("<return>")''' + "\n" + "print(result)" +  "\n" + '''print("</return>")'''
            code = code + '\nresult=' + invoke + info
        print("************************<code>**************************")
        print(code)
        print("************************</code>*************************")  
        state = self.environment.step(code)
        print("************************<state>**************************")
        print(state)
        # print("error: " + state.error + "\nresult: " + state.result + "\npwd: " + state.pwd + "\nls: " + state.ls)
        print("************************</state>*************************") 
        return state

    def judge_tool(self, code, task_description, state, next_action):
        """
        Evaluates the outcome of an executed tool to determine its success in completing a task.

        This method formulates and sends a judgment request to the language learning model (LLM) based on the
        executed tool's code, the task description, the execution state, and the expected next tool. It
        then parses the LLM's response to determine the tool's success, providing reasoning, a judgment (boolean),
        and a score that quantifies the tool's effectiveness.

        Args:
            code (str): The code of the tool that was executed.
            task_description (str): The description of the task the tool was intended to complete.
            state: The state object returned by the environments after executing the tool, containing execution results.
            next_action (str): The name of the next expected tool in the sequence.

        Returns:
            tuple: A tuple containing:
                - reasoning (str): The LLM's reasoning behind the judgment.
                - judge (bool): The LLM's judgment on whether the tool successfully completed the task.
                - score (float): A score representing the effectiveness of the tool.
        """
        next_action = json.dumps(next_action)
        sys_prompt = self.prompt['_SYSTEM_TASK_JUDGE_PROMPT']
        user_prompt = self.prompt['_USER_TASK_JUDGE_PROMPT'].format(
            current_code=code,
            task=task_description,
            code_output=state.result,
            current_working_dir=state.pwd,
            working_dir=self.environment.working_dir,
            files_and_folders=state.ls,
            next_action=next_action
        )
        response = send_chat_prompts(sys_prompt, user_prompt, self.llm)
        judge_json = self.extract_json_from_string(response) 
        print("************************<judge_json>**************************")
        print(judge_json)
        print("************************</judge_json>*************************")      
        reasoning = judge_json['reasoning']
        judge = judge_json['judge']
        score = judge_json['score']
        return reasoning, judge, score

    def repair_tool(self, current_code, task_description, state, critique, pre_tasks_info):
        """
        Modifies or corrects the code of an tool based on feedback to better complete a task.

        This method sends an amendment request to the LLM, including details about the current code, task description,
        execution state, critique of the tool's outcome, and information about prerequisite tasks. It aims to generate
        a revised version of the code that addresses any identified issues or incomplete aspects of the task. The method
        extracts and returns both the amended code and the specific logic or command to invoke the amended tool.

        Args:
            current_code (str): The original code of the tool that requires amendment.
            task_description (str): The description of the task the tool is intended to complete.
            state: The state object containing details about the tool's execution outcome.
            critique (str): Feedback or critique on the tool's execution, used to guide the amendment.
            pre_tasks_info (dict): Information about tasks that are prerequisites for the current task.

        Returns:
            tuple: A tuple containing:
                - new_code (str): The amended code for the tool.
                - invoke (str): The command or logic to invoke the amended tool.
        """
        sys_prompt = self.prompt['_SYSTEM_SKILL_AMEND_AND_INVOKE_PROMPT']
        user_prompt = self.prompt['_USER_SKILL_AMEND_AND_INVOKE_PROMPT'].format(
            original_code = current_code,
            task = task_description,
            error = state.error,
            code_output = state.result,
            current_working_dir = state.pwd,
            working_dir= self.environment.working_dir,
            files_and_folders = state.ls,
            critique = critique,
            pre_tasks_info = pre_tasks_info
        )
        amend_msg = send_chat_prompts(sys_prompt, user_prompt, self.llm)
        new_code = self.extract_python_code(amend_msg)
        invoke = self.extract_information(amend_msg, begin_str='<invoke>', end_str='</invoke>')[0]
        return new_code, invoke

    def analysis_tool(self, code, task_description, state):
        """
        Analyzes the execution outcome of an tool to determine the nature of any errors.

        This method evaluates the execution state of an tool, specifically looking for errors. Based on the
        analysis, it determines whether the error is environmental and requires new operations (handled by the
        planning modules) or is amendable via the `repair_tool` method. The analysis results, including the reasoning
        and error type, are returned in JSON format.

        Args:
            code (str): The code that was executed for the tool.
            task_description (str): The description of the task associated with the tool.
            state: The state object containing the result of the tool's execution, including any errors.

        Returns:
            tuple: A tuple containing:
                - reasoning (str): The analysis's reasoning regarding the nature of the error.
                - type (str): The type of error identified ('environmental' for new operations, 'amendable' for corrections).
        """
        sys_prompt = self.prompt['_SYSTEM_ERROR_ANALYSIS_PROMPT']
        user_prompt = self.prompt['_USER_ERROR_ANALYSIS_PROMPT'].format(
            current_code=code,
            task=task_description,
            code_error=state.error,
            current_working_dir=state.pwd,
            working_dir= self.environment.working_dir,
            files_and_folders= state.ls
        )

        response = send_chat_prompts(sys_prompt, user_prompt, self.llm)
        analysis_json = self.extract_json_from_string(response)   
        print("************************<analysis_json>**************************")
        print(analysis_json)
        print("************************</analysis_json>*************************")   

        reasoning = analysis_json['reasoning']
        error_type = analysis_json['type']
        return reasoning, error_type
        
    def store_tool(self, tool, code):
        """
        Stores the provided tool and its code in the tool library.

        If the specified tool does not already exist in the tool library, this method proceeds to store the tool's
        code, arguments description, and other relevant information. It involves saving these details into JSON files and
        updating the tool library database. If the tool already exists, it outputs a notification indicating so.

        Args:
            tool (str): The name of the tool to be stored.
            code (str): The executable code associated with the tool.

        Side Effects:
            - Adds a new tool to the tool library if it doesn't already exist.
            - Saves tool details to the filesystem and updates the tool library's database.
            - Outputs a message if the tool already exists in the library.
        """
        # If tool not in db.
        if not self.tool_manager.exist_tool(tool):
            # Implement tool storage logic and store new tools
            # args_description = self.extract_args_description(code)
            tool_description = self.extract_tool_description(code)
            # Save tool name, code, and description to JSON
            tool_info = self.save_tool_info_to_json(tool, code, tool_description)
            # Save code and descriptions to databases and JSON files
            self.tool_manager.add_new_tool(tool_info)
            # # Parameter description save path
            # args_description_file_path = self.tool_manager.generated_tool_repo_dir + '/args_description/' + tool + '.txt'      
            # # save args_description
            # self.save_str_to_path(args_description, args_description_file_path)
        else:
            print("tool already exists!")

    def api_tool(self, description, api_path, context="No context provided."):
        """
        Executes a task by calling an API tool with the provided description and context.

        This method formats a message to generate executable code for an API call based on the
        provided description and context. It sends this message to the language learning model (LLM),
        extracts the executable Python code from the LLM's response, and returns this code.

        Args:
            description (str): A description of the task to be performed by the API call.
            api_path (str): The path or endpoint of the API to be called.
            context (str, optional): Additional context to be included in the API call. Defaults to "No context provided.".

        Returns:
            str: The generated Python code to execute the API call.
        """
        self.sys_prompt = self.prompt['_SYSTEM_TOOL_USAGE_PROMPT'].format(
            openapi_doc = json.dumps(self.generate_openapi_doc(api_path)),
            tool_sub_task = description,
            context = context
        )
        self.user_prompt = self.prompt['_USER_TOOL_USAGE_PROMPT']
        response = send_chat_prompts(self.sys_prompt, self.user_prompt, self.llm)
        code = self.extract_python_code(response)
        return code 
    
    def question_and_answer_tool(self, context, question, current_question=None):
        sys_prompt = self.prompt['_SYSTEM_QA_PROMPT']
        user_prompt = self.prompt['_USER_QA_PROMPT'].format(
            context = context,
            question = question,
            current_question = current_question
        )
        return send_chat_prompts(sys_prompt, user_prompt, self.llm)  

    def extract_python_code(self, response):
        """
        Extracts Python code snippets from a response string that includes code block markers.

        This method parses a response string to extract Python code enclosed within '```python' and '```' markers.
        It's designed to retrieve executable Python code snippets from formatted responses, such as those returned
        by a language learning model after processing a code generation or analysis prompts.

        Args:
            response (str): The response string containing the Python code block to be extracted.

        Returns:
            str: The extracted Python code snippet, or an empty string if no code block is found.
        """
        python_code = ""
        if '```python' in response:
            python_code = response.split('```python')[1].split('```')[0]
        elif '```' in python_code:
            python_code = response.split('```')[1].split('```')[0]
        return python_code    

    def extract_class_name_and_args_description(self, class_code):
        """
        Extracts the class name and arguments description from a given Python class code.

        This method searches the provided class code for the class name and the documentation string
        of the `__call__` method, which typically includes descriptions of the arguments. It uses regular
        expressions to locate these elements within the code.

        Args:
            class_code (str): The Python code of the class from which information is to be extracted.

        Returns:
            tuple: A tuple containing:
                - class_name (str): The name of the class extracted from the code.
                - args_description (str): The arguments description extracted from the `__call__` method's docstring, if available; otherwise, None.
        """
        class_name_pattern = r"class (\w+)"
        class_name_match = re.search(class_name_pattern, class_code)
        class_name = class_name_match.group(1) if class_name_match else None

        # Extracting the __call__ method's docstring
        call_method_docstring_pattern = r"def __call__\([^)]*\):\s+\"\"\"(.*?)\"\"\""
        call_method_docstring_match = re.search(call_method_docstring_pattern, class_code, re.DOTALL)
        args_description = call_method_docstring_match.group(1).strip() if call_method_docstring_match else None

        return class_name, args_description
    
    def extract_args_description(self, class_code):
        """
        Extracts the arguments description from the `__call__` method's docstring within Python class code.

        This method specifically targets the docstring of the `__call__` method in a class, which is conventionally
        used to describe the method's parameters. The extraction is performed using a regular expression that
        captures the content of the docstring.

        Args:
            class_code (str): The Python code of the class from which the arguments description is to be extracted.

        Returns:
            str: The extracted arguments description from the `__call__` method's docstring, or None if the docstring is not found or does not contain descriptions.
        """
        # Extracting the __call__ method's docstring
        call_method_docstring_pattern = r"def __call__\([^)]*\):\s+\"\"\"(.*?)\"\"\""
        call_method_docstring_match = re.search(call_method_docstring_pattern, class_code, re.DOTALL)
        args_description = call_method_docstring_match.group(1).strip() if call_method_docstring_match else None
        return args_description

    def extract_tool_description(self, class_code):
        """
        Extracts the description of an tool from the class's initialization method in Python code.

        This method looks for the tool's description assigned to `self._description` within the `__init__` method
        of a class. It uses regular expressions to find this assignment and extracts the description string. This
        approach assumes that the tool's description is directly assigned as a string literal to `self._description`.

        Args:
            class_code (str): The complete Python code of the class from which the tool description is to be extracted.

        Returns:
            str: The extracted description of the tool if found; otherwise, None.
        """
        init_pattern = r"def __init__\s*\(self[^)]*\):\s*(?:.|\n)*?self\._description\s*=\s*\"([^\"]+)\""
        tool_match = re.search(init_pattern, class_code, re.DOTALL)
        tool_description = tool_match.group(1).strip() if tool_match else None
        return tool_description
    
    def save_str_to_path(self, content, path):
        """
        Saves a string content to a file at the specified path, ensuring the directory exists.

        This method takes a string and a file path, creating any necessary parent directories before
        writing the content to the file. It ensures that the content is written with proper encoding and
        that any existing content in the file is overwritten. The content is processed to remove extra
        whitespace at the beginning and end of each line before saving.

        Args:
            content (str): The string content to be saved to the file.
            path (str): The filesystem path where the content should be saved. If the directory does not exist,
                        it will be created.

        Side Effects:
            - Creates the directory path if it does not exist.
            - Writes the content to a file at the specified path, potentially overwriting existing content.
        """
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            lines = content.strip().splitlines()
            content = '\n'.join(lines)
            f.write(content)
                 
    def save_tool_info_to_json(self, tool, code, description):
        """
        Constructs a dictionary containing tool information suitable for JSON serialization.

        This method packages the name, code, and description of an tool into a dictionary, making it ready
        for serialization or further processing. This structured format is useful for saving tool details
        in a consistent manner, facilitating easy storage and retrieval.

        Args:
            tool (str): The name of the tool.
            code (str): The executable code associated with the tool.
            description (str): A textual description of what the tool does.

        Returns:
            dict: A dictionary containing the tool's name, code, and description.
        """
        info = {
            "task_name" : tool,
            "code": code,
            "description": description
        }
        return info

    def extract_API_Path(self, text):
        """
        Extracts both UNIX-style and Windows-style file paths from the provided text string.

        This method applies regular expressions to identify and extract file paths that may be present in
        the input text. It is capable of recognizing paths that are enclosed within single or double quotes
        and supports both UNIX-style paths (e.g., `/home/user/docs`) and Windows-style paths (e.g., `C:\\Users\\user\\docs`).
        If multiple paths are found, only the first match is returned, following the function's current implementation.

        Args:
            text (str): The string from which file paths are to be extracted.

        Returns:
            str: The first file path found in the input text, with any enclosing quotes removed. If no paths are
                found, an empty string is returned.

        Note:
            The current implementation returns only the first extracted path. If multiple paths are present in the
            input text, consider modifying the method to return all found paths if the use case requires it.
        """
        # Regular expression for UNIX-style and Windows-style paths
        unix_path_pattern = r"/[^/\s]+(?:/[^/\s]*)*"
        windows_path_pattern = r"[a-zA-Z]:\\(?:[^\\\/\s]+\\)*[^\\\/\s]+"

        # Combine both patterns
        pattern = f"({unix_path_pattern})|({windows_path_pattern})"

        # Find all matches
        matches = re.findall(pattern, text)

        # Extract paths from the tuples returned by findall
        paths = [match[0] or match[1] for match in matches]

        # Remove enclosing quotes (single or double) from the paths
        stripped_paths = [path.strip("'\"") for path in paths]
        return stripped_paths[0]

