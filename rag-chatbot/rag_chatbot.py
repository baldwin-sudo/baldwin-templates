from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from langchain_openai import ChatOpenAI  # Ensure this is the correct import
from langchain_core.prompts import PromptTemplate
import numpy as np

# Elasticsearch Retriever with BERT Embeddings
class ElasticsearchRetrieverWithEmbeddings:
    def __init__(self, es_instance, index_name, model_name='bert-large-nli-stsb-mean-tokens'):
        self.es_instance = es_instance
        self.index_name = index_name
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts):
        return self.model.encode(texts)

    def search(self, query, top_k=10):
        query_embedding = self.embed_texts([query])[0]
        response = self.es_instance.search(
            index=self.index_name,
            body={
                "size": top_k,
                "_source": ["document_id", "document_text"],  # Update _source fields as needed
                "query": {
                    "script_score": {
                        "query": {"match_all": {}},
                        "script": {
                            "source": "cosineSimilarity(params.query_vector, 'document_embedding') + 1.0",
                            "params": {"query_vector": query_embedding.tolist()}
                        }
                    }
                }
            }
        )
        hits = response['hits']['hits']
        return [hit['_source']['document_text'] for hit in hits]

# Initialize Elasticsearch
def init_es():
    return Elasticsearch("http://localhost:9200")

# LangChain Chatbot with Message History
class ConversationalChatbot:
    def __init__(self, retriever, llm, prompt_template):
        self.retriever = retriever
        self.llm = llm
        self.prompt_template = prompt_template
        self.message_history = []

    def update_message_history(self, user_message, assistant_message):
        self.message_history.append({"user": user_message, "assistant": assistant_message})

    def create_prompt(self, question, relevant_docs):
        conversation = "\n".join([f"User: {msg['user']}\nAssistant: {msg['assistant']}" for msg in self.message_history])
        docs_text = "\n".join([f"Document: {doc}" for doc in relevant_docs])
        return self.prompt_template.format(conversation=conversation, question=question, documents=docs_text)

    def ask(self, question):
        # Retrieve relevant documents
        relevant_docs = self.retriever.search(question)
        # Create prompt with message history and retrieved documents
        prompt = self.create_prompt(question, relevant_docs)
        # Get the response from the LLM
        response = self.llm.invoke(prompt)        # Update message history
        self.update_message_history(question, response)
        return response

# Initialize components
def setup_chatbot(index_name,es):
    retriever = ElasticsearchRetrieverWithEmbeddings(es, index_name)
    prompt_template = PromptTemplate(
        template="You are a helpful assistant. Based on the following conversation {conversation} "
                "and documents:\n{documents}\n\nAnswer the question from the documents and avoid broad answers: {question}.",
        input_variables=["conversation", "question", "documents"]
    )
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", max_tokens=150, temperature=0.7)
    
    chatbot = ConversationalChatbot(retriever, llm, prompt_template)
    return  chatbot
def test():
    es = init_es()
    index_name = "test"  # Replace with your index name
    retriever = ElasticsearchRetrieverWithEmbeddings(es, index_name)
    
    prompt_template = PromptTemplate(
        template="You are a helpful assistant. Based on the following conversation and documents:\n{documents}\n\nAnswer the question from the documents and avoid broad answers: {question}.",
        input_variables=["conversation", "question", "documents"]
    )
    
    # Use GPT-3.5 with the latest ChatOpenAI class
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", max_tokens=150, temperature=0.7)
    
    chatbot = ConversationalChatbot(retriever, llm, prompt_template)
    
    print("Chatbot is running. Type your questions below (Press Ctrl+C to stop):")
    
    while True:
        try:
            question = input("You: ")
            if question.lower() in ['exit', 'quit', 'stop']:
                print("Exiting chatbot. Have a great day!")
                break
            response = chatbot.ask(question)
            print(f"Assistant: {response.content}")
        except KeyboardInterrupt:
            print("\nExiting chatbot. Have a great day!")
            break

if __name__ == "__main__":
    test()
