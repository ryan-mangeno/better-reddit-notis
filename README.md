# Better Reddit Notifications

Script that gives more accurate and timely notifications for select subreddit ( and flair for now )


## Installation
```bash
# clone repo
git clone https://github.com/anakin004/better_reddit_notifications.git

# change to the project directory
cd better_reddit_notifications

# create a virtual environment 
python3 -m venv venv

# activate the virtual environment (adjust for platform)
# For Linux/macOS
source venv/bin/activate
# For Windows
venv\Scripts\activate

# install reqs
pip install -r requirements.txt

# Run the script in the background
# For Linux/macOS
nohup python your_script_name.py &
# For Windows 
start python your_script_name.py
```

1. Get an API key from [Reddit](https://www.reddit.com/prefs/apps).
2. Download [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki). and add it to system path.
3. Replace subreddit and queries in main.py
4. Optional: if you decide to use groq image analysis for a more tailored notification, replace the prompts in image_analysis.py, its there to give more information about a post if it has a image
4. Cont.. Get an API key from [Groq](https://groq.com/).
5. 

Once you have the keys, create a `.env` file in the project root
Any variable loaded from dotenv needs to be in the .env file

