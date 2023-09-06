from langchain import HuggingFaceHub, OpenAI
from langchain.text_splitter import CharacterTextSplitter
import os
import pinecone
import json
from PyPDF2 import PdfReader
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Pinecone
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENV = os.getenv('PINECONE_ENV')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
split_text = ""


def doc_preprocessing(text):
    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
    )
    print("test - 1", text)
    docs_split = text_splitter.create_documents([text])
    print(docs_split[0])
    return docs_split


def embedding_db(split_text):
    # we use the openAI embedding model
    # embeddings = HuggingFaceEmbeddings()
    embeddings = OpenAIEmbeddings()
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENV
    )

    doc_db = Pinecone.from_documents(
        split_text,
        embeddings,
        index_name='vector'
    )
    return doc_db


# llm = HuggingFaceHub(repo_id="OpenAssistant/oasst-sft-1-pythia-12b", model_kwargs={"temperature": 1.0, "max_length": 1156})
# llm = ChatOpenAI()
doc_db = embedding_db(split_text)


def get_similiar_docs(query, k=2, score=False):
    if score:
        similar_docs = doc_db.similarity_search_with_score(query, k=k)
    else:
        similar_docs = doc_db.similarity_search(query, k=k)
    return similar_docs


model_name = "gpt-3.5-turbo-16k"
llm = OpenAI(model_name=model_name)

chain = load_qa_chain(llm, chain_type="stuff")


def get_answer(query):
    similar_docs = get_similiar_docs(query)
    answer = chain.run(input_documents=similar_docs, question=query)
    return answer


def retrieval_answer(query):
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=doc_db.as_retriever(),
    )
    query = query
    result = qa.run(query)
    print(result)
    return result


def upload_pdf(request):
    global split_text
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        print(len(pdf_file))

        pdf_reader = PdfReader(pdf_file)
        text = ""

        for page in pdf_reader.pages:
            text += page.extract_text()

        split_text = doc_preprocessing(text)
        embedding_db(split_text)

        # print(text)

    return render(request, 'chat_with_pdfs.html')


def process_question(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        # bot_response = retrieval_answer('Do not give me answer other than text i am giving you ' + user_input)
        second = get_answer(user_input)
        response_text = f"User asked: {user_input}. Here is a sample response."

        print(response_text, second)
        return JsonResponse({'message': second})

    return JsonResponse({'error': 'Invalid request method'}, status=400)
