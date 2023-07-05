import datetime
import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.organization = os.getenv("OPEN_AI_ORG_ID")
openai.api_key = os.getenv("OPENAI_API_KEY")

models = openai.Model.list()['data']

ids = []
for model in models:
    ids.append(model.id)

# sort ids
ids.sort()

models_file = open('models', 'w')
for id in ids:
    models_file.write(id + '\n')
models_file.close()

# your selected model
MODEL = "gpt-3.5-turbo-0301"
response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello"}
    ],
    temperature=0,
)

content = response['choices'][0]['message']['content']

# create a loop that keep asking user to input a message, then use the message to call openai.ChatCompletion.create() to get the response, then print the response
# if the user input "quit", then break the loop


def write_to_file(file_name, list):
    file = open(file_name, 'a')
    for item in list:
        file.write(item + '\n')
    file.close()


all_questions_and_answers = []

while True:
    list_of_questions_and_answers = []
    print("..." + "\n")
    user_input = input("You: ")
    list_of_questions_and_answers.append({
        "type": "question",
        "content": user_input,
        "timestamp": datetime.datetime.now()
    })
    if user_input == "quit":
        break

    # keep your chat history in memory so  that the bot understands the context
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for item in all_questions_and_answers:
        if item['type'] == "question":
            messages.append({"role": "system", "content": item['content']})
        elif item['type'] == "answer":
            messages.append({"role": "user", "content": item['content']})
    
    messages.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        temperature=0,
    )
    content = response['choices'][0]['message']['content']
    list_of_questions_and_answers.append({
        "type": "answer",
        "content": content,
        "timestamp": datetime.datetime.now()
    })
    print("..." + "\n")
    print("Bot: " + content)

    current_questions_and_answers = []
    for item in list_of_questions_and_answers:
        user_name = ""
        if item['type'] == "question":
            user_name = "You"
        else:
            user_name = f"Bot ({MODEL})"
        current_questions_and_answers.append(f"{item['timestamp']} - {user_name}: {item['content']}")
    
    # log your chat history to file
    write_to_file("chat_history", current_questions_and_answers)

    for item in list_of_questions_and_answers:
        all_questions_and_answers.append(item)
    
    # go back to the top of the loop

