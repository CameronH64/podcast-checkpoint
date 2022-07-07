# Automatic YouTube Podcast Downloading!
This tool is an automatic YouTube podcast downloader; name is pending. Users can specify a YouTube channel's upload ID in a local .yaml file, start the script, and the latest videos will start downloading. A local file will be created and populated with the ID's of videos already downloaded, so they won't be downloaded again. I also plan on adding an option to change the metadata of the files after they download.

# How to Use
Using this program is quite simple.
- Enter each YouTube channel's upload ID in podcasts.yaml, preceded with a dash and space, i.e., "- ".
- Make sure the podcasts.yaml file is in same directory as main.py.
- Run the main.py script.

# How to Find A YouTube Channel's Upload ID
A YouTube channel's upload ID can be derived from its channel ID.
- Navigate to a YouTube channel's home page.
- Copy the URL.
- Enter that URL into this site: https://commentpicker.com/youtube-channel-id.php
- The resulting channel ID should begin with the characters "UC".
- Change those two characters to "UU", keeping the rest the same.
- This string of characters is the channel's upload ID!

## Alternative method
For the more tech-savvy, this method may be more reliable.

- Go to your desired YouTube channel's homepage.
- Inspect element
- In the source code, search for "channelid" (press ctrl + F).
- It may not come up; if it doesn't, **refresh the page, and try again**. It _should_ show up the second time.
- Replace the second character, the "C" to a "U". You now have that channel's upload playlist ID!

While I plan on coding a native or external way of doing this, this will work for most, if not all channels. And once the upload ID is in the podcasts.yaml file, this is the only setup you need to do to start downloading podcasts.

Happy listening!

# Need Help?
Contact me at cholbrook582@gmail.com.
I'll be happy to assist in any way I can. Thanks!
