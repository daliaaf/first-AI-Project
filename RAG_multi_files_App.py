# pip install -U langchain langchain-community langchain-openai pypdf python-dotenv faiss-cpu openai

import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# Load environment variable
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# === 🔍 SETTINGS ===
pdf_folder = "pdfs"  # folder with your PDF files
index_path = "multi_pdf_faiss_index"
chunk_size = 300
chunk_overlap = 50

# === 📖 LOAD ALL PDFs ===
def load_all_pdfs(folder_path):
    full_text = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            print(f"🔍 Reading {filename}...")
            try:
                reader = PdfReader(pdf_path)
                for page in reader.pages:
                    full_text += page.extract_text() or ""
            except Exception as e:
                print(f"⚠️ Failed to read {filename}: {e}")
    return full_text

raw_text = load_all_pdfs(pdf_folder)
print(f"📄 Total text length from PDFs: {len(raw_text)}")

# === ✂️ SPLIT INTO CHUNKS ===
splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
chunks = splitter.split_text(raw_text)
print(f"🔹 Number of chunks created: {len(chunks)}")
if not chunks:
    raise ValueError("No content was extracted from the PDFs.")

# === 💾 SAVE OR LOAD VECTOR INDEX ===
embedding = OpenAIEmbeddings(openai_api_key=api_key)

if not os.path.exists(index_path):
    print("🧠 Creating FAISS index...")
    vectorstore = FAISS.from_texts(chunks, embedding)
    vectorstore.save_local(index_path)
else:
    print("📦 Loading existing FAISS index...")
    vectorstore = FAISS.load_local(
            folder_path=index_path,
            embeddings=embedding,
            allow_dangerous_deserialization=True
    )

# === 🤖 SET UP CHATBOT ===
llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key)
qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        chain_type="stuff"
)

# === 💬 START TERMINAL CHAT ===
print("\n🤖 Multi-PDF chatbot ready! Ask questions about the documents (type 'exit' to quit)\n")

while True:
    query = input("You: ").strip()
    if query.lower() in {"exit", "quit"}:
        print("👋 Goodbye!")
        break
    response = qa.invoke({"query": query})
    print("Bot:", response["result"])
