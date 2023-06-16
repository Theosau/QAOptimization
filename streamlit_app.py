import os
import streamlit as st
from database_class import EventDatabase
from llm_actions import summarize_questions_gpt

def check_overlapping_questions(new_list, existing_list):
    new_list_set = set(new_list)
    existing_list_set = set(existing_list)
    new_list_set -= existing_list_set
    return list(new_list_set)

def main():
    st.set_page_config(layout="wide", page_title="Q&A Streamliner", page_icon=":microphone:") # Add this line
    st.markdown("<h1 style='text-align: center; color: black;'>Streamliner App</h1>", unsafe_allow_html=True)

    # Create the session state variables if they don't exist
    if 'eventdb' not in st.session_state:
        st.session_state['eventdb'] = None

    if 'event_name' not in st.session_state:
        st.session_state['event_name'] = ''

    if 'event_database_name' not in st.session_state:
        st.session_state['event_database_name'] = ''

    if 'event_presenter' not in st.session_state:
        st.session_state['event_presenter'] = ''

    if 'question_list' not in st.session_state:
        st.session_state['question_list'] = []

    if 'summarized_questions' not in st.session_state:
        st.session_state['summarized_questions'] = []

    if 'influential_questions' not in st.session_state:
        st.session_state['influential_questions'] = []

    if 'easy_questions' not in st.session_state:
        st.session_state['easy_questions'] = []

    if 'difficult_questions' not in st.session_state:
        st.session_state['difficult_questions'] = []

    if 'question_input' not in st.session_state:
        st.session_state['question_input'] = ''

    # Before you define your button, check if the 'last_action' is not in the session state
    if 'last_action' not in st.session_state:
        st.session_state['last_action'] = None

    if 'easy_button_counter' not in st.session_state:
        st.session_state['easy_button_counter'] = 0

    if 'hard_button_counter' not in st.session_state:
        st.session_state['hard_button_counter'] = 0

    # Create the session state variables if they don't exist
    if not st.session_state['eventdb']:
        with st.form(key='event_name_form'):
            event_name = st.text_input("Please enter your event name:")
            event_presenter = st.text_input("Please enter the presenter name:")
            event_name_button = st.form_submit_button(label='Provide Event Information')
        if event_name_button and len(event_name)>0 and len(event_presenter)>0:
            st.session_state['last_action'] = 'event_name'
            st.success('Provided event name successfully')
            event_database_name = event_name.replace(" ", "")
            st.session_state['eventdb'] = EventDatabase(event_database_name)
            st.session_state['event_name'] = event_name
            st.session_state['event_database_name'] = event_database_name
            st.session_state['event_presenter'] = event_presenter
            st.experimental_rerun() # remove the form and add the subheader
        elif event_name_button:
            st.warning('Please fill in both the event name and presenter fields before submitting.')
    else:
        eventdb = st.session_state['eventdb']
        st.subheader(f"Q&A: {st.session_state['event_name']}, by {st.session_state['event_presenter']}")


    if len(st.session_state['event_name'])>0:
        st.markdown(':blue[_Participant_] _view_.')
        with st.form(key='question_form', clear_on_submit=True):
            # Use columns to create a row of input fields
            col_form1, col_form2 = st.columns(2)
            name_input = col_form1.text_input('Please enter your name:')
            followers_input = col_form2.number_input('Number of followers:', min_value=0)
            question_input = st.text_input('Question:')
            submit_button = st.form_submit_button(label='Submit Question')

        if submit_button and name_input and followers_input is not None and question_input:
            st.session_state['last_action'] = 'submit_question'
            eventdb.add_question_to_db(name_input, followers_input, question_input)  # Store the data in the database
            st.success('Question submitted successfully')

        st.markdown(':blue[_Host_] _view_.')
        # Set up the layout with two columns
        col1, col2 = st.columns(2)    
        # Display the questions received in the left column
        with col1:
            st.header('Questions Received')
            if not st.session_state['eventdb'].is_db_empty():
                # Add a "Summarize Questions" button at the end of this column
                if st.button('Read and Summarize Questions'):
                    # If the button is clicked, update the last_action and summarized questions in the session state
                    st.session_state['last_action'] = 'summarize_questions'
                    st.session_state['summarized_questions'], st.session_state['easy_questions'], st.session_state['difficult_questions'] = summarize_questions_gpt(
                        st.session_state['event_database_name'],
                        st.session_state['event_name'], 
                        st.session_state['event_presenter']
                    )

                # Adding CSS for custom scrollable section
                css='''
                <style>
                [data-testid="stExpander"] .streamlit-expanderHeader, [data-testid="stExpander"] .streamlit-expanderContent {
                    overflow: auto;
                    max-height: 300px;
                }
                </style>
                '''
                st.markdown(css, unsafe_allow_html=True)

                # Create a container for the questions
                st.session_state['question_list'] = st.session_state['eventdb'].get_questions_from_db()
                if  len(st.session_state['question_list'])>0:
                    num_questions = len(st.session_state['question_list'])
                    tstring = f"See questions (Total: {num_questions})"
                else:
                    tstring = "No questions have been asked yet."
                with st.expander(tstring):  
                    for question in st.session_state['question_list']:
                        st.markdown(f'- {question}')
            else:
                st.markdown('No questions have been asked yet.')
        
        # Display the summarized questions in the right column
        with col2:
            st.header('Summarized Questions')
            if len(st.session_state['summarized_questions'])>0:
                for question in st.session_state['summarized_questions']:
                    st.markdown(f'- {question}')
            else:
                st.markdown("No questions have been summarized yet.")

        # Set up the layout with three columns
        col3, col4 = st.columns(2)

        # Display the easy questions in the second column
        with col3:
            st.header('Easy Questions')
            if not st.session_state['eventdb'].is_db_empty():
                if len(st.session_state["summarized_questions"])>0:
                    if st.button('Suggest Easy Questions'):
                        st.session_state['last_action'] = 'easy_questions'
                        st.session_state['easy_button_counter'] += 1
                        # st.session_state['easy_questions'] += st.session_state['eventdb'].get_random_questions()
                        # make sure there is no overlap between the easy and hard questions
                        if st.session_state['difficult_questions'] is not None:
                            st.session_state['easy_questions'] = check_overlapping_questions(
                                st.session_state['easy_questions'],
                                st.session_state['difficult_questions']
                            )
                    if st.session_state['easy_button_counter']>0:
                        for question in st.session_state['easy_questions']:
                            st.markdown(f'- {question}')
                else:
                    st.markdown('Requesting easy questions will be available after summarization.')
            else:
                st.markdown('No questions have been asked yet.')

        # Display the difficult questions in the third column
        with col4:
            st.header('Difficult Questions')
            if not st.session_state['eventdb'].is_db_empty():
                if len(st.session_state["summarized_questions"])>0:
                    if st.button('Suggest Difficult Questions'):
                        st.session_state['last_action'] = 'hard_questions'
                        st.session_state['hard_button_counter'] += 1
                        # st.session_state['difficult_questions'] += st.session_state['eventdb'].get_random_questions()
                        # make sure there is no overlap between the easy and hard questions
                        if st.session_state['easy_questions'] is not None:
                            st.session_state['difficult_questions'] = check_overlapping_questions(
                                st.session_state['difficult_questions'],
                                st.session_state['easy_questions']
                            )
                    if st.session_state['hard_button_counter']>0:
                        for question in st.session_state['difficult_questions']:
                            st.markdown(f'- {question}')
                else:
                    st.markdown('Requesting difficult questions will be available after summarization.')
            else:
                st.markdown('No questions have been asked yet.')

        # Display the influential person questions
        st.header('Influential Person Questions')
        if not st.session_state['eventdb'].is_db_empty():
            most_influential = st.session_state['eventdb'].get_most_influential_question()
            st.markdown(f"**{most_influential[2].strip()}**")
            st.markdown(f"by **{most_influential[0]}** with **{most_influential[1]}** followers")
        else:
            st.markdown('No questions have been asked yet.')

if __name__ == "__main__":
    main()
