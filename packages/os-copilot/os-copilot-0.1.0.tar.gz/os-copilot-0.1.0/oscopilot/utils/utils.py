import copy
import numpy as np
import itertools
import json
import logging
import os
import re
import string
from typing import Any
import tqdm
import re
import tiktoken
import random
from datasets import load_dataset


def random_string(length):
    """
    Generates a random string of a specified length.

    Args:
        length (int): The desired length of the random string.

    Returns:
        str: A string of random characters and digits of the specified length.
    """
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def num_tokens_from_string(string: str) -> int:
    """
    Calculates the number of tokens in a given text string according to a specific encoding.

    Args:
        text (str): The text string to be tokenized.

    Returns:
        int: The number of tokens the string is encoded into according to the model's tokenizer.
    """
    encoding = tiktoken.encoding_for_model('gpt-4-1106-preview')
    num_tokens = len(encoding.encode(string))
    return num_tokens


def parse_content(content, html_type="html.parser"):
    """
    Parses and cleans the given HTML content, removing specified tags, ids, and classes.

    Args:
        content (str): The HTML content to be parsed and cleaned.
        type (str, optional): The type of parser to be used by BeautifulSoup. Defaults to "html.parser".
            Supported types include "html.parser", "lxml", "lxml-xml", "xml", and "html5lib".

    Raises:
        ValueError: If an unsupported parser type is specified.

    Returns:
        str: The cleaned text extracted from the HTML content.
    """
    implemented = ["html.parser", "lxml", "lxml-xml", "xml", "html5lib"]
    if html_type not in implemented:
        raise ValueError(f"Parser type {html_type} not implemented. Please choose one of {implemented}")

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(content, html_type)
    original_size = len(str(soup.get_text()))

    tags_to_exclude = [
        "nav",
        "aside",
        "form",
        "header",
        "noscript",
        "svg",
        "canvas",
        "footer",
        "script",
        "style",
    ]
    for tag in soup(tags_to_exclude):
        tag.decompose()

    ids_to_exclude = ["sidebar", "main-navigation", "menu-main-menu"]
    for id in ids_to_exclude:
        tags = soup.find_all(id=id)
        for tag in tags:
            tag.decompose()

    classes_to_exclude = [
        "elementor-location-header",
        "navbar-header",
        "nav",
        "header-sidebar-wrapper",
        "blog-sidebar-wrapper",
        "related-posts",
    ]
    for class_name in classes_to_exclude:
        tags = soup.find_all(class_=class_name)
        for tag in tags:
            tag.decompose()

    content = soup.get_text()
    content = clean_string(content)

    cleaned_size = len(content)
    if original_size != 0:
        logging.info(
            f"Cleaned page size: {cleaned_size} characters, down from {original_size} (shrunk: {original_size-cleaned_size} chars, {round((1-(cleaned_size/original_size)) * 100, 2)}%)"  # noqa:E501
        )

    return content


def clean_string(text):
    """
    Cleans a given string by performing various operations such as whitespace normalization,
    removal of backslashes, and replacement of hash characters with spaces. It also reduces
    consecutive non-alphanumeric characters to a single occurrence.

    Args:
        text (str): The text to be cleaned.

    Returns:
        str: The cleaned text after applying all the specified cleaning operations.
    """
    # Replacement of newline characters:
    text = text.replace("\n", " ")

    # Stripping and reducing multiple spaces to single:
    cleaned_text = re.sub(r"\s+", " ", text.strip())

    # Removing backslashes:
    cleaned_text = cleaned_text.replace("\\", "")

    # Replacing hash characters:
    cleaned_text = cleaned_text.replace("#", " ")

    # Eliminating consecutive non-alphanumeric characters:
    # This regex identifies consecutive non-alphanumeric characters (i.e., not
    # a word character [a-zA-Z0-9_] and not a whitespace) in the string
    # and replaces each group of such characters with a single occurrence of
    # that character.
    # For example, "!!! hello !!!" would become "! hello !".
    cleaned_text = re.sub(r"([^\w\s])\1*", r"\1", cleaned_text)

    return cleaned_text


def is_readable(s):
    """
    Heuristic to determine if a string is "readable" (mostly contains printable characters and forms meaningful words)

    :param s: string
    :return: True if the string is more than 95% printable.
    """
    try:
        printable_ratio = sum(c in string.printable for c in s) / len(s)
    except ZeroDivisionError:
        logging.warning("Empty string processed as unreadable")
        printable_ratio = 0
    return printable_ratio > 0.95  # 95% of characters are printable


def format_source(source: str, limit: int = 20) -> str:
    """
    Format a string to only take the first x and last x letters.
    This makes it easier to display a URL, keeping familiarity while ensuring a consistent length.
    If the string is too short, it is not sliced.
    """
    if len(source) > 2 * limit:
        return source[:limit] + "..." + source[-limit:]
    return source


def is_valid_json_string(source: str):
    """
    Checks if a given string is a valid JSON.
    
    Args:
        source (str): The string to be validated as JSON.

    Returns:
        bool: True if the given string is a valid JSON format, False otherwise.
    """
    try:
        _ = json.loads(source)
        return True
    except json.JSONDecodeError:
        logging.error(
            "Insert valid string format of JSON. \
            Check the docs to see the supported formats - `https://docs.embedchain.ai/data-sources/json`"
        )
        return False


def chunks(iterable, batch_size=100, desc="Processing chunks"):
    """
    Breaks an iterable into smaller chunks of a specified size, yielding each chunk in sequence.

    Args:
        iterable (iterable): The iterable to be chunked.
        batch_size (int, optional): The size of each chunk. Defaults to 100.
        desc (str, optional): Description text to be displayed alongside the progress bar. Defaults to "Processing chunks".

    Yields:
        tuple: A chunk of the iterable, with a maximum length of `batch_size`.
    """
    it = iter(iterable)
    total_size = len(iterable)

    with tqdm(total=total_size, desc=desc, unit="batch") as pbar:
        chunk = tuple(itertools.islice(it, batch_size))
        while chunk:
            yield chunk
            pbar.update(len(chunk))
            chunk = tuple(itertools.islice(it, batch_size))


def generate_prompt(template: str, replace_dict: dict):
    """
    Generates a string by replacing placeholders in a template with values from a dictionary.

    Args:
        template (str): The template string containing placeholders to be replaced.
        replace_dict (dict): A dictionary where each key corresponds to a placeholder in the template
                             and each value is the replacement for that placeholder.

    Returns:
        str: The resulting string after all placeholders have been replaced with their corresponding values.
    """
    prompt = copy.deepcopy(template)
    for k, v in replace_dict.items():
        prompt = prompt.replace(k, str(v))
    return prompt


def cosine_similarity(a, b):
    """
    Calculates the cosine similarity between two vectors.

    Args:
        a (array_like): The first vector.
        b (array_like): The second vector.

    Returns:
        float: The cosine similarity between vectors `a` and `b`.
    """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))\
    

def send_chat_prompts(sys_prompt, user_prompt, llm):
    """
    Sends a sequence of chat prompts to a language learning model (LLM) and returns the model's response.

    Args:
        sys_prompt (str): The system prompt that sets the context or provides instructions for the language learning model.
        user_prompt (str): The user prompt that contains the specific query or command intended for the language learning model.
        llm (object): The language learning model to which the prompts are sent. This model is expected to have a `chat` method that accepts structured prompts.

    Returns:
        The response from the language learning model, which is typically a string containing the model's answer or generated content based on the provided prompts.

    The function is a utility for simplifying the process of sending structured chat prompts to a language learning model and parsing its response, useful in scenarios where dynamic interaction with the model is required.
    """
    message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
    return llm.chat(message)


def get_project_root_path():
    """
    This function returns the absolute path of the project root directory. It assumes that it is being called from a file located in oscopilot/utils/.
    
    Args:
        None
    
    Returns:
        str: The absolute path of the project root directory.
    """
    script_path = os.path.abspath(__file__)

    # Get the directory of the script (oscopilot/utils)
    script_directory = os.path.dirname(script_path)

    # Get the parent directory of script_directory (oscopilot)
    oscopilot_directory = os.path.dirname(script_directory)

    # Get the project root directory
    project_root_path = os.path.dirname(oscopilot_directory)

    return project_root_path + '/'


class GAIALoader:
    def __init__(self, level=1, cache_dir=None):
        if cache_dir != None:
            assert os.path.exists(cache_dir), f"Cache directory {cache_dir} does not exist."
            self.cache_dir = cache_dir
            try:
                self.dataset = load_dataset("gaia-benchmark/GAIA", "2023_level{}".format(level), cache_dir=self.cache_dir)
            except Exception as e:
                raise Exception(f"Failed to load GAIA dataset: {e}")
        else:
            self.dataset = load_dataset("gaia-benchmark/GAIA", "2023_level{}".format(level))
            
        
    def get_data_by_task_id(self, task_id, dataset_type):
        if self.dataset is None or dataset_type not in self.dataset:
            raise ValueError("Dataset not loaded or data set not available.")

        data_set = self.dataset[dataset_type]
        for record in data_set:
            if record['task_id'] == task_id:
                return record
        return None

    def task2query(self, task):
        query = 'Your task is: {}'.format(task['Question'])
        if task['file_name'] != '':
            query = query + '\nThe path of the files you need to use: {0}.{1}'.format(task['file_path'], task['file_name'].split('.')[-1])
        print('GAIA Task {1}:\n{2}'.format(task['task_id'], query))
        logging.info(query)
        return query
    
class SheetTaskLoader:
    def __init__(self, sheet_task_path=None):
        if sheet_task_path != None:
            assert os.path.exists(sheet_task_path), f"Sheet task jsonl file {sheet_task_path} does not exist."
            self.sheet_task_path = sheet_task_path
            try:
                self.dataset = self.load_sheet_task_dataset()
            except Exception as e:
                raise Exception(f"Failed to load sheet task dataset: {e}")
        else:
            print("Sheet task jsonl file not provided.")


    def load_sheet_task_dataset(self):
        dataset = []
        with open(self.sheet_task_path, 'r') as file:
            for _, line in enumerate(file):
                task_info = json.loads(line)
                query = self.task2query(task_info['Context'], task_info['Instructions'], get_project_root_path() + task_info['file_path'])
                dataset.append(query)
        return dataset

    def task2query(self, context, instructions, file_path):
        SHEET_TASK_PROMPT = """You are an expert in handling excel file. {context}
                               Your task is: {instructions}
                               The file path of the excel is: {file_path}. Every subtask's description must include the file path, and all subtasks are completed on the file at that path.
                            """
        query = SHEET_TASK_PROMPT.format(context=context, instructions=instructions, file_path=file_path)
        return query
    
    def get_data_by_task_id(self, task_id):
        if self.dataset is None:
            raise ValueError("Dataset not loaded.")
        return self.dataset[task_id]