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
