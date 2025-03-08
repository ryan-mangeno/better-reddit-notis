import praw
import os
import requests
from dotenv import load_dotenv
import time
import pygame

# for send_mail function
from send_mail import send_email


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
username = os.getenv("REDDIT_USERNAME")
password = os.getenv("REDDIT_PASSWORD")
user_agent = os.getenv("USER_AGENT")


# Initialize Reddit API
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    username=username,
    password=password,
    user_agent=user_agent
)


# playing notification sound is optional

# init pygame mixer
pygame.mixer.init()
notification_sound = pygame.mixer.Sound("notification.wav")


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
    subreddit = reddit.subreddit("") # add a subreddit 

    while True:
        remaining_requests = reddit.auth.limits['remaining']
        query = '' # change this
        for post in subreddit.search(query, sort="new", limit=1): 
            if post.id not in seen_posts:

                notification_sound.play()

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
                    send_email('','', save_path)

                    #analyze_image(save_path, "find promo codes on the image") # to work on
                    
                else:
                    # you can put whatever you want here
                    send_email('', '')
        
        time.sleep(1)  

process_new_posts()


