import os

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()  # lê a chave do arquivo .env

app = FastAPI(title="Tradutor EN -> FR com LangChain")

# Interface compatível com OpenAI (ChatOpenAI), usando o provedor Groq
llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    temperature=0,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Traduza o texto do inglês para o francês. Responda apenas com a tradução."),
    ("human", "{texto}"),
])

cadeia = prompt | llm


class Entrada(BaseModel):
    texto: str


@app.post("/traduzir")
def traduzir(entrada: Entrada):
    resposta = cadeia.invoke({"texto": entrada.texto})
    return {"original": entrada.texto, "traducao": resposta.content}