import os
import openai
import datetime
import getpass
import time
from termcolor import colored
from halo import Halo

# Set up OpenAI API key
try:
    with open("openai_api_key.txt", "r") as file:
        api_key = file.read().strip()
        openai.api_key = api_key
except:
    print(colored("Error: Could not read OpenAI API key from file.", "red"))
    print(colored("Please get an API key from https://platform.openai.com/account/api-keys, and enter it below.", "yellow"))
    api_key = getpass.getpass("OpenAI API key: ")
    openai.api_key = api_key
    with open("openai_api_key.txt", "w") as file:
        file.write(api_key)

# Set API model name
model_engine = "gpt-3.5-turbo"

# Create a logs directory if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

# Global array to store user messages and OpenAI responses
messages = []

# Function to send a message to the ChatGPT API
def send_message(message, assistant_name):
    if not messages:
        messages.append({"role": "system", "content": assistant_name})
    messages.append({"role": "user", "content": message})

    with Halo(text='ChatGPT: thinking', spinner='dots'):
        response = openai.ChatCompletion.create(
            model=model_engine,
            messages=messages
        )
    
    return response["choices"][0]["message"]["content"]

# Function to save chat history to a file
def save_history(history, filename):
    with open(filename, "a") as file:
        file.write(history + "\n")

# Main program loop
def main():
    # Get the current date and time in the format 02.03.2023_14_45
    current_time = datetime.datetime.now().strftime("%d.%m.%Y_%H_%M")

    # Ask the user how ChatGPT should introduce itself
    default_assistant_name = "a helpful assistant"
    assistant_name = input(colored("How should ChatGPT introduce itself? (press Enter to use default: 'a helpful assistant') ", "yellow")) or default_assistant_name

    # Create a file to save the chat history for this session
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    filename = f"{logs_dir}/{assistant_name.replace(' ', '_')}_{current_time}.txt"
    with open(filename, "w") as file:
        file.write(f"Start of session with ChatGPT acting as {assistant_name}\n")

    while True:
        message = input(colored("You: ", "cyan"))

        # Get the response from the ChatGPT API
        response = send_message(message, assistant_name)

        # Display the response and save the chat history
        output_message = colored(f"{assistant_name}: ", "green") + response
        print(output_message)

        # Save the chat history to a file
        history = f"You: {message}\n{assistant_name}: {response}\n"
        save_history(history, filename)

        # Update the message history
        messages.append({"role": "user", "content": message})
        messages.append({"role": "assistant", "content": response})

        # Wait a short time before sending the next message to avoid sending too many API requests
        time.sleep(1)

main()
