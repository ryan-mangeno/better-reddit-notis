# Better Reddit Notifications

Script that gives more accurate and timely notifications for select subreddit ( and flair for now )


## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/anakin004/better_reddit_notifications.git
   cd better_reddit_notifications
   pip install -r requirements.txt

1. Get an API key from [Groq](https://groq.com/).
2. Get an API key from [Reddit](https://www.reddit.com/prefs/apps).
3. Download [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki). and add it to system path.
4. Replace subreddit and queries in main.py
5. Optional: if you decide to use groq image analysis for a more tailored notification, replace the prompts in image_analysis.py, its there to give more information about a post if it has a image

Once you have the keys, create a `.env` file in the project root
Any variable loaded from dotenv needs to be in the .env file

