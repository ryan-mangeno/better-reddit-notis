import praw
import os
import requests
from dotenv import load_dotenv
import time
import pygame


# for send_mail function
from send_mail import send_email

# to analyze text from image on post
from image_analysis import process_post


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

# not necessary

# init pygame mixer
#pygame.mixer.init()
#notification_sound = pygame.mixer.Sound("notification.wav")


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
    subreddit = reddit.subreddit('') # to be chosen
    
    while True:
        query = '' # to be chosen

        # if you change limit you will need to change the sleep time, 1000 requests refreshed every 10 minutes
        for post in subreddit.new(limit=1):

            if post.link_flair_text == query:
                
                if post.id not in seen_posts:
                    seen_posts.add(post.id)
                    
        
                    image_urls = []
                    
                    #  gallery posts
                    if hasattr(post, 'is_gallery') and post.is_gallery:
                        if hasattr(post, 'media_metadata'):
                            for item_id in post.media_metadata:
                                image_data = post.media_metadata[item_id]
                                if image_data['e'] == 'Image':
                                    if 's' in image_data and 'u' in image_data['s']:
                                        image_url = image_data['s']['u']
                                        image_urls.append(image_url)
                    
                    #  single image posts
                    elif hasattr(post, 'preview') and 'images' in post.preview:
                        for image in post.preview['images']:
                            if 'source' in image:
                                image_urls.append(image['source']['url'])
                    
                    # fallback to the standard url
                    elif hasattr(post, 'url'):
                        url = post.url
                        if url.endswith(('.jpg', '.jpeg', '.png')):
                            image_urls.append(url)
                    
        
                    for image_url in image_urls:
                        # fixing the URL encoding (Reddit URLs are sometimes double-encoded)
                        image_url = image_url.replace('&amp;', '&')
                        
                        post_count += 1
                        save_path = os.path.join(os.getcwd(), f"downloaded_image_{post_count}.jpeg")
                        
                        try:
                            download_image(image_url, save_path)
                            email_body = process_post(save_path, None)
                            send_email('subject', 'body', save_path)
                        except Exception as e:
                            print(f"Error processing image {image_url}: {e}")
        
                    if not image_urls:
                        email_body = process_post(None, post.selftext)
                        send_email('subject', f'Code: {email_body}')
                
        time.sleep(1)

process_new_posts()




