import os
import streamlit as st
from database_class import EventDatabase
from llm_actions import summarize_questions_gpt

# def check_overlapping_questions(new_list, existing_list):
#     new_list_set = set(new_list)
#     existing_list_set = set(existing_list)
#     new_list_set -= existing_list_set
#     return list(new_list_set)

# # Define the pages
# def host_page():
#     st.markdown(':blue[_Host_] _view_.')
#     # Host-related activities go here
#     if 'eventdb' not in st.session_state:
#         st.session_state['eventdb'] = None

#     if 'event_name' not in st.session_state:
#         st.session_state['event_name'] = ''

#     if 'event_database_name' not in st.session_state:
#         st.session_state['event_database_name'] = ''

#     if 'event_presenter' not in st.session_state:
#         st.session_state['event_presenter'] = ''

#     if 'question_list' not in st.session_state:
#         st.session_state['question_list'] = []

#     if 'summarized_questions' not in st.session_state:
#         st.session_state['summarized_questions'] = []

#     if 'influential_questions' not in st.session_state:
#         st.session_state['influential_questions'] = []

#     if 'easy_questions' not in st.session_state:
#         st.session_state['easy_questions'] = []

#     if 'difficult_questions' not in st.session_state:
#         st.session_state['difficult_questions'] = []

#     # Before you define your button, check if the 'last_action' is not in the session state
#     if 'last_action' not in st.session_state:
#         st.session_state['last_action'] = None

#     if 'easy_button_counter' not in st.session_state:
#         st.session_state['easy_button_counter'] = 0

#     if 'hard_button_counter' not in st.session_state:
#         st.session_state['hard_button_counter'] = 0


#     # Create the session state variables if they don't exist
#     if not st.session_state['eventdb']:
#         with st.form(key='event_name_form'):
#             event_name = st.text_input("Please enter your event name:")
#             event_presenter = st.text_input("Please enter the presenter name:")
#             event_name_button = st.form_submit_button(label='Provide Event Information')
#         if event_name_button and len(event_name)>0 and len(event_presenter)>0:
#             st.session_state['last_action'] = 'event_name'
#             st.success('Provided event name successfully')
#             event_database_name = event_name.replace(" ", "")
#             st.session_state['eventdb'] = EventDatabase(event_database_name)
#             st.session_state['event_name'] = event_name
#             st.session_state['event_database_name'] = event_database_name
#             st.session_state['event_presenter'] = event_presenter
#             st.experimental_rerun() # remove the form and add the subheader
#         elif event_name_button:
#             st.warning('Please fill in both the event name and presenter fields before submitting.')
#     else:
#         eventdb = st.session_state['eventdb']
#         st.subheader(f"Q&A: {st.session_state['event_name']}, by {st.session_state['event_presenter']}")

#     if len(st.session_state['event_name'])>0:
#         # Set up the layout with two columns
#         col1, col2 = st.columns(2)    
#         # Display the questions received in the left column
#         with col1:
#             st.header('Questions Received')
#             if not st.session_state['eventdb'].is_db_empty():
#                 # Add a "Summarize Questions" button at the end of this column
#                 if st.button('Read and Summarize Questions'):
#                     # If the button is clicked, update the last_action and summarized questions in the session state
#                     st.session_state['last_action'] = 'summarize_questions'
#                     st.session_state['summarized_questions'], st.session_state['easy_questions'], st.session_state['difficult_questions'] = summarize_questions_gpt(
#                         st.session_state['event_database_name'],
#                         st.session_state['event_name'], 
#                         st.session_state['event_presenter']
#                     )

#                 # Adding CSS for custom scrollable section
#                 css='''
#                 <style>
#                 [data-testid="stExpander"] .streamlit-expanderHeader, [data-testid="stExpander"] .streamlit-expanderContent {
#                     overflow: auto;
#                     max-height: 300px;
#                 }
#                 </style>
#                 '''
#                 st.markdown(css, unsafe_allow_html=True)

#                 # Create a container for the questions
#                 st.session_state['question_list'] = st.session_state['eventdb'].get_questions_from_db()
#                 if  len(st.session_state['question_list'])>0:
#                     num_questions = len(st.session_state['question_list'])
#                     tstring = f"See questions (Total: {num_questions})"
#                 else:
#                     tstring = "No questions have been asked yet."
#                 with st.expander(tstring):  
#                     for question in st.session_state['question_list']:
#                         st.markdown(f'- {question}')
#             else:
#                 st.markdown('No questions have been asked yet.')
        
#         # Display the summarized questions in the right column
#         with col2:
#             st.header('Summarized Questions')
#             if len(st.session_state['summarized_questions'])>0:
#                 for question in st.session_state['summarized_questions']:
#                     st.markdown(f'- {question}')
#             else:
#                 st.markdown("No questions have been summarized yet.")

#         # Set up the layout with three columns
#         col3, col4 = st.columns(2)

#         # Display the easy questions in the second column
#         with col3:
#             st.header('Easy Questions')
#             if not st.session_state['eventdb'].is_db_empty():
#                 if len(st.session_state["summarized_questions"])>0:
#                     if st.button('Suggest Easy Questions'):
#                         st.session_state['last_action'] = 'easy_questions'
#                         st.session_state['easy_button_counter'] += 1
#                         # st.session_state['easy_questions'] += st.session_state['eventdb'].get_random_questions()
#                         # make sure there is no overlap between the easy and hard questions
#                         if st.session_state['difficult_questions'] is not None:
#                             st.session_state['easy_questions'] = check_overlapping_questions(
#                                 st.session_state['easy_questions'],
#                                 st.session_state['difficult_questions']
#                             )
#                     if st.session_state['easy_button_counter']>0:
#                         for question in st.session_state['easy_questions']:
#                             st.markdown(f'- {question}')
#                 else:
#                     st.markdown('Requesting easy questions will be available after summarization.')
#             else:
#                 st.markdown('No questions have been asked yet.')

#         # Display the difficult questions in the third column
#         with col4:
#             st.header('Difficult Questions')
#             if not st.session_state['eventdb'].is_db_empty():
#                 if len(st.session_state["summarized_questions"])>0:
#                     if st.button('Suggest Difficult Questions'):
#                         st.session_state['last_action'] = 'hard_questions'
#                         st.session_state['hard_button_counter'] += 1
#                         # st.session_state['difficult_questions'] += st.session_state['eventdb'].get_random_questions()
#                         # make sure there is no overlap between the easy and hard questions
#                         if st.session_state['easy_questions'] is not None:
#                             st.session_state['difficult_questions'] = check_overlapping_questions(
#                                 st.session_state['difficult_questions'],
#                                 st.session_state['easy_questions']
#                             )
#                     if st.session_state['hard_button_counter']>0:
#                         for question in st.session_state['difficult_questions']:
#                             st.markdown(f'- {question}')
#                 else:
#                     st.markdown('Requesting difficult questions will be available after summarization.')
#             else:
#                 st.markdown('No questions have been asked yet.')

#         # Display the influential person questions
#         st.header('Influential Person Questions')
#         if not st.session_state['eventdb'].is_db_empty():
#             most_influential = st.session_state['eventdb'].get_most_influential_question()
#             st.markdown(f"**{most_influential[2].strip()}**")
#             st.markdown(f"by **{most_influential[0]}** with **{most_influential[1]}** followers")
#         else:
#             st.markdown('No questions have been asked yet.')


# def participant_page():
#     st.markdown(':blue[_Participant_] _view_.')
#     # Participant-related activities go here

#     # Create the session state variables if they don't exist
#     if 'eventdb' not in st.session_state:
#         st.session_state['eventdb'] = None

#     if 'event_name' not in st.session_state:
#         st.session_state['event_name'] = ''

#     if 'event_database_name' not in st.session_state:
#         st.session_state['event_database_name'] = ''

#     if 'event_presenter' not in st.session_state:
#         st.session_state['event_presenter'] = ''

#     # Before you define your button, check if the 'last_action' is not in the session state
#     if 'last_action' not in st.session_state:
#         st.session_state['last_action'] = None

#     if 'num_questions_asked' not in st.session_state:
#         st.session_state['num_questions_asked']=0
    
#     if 'name_input' not in st.session_state:
#         st.session_state['name_input']=0
#     if 'followers_input' not in st.session_state:
#         st.session_state['followers_input']=0
#     if 'question_input' not in st.session_state:
#         st.session_state['question_input']=0

#     if not st.session_state['eventdb']:
#         # Get all items in the "events" directory
#         items = os.listdir('./events/')
#         # Filter the list to only include ".sqlite" files
#         event_name_files = [item.split('.')[0] for item in items if item.endswith('.sqlite')]
#         # Add the placeholder string to the beginning of the list
#         event_name_files.insert(0, 'Select a file...')
#         selected_file = st.selectbox('What event are you participating in?', event_name_files) 
#         st.session_state['event_database_name'] = selected_file
#         if selected_file != 'Select a file...':
#             st.session_state['eventdb'] = EventDatabase(st.session_state['event_database_name'])
#             st.experimental_rerun() # remove the form and add the subheader
#     else:
#         st.subheader(f"Q&A: {st.session_state['event_database_name']}")
#         eventdb = st.session_state['eventdb']
#         if st.session_state['num_questions_asked'] == 0:
#             with st.form(key='question_form'):
#                 # Use columns to create a row of input fields
#                 col_form1, col_form2 = st.columns(2)
#                 st.session_state['name_input'] = col_form1.text_input('Please enter your name:')
#                 st.session_state['followers_input'] = col_form2.number_input('Number of followers:', min_value=0)
#                 st.session_state['question_input'] = st.text_input('Question:')
#                 submit_button = st.form_submit_button(label='Submit Question')
            
#             if submit_button and st.session_state['name_input'] and st.session_state['followers_input'] is not None and st.session_state['question_input']:
#                 st.session_state['last_action'] = 'submit_question'
#                 eventdb.add_question_to_db(
#                     st.session_state['name_input'], 
#                     st.session_state['followers_input'], 
#                     st.session_state['question_input']
#                 ) 
#                 st.session_state['num_questions_asked'] += 1
#                 num_counts = st.session_state['num_questions_asked']
#                 st.success(f'Question {num_counts} submitted successfully')
#                 st.experimental_rerun()

#         else:
#             st.markdown(st.session_state['name_input'] + \
#                         ', ' + str(st.session_state['followers_input']) + \
#                         ' followers.'    
#             )
#             with st.form(key='question_form', clear_on_submit=True):
#                 st.session_state['question_input'] = st.text_input('Question:')
#                 submit_button = st.form_submit_button(label='Submit Question')
#                 num_counts = st.session_state['num_questions_asked']
#             if submit_button and st.session_state['question_input']:
#                 eventdb.add_question_to_db(
#                     st.session_state['name_input'], 
#                     st.session_state['followers_input'], 
#                     st.session_state['question_input']
#                 )
#                 st.session_state['num_questions_asked'] += 1
#                 num_counts = st.session_state['num_questions_asked']
#             st.success(f'Question {num_counts} submitted successfully')


def main_page():
    # st.set_page_config(layout="wide", page_title="Q&A Streamliner", page_icon=":microphone:") # Add this line
    # st.markdown("<h1 style='text-align: center; color: black;'>Streamliner App</h1>", unsafe_allow_html=True)
    # st.sidebar.markdown("# Main page 🎈")
    # # Initialize session state
    # if 'user_role' not in st.session_state:
    #     st.session_state['user_role'] = ''

    # if len(st.session_state['user_role'])==0:
    #     st.header("Please choose your role")
    #     role = st.radio("", ["Host", "Participant"])
    #     if st.button("Submit"):
    #         st.session_state['user_role'] = role
    #         st.experimental_rerun()
    # elif st.session_state['user_role'] == "Host":
    #     host_page()
    # elif st.session_state['user_role'] == "Participant":
    #     participant_page()
    # page_names_to_funcs = {
    #     "Main Page": main_page,
    #     "Host": host_page,
    #     "Participant": participant_page,
    # }

    # selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
    # page_names_to_funcs[selected_page]()
    # st.sidebar.markdown("# What and why?.")
    st.markdown("""
# Q&A Streamliner - Revolutionizing Q&A Sessions 

## Introduction

Are you an event organizer constantly grappling with a torrent of questions during your Q&A sessions? Do you strive to ensure that the most meaningful questions get answered, but often feel overwhelmed by the sheer volume? Welcome to **Q&A Streamliner!** We're thrilled to introduce our innovative web application that will revolutionize your Q&A management experience. 

---

## Why Q&A Streamliner is Essential?

Q&A sessions are a cornerstone in any event. They open avenues for engaging dialogue and foster a sense of involvement among the audience. But, as the event size increases, managing this critical part can turn daunting. 

- **Are you overwhelmed by volume?** Traditional Q&A systems struggle with hundreds, even thousands, of questions.
- **Missing out on meaningful exchanges?** Amidst a flood of queries, meaningful ones can get lost, leaving key discussions untapped.
- **Feeling the pinch of time and resources?** Manual sorting of questions can consume significant resources and time.
- **Need a tailored approach?** Traditional systems don't recognize the influence or expertise of individuals, often treating a vital question from a key participant as just another query.

This is where Q&A Streamliner comes to your rescue, presenting a much-needed solution to these challenges.

---

## The Solution - Efficient, Innovative, and Inclusive

Q&A Streamliner uses the power of AI and machine learning technologies to organize, prioritize, and streamline your Q&A sessions:

- **Categorize & Summarize:** Our AI clusters similar questions into manageable categories and provides summaries, enabling you to address broader topics rather than each individual question.
- **Ranking by Complexity:** Questions are ranked based on their complexity, giving you the flexibility to customize the flow of your Q&A session.
- **Recognizing Influencers:** Q&A Streamliner highlights questions from influential individuals, ensuring their inputs aren't overlooked.

The result? An organized, efficient, and inclusive Q&A session that delivers value to your audience and aligns perfectly with your event objectives.

---

## The Innovation You've Been Waiting For

Q&A Streamliner isn't just another Q&A management tool. It's a vision to redefine event planning, combining the power of machine learning with a user-friendly web-based interface. We've designed Q&A Streamliner with your needs at heart, ensuring an intuitive, scalable, and secure platform suitable for both small gatherings and larger, international events.

---

## Embrace the Future with Q&A Streamliner

Our vision for the future goes beyond just enhancing Q&A sessions. We're looking at a transformation in the event management landscape, thanks to AI-driven innovations:

- **AI-Driven Event Planning:** Imagine machine learning predicting your event needs and offering precise planning recommendations.
- **Smart Networking:** What about AI-powered matchmaking to foster meaningful connections among attendees based on shared interests and expertise?
- **Real-Time Event Analysis:** Or AI providing instant insights into attendee engagement and session popularity, allowing you to adapt your event dynamics in real-time?
- **AI-Generated Summaries:** How about AI summarizing your event, capturing key highlights and discussion points?

Moreover, we're thrilled to announce our upcoming feature - a **Live Event Chatbot**:

- **Catch-Up Feature:** Attendees arriving late can chat with the bot to get up to speed with the event.
- **Concept Clarification:** If participants need clarity on concepts discussed during the event, the chatbot is at their service.

---

By choosing Q&A Streamliner, you're not just buying a product; you're partnering with the future of event management. So, let's make every question, every interaction, and every event count! Welcome to the next level of event experiences.

""")


if __name__ == "__main__":
    main_page()
