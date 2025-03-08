import base64
import io
import gradio as gr
from groq import Groq
from PIL import Image
import os


# work in progress

groq_api_key =  os.getenv("GROQ_KEY")
groq_url = "https://groqapi.com/v1/ocr"  

client = Groq(
    api_key= groq_api_key,
)



def encode_image(image_path):
    """Encodes an image into base64 format after resizing"""
    max_size = 512  
    image = Image.open(image_path)
    image.thumbnail((max_size, max_size)) 
    
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def analyze_image(image_path, prompt, is_url=False):
    """Sends the image to Groq API for analysis, either from URL or local file"""

    if is_url:
        image_content = {"type": "image_url", "image_url": image_path}
    else:
        base64_image = encode_image(image_path)
        image_content = {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_image}"}  

    messages = [
        {"role": "user", "content": prompt}, 
        {"role": "user", "content": f"data:image/jpeg;base64,{base64_image}"}
    ]

    chat_completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",  
        messages=messages  
    )

    print(chat_completion)


def process_image(image, prompt):
    if image is not None:
        return analyze_image(image, prompt)
    
