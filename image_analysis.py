import base64
import io
import gradio as gr
from groq import Groq
from PIL import Image
import pytesseract
import os


groq_api_key =  os.getenv("GROQ_KEY")
groq_url = "https://groqapi.com/v1/ocr"  

client = Groq(
    api_key= groq_api_key,
)


def analyze_image_text(image_path):
    """analyzes image text from tesseract"""

    
    prompt = "" # enter your prompt here


    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)


    messages = [
        {"role": "user", "content": prompt + " " + text}, 
    ]

    chat_completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",  
        messages=messages  
    )

    return chat_completion.choices[0].message.content



def analyze_post_text(text):

    prompt = "" # enter your prompt here

    messages = [
        {"role": "user", "content": prompt + " " + text}, 
    ]


    chat_completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",  
        messages=messages  
    )

    return chat_completion.choices[0].message.content



def process_post(image, text):
    if image:
        return analyze_image_text(image)
    if text:
        return analyze_post_text(text)
    
    
    
