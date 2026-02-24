"""
Yerel (Local) RAG (Retrieval-Augmented Generation) Motoru
Bu modül PDF belgelerini işler, vektör veritabanına kaydeder ve Ollama LLM
kullanarak bağlam destekli soru-cevap işlemleri gerçekleştirir.
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Yapay Zeka Modeli ve Vektör Gömme (Embedding) Ayarları
llm = ChatOllama(model="gemma3:4b")
embeddings = OllamaEmbeddings(model="nomic-embed-text")

def process_pdf(pdf_path: str):
    """
    Belirtilen PDF dosyasını okur, metin parçalarına böler ve bir vektör veritabanı oluşturur.

    Args:
        pdf_path (str): İşlenecek PDF dosyasının dosya yolu.

    Returns:
        FAISS: Oluşturulan vektör veritabanı nesnesi.
    """
    print(f"{pdf_path} dosyası yükleniyor ve işleniyor...")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
    return vectorstore

def format_docs(docs) -> str:
    """
    Bulunan doküman parçalarını tek bir metin formatında birleştirir.
    """
    return "\n\n".join(doc.page_content for doc in docs)

def answer_question(vectorstore, question: str) -> str:
    """
    Kullanıcıdan gelen soruyu, vektör veritabanındaki bağlamı kullanarak cevaplar.

    Args:
        vectorstore (FAISS): Bağlamın çekileceği vektör veritabanı.
        question (str): Kullanıcının sorduğu soru.

    Returns:
        str: LLM tarafından üretilen cevap.
    """
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