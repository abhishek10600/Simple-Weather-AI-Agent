import os
from dotenv import load_dotenv
import openai
import json

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Tools


def get_weather_details(city):
    if (city.lower() == "kolkata"):
        return "25°C"
    if (city.lower() == "delhi"):
        return "30°C"
    if (city.lower() == "mumbai"):
        return "36°C"
    if (city.lower() == "bangalore"):
        return "29°C"
    if (city.lower() == "hyderabad"):
        return "32°C"


tools = {
    "get_weather_details": get_weather_details
}

SYSTEM_PROMPT = """
You are an AI Assistant with START, PLAN, ACTION, Observation and Output State.
Wait for the user prompt and first PLAN using available tools.
After Planning, take the action with appropriate tools and wait for observation based on action.
Once you get the observations, return the AI response based on START prompt and observations.

Strictly follow the JSON output format as in examples.

Available Tools:
- def get_weather_details(city->string)->string
get_weather_details is a function that accepts city name as a string and returns the weather details.

Example:
START
{'type': 'user', 'user': 'What is the sum of weather of Kolkata and Delhi ?'}
{'type': 'plan', 'plan': 'I will call the get_weather_details for Kolkata'}
{'type': 'action', 'function':'get_weather_details', 'input': 'Kolkata'}
{'type': 'observation', 'observation': '25°C'}
{'type': 'plan', 'plan': 'I will call the get_weather_details for Delhi'}
{'type': 'action', 'function': 'get_weather_details', 'input': 'Delhi'}
{'type': 'observation', 'observation': '30°C'}
{'type': 'output', 'output': 'The sum of weather of Kolkata and Delhi is 55°C'}
"""

messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

while (True):
    query = input(">>")
    formatted_query = {'type': 'user', 'user': query}
    messages.append({"role": "user", "content": f"{formatted_query}"})
    while (True):
        chat = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            response_format={"type": "json_object"}
        ).choices[0].message.content
        print("\n\n--------START AI --------")
        print(chat)
        print("--------END AI --------\n\n")
        messages.append({"role": "assistant", "content": chat})
        call = json.loads(chat)
        if (call["type"] == "output"):
            print(f'Bot: {call["output"]}')
            break
        elif (call["type"] == "action"):
            fn = tools[call["function"]]
            observation = fn(call["input"])
            obs = {"type": "observation", "observation": observation}
            messages.append({"role": "developer", "content": f"{obs}"})

            # # user_input = "Hey, what is the weather of Delhi ?"

            # # def chat():
            # #     response = openai.chat.completions.create(
            # #         model="gpt-4",
            # #         messages=[
            # #             {"role": "system", "content": SYSTEM_PROMPT},
            # #             {"role": "developer",
            # #                 "content": "{'type': 'plan', 'plan': 'I will call the get_weather_details for Delhi'}"},
            # #             {"role": "developer",
            # #                 "content": "{'type': 'action', 'function':'get_weather_details', 'input': 'Delhi'}"},
            # #             {"role": "developer",
            # #                 "content": "{'type': 'observation', 'observation': '30°C'}"},
            # #             {"role": "user", "content": user_input}
            # #         ]
            # #     ).choices[0].message.content.strip()
            # #     return response

            # # print(chat())

            # a = {"role": "user", "content": "hello"}
            # formatted_a = json.dumps(a)
            # print(a)
            # print(formatted_a)
            # print(f'"{formatted_a}"')
