from typing import List
import os
from dotenv import load_dotenv
import PyPDF2
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import (
    ConversationalRetrievalChain,
)
#from langchain_community.llms import Ollama
from langchain.docstore.document import Document
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from langchain.memory import ChatMessageHistory, ConversationBufferMemory

from langchain.prompts import PromptTemplate

import chainlit as cl

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

import openai

embedding_model="nomic-embed-text"
chat_model_name="mistral"
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)


@cl.on_chat_start
async def on_chat_start():
    files = None

    # Wait for the user to upload a file
    while files is None:
        files = await cl.AskFileMessage(
            content="Please upload a pdf file to begin!",
            accept=["application/pdf"],
            max_size_mb=50,
            timeout=180,
        ).send()

    file = files[0]
    print(file)

    msg = cl.Message(content=f"Processing `{file.name}`...")
    await msg.send()

    # Read the PDF file
        
    #pdf_stream = BytesIO(content)
    pdf = PyPDF2.PdfReader(file.path)
    pdf_text = ""
    for page in pdf.pages:
        pdf_text += page.extract_text()
        

    # Split the text into chunks
    texts = text_splitter.split_text(pdf_text)

    # Create a metadata for each chunk
    metadatas = [{"source": f"{i}-pl"} for i in range(len(texts))]

    # Create a Chroma vector store
    embeddings = OllamaEmbeddings(model=embedding_model)
    #embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=openai_api_key)
    docsearch = await cl.make_async(Chroma.from_texts)(
        texts, embeddings, metadatas=metadatas
    )

    message_history = ChatMessageHistory()


    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        chat_memory=message_history,
        return_messages=True,
    )

    prompt_template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you dont know, don't try to make up an answer.
    
    {context}
    
    Question: {question}
    Answer in {language_choice}:
    """
    
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["language_choice"],
    )
    
    languageDefined = PROMPT.format(language_choice="French", context="{context}", question="{question}")
    
    chain_type_kwargs = {"prompt": PromptTemplate(template=languageDefined , input_variables=["context", "question"])}
    
    # Create a chain that uses the Chroma vector store
    chain = ConversationalRetrievalChain.from_llm(
        #ChatOpenAI(api_key=openai_api_key, model="gpt-4"),
        ChatOllama(model=chat_model_name),
        chain_type="stuff",
        combine_docs_chain_kwargs=chain_type_kwargs,
        retriever=docsearch.as_retriever(),
        memory=memory,
        return_source_documents=True,
    )

    # Let the user know that the system is ready
    msg.content = f"Processing `{file.name}` done. You can now ask questions!"
    await msg.update()

    cl.user_session.set("chain", chain)


@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("chain")  # type: ConversationalRetrievalChain
    cb = cl.AsyncLangchainCallbackHandler()

    res = await chain.ainvoke(message.content, callbacks=[cb])
    answer = res["answer"]
    source_documents = res["source_documents"]  # type: List[Document]

    text_elements = []  # type: List[cl.Text]

    if source_documents:
        for source_idx, source_doc in enumerate(source_documents):
            source_name = f"source_{source_idx}"
            # Create the text element referenced in the message
            text_elements.append(
                cl.Text(content=source_doc.page_content, name=source_name)
            )
        source_names = [text_el.name for text_el in text_elements]

        if source_names:
            answer += f"\nSources: {', '.join(source_names)}"
        else:
            answer += "\nNo sources found"

    await cl.Message(content=answer, elements=text_elements).send()
