import pprint
import yt_dlp
import os
import yaml
from yaml.loader import SafeLoader
from dotenv import load_dotenv
from googleapiclient.discovery import build
import datetime
import isodate


def main():

    print("Program is running...")

    api_key = return_api_key()

    podcast_ids = get_podcast_ids(api_key)                    # Get all the podcast ids of recent videos.

    valid_podcast_ids = determine_valid_podcasts(api_key, podcast_ids)          # Determine from ids which podcasts are valid. RETURN ONLY VALID IDS.

    # update_checkpoint()

    podcast_urls = derive_podcast_urls(valid_podcast_ids)                       # Append YouTube ids to valid podcast ids.

    download_m4a(podcast_urls)

    # Change file title and metadata (use regex)

    # If some sort of error happened, do not update the podcast checkpoint.


def return_api_key():

    load_dotenv()
    api_key = os.getenv("API_KEY")
    return api_key


def get_podcast_ids(api_key):

    # Load the list of podcasts.
    with open("podcasts.yml") as f:
        podcast_channels = yaml.load(f, Loader=SafeLoader)

    # In case podcast_channels has no upload playlist to download from.
    if not podcast_channels:
        print("podcast_channels file is empty. Returning... ")
        return

    cumulative_video_info = []
    video_ids = []
    max_returns = 25            # Using a separate variable for video id extraction below.

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
        cumulative_video_info.append(response)


    # 2. Extract the video_ids.

    # This code is strange, and I'm not completely settled on it.
    # Basically, it's a nested for loop to iterate through a YouTube channel's videos for EACH channel.
    # Outer is for each channel, inner is for each video in that one channel.
    for x in range(0, len(cumulative_video_info)):
        for y in range(0, max_returns):
            video_ids.append(cumulative_video_info[x]['items'][y]['contentDetails']['videoId'])


    return video_ids


def determine_valid_podcasts(api_key, podcast_urls):

    valid_podcasts = []
    valid_publish_datetime = False
    valid_duration = False
    set_minutes = 2

    # Variable for duration checking
    minimum_duration = datetime.timedelta(days=0, minutes=set_minutes, seconds=0)

    # Variable for checkpoint checking.
    with open("checkpoint.yml", "r") as file:
        checkpoint_file = yaml.load(file, Loader=yaml.SafeLoader)       # type: list
        checkpoint = checkpoint_file[0]

    checkpoint = checkpoint.strftime("%Y-%m-%dT%H:%M:%SZ")
    checkpoint = datetime.datetime.strptime(checkpoint, "%Y-%m-%dT%H:%M:%SZ")

    # The checkpoint checking requires some explanation.
    # The YouTube returns a string, which is parsed to a datetime object. This is datetime object is naive.
    # However, the checkpoint.yml file needs to be loaded.
    # Then, the single content is offloaded to a variable.
    # Then, the variable is converted to a string in the correct format.
    # This string does the same thing that the YouTube return does (string to datetime).
    # This resolves the datetime naive vs. aware problem!
    # (Though it's quite convoluted).

    youtube_service = build('youtube', 'v3', developerKey=api_key)

    for podcast_id in podcast_urls:

        # Build YouTube object, and execute it.
        request = youtube_service.videos().list(
            part="snippet, contentDetails, liveStreamingDetails",
            id=podcast_id
        )

        response = request.execute()

        # ---------------------------------------- Podcast Checks ----------------------------------------

        # ------- Duration Check -------
        duration = isodate.parse_duration(response['items'][0]['contentDetails']['duration'])

        if duration >= minimum_duration:
            valid_duration = True

        # ------- Checkpoint Check -------
        video_publishedAt = response['items'][0]['snippet']['publishedAt']                          # Return YouTube published datetime.
        video_publishedAt = datetime.datetime.strptime(video_publishedAt, "%Y-%m-%dT%H:%M:%SZ")     # Convert to string.

        if video_publishedAt > checkpoint:
            valid_publish_datetime = True

        # ---------------------------------------- Final Checks ----------------------------------------

        # Determine if video is a valid podcast.
        if valid_duration and valid_publish_datetime:
            valid_podcasts.append(podcast_id)


        # Reset variables for next iteration.
        valid_publish_datetime = False
        valid_duration = False

        # print("----------------------------------------")
        # pprint.pprint(response)

    pprint.pprint(valid_podcasts)

    return valid_podcasts


def derive_podcast_urls(podcast_ids):

    podcast_urls = []

    for video in podcast_ids:
        podcast_urls.append("https://www.youtube.com/watch?v=" + video)

    # DEBUGGING
    pprint.pprint(podcast_urls)

    return podcast_urls


def update_checkpoint():

    datetime_now = datetime.datetime.now()
    datetime_now_string = datetime.datetime.strftime(datetime_now, "%Y-%m-%dT%H:%M:%SZ")

    yaml_date = f"- {datetime_now_string}"

    with open('checkpoint.yml', 'w') as f:
        f.write(yaml_date)


def download_m4a(URLS):

    SAVE_PATH = './downloads'

    options = {
        'format': 'm4a/bestaudio/best',
        # See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'ffmpeg_location': os.path.realpath(os.getenv('FFMPEG_LOCATION')),
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }],
        'outtmpl': os.path.join(SAVE_PATH, '%(title)s.%(ext)s')
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





if __name__ == "__main__":
    main()



# ---------------------------------------- TESTING

# # Extract videoId and videoPublishedAt
# video_urls.append(response['items'][0]['contentDetails']['videoId'])
# video_published_ats.append(response['items'][0]['contentDetails']['videoPublishedAt'])
#
# print("Video ids: \t\t\t\t", video_urls)
# print("Video publish dates: \t", video_published_ats)
#
# test_list = [video_urls, video_published_ats]
# print(test_list[0])


# print("video published:", response['items'][0]['snippet']['publishedAt'], end=". ")
#
# try:
#     print("actualStartTime:", response['items'][0]['liveStreamingDetails']['actualStartTime'], end=" ")
# except Exception:
#     print("Eh, an actual error happened.", end=" ")
#
# try:
#     print("scheduleStartTime:", response['items'][0]['liveStreamingDetails']['scheduledStartTime'], end=" ")
# except Exception:
#     print("Eh, a schedule error happened.", end=" ")
#
# print()

