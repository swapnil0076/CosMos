from django.shortcuts import render

import openai
import chromadb
import os
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator

os.environ["OPENAI_API_KEY"] = "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"

loader = TextLoader("Data\info.txt")
index = VectorstoreIndexCreator().from_loaders([loader])
print(index.query("Tell me something about Harpreet’s family?"))
