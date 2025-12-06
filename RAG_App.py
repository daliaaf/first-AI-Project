# pip install -U langchain langchain-community langchain-openai pypdf python-dotenv faiss-cpu openai

import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Load and read the PDF file
pdf_path = "Resume.pdf"  # ← Replace with your file name
reader = PdfReader(pdf_path)
raw_text = ""

for page in reader.pages:
    raw_text += page.extract_text() or ""

print(f"Loaded PDF text length: {len(raw_text)}")

# Split text into chunks
splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_text(raw_text)
print(f"Number of chunks created: {len(chunks)}")

if not chunks:
    raise ValueError("No content was extracted from the PDF. Please check the file.")

# Create or load FAISS vector index
embedding = OpenAIEmbeddings(openai_api_key=api_key)
index_path = "my_pdf_faiss_index"

if not os.path.exists(index_path):
    print("Creating FAISS index...")
    vectorstore = FAISS.from_texts(chunks, embedding)
    vectorstore.save_local(index_path)
else:
    print("Loading existing FAISS index...")
    vectorstore = FAISS.load_local(
            folder_path=index_path,
            embeddings=embedding,
            allow_dangerous_deserialization=True
    )

# Set up retrieval QA
llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key)
qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        chain_type="stuff"
)

# Start terminal chat
print("\n🤖 PDF chatbot ready! Ask questions about the document (type 'exit' to quit)\n")

while True:
    query = input("You: ").strip()
    if query.lower() in {"exit", "quit"}:
        print("👋 Goodbye!")
        break
    response = qa.invoke({"query": query})
    print("Bot:", response["result"])
