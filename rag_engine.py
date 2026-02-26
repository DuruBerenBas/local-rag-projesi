import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="llama3", temperature=0)
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

def answer_question(vectorstore, query):
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 6, "fetch_k": 20}
    )

    system_prompt = (
        "Sen şirketin resmi, son derece zeki ve TÜRKÇE DİL KURALLARINA ÜST DÜZEYDE HAKİM bir asistanısın.\n"
        "Kullanıcının sorusunu SADECE aşağıdaki bağlamı kullanarak yanıtla.\n"
        "YAZIM KURALLARI EMRİ:\n"
        "1. Yanıtlarını verirken Türkçedeki ses olaylarına (ünsüz yumuşaması, ses düşmesi vb.) harfiyen uy.\n"
        "2. Örn: 'Bebekiniz' değil 'Bebeğiniz', 'Kitapı' değil 'Kitabı' yazmalısın.\n"
        "3. Her zaman profesyonel, nazik ve kurumsal bir dil kullan.\n\n"
        "4.KESİNLİKLE İNGİLİZCE KELİME VEYA CÜMLE KULLANMA. Yanıtın tamamı %100 Türkçe olmalıdır.\n"
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

    return rag_chain.invoke(query)