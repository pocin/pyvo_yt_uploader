#!/usr/bin/env python
''' A Youtube uploader for videos recorded at Pyvo meetings.

Leverages existing youtube-uploading package https://github.com/tokland/youtube-upload
- Loads metadata from supplied yaml file
- creates description
- creates title

Usage:
$ python3 nahraj_pyvo.py /path/to/folder/containing/yaml/and/video

! IMPORTANT !
before the first run on your machine it is necessary to run
$ youtube-upload --title="DummyVideo" dummy_video.mp4
manually.
It will give you url to visit in your browser and you will be
prompted for verification code in the command line.
This is required since the underlying youtube-upload uses OAuth2.0.

Every subsequent calls should require no authentication,
unless your OAuth token expires.


'''
import glob
import os
import yaml
import sys
import logging
import argparse
import subprocess


def load_metadata(directory):
    """Load metadata from yaml file.


    Contents of a sample metadata file:
        speaker: Jiří Bartoň & Jakub Vysoký
        title: "Auth*"
        event: Pražské Pyvo
        date: 2016-02-20
        url: http://lanyrd.com/2016/praha-pyvo-january/
        speaker_only: true
        speaker_vid: '*.MTS'
        praha: true

    Args:
        directory (str): path to directory containing .yaml metadata
            file and .MTS video
    Returns:
        data (dict)
    """
    try:
        logging.debug("Loading yaml file from {}".format(os.path.abspath(
            directory)))
        yaml_filename = glob.glob("*.y*ml")[0]
        with open(yaml_filename, 'r') as f:
            data = yaml.load(f)
        return data

    # IndexError becuase glob returns list
    except (IndexError, FileNotFoundError) as e:
        logging.error("yaml/yml file in {} was not found."
                      "Make sure it exists and try again.".format(
                          os.path.abspath(directory)))
        logging.error(e)
        sys.exit(1)


def create_video_description(metadata):
    '''Parse metadata and create description

    The final format is:
    Pražské Pyvo 2016-02-20
    http://lanyrd.com/2016/praha-pyvo-jan...

    Args:
        metadata (dict): as parsed by load_metadata() function

    Returns:
        description (str)
    '''
    logging.debug("Creating video description")
    date = metadata['date'].strftime("%Y-%b-%d")
    description = [metadata['event'] + ' ' + date, metadata['url']]
    return '\n'.join(description)


def create_video_title(metadata):
    '''Parse metadata and create video title.

    The final format is:
    speaker - title

    Args:
        metadata (dict): parsed yaml metadata

    Returns:
        title (str)
    '''
    logging.debug("Creating video title")
    title = ' - '.join([metadata['speaker'], metadata['title']])
    return title


def parse_args():
    parser = argparse.ArgumentParser(description='Pyvo Youtube uploader')
    parser.add_argument(
        'directory',
        action='store',
        type=str,
        help='directory containing .yaml/.yml file and video.MTS')
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help='display debug info')
    args = parser.parse_args()

    if not args:
        parser.print_help()
        sys.exit(1)

    logging_format = '%(asctime)s:%(levelname)s line:%(lineno)d; %(message)s'
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format=logging_format)
    else:
        logging.basicConfig(format=logging_format)
    return args


def upload_video(directory):
    '''Upload video to yt.

    Parse the metadata file, create description and title and
    send it to yt using youtube-upload library
    https://github.com/tokland/youtube-upload

    Args:
        directory (str): /path/to/dir/containing yaml metadata
            file and video file
    '''

    metadata = load_metadata(directory)
    description = create_video_description(metadata)
    title = create_video_title(metadata)
    video = glob.glob(os.path.join(directory, "*.MTS"))[0]

    logging.info('Uploading {}'.format(video))

    with subprocess.Popen(
        ['youtube-upload', "--title='{}'".format(title),
         "--description='{}'".format(description), video],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT) as proc:
        for line in proc.stdout:
            logging.info(line)


def main():
    args = parse_args()
    upload_video(args.directory)


if __name__ == '__main__':
    main()
