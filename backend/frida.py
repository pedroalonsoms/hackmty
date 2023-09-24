import os
import ast
from softtek_llm.chatbot import Chatbot
from softtek_llm.models import OpenAI
from dotenv import load_dotenv
from pdf_reader import get_pdf_text

def get_info_user(text):
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if OPENAI_API_KEY is None:
        raise ValueError("OPENAI_API_KEY not found in .env file")

    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
    if OPENAI_API_BASE is None:
        raise ValueError("OPENAI_API_BASE not found in .env file")

    OPENAI_CHAT_MODEL_NAME = os.getenv("OPENAI_CHAT_MODEL_NAME")

    if OPENAI_CHAT_MODEL_NAME is None:
        raise ValueError("OPENAI_CHAT_MODEL_NAME not found in .env file")

    model = OpenAI(
        api_key=OPENAI_API_KEY,
        model_name=OPENAI_CHAT_MODEL_NAME,
        api_type="azure",
        api_base=OPENAI_API_BASE,
        verbose=True,
    )
    chatbot = Chatbot(
        model=model,
        description="You are a very helpful and polite chatbot",
        verbose=True,
    )


    ## PROMPT
    response = chatbot.chat(
        "The following text represents a resume of an applicant, just return a read confirmation text. This is the resume: " + text
    )
    confirmation = response.message.content


    response = chatbot.chat(
        "Return a python style list of personal information of the applicant, strictly and only with the format and not including label: [Full name, residence, telephone, email, other contact links...]. Do not return a message, strictly only return the array"
    )
    personal_info = response.message.content

    response = chatbot.chat(
        "Return a python style list with all the soft skills, and without any technical skill found in the text given, strictly and only with the format: [skill 1, skill 2, skill 3, ...]. Do not return a message, strictly only return the array"
    )
    soft_skills = response.message.content

    response = chatbot.chat(
        "Return a python style list with all the technical skills found in the text given, strictly and only with the format: [skill 1, skill 2, skill 3, ...]. Do not return a message, strictly only return the array"
    )
    technical_skills = response.message.content

    response = chatbot.chat(
        "Return the time periods, including month and year, when the main projects where done. If not specified return an empty python array. Do not return a message, strictly only return the array"
    )
    periods = response.message.content

    response = chatbot.chat(
        "Calculate and return just number the months passed in every time period in the next list: " +  periods + ". Do not return a message, strictly only return the array"
    )
    number_time_periods = response.message.content


    print("\n\n============================= AI RESPONSE =============================\n\n")
    print(confirmation  + "\n\n" + personal_info + "\n\n" + soft_skills + "\n\n" + technical_skills + "\n\n" + number_time_periods)
    # print(type(response))

    print("\n\n============================= Parsed DATA =============================\n\n")

    # Convert the string to a Python list
    personal_info_arr = ast.literal_eval(personal_info)
    soft_skills_arr = ast.literal_eval(soft_skills)
    technical_skills_arr = ast.literal_eval(technical_skills)
    number_time_periods_arr = ast.literal_eval(number_time_periods)
    print(personal_info_arr) 
    print(soft_skills_arr) 
    print(technical_skills_arr) 
    print(number_time_periods_arr)

    return_arr = [personal_info_arr, soft_skills_arr, technical_skills_arr, number_time_periods_arr]

    return return_arr

    



    