import streamlit as st
from database_class import EventDatabase
from llm_actions import suggest_easy_hard_questions, suggest_categories, categorize_questions

def check_overlapping_questions(new_list, existing_list):
    new_list_set = set(new_list)
    existing_list_set = set(existing_list)
    new_list_set -= existing_list_set
    return list(new_list_set)

# Define the pages
def host_page():
    st.markdown(':blue[_Host_] _view_.')
    # st.sidebar.markdown("# Host Page 2 ❄️")
    # Host-related activities go here
    if 'host_eventdb' not in st.session_state:
        st.session_state['host_eventdb'] = None

    if 'host_event_name' not in st.session_state:
        st.session_state['host_event_name'] = ''

    if 'host_event_database_name' not in st.session_state:
        st.session_state['host_event_database_name'] = ''

    if 'host_event_presenter' not in st.session_state:
        st.session_state['host_event_presenter'] = ''

    if 'question_list' not in st.session_state:
        st.session_state['question_list'] = []

    if 'summarized_questions' not in st.session_state:
        st.session_state['summarized_questions'] = []

    if 'influential_questions' not in st.session_state:
        st.session_state['influential_questions'] = []

    if 'easy_questions' not in st.session_state:
        st.session_state['easy_questions'] = []

    if 'hard_questions' not in st.session_state:
        st.session_state['hard_questions'] = []

    # Before you define your button, check if the 'last_action' is not in the session state
    if 'last_action' not in st.session_state:
        st.session_state['last_action'] = None

    if 'easy_button_counter' not in st.session_state:
        st.session_state['easy_button_counter'] = 0

    if 'hard_button_counter' not in st.session_state:
        st.session_state['hard_button_counter'] = 0

    if 'event_categories' not in st.session_state:
        st.session_state['event_categories'] = []

    if 'questions_cat0' not in st.session_state:
        st.session_state['questions_cat0'] = []

    if 'questions_cat1' not in st.session_state:
        st.session_state['questions_cat1'] = []

    if 'questions_cat2' not in st.session_state:
        st.session_state['questions_cat2'] = []

    if 'questions_cat3' not in st.session_state:
        st.session_state['questions_cat3'] = []

    if 'use_model' not in st.session_state:
        st.session_state['use_model'] = False

    # Create the session state variables if they don't exist
    if not st.session_state['host_eventdb']:
        with st.form(key='event_name_form'):
            event_name = st.text_input("Please enter your event name:")
            event_presenter = st.text_input("Please enter the presenter name:")
            event_name_button = st.form_submit_button(label='Provide Event Information')
        if event_name_button and len(event_name)>0 and len(event_presenter)>0:
            st.session_state['last_action'] = 'host_event_name'
            st.success('Provided event name successfully')
            event_database_name = (event_name + ' by ' + event_presenter).replace(" ", "_")
            st.session_state['host_eventdb'] = EventDatabase(event_database_name)
            st.session_state['host_event_name'] = event_name
            st.session_state['host_event_database_name'] = event_database_name
            st.session_state['host_event_presenter'] = event_presenter
            st.experimental_rerun() # remove the form and add the subheader
        elif event_name_button:
            st.warning('Please fill in both the event name and presenter fields before submitting.')
    else:
        eventdb = st.session_state['host_eventdb']
        event_name = st.session_state['host_event_database_name'].replace("_", " ")
        st.subheader(f"Q&A: {event_name}")

    if len(st.session_state['host_event_name'])>0:
        if st.session_state["event_categories"]==0:
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
            st.session_state['question_list'] = st.session_state['host_eventdb'].get_questions_from_db()
            if  len(st.session_state['question_list'])>0:
                num_questions = len(st.session_state['question_list'])
                tstring = f"See questions (Total: {num_questions})"
            else:
                tstring = "No questions have been asked yet."
                st.markdown(tstring)
            with st.expander(tstring):  
                for question in st.session_state['question_list']:
                    st.markdown(f'- {question}')
            
            # button to categorize the questions
            threshold_num_questions = 10
            if len(st.session_state['question_list'])>=threshold_num_questions:
                if st.button("Categorize questions"):
                    if st.session_state["use_model"]:
                        st.session_state["event_categories"] = suggest_categories(
                            st.session_state['question_list']
                        )
                        questions_categories = categorize_questions(st.session_state['question_list'])
                        st.session_state['host_eventdb'].add_questions_category(
                            st.session_state['question_list'], 
                            questions_categories
                        )
                        for i in range(4):
                            st.session_state[f'questions_cat{i}'] = st.session_state['host_eventdb'].get_questions_in_category(
                                st.session_state["event_categories"][i]
                            )
                    else:
                        st.session_state["event_categories"] = [
                            "Climate Policy Implementation and Enforcement", 
                            "Business Incentives and Global Challenges",
                            "Other",
                            "Off topic"
                        ]
            else:
                st.markdown(f"When there will be more than {threshold_num_questions} questions, you will have the option to categorize and summarize them.")
        else:
            # Set up the layout with two columns
            col0_cat0, col1_cat0, col2_cat0 = st.columns(3)

            # Display the questions received in the left column
            with col0_cat0:
                st.markdown(st.session_state["event_categories"][0])
            with col1_cat0:
                with st.expander("Expand questions"):  
                    for question in ["Question 0", "Question 1"]:
                        st.markdown(f'- {question}')
                # Add a "Summarize Questions" button at the end of this column
            with col2_cat0:
                if st.button('Summarize_Cat0'):
                    st.session_state['last_action'] = 'summarize_questions_cat0'
        
            st.divider()

            # Set up the layout with two columns
            col0_cat1, col1_cat1, col2_cat1 = st.columns(3)

            # Display the questions received in the left column
            with col0_cat1:
                st.markdown(st.session_state["event_categories"][1])
            with col1_cat1:
                with st.expander("Expand questions"):  
                    for question in ["Question 0", "Question 1"]:
                        st.markdown(f'- {question}')
                # Add a "Summarize Questions" button at the end of this column
            with col2_cat1:
                if st.button('Summarize_Cat1'):
                    st.session_state['last_action'] = 'summarize_questions_cat1'

        #### Easy, hard, influential - not impacted by categorization 
        # (though I still need to make sure that I gather the easy and hard from my initial categorization call)
        # Set up the layout with three columns
        col_easy, col_hard = st.columns(2)
        threshold_easy_hard_questions = 4
        with col_easy:
            st.header('Straightforward')
            if not st.session_state['host_eventdb'].is_db_empty():
                if len(st.session_state["question_list"])>=threshold_easy_hard_questions:
                    if st.button('Suggest Questions', key='Suggest_Straightforward_Questions'):
                        st.session_state['last_action'] = 'easy_questions'
                        st.session_state['easy_button_counter'] += 1
                        if len(st.session_state['easy_questions'])==0:
                            if st.session_state["use_model"]:
                                st.session_state['easy_questions'], st.session_state['hard_questions'] = suggest_easy_hard_questions(
                                    st.session_state['question_list']
                                )
                            else:
                                st.session_state['easy_questions'] = [
                                    "Template simple 0", 
                                    "Template simple 1"
                                ]
                                st.session_state['hard_questions'] = [
                                    "Template complex 0", 
                                    "Template complex 1"
                                ]
                        # make sure there is no overlap between the easy and hard questions
                        if len(st.session_state['hard_questions'])>0:
                            st.session_state['easy_questions'] = check_overlapping_questions(
                                st.session_state['easy_questions'],
                                st.session_state['hard_questions']
                            )
                    if st.session_state['easy_button_counter']>0:
                        for question in st.session_state['easy_questions']:
                            st.markdown(f'- {question}')
                else:
                    st.markdown(f'Requesting straightforward questions will be available once there will be more than {threshold_easy_hard_questions} questions.')
            else:
                st.markdown('No questions have been asked yet.')

        # Display the challenging questions
        with col_hard:
            st.header('Challenging')
            if not st.session_state['host_eventdb'].is_db_empty():
                if len(st.session_state["question_list"])>=threshold_easy_hard_questions:
                    if st.button('Suggest Questions', key='Suggest_Challenging_Questions'):
                        st.session_state['last_action'] = 'hard_questions'
                        st.session_state['hard_button_counter'] += 1
                        if len(st.session_state['hard_questions'])==0:
                            if st.session_state["use_model"]:
                                st.session_state['easy_questions'], st.session_state['hard_questions'] = suggest_easy_hard_questions(
                                    st.session_state['question_list']
                                )
                            else:
                                st.session_state['easy_questions'] = [
                                    "Template simple 0", 
                                    "Template simple 1"
                                ]
                                st.session_state['hard_questions'] = [
                                    "Template complex 0", 
                                    "Template complex 1"
                                ]
                        # make sure there is no overlap between the easy and hard questions
                        if len(st.session_state['easy_questions'])>0:
                            st.session_state['hard_questions'] = check_overlapping_questions(
                                st.session_state['hard_questions'],
                                st.session_state['easy_questions']
                            )
                    if st.session_state['hard_button_counter']>0:
                        for question in st.session_state['hard_questions']:
                            st.markdown(f'- {question}')
                else:
                    st.markdown(f'Requesting challenging questions will be available once there will be more than {threshold_easy_hard_questions} questions.')
            else:
                st.markdown('No questions have been asked yet.')

        # Display the influential person questions
        st.header('Influential Person Questions')
        if not st.session_state['host_eventdb'].is_db_empty():
            most_influential = st.session_state['host_eventdb'].get_most_influential_question()
            st.markdown(f"**{most_influential[2].strip()}**")
            st.markdown(f"by **{most_influential[0]}** with **{most_influential[1]}** followers")
        else:
            st.markdown('No questions have been asked yet.')

if __name__ == "__main__":
    host_page()