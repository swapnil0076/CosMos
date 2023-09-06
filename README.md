# Project AIONE - Chat with PDF App

Project AIONE is a web application that allows users to upload PDF documents, extract text from them, and then have conversations with a chatbot using the extracted content. This project is not hosted on Colab and is developed using the following technologies:

- Python
- Django
- OpenAI
- Pinecone
- HTML
- CSS
- JavaScript

## Project Overview

The goal of this project is to provide users with an interactive and conversational experience with PDF documents. Users can upload PDF files, which are then processed to extract text. This extracted text is used as a knowledge base for a chatbot powered by OpenAI. Users can input questions or queries, and the chatbot responds with relevant information from the PDF content.

## Tech Stack

### Backend
- **Python**: The primary programming language for building the backend logic.
- **Django**: A high-level Python web framework used for server-side development.
- **OpenAI**: Integration with OpenAI's powerful language models for chatbot functionality.
- **Pinecone**: Utilized for managing and searching the vector embeddings of text data.

### Frontend
- **HTML/CSS/JavaScript**: Frontend technologies for creating the user interface and interactivity.

## Installation and Setup

1. Clone the repository to your local machine:

   ```bash
   git clone <repository-url>
   cd project-aione
Install the required Python packages:

bash
Copy code
pip install -r requirements.txt
Set up your environment variables, including API keys for OpenAI and Pinecone.

Run the Django development server:

bash
Copy code
python manage.py runserver
Access the application in your web browser at http://localhost:8000.

Usage
Upload a PDF document using the "Upload PDF" feature.

Wait for the document to be processed.

Once processed, you can enter questions or queries in the input field and submit them.

The chatbot will respond with relevant information extracted from the PDF.

Project Timeline
The project is expected to be completed within 5 days.

Contributors
Swapnil Dhiman
