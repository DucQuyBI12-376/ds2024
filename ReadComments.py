import googleapiclient.discovery
import re

API_KEY = "AIzaSyA6nZQtC2a8Kr5Uc74iRBbPhtebvpVbYBY"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
VIDEO_ID = "767xPIjTm2A"

# Initialize the YouTube API client
youtube = googleapiclient.discovery.build(
    API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

# Function to fetch and save comments
def save_comments_to_txt(video_id):
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=50,
        textFormat="plainText"
    )
    response = request.execute()

    # Regular expression to remove emojis and icons
    emoji_pattern = re.compile("["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                u"\U00002500-\U00002BEF"  # chinese char
                                u"\U00002702-\U000027B0"
                                u"\U00002702-\U000027B0"
                                u"\U000024C2-\U0001F251"
                                u"\U0001f926-\U0001f937"
                                u"\U00010000-\U0010ffff"
                                u"\u2640-\u2642"
                                u"\u2600-\u2B55"
                                u"\u200d"
                                u"\u23cf"
                                u"\u23e9"
                                u"\u231a"
                                u"\ufe0f"  # dingbats
                                u"\u3030"
                                "]+", flags=re.UNICODE)
    
    # Open a text file to write comments
    with open(f'comments.txt', 'w', encoding='utf-8') as file:
        count = 0
        maxResult = 50
        for item in response.get("items", []):
            if count >= maxResult:
                break
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comment = comment.lower()
            comment = re.sub(emoji_pattern, '',comment)
            comment = "\n".join([line for line in comment.splitlines() if line.strip()])
            file.write(comment)  # Write each comment on a new line
            count += 1
            if count < maxResult:
                file.write('\n')
            

        # Check if there are more comments to fetch
        while 'nextPageToken' in response:
            if count >= maxResult:
                break
            request = youtube.commentThreads().list_next(
                request, response)
            response = request.execute()
            for item in response.get("items", []):
                if count >= maxResult:
                    break
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comment = comment.lower()
                comment = re.sub(emoji_pattern, '',comment)
                comment = "\n".join([line for line in comment.splitlines() if line.strip()])
                file.write(comment)  # Continue writing each comment on a new line
                count += 1
                if count < maxResult:
                    file.write('\n')

# Call function to save comments
save_comments_to_txt(VIDEO_ID)