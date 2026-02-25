import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="gemma3:4b")
embeddings = OllamaEmbeddings(model="nomic-embed-text")


def process_documents(folder_path: str):
    """
    Belirtilen klasördeki TÜM PDF dosyalarını okur ve tek bir vektör veritabanında birleştirir.
    """
    print(f"'{folder_path}' klasöründeki dokümanlar taranıyor...")
    all_docs = []

    # İŞTE EKSİK OLAN SİHİRLİ DÖNGÜ BURASI:
    # Klasörün içine girip sadece PDF'leri tek tek buluyoruz
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            print(f"-> Okunuyor: {filename}")
            # PyPDFLoader'a artık klasörü değil, bulduğumuz o tekil dosyayı veriyoruz
            loader = PyPDFLoader(pdf_path)
            all_docs.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(all_docs)

    vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
    return vectorstore


def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def answer_question(vectorstore, question: str) -> str:
    retriever = vectorstore.as_retriever()

    system_prompt = (
        "Sen bilgili ve yardımsever bir asistansın. "
        "Kullanıcının sorusunu cevaplamak için yalnızca aşağıda sağlanan bağlam (context) metnini kullan. "
        "Cevabı bağlam metninde bulamıyorsan, sadece 'Bu bilgiyi sağlanan belgede bulamadım' de. Kendi kendine bilgi uydurma.\n\n"
        "Bağlam:\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    rag_chain = (
            {"context": retriever | format_docs, "input": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )

    return rag_chain.invoke(question)