from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import BSHTMLLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain.chains import create_retrieval_chain

loader = DirectoryLoader("./nidc-pages", glob="**/*.html", loader_cls=BSHTMLLoader)
docs = loader.load()

embeddings = OllamaEmbeddings(model="mxbai-embed-large:latest")

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)

llm = Ollama(model="gemma2:27b")

prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)

document_chain.invoke({
    "input": "Who makes up the NIDC team?",
    "context": [Document(page_content="")]
})

retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

response = retrieval_chain.invoke({"input": "Who makes up the NIDC team?"})
print(response["answer"])
