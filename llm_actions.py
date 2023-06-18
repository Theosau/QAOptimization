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

def parse_question_string(question_string):
    summary_questions = re.findall(r"Question \d+: (.*? \(covering \d+ questions\))\n?", question_string)
    easy_questions = re.findall(r"Easiest questions:\nQuestion \d+: (.*?)\nQuestion \d+: (.*?)\n", question_string)
    hard_questions = re.findall(r"Hardest questions:\nQuestion \d+: (.*?)\nQuestion \d+: (.*?)(?:\n|$)", question_string)
    print(summary_questions)
    print()
    print(easy_questions)
    print()
    print(hard_questions)
    return summary_questions, [q for q in easy_questions[0] if q], [q for q in hard_questions[0] if q]

def summarize_questions_gpt(event_database_name, event_name, event_presenter, use_model=False):
    print('in summarize')
    if not use_model:
        summary_questions = [
            "What are the potential impacts of AI in various industries and fields, such as mechanical engineering, finance, education, healthcare, climate change mitigation, poverty reduction, and space exploration? (covering 9 questions)",
            "What are the ethical considerations and strategies needed to ensure job security and prevent mass unemployment in light of AI advancements? (covering 2 questions)"
        ]
        easy_questions = [
            "How will AI impact mechanical engineering?",
            "What potential does AI have in revolutionizing the healthcare industry, particularly in areas of disease prediction and diagnosis?"
        ]
        hard_questions = [
            "What are the prospects of AI surpassing human intelligence, and what would be its implications?",
            "How can AI be harnessed in the future to better tackle global poverty and economic disparity?"
        ]
        return summary_questions, easy_questions, hard_questions
    else:
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
            content="You are a helpful assistant that works in event management. Your role is to take care of analyze all the queestions in Q&A sessions."
        )

        summarize_template = """
Given the list of questions from our Q&A on {presenter}'s {name}, synthesize two succinct and overarching questions. These questions should encapsulate the core themes of the initial list without merely listing or paraphrasing them. In addition, determine the two simplest questions, based on their straight-forwardness and specificity, and the two most challenging questions, based on their breadth or potential to challenge the presenter's views.
Make sure to mention how many of the initial questions are covered by each new question.

Initial questions list: {questions}

Your response should only include:

Question 1: question (covering n questions)
Question 2: question (covering n questions)
Easiest questions:
Question 1: question
Question 2: question
Hardest questions:
Question 1: question
Question 2: question

Note: The newly synthesized questions should not be a simple enumeration or paraphrasing of the original questions but should capture their essence in a concise and novel manner. Make sure to mention the total count of questions covered by each new question at their end.
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
        summary_questions, easy_questions, hard_questions = parse_question_string(llm_output)

        return summary_questions, easy_questions, hard_questions