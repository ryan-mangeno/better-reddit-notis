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

# Go through steps 1-6 below

# Run the script in the background
# For Linux/macOS
nohup python src/main.py &
# For Windows 
start python src/main.py
```
1. Create a .env for environment variables for reddit api, chosen email service, groq, etc. These will be found at the top of each source file.
2. Get an API key from [Reddit](https://www.reddit.com/prefs/apps).
3. Download [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki). and add it to system path.
4. Replace subreddit and queries in main.py
5. Optional: if you decide to use groq image analysis for a more tailored notification, replace the prompts in image_analysis.py, its there to give more information about a post if it has a image. Get an API key from [Groq](https://groq.com/) if you decide to do this.
6. If you don't decide to use groq, you still need to make .env variabels for them, you can use dummy values.

Note -> The reddit and groq api is subject to change, keep in mind potential rate limiting changes and depreciated models used with groq. Refer to [these current models](https://console.groq.com/docs/models)

