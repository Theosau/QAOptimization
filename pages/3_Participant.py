import os
import streamlit as st
from database_class import EventDatabase

def participant_page():
    st.markdown(':blue[_Participant_] _view_.')
    # Create the session state variables if they don't exist
    if 'participant_eventdb' not in st.session_state:
        st.session_state['participant_eventdb'] = None

    if 'participant_event_name' not in st.session_state:
        st.session_state['participant_event_name'] = ''

    if 'participant_event_database_name' not in st.session_state:
        st.session_state['participant_event_database_name'] = ''

    if 'participant_event_presenter' not in st.session_state:
        st.session_state['participant_event_presenter'] = ''

    # Before you define your button, check if the 'last_action' is not in the session state
    if 'last_action' not in st.session_state:
        st.session_state['last_action'] = None

    if 'num_questions_asked' not in st.session_state:
        st.session_state['num_questions_asked']=0
    
    if 'name_input' not in st.session_state:
        st.session_state['name_input']=''
    if 'followers_input' not in st.session_state:
        st.session_state['followers_input']=0
    if 'question_input' not in st.session_state:
        st.session_state['question_input']=''
    if 'initial_question_input' not in st.session_state:
        st.session_state['initial_question_input']=''
        
    if not st.session_state['participant_eventdb']:
        # Get all items in the "events" directory
        items = os.listdir('./events/')
        # Filter the list to only include ".sqlite" files
        event_name_files = [item.split('.')[0] for item in items if item.endswith('.sqlite')]
        # Add the placeholder string to the beginning of the list
        event_name_files.insert(0, 'Select a file...')
        selected_file = st.selectbox('What event are you participating in?', event_name_files) 
        st.session_state['participant_event_database_name'] = selected_file
        if selected_file != 'Select a file...':
            st.session_state['participant_eventdb'] = EventDatabase(st.session_state['participant_event_database_name'])
            st.experimental_rerun() # remove the form and add the subheader
    else:
        st.subheader(f"Q&A: {st.session_state['participant_event_database_name']}")
        eventdb = st.session_state['participant_eventdb']
        if st.session_state['num_questions_asked'] == 0:
            with st.form(key='question_form', clear_on_submit=True):
                # Use columns to create a row of input fields
                col_form1, col_form2 = st.columns(2)
                st.session_state['name_input'] = col_form1.text_input('Please enter your name:')
                st.session_state['followers_input'] = col_form2.number_input('Number of followers:', min_value=0)
                st.session_state['initial_question_input'] = st.text_input('Question:')
                submit_button = st.form_submit_button(label='Submit Question')
            
            if submit_button and st.session_state['name_input'] and st.session_state['followers_input'] is not None and st.session_state['initial_question_input']:
                st.session_state['last_action'] = 'submit_question'
                eventdb.add_question_to_db(
                    st.session_state['name_input'], 
                    st.session_state['followers_input'], 
                    st.session_state['initial_question_input']
                )
                st.session_state['num_questions_asked'] += 1
                num_counts = st.session_state['num_questions_asked']
                st.success(f'Question {num_counts} submitted successfully')
                st.experimental_rerun()

        else:
            st.markdown(st.session_state['name_input'] + \
                        ', ' + str(st.session_state['followers_input']) + \
                        ' followers.'    
            )
            if st.button('Change Participant'):
                # Reset specific session state variables
                st.session_state['num_questions_asked'] = 0
                st.session_state['name_input'] = ''
                st.session_state['followers_input'] = 0
                st.session_state['initial_question_input'] = ''
                st.experimental_rerun() # reset

            with st.form(key='question_form', clear_on_submit=True):
                st.session_state['question_input'] = st.text_input('Question:')
                submit_button = st.form_submit_button(label='Submit Question')
                num_counts = st.session_state['num_questions_asked']
            if submit_button and st.session_state['question_input']:
                eventdb.add_question_to_db(
                    st.session_state['name_input'], 
                    st.session_state['followers_input'], 
                    st.session_state['question_input']
                )
                st.session_state['num_questions_asked'] += 1
                num_counts = st.session_state['num_questions_asked']
            st.success(f'Question {num_counts} submitted successfully')

if __name__ == "__main__":
    participant_page()