import os
import streamlit as st
from database_class import EventDatabase
from llm_actions import suggest_easy_hard_questions, suggest_categories, categorize_questions, summarize_questions_gpt

def check_overlapping_questions(new_list, existing_list):
    new_list_set = set(new_list)
    existing_list_set = set(existing_list)
    new_list_set -= existing_list_set
    return list(new_list_set)

# Define the pages
def host_page():
    st.set_page_config(layout="wide")
    st.markdown(':blue[_Host_] _view_.')
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
    if 'summarized_cat0' not in st.session_state:
        st.session_state["summarized_cat0"] = []
    if 'summarized_cat1' not in st.session_state:
        st.session_state["summarized_cat1"] = []
    if 'summarized_cat2' not in st.session_state:
        st.session_state["summarized_cat2"] = []
    if 'summarized_cat3' not in st.session_state:
        st.session_state["summarized_cat3"] = []
    if 'newly_added_questions' not in st.session_state:
        st.session_state['newly_added_questions'] = []
    if 'list_categories_string' not in st.session_state:
        st.session_state['list_categories_string'] = []
    if 'new_qs_categorized' not in st.session_state:
        st.session_state['new_qs_categorized'] = False

    # Create the session state variables if they don't exist
    if not st.session_state['host_eventdb']:
        event_type = st.radio(
            'Select your event', 
            ('New', 'Existing')
        )
        if event_type == 'New':
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
             # Get all items in the "events" directory
            items = os.listdir('./events/')
            # Filter the list to only include ".sqlite" files
            event_name_files = [item.split('.')[0].replace("_", " ") for item in items if item.endswith('.sqlite')]

            # Add the placeholder string to the beginning of the list
            event_name_files.insert(0, 'Select a file...')
            selected_file = st.selectbox('What event are you participating in?', event_name_files)
            # When processing the selection, replace spaces back with underscores
            if selected_file != 'Select a file...':
                st.session_state['host_event_name'], st.session_state['host_event_presenter'] = selected_file.split(' by ')
                selected_file = selected_file.replace(" ", "_")
                st.session_state['host_event_database_name'] = selected_file
                st.session_state['host_eventdb'] = EventDatabase(st.session_state['host_event_database_name'])
                st.experimental_rerun()
    else:
        # eventdb = st.session_state['host_eventdb']
        event_name = st.session_state['host_event_database_name'].replace("_", " ")
        st.subheader(f"Q&A: {event_name}")

    if len(st.session_state['host_event_name'])>0:
        if len(st.session_state["event_categories"])==0:
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
                        catergories_dict, st.session_state["list_categories_string"] = suggest_categories(
                            st.session_state['host_event_database_name'],
                            st.session_state['host_event_name'], 
                            st.session_state['host_event_presenter']
                        )
                        st.session_state["event_categories"] = list(catergories_dict.values())
                        questions_categories = categorize_questions(
                            st.session_state['question_list'],
                            st.session_state["list_categories_string"]
                        )
                        print(st.session_state["event_categories"])
                    else:
                        st.session_state["event_categories"] = [
                            "Climate Change Policy Implementation", 
                            "Renewable Energy and Carbon Capture",
                            "Climate Justice and Business Incentivization",
                            "Other"
                        ]
                        questions_categories = [0,1,2,0,0,2,0,1,0,3,3,3,3,3,3]
                    # add the categories in the database, and add each question to the categories' list
                    st.session_state['host_eventdb'].add_questions_category(
                        st.session_state['question_list'], 
                        questions_categories
                    )
                    for i in range(4):
                        st.session_state[f'questions_cat{i}'] = st.session_state['host_eventdb'].get_questions_by_category(i)
                    st.experimental_rerun() # update website  
            else:
                st.markdown(f"When there will be more than {threshold_num_questions} questions, you will have the option to categorize and summarize them.")
        else:
            threshold_num_questions_cat = 4
            # Set up the layout with three column per category
            col0_cat0, col1_cat0, col2_cat0 = st.columns(3)
            # Display the questions received in the left column
            with col0_cat0:
                st.markdown(st.session_state["event_categories"][0])
            with col1_cat0:
                num_qs = len(st.session_state['questions_cat0'])
                with st.expander(f"{num_qs} questions"):  
                    for question in st.session_state['questions_cat0']:
                        st.markdown(f'- {question}')
            with col2_cat0:
                if len(st.session_state['questions_cat0']) >= threshold_num_questions_cat:
                    if len(st.session_state["summarized_cat0"])==0:
                        if st.button('Summarize', key='Summarize_Cat0'):
                            print("summarized_cat0")
                            if st.session_state['use_model']:
                                st.session_state["summarized_cat0"] = summarize_questions_gpt(
                                    st.session_state['questions_cat0'],
                                    st.session_state['host_event_name'],
                                    st.session_state['host_event_presenter']
                                )
                            else:
                                st.session_state["summarized_cat0"] = [
                                   "How can climate change policies be effectively implemented on a global scale to address existing challenges and align with the Paris Agreement goals? (covering 3 questions)",
                                   "What policy changes can be made to drive both large-scale carbon capture and storage technologies and improve biodiversity conservation in the context of climate change? (covering 2 questions)"
                                ]
                            st.experimental_rerun() # update button print
                    else:
                        with st.expander("Summarized questions"):  
                            for question in st.session_state["summarized_cat0"]:
                                st.markdown(f'- {question}')
                else:
                    st.markdown(f'Summarization will be avilable once there will be more than {threshold_num_questions_cat} questions.')

            st.divider()

            # Set up the layout with three column per category
            col0_cat1, col1_cat1, col2_cat1 = st.columns(3)
            threshold_num_questions_cat = 4
            # Display the questions received in the left column
            with col0_cat1:
                st.markdown(st.session_state["event_categories"][1])
            with col1_cat1:
                num_qs = len(st.session_state['questions_cat1'])
                with st.expander(f"{num_qs} questions"):  
                    for question in st.session_state['questions_cat1']:
                        st.markdown(f'- {question}')
            with col2_cat1:
                if len(st.session_state['questions_cat1']) >= threshold_num_questions_cat:
                    if len(st.session_state["summarized_cat1"])==0:
                        if st.button('Summarize', key='Summarize_Cat1'):
                            print("summarized_cat1")
                            if st.session_state['use_model']:
                                st.session_state["summarized_cat1"] = summarize_questions_gpt(
                                    st.session_state['questions_cat1'],
                                    st.session_state['host_event_name'],
                                    st.session_state['host_event_presenter']
                                )
                            else:
                                pass
                            st.experimental_rerun() # update button print
                    else:
                        with st.expander("Summarized questions"):
                            for question in st.session_state["summarized_cat1"]:
                                st.markdown(f'- {question}')
                else:
                    st.markdown(f'Summarization will be avilable once there will be more than {threshold_num_questions_cat} questions.')

            st.divider()

            # Set up the layout with three column per category
            col0_cat2, col1_cat2, col2_cat2 = st.columns(3)
            # Display the questions received in the left column
            with col0_cat2:
                st.markdown(st.session_state["event_categories"][2])
            with col1_cat2:
                num_qs = len(st.session_state['questions_cat2'])
                with st.expander(f"{num_qs} questions"):   
                    for question in st.session_state['questions_cat2']:
                        st.markdown(f'- {question}')
            with col2_cat2:
                if len(st.session_state['questions_cat2']) >= threshold_num_questions_cat:
                    if len(st.session_state["summarized_cat2"])==0:
                        if st.button('Summarize', key='Summarize_Cat2'):
                            print("summarized_cat2")
                            if st.session_state['use_model']:
                                st.session_state["summarized_cat2"] = summarize_questions_gpt(
                                    st.session_state['questions_cat2'],
                                    st.session_state['host_event_name'],
                                    st.session_state['host_event_presenter']
                                )
                            else:
                                pass
                            st.experimental_rerun() # update button print
                    else:
                        with st.expander("Summarized questions"):
                            for question in st.session_state["summarized_cat2"]:
                                st.markdown(f'- {question}')
                else:
                    st.markdown(f'Summarization will be avilable once there will be more than {threshold_num_questions_cat} questions.')

            st.divider()

            # Set up the layout with three column per category
            col0_cat3, col1_cat3, col2_cat3 = st.columns(3)
            # Display the questions received in the left column
            with col0_cat3:
                st.markdown(st.session_state["event_categories"][3])
            with col1_cat3:
                num_qs = len(st.session_state['questions_cat3'])
                with st.expander(f"{num_qs} questions"):  
                    for question in st.session_state['questions_cat3']:
                        st.markdown(f'- {question}')
            with col2_cat3:
                if len(st.session_state['questions_cat3']) >= threshold_num_questions_cat:
                    if len(st.session_state["summarized_cat3"])==0:
                        if st.button('Summarize', key='Summarize_Cat3'):
                            print("summarized_cat3")
                            if st.session_state['use_model']:
                                st.session_state["summarized_cat3"] = summarize_questions_gpt(
                                    st.session_state['questions_cat3'],
                                    st.session_state['host_event_name'],
                                    st.session_state['host_event_presenter']
                                )
                            else:
                                st.session_state["summarized_cat3"] = [
                                    "How will Joe Biden's climate change policies address the feasibility of transitioning to a circular economy, updating university curriculums, and the impact of climate change on food prices? (covering 3 questions)",
                                    "What is Joe Biden's stance on governmental contributions to Tesla cars and their role in limiting climate change, and how does this fit into his overall climate change policies? (covering 2 questions)",
                                  ]
                            st.experimental_rerun() # update button print
                    else:
                        with st.expander("Summarized questions"):
                            for question in st.session_state["summarized_cat3"]:
                                st.markdown(f'- {question}')
                else:
                    st.markdown(f'Summarization will be avilable once there will be more than {threshold_num_questions_cat} questions.')
            st.divider()
            # give the opportunity to recategorize as new questions have been added
            col_re1, col_re2 = st.columns(2)
            with col_re1:
                if st.button('Recategorize questions'):
                    st.session_state["event_categories"]= []
                    for i in range(4):
                        st.session_state[f"summarized_cat{i}"] = []
                    st.experimental_rerun()
            with col_re2:
                if st.session_state['use_model']:
                    st.session_state["newly_added_questions"] = st.session_state['host_eventdb'].get_uncategorized_questions()
                    # st.experimental_rerun()
                else:
                    if not st.session_state["new_qs_categorized"]:
                        st.session_state["newly_added_questions"] = [
                            'Added Q1', 
                            'Added Q2', 
                            'Added Q3', 
                            'Added Q4'
                        ]
                if len(st.session_state["newly_added_questions"])>4:
                    if st.session_state['use_model']:
                        if st.button(f'Categorize the {len(st.session_state["newly_added_questions"])} newly added questions'):
                            questions_categories = categorize_questions(
                                st.session_state['newly_added_questions'],
                                st.session_state["list_categories_string"]
                            )
                            st.session_state['host_eventdb'].add_questions_category(
                                st.session_state['newly_added_questions'], 
                                questions_categories
                            )
                            st.session_state["newly_added_questions"] = []
                            for i in range(4):
                                st.session_state[f'questions_cat{i}'] = st.session_state['host_eventdb'].get_questions_by_category(i)
                            st.experimental_rerun()
                    else:
                        if st.button('Categorize newly added questions'):
                            for i in range(4):
                                st.session_state[f'questions_cat{i}'].append(st.session_state["newly_added_questions"][i])
                            st.session_state["newly_added_questions"] = []
                            st.session_state["new_qs_categorized"] = True
                            st.experimental_rerun()
                else:
                    if len(st.session_state["newly_added_questions"]) == 0:
                        st.markdown('There are no new questions to categorize.')
                    elif len(st.session_state["newly_added_questions"]) == 1:
                        st.markdown('1 new question has not been categorized yet.')
                    else:
                        st.markdown(f'{len(st.session_state["newly_added_questions"])} new questions have not been categorized yet.')
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
                                    st.session_state['host_event_database_name'],
                                    st.session_state['host_event_name'], 
                                    st.session_state['host_event_presenter']
                                )
                            else:
                                st.session_state['easy_questions'] = [
                                    '"What strategies are being implemented at the national level to transition towards renewable energy?" - This question is specific and straightforward, asking about a specific action being taken to address climate change.',
                                    '"How can governments better incentivize businesses to adopt greener practices and reduce their carbon footprint?" - This question is also specific and straightforward, asking about a specific action that can be taken to address climate change.'
                                ]
                                st.session_state['hard_questions'] = [
                                    '"Can fictional characters play a role in preventing global warming to increase in the next 40 years?" - This question challenges the presenter to think creatively and outside the box, as well as to provide evidence-based reasoning for their answer. It is also a bit whimsical and may require the presenter to balance humor with seriousness in their response.', 
                                    '"What are your thoughts on the feasibility of transitioning to a circular economy, and what policy changes will this require?" - This question is broad and requires the presenter to have a deep understanding of circular economies and policy changes required to transition towards it.'
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
                                    '"What strategies are being implemented at the national level to transition towards renewable energy?" - This question is specific and straightforward, asking about a specific action being taken to address climate change.',
                                    '"How can governments better incentivize businesses to adopt greener practices and reduce their carbon footprint?" - This question is also specific and straightforward, asking about a specific action that can be taken to address climate change.'
                                ]
                                st.session_state['hard_questions'] = [
                                    '"Can fictional characters play a role in preventing global warming to increase in the next 40 years?" - This question challenges the presenter to think creatively and outside the box, as well as to provide evidence-based reasoning for their answer. It is also a bit whimsical and may require the presenter to balance humor with seriousness in their response.', 
                                    '"What are your thoughts on the feasibility of transitioning to a circular economy, and what policy changes will this require?" - This question is broad and requires the presenter to have a deep understanding of circular economies and policy changes required to transition towards it.'
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