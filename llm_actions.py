import os, re
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

from database_class import EventDatabase

def parse_summary_questions(summary_string):
    summary_questions = re.findall(r"Question \d+: (.*? \(covering \d+ questions\))(?:\n|$)", summary_string)
    return summary_questions

def parse_question_string(question_string):
    easy_questions = re.findall(r"Easiest questions:\nQuestion \d+: (.*?)\nQuestion \d+: (.*?)\n", question_string)
    hard_questions = re.findall(r"Hardest questions:\nQuestion \d+: (.*?)\nQuestion \d+: (.*?)(?:\n|$)", question_string)
    print(easy_questions)
    print()
    print(hard_questions)
    return [q for q in easy_questions[0] if q], [q for q in hard_questions[0] if q]

def parse_categories(answer_string):
    # catergories = re.findall(r"Category \d+: ([\w\s]+)", answer_string)
    # categories = re.findall(r"Category (\d+): ([\w\s]+?)(?=\n|$)", answer_string)
    categories = re.findall(r"Category (\d+): ([^\(\n]+)", answer_string)
    categories_dict = {cat[0]:cat[1] for cat in categories}
    return categories_dict

def remove_final_dot(s):
    return s[:-1] if (s.endswith(".") or s[-1]==',') else s

def parse_questions_categories(numbers_string):
    numbers_string = remove_final_dot(numbers_string)
    numbers_list = [int(num) for num in numbers_string.split(',')]
    return numbers_list

def summarize_questions_gpt(category_questions, event_name, event_presenter):
    print('in summarize')
    # set up openai api key, model
    load_dotenv()  # take environment variables from .env.
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    chat = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=OPENAI_API_KEY
    )
    # These questions should encapsulate the core themes of the initial list without merely listing or paraphrasing them.
    # set up the prompt template for the specific application
    system_message=SystemMessage(
        content="You are a helpful assistant that works in event management. Your role is to take care of analyze all the queestions in Q&A sessions."
    )

    summarize_template = """
Given the list of questions from our Q&A on {presenter}'s {name}, synthesize two succinct and overarching questions.

Initial questions list: {questions}

Please provide your answer following the template below exactly:

Question 1: question (covering n questions)
Question 2: question (covering n questions)

Note: The newly synthesized questions should not be a simple enumeration or paraphrasing of the original questions but should capture their essence in a concise and novel manner. Make sure to mention the count of questions covered by each new question at their end.
"""
    human_message_prompt = HumanMessagePromptTemplate.from_template(summarize_template)

    # list the messages
    messages = [
        system_message,
        human_message_prompt,
    ]
    chat_prompt = ChatPromptTemplate.from_messages(messages)
    
    # get a chat completion from the formatted messages
    chain = LLMChain(llm=chat, prompt=chat_prompt)
    llm_output = chain.run(questions=category_questions, name=event_name, presenter=event_presenter)
    print(llm_output)
    summary_questions = parse_summary_questions(llm_output)
    return summary_questions

def suggest_categories(event_database_name, event_name, event_presenter):
    # set up openai api key, model
    load_dotenv()  # take environment variables from .env.
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    chat = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=OPENAI_API_KEY
    )

    # set up the prompt template for the specific application
    system_message=SystemMessage(
        content="You are a helpful assistant that works in event management. Your role is to define categories from a Q&A session."
    )

    summarize_template = """
Given the list of questions from our Q&A on {presenter}'s {name}, determine three overarching categories.
Provide a short name for each category.

Initial questions list: {questions}

Please only provide the categories respecting the follwoing template exactly and including the Other category.

Category 0: (category)
Category 1: (category)
Category 2: (category)
Category 3: Other

Note: make sure the category number starts at 0.
"""
    human_message_prompt = HumanMessagePromptTemplate.from_template(summarize_template)

    # list the messages
    messages = [
        system_message,
        human_message_prompt,
    ]
    chat_prompt = ChatPromptTemplate.from_messages(messages)
    
    # gather the questions from the database
    eventdb = EventDatabase(event_database_name)
    questions = eventdb.get_questions_from_db()
    event_questions = " ".join(questions)
    
    # get a chat completion from the formatted messages
    chain = LLMChain(llm=chat, prompt=chat_prompt)
    llm_output = chain.run(questions=event_questions, name=event_name, presenter=event_presenter)
    print(llm_output)

    catergories_dict = parse_categories(llm_output)
    return catergories_dict, llm_output

def suggest_easy_hard_questions(event_database_name, event_name, event_presenter):
    # set up openai api key, model
    load_dotenv()  # take environment variables from .env.
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    chat = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=OPENAI_API_KEY
    )

    # set up the prompt template for the specific application
    system_message=SystemMessage(
        content="You are a helpful assistant that works in event management. Your role is to select easy and challenging questions from a Q&A session."
    )

    summarize_template = """
Given the list of questions from our Q&A on {presenter}'s {name}, determine the two simplest questions, based on their straight-forwardness and specificity, and the two most challenging questions, based on their breadth or potential to challenge the presenter's views.
Provide a reasoning and explanation for each selection.

Question list: {questions}

Your response should only include:

Easiest questions:
Question 1: question (explanation)
Question 2: question (explanation)
Hardest questions:
Question 1: question (explanation)
Question 2: question (explanation)
"""
    human_message_prompt = HumanMessagePromptTemplate.from_template(summarize_template)

    # list the messages
    messages = [
        system_message,
        human_message_prompt,
    ]
    chat_prompt = ChatPromptTemplate.from_messages(messages)
    
    # gather the questions from the database
    eventdb = EventDatabase(event_database_name)
    questions = eventdb.get_questions_from_db()
    event_questions = " ".join(questions)
    
    # get a chat completion from the formatted messages
    chain = LLMChain(llm=chat, prompt=chat_prompt)
    llm_output = chain.run(questions=event_questions, name=event_name, presenter=event_presenter)
    print(llm_output)
    easy_questions, hard_questions = parse_question_string(llm_output)

    return easy_questions, hard_questions

def categorize_questions(questions_to_categorize, current_categories):
    # set up openai api key, model
    load_dotenv()  # take environment variables from .env.
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    chat = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=OPENAI_API_KEY
    )

    # set up the prompt template for the specific application
    system_message=SystemMessage(
        content="You are a helpful assistant that works in event management. Your role is to categorise questions from a Q&A session."
    )

    summarize_template = """
Please categorize each question by assigning it a category number.

Questions: {questions}

Categories: {categories}

Please provide the desired list of integers as a comma-separated string. For example: '0,1,2,3,4'.
Do not add anything else to the answer.
"""
    human_message_prompt = HumanMessagePromptTemplate.from_template(summarize_template)

    # list the messages
    messages = [
        system_message,
        human_message_prompt,
    ]
    chat_prompt = ChatPromptTemplate.from_messages(messages)
    
    # get a chat completion from the formatted messages
    chain = LLMChain(llm=chat, prompt=chat_prompt)
    llm_output = chain.run(questions=questions_to_categorize, categories=current_categories)
    print(llm_output)
    questions_categories = parse_questions_categories(llm_output)
    return questions_categories