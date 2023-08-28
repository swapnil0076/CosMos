from django.shortcuts import render

import openai
import chromadb
import os
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator

os.environ["OPENAI_API_KEY"] = ""

loader = TextLoader("Data\info.txt")
index = VectorstoreIndexCreator().from_loaders([loader])
print(index.query("Tell me something about Harpreet’s family?"))
