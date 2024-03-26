from oscopilot.agents.base_agent import BaseAgent
from oscopilot.tool_repository.basic_tools.get_os_version import check_os_version
from oscopilot.utils import setup_pre_run
import json
import logging
import sys
from oscopilot.prompts.friday_pt import prompt
from oscopilot.utils import TaskStatusCode, InnerMonologue, ExecutionState, JudgementResult, RepairingResult


class FridayAgent(BaseAgent):
    """
    A FridayAgent orchestrates the execution of tasks by integrating planning, retrieving, and executing strategies.
    
    This agent is designed to process tasks, manage errors, and refine strategies as necessary to ensure successful task completion. It supports dynamic task planning, information retrieval, execution strategy application, and employs a mechanism for self-refinement in case of execution failures.
    """

    def __init__(self, planner, retriever, executor, Tool_Manager, config):
        """
        Initializes the FridayAgent with specified planning, retrieving, and executing strategies, alongside configuration settings.

        Args:
            planner (callable): A strategy for planning the execution of tasks.
            retriever (callable): A strategy for retrieving necessary information or tools related to the tasks.
            executor (callable): A strategy for executing planned tasks.
            config (object): Configuration settings for the agent.

        Raises:
            ValueError: If the OS version check fails.
        """
        super().__init__()
        self.config = config
        tool_manager = Tool_Manager(config.generated_tool_repo_path)
        self.planner = planner(prompt['planning_prompt'])
        self.retriever = retriever(prompt['retrieve_prompt'], tool_manager)
        self.executor = executor(prompt['execute_prompt'], tool_manager, config.max_repair_iterations)
        self.score = self.config.score
        self.task_status = TaskStatusCode.START
        self.inner_monologue = InnerMonologue()
        try:
            check_os_version(self.system_version)
        except ValueError as e:
            print(e)        

    def run(self, query):
        """
        Executes the given task by planning, executing, and refining as needed until the task is completed or fails.

        Args:
            query (object): The high-level task to be executed.

        No explicit return value, but the method controls the flow of task execution and may exit the process in case of irreparable failures.
        """
        self.planner.reset_plan()
        task = setup_pre_run(query, self.config)
        sub_tasks_list = self.planning(task)
        print("The task list obtained after planning is: {}".format(sub_tasks_list))

        while self.planner.sub_task_list:
            sub_task = self.planner.sub_task_list.pop(0)
            execution_state = self.executing(sub_task, task)
            isTaskCompleted, isReplan = self.self_refining(sub_task, execution_state)
            if isReplan: continue
            if isTaskCompleted:
                print("The execution of the current sub task has been successfully completed.")
            else:
                print("{} not completed in repair round {}".format(sub_task, self.config.max_repair_iterations))
                sys.exit()

    def self_refining(self, tool_name, execution_state: ExecutionState):
        """
        Analyzes and potentially refines the execution of a tool based on its current execution state. 
        This can involve replanning or repairing the execution strategy based on the analysis of execution errors and outcomes.

        Args:
            tool_name (str): The name of the tool being executed.
            execution_state (ExecutionState): The current state of the tool's execution, encapsulating all relevant execution information including errors, results, and codes.

        Returns:
            tuple:
                - isTaskCompleted (bool): Indicates whether the task associated with the tool has been successfully completed.
                - isReplan (bool): Indicates whether a replan is required due to execution state analysis.

        The method decides on the next steps by analyzing the type of error (if any) and the execution results, aiming to either complete the task successfully or identify the need for further action, such as replanning.
        """
        isTaskCompleted = False
        isReplan = False
        score = 0
        state, node_type, description, code, result, relevant_code = execution_state.get_all_state()
        if node_type == 'Code':
            judgement= self.judging(tool_name, state, code, description)
            score = judgement.score
            # need_repair, critique, score, reasoning, error_type 
            if judgement.need_repair:
                if judgement.error_type == 'replan':
                    print("The current task requires replanning...")
                    new_sub_task_list = self.replanning(tool_name, judgement.reasoning)
                    print("The new task list obtained after planning is: {}".format(new_sub_task_list))
                    isReplan = True
                else:
                    repairing_result = self.repairing(tool_name, code, description, state, judgement.critique, judgement.need_repair)
                    isTaskCompleted = repairing_result.isTaskCompleted
                    score = repairing_result.score
                    result = repairing_result.result
                    # isTaskCompleted, code, critique, score, result
                    # if not isTaskCompleted:
                    #     print("{} not completed in repair round {}".format(tool, args.max_repair_iterations))
                    #     break
            else:
                isTaskCompleted = True
            if isTaskCompleted and score >= self.score:
                self.executor.store_tool(tool_name, code)
                print("{} has been stored in the tool repository.".format(tool_name))
        else:
            isTaskCompleted = True
        if isTaskCompleted:
            self.planner.update_tool(tool_name, result, relevant_code, True, node_type)
        # print("The execution of the current task has been successfully completed.")
        return isTaskCompleted, isReplan

    def planning(self, task):
        """
        Decomposes a given high-level task into a list of sub-tasks by retrieving relevant tool names and descriptions, facilitating structured execution planning.

        Args:
            task (object): The high-level task to be planned and executed.

        Returns:
            list: A list of sub-tasks generated by decomposing the high-level task, intended for sequential execution to achieve the task's goal.

        This method leverages the retriever component to fetch information relevant to the task, which is then used by the planner component to decompose the task into manageable sub-tasks.
        """
        retrieve_tool_name = self.retriever.retrieve_tool_name(task)
        retrieve_tool_description_pair = self.retriever.retrieve_tool_description_pair(retrieve_tool_name)

        # decompose task
        self.planner.decompose_task(task, retrieve_tool_description_pair)

        return self.planner.sub_task_list
    
    def executing(self, tool_name, original_task):
        """
        Executes a given sub-task as part of the task execution process, handling different types of tasks including code execution, API calls, and question-answering.

        Args:
            tool_name (str): The name of the tool associated with the sub-task.
            original_task (object): The original high-level task that has been decomposed into sub-tasks.

        Returns:
            ExecutionState: The state of execution for the sub-task, including the result, any errors encountered, and additional execution-related information.

        The method dynamically adapts the execution strategy based on the type of sub-task, utilizing the executor component for code execution, API interaction, or question-answering as appropriate.
        """
        tool_node = self.planner.tool_node[tool_name]
        description = tool_node.description
        logging.info("The current subtask is: {subtask}".format(subtask=description))
        code = ''
        state = None
        # The return value of the current task
        result = ''
        relevant_code = {}
        node_type = tool_node.node_type
        pre_tasks_info = self.planner.get_pre_tasks_info(tool_name)
        if node_type == 'Code':
            # retrieve existing tool
            retrieve_name = self.retriever.retrieve_tool_name(description, 3)
            relevant_code = self.retriever.retrieve_tool_code_pair(retrieve_name)
        # task execute step
        if node_type == 'QA':
            # result = execute_agent.question_and_answer_tool(pre_tasks_info, task, task)
            if self.planner.tool_num == 1:
                result = self.executor.question_and_answer_tool(pre_tasks_info, original_task, original_task)
            else:
                result = self.executor.question_and_answer_tool(pre_tasks_info, original_task, description)
            print(result)
            logging.info(result)
        else:
            invoke = ''
            if node_type == 'API':
                api_path = self.executor.extract_API_Path(description)
                code = self.executor.api_tool(description, api_path, pre_tasks_info)
            else:
                code, invoke = self.executor.generate_tool(tool_name, description, pre_tasks_info, relevant_code)
            # Execute python tool class code
            state = self.executor.execute_tool(code, invoke, node_type)
            result = state.result
            logging.info(state)
            output = {
                "result": state.result,
                "error": state.error
            }
            logging.info(f"The subtask result is: {json.dumps(output)}")

        return ExecutionState(state, node_type, description, code, result, relevant_code)
    
    def judging(self, tool_name, state, code, description):
        """
        Evaluates the execution of a tool based on its execution state and the provided code and description, determining whether the tool's execution was successful or requires amendment.

        Args:
            tool_name (str): The name of the tool being judged.
            state (ExecutionState): The current execution state of the tool, including results and error information.
            code (str): The source code associated with the tool's execution.
            description (str): A description of the tool's intended functionality.

        Returns:
            JudgementResult: An object encapsulating the judgement on the tool's execution, including whether it needs repair, a critique of the execution, and an optional error type and reasoning for the judgement.

        This method assesses the correctness of the executed code and its alignment with the expected outcomes, guiding potential repair or amendment actions.
        """
        # Check whether the code runs correctly, if not, amend the code
        reasoning = ''
        error_type = ''
        tool_node = self.planner.tool_node[tool_name]
        next_action = tool_node.next_action
        need_repair = False
        critique = ''
        score = 0
        # If no error is reported, check whether the task is completed
        if state.error == None:
            critique, judge, score = self.executor.judge_tool(code, description, state, next_action)
            if not judge:
                print("critique: {}".format(critique))
                need_repair = True
        else:
            #  Determine whether it is caused by an error outside the code
            reasoning, error_type = self.executor.analysis_tool(code, description, state)
            need_repair = True
        return JudgementResult(need_repair, critique, score, reasoning, error_type)
    
    def replanning(self, tool_name, reasoning):
        """
        Initiates the replanning process for a task based on new insights or failures encountered during execution, aiming to adjust the plan to better achieve the task goals.

        Args:
            tool_name (str): The name of the tool related to the task that requires replanning.
            reasoning (str): The rationale behind the need for replanning, often based on execution failures or updated task requirements.

        Returns:
            list: An updated list of sub-tasks after the replanning process, intended for sequential execution to complete the task.

        This method identifies alternative or additional tools and their descriptions based on the provided reasoning, updating the task plan accordingly.
        """
        relevant_tool_name = self.retriever.retrieve_tool_name(reasoning)
        relevant_tool_description_pair = self.retriever.retrieve_tool_description_pair(relevant_tool_name)
        self.planner.replan_task(reasoning, tool_name, relevant_tool_description_pair)
        return self.planner.sub_task_list

    def repairing(self, tool_name, code, description, state, critique, need_repair):
        """
        Attempts to repair the execution of a tool by amending its code based on the critique received and the current execution state, iterating until the code executes successfully or reaches the maximum iteration limit.

        Args:
            tool_name (str): The name of the tool being repaired.
            code (str): The current code of the tool that requires repairs.
            description (str): A description of the tool's intended functionality.
            state (ExecutionState): The current execution state of the tool, including results and error information.
            critique (str): Feedback on the tool's last execution attempt, identifying issues to be addressed.
            need_repair (bool): A flag indicating whether the tool's code needs repairs.

        Returns:
            RepairingResult: An object encapsulating the result of the repair attempt, including whether the task has been completed successfully, the amended code, critique, execution score, and the execution result.

        The method iterates, amending the tool's code based on feedback until the code executes correctly or the maximum number of iterations is reached. It leverages the executor component for amending the code and re-evaluating its execution.
        """
        tool_node = self.planner.tool_node[tool_name]
        next_action = tool_node.next_action
        pre_tasks_info = self.planner.get_pre_tasks_info(tool_name)
        trial_times = 0
        score = 0
        while (trial_times < self.executor.max_iter and need_repair == True):
            trial_times += 1
            print("current amend times: {}".format(trial_times))
            new_code, invoke = self.executor.repair_tool(code, description, state, critique, pre_tasks_info)
            critique = ''
            code = new_code
            # Run the current code and check for errors
            state = self.executor.execute_tool(code, invoke, 'Code')
            result = state.result
            logging.info(state) 
            # print(state)
            # Recheck
            if state.error == None:
                critique, judge, score = self.executor.judge_tool(code, description, state, next_action)
                # The task execution is completed and the loop exits
                if judge:
                    need_repair = False
                    break
                # print("critique: {}".format(critique))
            else: # The code still needs to be corrected
                need_repair = True
        return RepairingResult(not need_repair, code, critique, score, result)
