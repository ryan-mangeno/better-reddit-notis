import praw
import os
import requests
from dotenv import load_dotenv
import time
import base64
import io
import gradio as gr
from groq import Groq
from PIL import Image


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
user_agent = os.getenv("USER_AGENT")

groq_api_key =  os.getenv("GROQ_KEY")
groq_url = "https://groqapi.com/v1/ocr"  

client = Groq(
    api_key= groq_api_key,
)

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    username=username,
    password=password,
    user_agent=user_agent
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
    

def download_image(image_url, save_path):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Referer": "https://www.reddit.com/",
            "Origin": "https://www.reddit.com"
        }

        response = requests.get(image_url, headers=headers)
        
        if response.status_code == 200:
            
            if 'image' in response.headers['Content-Type']:
                os.makedirs(os.path.dirname(save_path), exist_ok=True)

                with open(save_path, 'wb') as f:
                    f.write(response.content)
                print(f"Image downloaded and saved as {save_path}")

            else:
                print(f"The URL does not link to an image: {image_url}")
       
        else:
            print(f"Failed to retrieve image. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")




def process_new_posts():

    post_count = 0
    seen_posts = set()
    subreddit = reddit.subreddit("Something") # replace this <----
  
    # you also dont need to search with a query, you can also just search the subreddit
  
    while True:
        remaining_requests = reddit.auth.limits['remaining']
        query = 'flair' # replace this <------
        for post in subreddit.search(query, sort="new", limit=1): 
            if post.id not in seen_posts:
                seen_posts.add(post.id) 
                print(f"\nTitle: {post.title}")
                print(f"Posted by: u/{post.author.name}")
                print(f"Posted on: {post.created_utc}")
                print(f"Score: {post.score}")
                print(f"URL: https://www.reddit.com{post.permalink}\n")

                save_path = os.path.join(os.getcwd(), "downloaded_image" + str(post_count) + ".jpeg")  
                post_count += 1


                if post.url.endswith(('.jpg', '.jpeg', '.png')): 
                    image_url = post.url
                    
                    download_image(image_url, save_path)

                    #analyze_image(save_path, "find promo codes on the image") # to work on
                    
                else:
                    print("No image found in this post.")
        
        if remaining_requests == 100 or remaining_requests == 10
            print(f"Remaining requests: {remaining_requests}")
        time.sleep(1)  # 1000 api calls available per 10 mins, i am doing 600 per 10 mins

process_new_posts()
