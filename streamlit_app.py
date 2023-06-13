import streamlit as st

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

    # Button press triggers clearing the input box
    clear_input = False
    if 'clear_input' in st.session_state:
        if st.session_state['clear_input']:
            clear_input = True
            st.session_state['clear_input'] = False

    user_question = st.text_input('Please enter your question:', value='' if clear_input else '', key='question_input')
    if st.button('Submit'):
        if user_question:
            # Add the question to the list
            st.session_state['question_list'].append(user_question)
            st.session_state['clear_input'] = True
            # st.success('Question submitted successfully')
        else:
            st.session_state['question_list'] = [
                "How will advancements in artificial intelligence impact the job market in the next decade?",
                "What ethical considerations should be taken into account when developing and deploying AI technologies in various industries?",
                "Will AI eventually surpass human intelligence, and if so, what are the potential implications?",
                "How will AI contribute to advancements in healthcare and medical research in the coming years?",
                "What steps should be taken to ensure the responsible and accountable use of AI in autonomous vehicles?",
                "How might AI impact privacy and data security concerns in the future?",
                "What are the potential risks and challenges associated with the widespread adoption of AI in military applications?",
                "How will AI shape the future of education and learning methodologies?",
                "What are the possibilities and risks of AI in the field of criminal justice and law enforcement?",
                "How will AI impact the economy and global geopolitics in the next decade?",
            ]
            # st.warning('You did not enter a question.')

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
