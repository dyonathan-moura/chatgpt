import openai
import json
import time

from dotenv import load_dotenv
import os

# Configurar o caminho para o arquivo .env

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()


# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv('API_KEY')


def chat_with_gpt(user_input, messages=[]):
    # Append the user's message to the existing conversation
    messages.append({"role": "user", "content": user_input})

    # Send the updated conversation to the ChatGPT modelola 
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=messages,
        temperature = 0.8
    )

    # Get the model's reply from the response
    reply = response['choices'][0]['message']['content']

    # Append the model's reply to the conversation
    messages.append({"role": "assistant", "content": reply})

    return reply, messages

# Load the conversation from a file
def load_conversation(filename):
    try:
        with open(filename, 'r') as file:
            conversation = json.load(file)
            return conversation
    except FileNotFoundError:
        return []

# Save the conversation to a file
def save_conversation(conversation, filename):
    try:
        with open(filename, 'w') as file:
            json.dump(conversation, file)
    except FileNotFoundError:
        with open(filename, 'x') as file:
            json.dump(conversation, file)


# Example usage
filename = 'conversation.json'
conversation = load_conversation(filename)

while True:
    user_input = input("User: ")
    if user_input.lower() == 'quit':
        break
    reply, conversation = chat_with_gpt(user_input, messages=conversation)
    print("\n ChatGPT:", reply)

    # Wait for 10 seconds before the next request
    time.sleep(3)

# Save the conversation to a file
save_conversation(conversation, filename)
