# Automatic YouTube Podcast Downloading!
This tool is an automatic YouTube podcast downloader; name is pending. Users can specify a YouTube channel's upload ID in a local .yaml file, start the script, and the latest videos will start downloading. local file will be created and populated with the ID's of videos already downloaded so they I also plan on adding an option to change some of the metadata of the files after they download.

# How to Use
- Enter upload ID's in podcasts.yaml, preceded with a dash and space, i.e., "- ".
- Make sure podcasts.yaml file is in same directory as main.py
- Run main.py script.

# How to Find A YouTube Channel's Upload ID
A YouTube channel's upload ID can be derived from its channel ID.
- Navigate to a YouTube channel's home page.
- Copy the URL.
- Enter that URL into this site: https://commentpicker.com/youtube-channel-id.php
- The resulting channel ID should begin the characters "UC".
- Change those two characters to "UU", keeping the rest the same.
- This string of characters is the channel's upload ID!

## Alternative method
For the more tech savvy, this method may be more reliable.

- Go to a YouTube channel's homepage.
- Inspect element.
- In the source code, search for "channelid".
- It may not come up; if so, refresh the page, and try again.
- It should show up in the search.
- Replace the second character, the "C" to a "U". You now have that channel's upload playlist ID!

While I plan on coding a native or external way of doing this, this will work for most, if not all channels.

# Need Help?
Contact me at cholbrook582@gmail.com.
I'll be happy to assist in any way I can. Thanks!
