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
# to download. BUT, it CAN and MUST return results for each YouTube channel's upload playlist. Because of the
# limitations of the youtube.videos() functions. It can only deal with videos, not playlists.
# The youtube.videos() function can then take the video ids returned by playlistItems() and derive the
# important details from that. Convoluted? Yes. Works? Also yes. I will look into simplifying this in the future,
# but as of now, this will have to do.

def get_podcast_ids(api_key, podcast_channels):

    # In case podcast_channels has no upload playlist to download from.
    if not podcast_channels:
        print("podcast_channels file is empty. Returning... ")
        return

    cumulative = []
    video_ids = []
    max_returns = 1            # Using a separate variable for video id extraction below.

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
            maxResults=max_returns,             # The max value allowed is 50.
            playlistId=upload_playlist_id       # For each channel's upload playlist.
        )

        # Execute API call for each channel.
        response = request.execute()        # response is a dictionary
        cumulative.append(response)


    # 2. Extract the video_ids.

    # This code is strange, and I'm not completely settled on it.
    # Basically, it's a nested for loop to iterate through a YouTube channel's videos for EACH channel.
    # Outer is for each channel, inner is for each video in that one channel.
    for x in range(0, len(cumulative)):
        for y in range(0, max_returns):
            video_ids.append(cumulative[x]['items'][y]['contentDetails']['videoId'])


    # DEBUGGING
    # print("Cumulative: ")
    # print()
    # pprint.pprint(cumulative)
    # print()
    #
    # print()
    # print("video_ids: ")
    # print()
    # pprint.pprint(video_ids)
    # END DEBUGGING

    return video_ids


def determine_valid_podcasts(api_key, podcast_urls):

    valid_podcasts = []
    test_kickstart_date = datetime(2022-07-08T19:19:35Z)

    # Here, I have just a list of id's; that's it. I've no way to differentiate it.
    # To distinguish podcasts:
    # Greater than 45 minutes long.             # items, contentDetails, duration
    # Published AFTER kickstart datetime.       # items, snippet, publishedAt
    # Other: items, id
    youtube_service = build('youtube', 'v3', developerKey=api_key)

    for podcast_id in podcast_urls:

        request = youtube_service.videos().list(
            part="snippet, contentDetails, statistics",
            id=podcast_id
        )

        response = request.execute()

        pprint.pprint(response)




    return valid_podcasts


def derive_podcast_urls(podcast_ids):

    podcast_urls = []

    for video in podcast_ids:
        podcast_urls.append("www.youtube.com/watch?v=" + video)

    # DEBUGGING
    # pprint.pprint(podcast_urls)

    return podcast_urls


def main():
    """The main driver function"""

    load_dotenv()
    api_key = os.getenv("API_KEY")

    # Load the list of podcasts.
    with open("podcasts.yaml") as f:
        podcast_channels = yaml.load(f, Loader=SafeLoader)

    podcast_ids = get_podcast_ids(api_key, podcast_channels)                    # Get all the podcast ids of recent videos.
    valid_podcast_ids = determine_valid_podcasts(api_key, podcast_ids)          # Determine from ids which podcasts are valid. RETURN ONLY VALID IDS.
    # podcast_urls = derive_podcast_urls(valid_podcast_ids)                     # Append YouTube ids to valid podcast ids.

    # These YouTube urls can now be downloaded!
    # download_m4a(podcast_urls)


if __name__ == "__main__":
    main()



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
