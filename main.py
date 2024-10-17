from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """
You are a fashion chatbot designed to assist users in identifying their style preferences. Give quick and brief responses.
Here is the conversation history: {context}

Question: {question}

Answer:
"""

model = OllamaLLM(model = "llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def handle_conversation():
    context = ""
    print("I'm Miranda, and you look like you need me. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input. lower() == "exit":
            break

        # formatted_prompt = prompt.format(context="", question="hey, how are you")
        result = chain. invoke({"context": context, "question": user_input})
        print("Bot: ", result)
        context += f"\nUser: {user_input}\nAI: {result}"

if __name__ == "__main__":
    handle_conversation()