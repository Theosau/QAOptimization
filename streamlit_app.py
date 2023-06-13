import sqlite3
import streamlit as st

# Database setup
def create_table():
    conn = sqlite3.connect('questionsDB.sqlite')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS questions (question TEXT)')
    conn.close()

def add_question_to_db(question):
    conn = sqlite3.connect('questionsDB.sqlite')
    c = conn.cursor()
    c.execute('INSERT INTO questions (question) VALUES (?)', (question,))
    conn.commit()
    conn.close()

# Create the database table
create_table()

def main():
    st.set_page_config(layout="wide")  # Add this line
    st.title('Event Q&A Streamlining App')

    # Create the session state variables if they don't exist
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

    # Button press triggers clearing the input box
    clear_input = False
    if 'clear_input' in st.session_state:
        if st.session_state['clear_input']:
            clear_input = True
            st.session_state['clear_input'] = False
    
    # Text input and submit button for new question
    question_input = st.text_input('Please enter your question:', key='question_input')

    # Only append to the list and rerun if the button is clicked and there's a question to add
    if (st.button('Submit Question') or question_input) and question_input:
        st.session_state['question_list'].append(question_input)  # Add the question to the list
        add_question_to_db(question_input)  # Store the question in the database
        st.experimental_rerun()  # Rerun the app to update the list of displayed questions


    # Set up the layout with two columns
    col1, col2 = st.columns(2)

    # Display the questions received in the left column
    with col1:
        st.header('Questions Received')

        # Add a "Summarize Questions" button at the end of this column
        if st.button('Summarize Questions'):
            # Here I'm just selecting the first three questions as a dummy "summarizing" function
            # Replace this with your actual summarizing function
            # st.session_state['summarized_questions'] = st.session_state['question_list'][:3]
            st.session_state['summarized_questions'] = [
                "What are the potential impacts and ethical considerations of AI in various domains such as the job market, healthcare, transportation, education, privacy, security, and criminal justice? (covers 8 questions)", 
                "How will AI influence the economy, global geopolitics, and military applications? (covers 2 questions)"
            ]

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
        num_questions = len(st.session_state['question_list'])
        with st.expander(f"See questions (Total: {num_questions})"):  
            for question in st.session_state['question_list']:
                st.markdown(f'- {question}')

    # Display the summarized questions in the right column
    with col2:
        st.header('Summarized Questions')
        for question in st.session_state['summarized_questions']:
            st.markdown(f'- {question}')

    # Set up the layout with three columns
    col3, col4, col5 = st.columns(3)

    # Display the influential person questions in the first column
    with col3:
        st.header('Influential Person Questions')
        for question in st.session_state['influential_questions']:
            st.markdown(f'- {question}')

    # Display the easy questions in the second column
    with col4:
        st.header('Easy Questions')
        for question in st.session_state['easy_questions']:
            st.markdown(f'- {question}')

    # Display the difficult questions in the third column
    with col5:
        st.header('Difficult Questions')
        for question in st.session_state['difficult_questions']:
            st.markdown(f'- {question}')

if __name__ == "__main__":
    main()
