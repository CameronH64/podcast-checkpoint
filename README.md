# Automatic YouTube Podcast Downloading!
This tool is an automatic YouTube podcast downloader. Once the program is set up, all the user has to do is start the script, and the latest YouTube channel podcasts will start downloading. More features are pending, but this base functionality will remain.
# How to Use
Using this program is quite simple.
- Enter each YouTube channel's upload ID in podcasts.yaml, preceded with a dash and space, i.e., "- ".
- Ensure that "main.py", "podcasts.yml", and "checkpoint.yml" are all in the same directory.
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

# API Key Generation
In order to use this application, you must have a .env file containing an API key in the same directory as that executable. I'm not sharing my API key. However, this guide can show you how to do generate your own.

*Only steps 2 and 3 are necessary*.
https://developers.google.com/youtube/v3/getting-started

Once you generate it, paste the key and variable declaration in the .env file and save. The program is now completely ready to be used!

    API_KEY=api_key_goes_here

While I plan on coding a native or external way of doing this, this will work for most, if not all channels. And once the upload ID is in the podcasts.yaml file, this is the only setup you need to do to start downloading podcasts.

Happy listening!

# Need Help?
Contact me at cholbrook582@gmail.com.
I'll be happy to assist in any way I can. Thanks!
