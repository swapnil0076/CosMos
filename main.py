import streamlit as st
from signUp import sign_uo, fetch_users
import streamlit_authenticator as auth

# st.set_page_config(page_title='Sign In', page_icon='🛤', initial_sidebar_state='collapsed')

try:
    users = fetch_users()
    emails = []
    usernames = []
    passwords = []
    st.header("WELCOME PDF CHAT APP")
    print("done .... 1")

    for user in users:
        emails.append(user['key'])
        usernames.append(user['username'])
        passwords.append(user['password'])
    print("done .... 1")
    credentials = {'usernames': {}}

    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}
    print("done .... 1")
    # print(credentials)
    Authenticator = auth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=4)

    email, authentication_status, username = Authenticator.login(':green[Login]', 'main')
    info, info1 = st.columns(2)

    if not authentication_status:
        sign_uo()
    print("done .... 1")
    if username:
        if username in usernames:
            if authentication_status:
                st.subheader('This is Main Page')

                st.sidebar.subheader(f'Welcome :-{username}')

                Authenticator.logout('Log Out', 'sidebar')
                print('done auth')


            import streamlit as st
            from dotenv import load_dotenv
            from PyPDF2 import PdfReader
            import streamlit_authenticator as auth
            import datetime
            import  re
            from deta import  Deta
            from langchain.text_splitter import CharacterTextSplitter
            from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
            from langchain.vectorstores import FAISS
            from langchain.memory import ConversationBufferMemory
            from langchain.chains import ConversationalRetrievalChain
            from langchain.chat_models import ChatOpenAI
            from index import css, bot_template, user_template



            def get_pdf_text(pdf_docs):
                text = ""
                for pdf in pdf_docs:
                    pdf_reader = PdfReader(pdf)
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                return text


            def get_pdf_chunks(text):
                text_split = CharacterTextSplitter(
                    separator="\n",
                    chunk_size=800,
                    chunk_overlap=200,
                    length_function=len
                )
                chunks = text_split.split_text(text)
                return chunks


            def storing_chunks(make_chunks):
                embeddings = OpenAIEmbeddings()
                store = FAISS.from_texts(texts=make_chunks, embedding=embeddings)
                return store


            def get_conv(store):
                llm = ChatOpenAI()

                memory = ConversationBufferMemory(
                    memory_key='chat_history', return_messages=True)
                conversation_chain = ConversationalRetrievalChain.from_llm(
                    llm=llm,
                    retriever=store.as_retriever(),
                    memory=memory
                )
                return conversation_chain


            def handleQuestion(ques):
                response = st.session_state.conversation({'question': ques})
                st.session_state.chat_history = response['chat_history']

                for i, message in enumerate(st.session_state.chat_history):
                    if i % 2 == 0:
                        st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

                    else:
                        st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)


            def main():
                # st.set_page_config(page_title="AIONE", page_icon=":🛩:")
                st.write(css, unsafe_allow_html=True)
                if "conversation" not in st.session_state:
                    st.session_state.conversation = None

                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = None

                with st.container():
                    st.subheader("PDF FILES")
                    pdf_docs = st.file_uploader("Upload your docs", accept_multiple_files=True)
                    if st.button("Process"):
                        st.balloons()
                        with st.spinner(text='In progress'):
                            text = get_pdf_text(pdf_docs)

                            make_chunks = get_pdf_chunks(text)

                            store = storing_chunks(make_chunks)

                            st.session_state.conversation = get_conv(store)

                load_dotenv()

                st.header("AIONE " + ":🛩:")
                ques = st.text_input("Ask a question only about the documents")

                if ques:
                    handleQuestion(ques)


            if __name__ == '__main__':
                main()


            elif not authentication_status:
                with info:
                    st.error('Incorrect Password or username')
            else:
                with info:
                    st.warning('Please add the Proper credentials')
        else:
            with info:
                st.warning('Username does not exist,Please signUp')

except:
    st.success('Refresh Page')
