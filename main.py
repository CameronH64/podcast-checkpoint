import pprint
import yt_dlp
import os
import yaml
from yaml.loader import SafeLoader
from dotenv import load_dotenv
from googleapiclient.discovery import build


def download_m4a(URLS):

    options = {
        'format': 'm4a/bestaudio/best',
        # See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        error_code = ydl.download(URLS)


def get_complete_podcast_information(api_key, podcast_channels):

    download_urls = []
    total_responses = []
    needed_information = []
    # Build YouTube service object.
    youtube_service = build('youtube', 'v3', developerKey=api_key)

    # Use yaml file as a list of channels; use for loops.
    # Using YouTube service object, create a request.

    for upload_id in podcast_channels:   # I want this to repeat for each YouTube channel.

        # 'videoPublishedAt': '2022-06-04T00:30:11Z'

        # Return results from upload playlist (it's its own playlist)
        request = youtube_service.playlistItems().list(
            part="contentDetails, snippet",     # contentDetails has videoId and videoPublishedAt. Snippet has some video information.
            maxResults=2,
            playlistId=upload_id
        )

        # Execute API call for each channel.
        response = request.execute()        # Response is a dictionary.
        total_responses.append(response)

    # Note: total_responses is a list.
    return total_responses      # total_responses is a list.


def extract_podcast_urls(total_responses):

    podcast_urls = []

    print(total_responses)

    return podcast_urls


def main():
    """The main driver function"""

    load_dotenv()
    api_key = os.getenv("API_KEY")

    # Load the list of podcasts.
    with open("podcasts.yaml") as f:
        podcast_channels = yaml.load(f, Loader=SafeLoader)

    # Find the urls to download, latest 10 videos from each channel.
    total_responses = get_complete_podcast_information(api_key, podcast_channels)
    podcast_urls = extract_podcast_urls(total_responses)

    print(podcast_urls)


if __name__ == "__main__":
    main()
