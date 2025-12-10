
import chromadb

from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import GPT4All
from langchain_chroma import Chroma

CHROMA_DATA_PATH = "../Task3/chroma_data/"
COLLECTION_NAME = "star_wars"

client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

llm = GPT4All(model='mistral-7b-openorca.gguf2.Q4_0.gguf') 

#template0 = """
#Please use the following context to answer the question concisely
#and without including the context in your answer.
#Context: {context}
#Question: {question}
#Answer:
#"""

template1 = """
Ответь на вопрос коротко и по-русски. 

Пример: 
Q: Где родилась Zina Iunpwsd?
A: Zina Iunpwsd родилась на астеройде Polis Messa.
Q: Сколько систер у Johh Iunpwsd?
A: У Johh Iunpwsd одна сестра.

Используй следующий конекст чтобы ответить на вопрос.
Контекст: {context}
Вопрос: {question}
"""

template2 = """
Ответь на вопрос коротко и по-русски, распиши ход рассуждений по шагам.

Используй следующий контекст.
Контекст: {context}
Вопрос: {question}
"""

template3 = """
Ответь на вопрос коротко и по-русски. Если в контексте нет нужной информации, не придумывай, честно скажи "Нет данных".

Используй следующий конекст чтобы ответить на вопрос. 
Контекст: {context}
Вопрос: {question}
"""

def ask(question):
  matched_docs = collection.query(query_texts=[question], n_results=5)
  context = ""

  for doc in matched_docs["documents"][0]:
    context += doc + " \n\n"  

  prompt = PromptTemplate(template=template3, input_variables=["context", "question"]).partial(context=context)

  chain = prompt | llm | StrOutputParser()
  return chain.invoke({"question": question}) 

while True:
  q = input('Question: ')
  if q == 'quit':
    break
  print(ask(q))

