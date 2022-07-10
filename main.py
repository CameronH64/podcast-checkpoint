import pprint
import yt_dlp
import os
import yaml
from yaml.loader import SafeLoader
from dotenv import load_dotenv
from googleapiclient.discovery import build
import time


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

# The reason we have to gather all the video_ids first instead of doing this all in one fell swoop is
# because the playlistItems() function can't return all the pertinent details needed to specify which podcasts
# to download. BUT, it CAN return results for each YouTube channel's upload playlist.
# Then, the youtube.videos() function can take the video ids returned by playlistItems() and derive the
# important details from that. Convoluted? Yes. Works? Also yes. I will look into simplifying this in the future,
# but as of now, this will do.

def get_podcast_ids(api_key, podcast_channels):

    cumulative = []
    video_ids = []

    # Build YouTube service object.
    youtube_service = build('youtube', 'v3', developerKey=api_key)

    # The following code has two for loops:
    # 1. Get ALL of the information
    # 2. Extract the video_ids.

    # For each listed upload playlist (per channel) in the .yaml file.
    # 1. Get ALL of the information
    for upload_playlist_id in podcast_channels:

        # Return results from upload playlist (it's its own playlist)
        request = youtube_service.playlistItems().list(
            part="contentDetails",              # contentDetails has video id, which is what we're interested in.
            maxResults=2,                       # The max value allowed is 50.
            playlistId=upload_playlist_id       # For each channel's upload playlist.
        )

        # Execute API call for each channel.
        response = request.execute()        # response is a dictionary
        cumulative.append(response)


    # 2. Extract the video_ids.

    for x in range(0, len(cumulative)):
        video_ids.append(cumulative[x]['items'][x]['contentDetails']['videoId'])


    # print("Working: ")
    # print()
    #
    # # KEY CODE
    # pprint.pprint(cumulative[0]['items'][0]['contentDetails']['videoId'])
    #
    # print()


    # DEBUGGING
    print("Cumulative: ")
    print()
    pprint.pprint(cumulative)
    print()

    print()
    print("video_ids: ")
    print()
    pprint.pprint(video_ids)

    return video_ids


def derive_podcast_urls(total_responses):

    podcast_urls = []


    print()

    # print("Single responses: ")
    # pprint.pprint(total_responses[0]['items'][0]['contentDetails'])
    # pprint.pprint(total_responses[0]['items'][0]['contentDetails']['videoId'])
    # pprint.pprint(total_responses[0]['items'][0]['contentDetails']['videoPublishedAt'])

    # print()

    # Needed to create downloadable video links.
    # www.youtube.com/watch?v=

    return podcast_urls


def main():
    """The main driver function"""

    load_dotenv()
    api_key = os.getenv("API_KEY")

    # Load the list of podcasts.
    with open("podcasts.yaml") as f:
        podcast_channels = yaml.load(f, Loader=SafeLoader)

    # Find the urls to download, latest 10 videos from each channel.
    total_responses = get_podcast_ids(api_key, podcast_channels)
    podcast_urls = derive_podcast_urls(total_responses)


if __name__ == "__main__":
    main()






################ LATER
# request = youtube.videos().list(
#     part="snippet,contentDetails,statistics",
#     id="3E6V9TrVkLY"
# )
# response = request.execute()
#
# print(response)

################ LATER



################ TESTING

# # Extract videoId and videoPublishedAt
# video_urls.append(response['items'][0]['contentDetails']['videoId'])
# video_published_ats.append(response['items'][0]['contentDetails']['videoPublishedAt'])
#
# print("Video ids: \t\t\t\t", video_urls)
# print("Video publish dates: \t", video_published_ats)
#
# test_list = [video_urls, video_published_ats]
# print(test_list[0])

################ TESTING
