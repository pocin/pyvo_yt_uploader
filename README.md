#A Youtube uploader for videos recorded at [Pyvo](www.python.cz) meetings.
Leverages existing youtube-uploading package https://github.com/tokland/youtube-upload
- Load metadata from supplied yaml file
- create description
- create title

# Installation
see https://github.com/tokland/youtube-upload

# Usage
`$ python3 upload_pyvo.py /path/to/folder/containing/yaml_and_video`

Make sure the `/path/to/folder/containing/yaml_and_video contains`
both yaml file and video (format specified by 'speaker\_vid' attr).

**! IMPORTANT !**
before the first run on your machine it is necessary to upload any video with command

`$ youtube-upload --title="DummyVideo" dummy_video.mp4`

you will be given url to visit in your browser and prompted for verification code in the command line.

This is required since the underlying youtube-upload uses OAuth2.0.
Every subsequent calls should require no authentication, unless your OAuth token expires.
