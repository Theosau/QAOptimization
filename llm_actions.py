import os
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


def summarize_questions_gpt(event_database_name):
    print('in summarize')
    qs_formatted = [
        "What will be the impact of AI on various industries, including mechanical engineering, finance, education, healthcare, and climate change mitigation? (5)",
        "In what ways can AI be utilized in the future to address global issues such as poverty, economic disparity, space exploration, and understanding the universe? (5)"
    ]
    return qs_formatted
    # # set up openai api key, model
    # load_dotenv()  # take environment variables from .env.
    # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # chat = ChatOpenAI(
    #     model_name="gpt-3.5-turbo",
    #     temperature=0.7,
    #     openai_api_key=OPENAI_API_KEY
    # )

    # # set up the prompt template for the specific application
    # system_message=SystemMessage(
    #     content="You are a helpful assistant that works in event management." + \
    #     "Your role is to take care of any queries concerning Q&A sessions."
    # )
    # summarize_template="We received a list of questions from our Q&A." + \
    #     "Make sure to read them with attention and understand them. Then summarize these questions into 2 new questions." + \
    #     "Mention how many questions are covered by each new question." + \
    #     "You answer should look like: question 1 (number of questions covered), question 2 (number of questions covered)." + \
    #     "Do not add any other text and do not simply paraphrase the questions." + \
    #     "Here is the inital questions list: {questions}."
    # human_message_prompt = HumanMessagePromptTemplate.from_template(summarize_template)

    # # list the messages
    # messages = [
    #     system_message,
    #     human_message_prompt,
    # ]
    # chat_prompt = ChatPromptTemplate.from_messages(messages)
    
    # # gather the questions from the database
    # # event_database_name = 'TheFutureofAI'
    # eventdb = EventDatabase(event_database_name)
    # questions = eventdb.get_questions_from_db()
    # event_questions = " ".join(questions)
    
    # # get a chat completion from the formatted messages
    # chain = LLMChain(llm=chat, prompt=chat_prompt)
    # llm_output = chain.run(questions=event_questions)
    # print(llm_output)

    # # Split the input_data by newlines to create a list
    # qs_list = llm_output.strip().split('\n')
    # # Initialize an empty list to hold the output
    # qs_formatted = []

    # # Iterate over each element in the list
    # for i in qs_list:
    #     try:
    #         # Split each line into two parts: the question number and the question text
    #         question_num, question_text = i.split(': ', 1)
    #         # Extract the difficulty level from the question number
    #         num_covered = question_num[-2:-1]
    #         # Create the desired format and append to output_list
    #         qs_formatted.append(f"{question_text} ({num_covered})")
    #     except:
    #         continue


    # # llm_output = chain.run(questions=
    # #                        "What is the future of AI?, Will AI impact healthcare?, Will AI destroy humanity?"+\
    # #                        "Who are the big actors in AI? Who is known to have the best foundation models?"+\
    # #                        "Can anyone enter AI research from scratch?, What books should I read to get up to date with AI?"
    # # )
    # # print(llm_output)

    # return qs_formatted