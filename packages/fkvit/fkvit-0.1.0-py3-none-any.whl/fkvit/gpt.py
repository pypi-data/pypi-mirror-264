import json
import google.generativeai as genai
from fkvit.utils import JSON_FILE, INSTRUCTIONS

# from openai import OpenAI

# def gpt_answers(question_string):
#     client = OpenAI()
#     try:
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": INSTRUCTIONS},
#                 {"role": "user", "content": f"{question_string}"},
#             ]
#         )
        
#         return response.choices[0].message.content

#     except Exception as e:
#         return f"An unexpected error occurred: {e}"


with open(JSON_FILE, "r") as file:
    data = json.load(file)
    GOOGLE_API_KEY = data.get("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

def gemini_answers(question_string):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(question_string)
        return response.candidates[0].content.parts[0].text
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == "__main__":
    question_string = """
    {}

    What is the capital of India?\nA) Mumbai\nB) New Delhi\nC) Kolkata\nD) Chennai
    Who is the Prime Minister of India?\nA) Narendra Modi\nB) Rahul Gandhi\nC) Arvind Kejriwal\nD) Mamata Banerjee
    What is the currency of India?\nA) Dollar\nB) Rupee\nC) Euro\nD) Yen
    Where is the Taj Mahal located?\nA) Agra\nB) Delhi\nC) Jaipur\nD) Mumbai
    
    """.format(INSTRUCTIONS)
    
    print(gemini_answers(question_string))