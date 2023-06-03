#!/usr/bin/env python3.8
from __future__ import absolute_import, print_function, unicode_literals
import os
import sys
import argparse
import subprocess
from progressbar import ProgressBar, Percentage, Bar, ETA
from glob import glob, escape
import shlex
import json
import pysrt
from pathlib import Path

VERSION = "0.0.4"

def check_file_type(file_path, error_messages_callback=None):
    try:
        ffprobe_cmd = ['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-print_format', 'json', file_path]
        output = None
        if sys.platform == "win32":
            output = subprocess.check_output(ffprobe_cmd, creationflags=subprocess.CREATE_NO_WINDOW).decode('utf-8')
        else:
            output = subprocess.check_output(ffprobe_cmd).decode('utf-8')
        data = json.loads(output)

        if 'streams' in data:
            for stream in data['streams']:
                if 'codec_type' in stream and stream['codec_type'] == 'audio':
                    return 'audio'
                elif 'codec_type' in stream and stream['codec_type'] == 'video':
                    return 'video'
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        pass

    except Exception as e:
        if error_messages_callback:
            error_messages_callback(e)
        else:
            print(e)

    return None


def is_valid_srt_file(file_path, error_messages_callback=None):
    if os.path.isfile(file_path):
        try:
            # Load the SRT subtitle file
            subs = pysrt.open(file_path)
            # If parsing succeeds, the file is considered valid
            return True
        except Exception as e:
            # If parsing fails, the file is considered invalid
            return False
            if error_messages_callback:
                error_messages_callback(e)
            else:
                print(e)
        

def show_error_messages(messages):
    print(messages)


def render_media_with_subtitle(video_path, media_type, media_ext, subtitle_path, output_path, error_messages_callback=None):

    try:
        if "\\" in video_path:
            video_path = video_path.replace("\\", "/")

        if "\\" in subtitle_path:
            subtitle_path = subtitle_path.replace("\\", "/")

        if "\\" in output_path:
            output_path = output_path.replace("\\", "/")


        ffprobe_command = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{video_path}"'
        ffprobe_process = subprocess.Popen(ffprobe_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        total_duration = float(ffprobe_process.stdout.read().decode().strip())

        ffmpeg_command = f'ffmpeg -y -i "{video_path}" -vf "subtitles={shlex.quote(subtitle_path)}" "{output_path}"'

        widgets = [f"Rendering subtitles with {media_type} : ", Percentage(), ' ', Bar(marker="#"), ' ', ETA()]
        pbar = ProgressBar(widgets=widgets, maxval=100).start()
        percentage = 0

        if sys.platform == "win32":
            process = subprocess.Popen(ffmpeg_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        else:
            process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

        for line in process.stdout:
            if "time=" in line:
                #print(line)
                time_str = line.split("time=")[1].split()[0]
                #print("time_str = %s" %time_str)
                current_duration = sum(float(x) * 60 ** i for i, x in enumerate(reversed(time_str.split(":"))))
                #print("current_duration = %s" %current_duration)
                if current_duration>0:
                    percentage = int(current_duration*100/total_duration)
                    #print("percentage = {}%".format(percentage))
                    pbar.update(percentage)
        pbar.finish()
        return output_path

    except Exception as e:
        if error_messages_callback:
            error_messages_callback(e)
        else:
            print(e)
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('video_file_path', help="video file path")
    parser.add_argument('subtitle_file_path', help="SRT subtitle file path")
    parser.add_argument('output_file_path', help="output video file path")
    parser.add_argument('-v', '--version', action='version', version=VERSION)
    args = parser.parse_args()

    video_path = args.video_file_path
    subtitle_path = args.subtitle_file_path
    output_path = args.output_file_path

    media_paths = []
    not_exist_media_paths = []
    invalid_media_filepaths = []
    media_filepaths = []
    media_path_str = ""
    media_type = None

    if (not ("*" and "?") in str(args.video_file_path)):
        fpath = Path(args.video_file_path)
        #print("fpath = %s" %fpath)
        if not os.path.isfile(fpath):
            not_exist_media_paths.append(args.video_file_path)
            #print(str(fpath) + " is not exist")

    if sys.platform == "win32":
        if ("[" or "]") in str(video_path):
            placeholder = "#TEMP#"
            media_path_str = str(video_path)
            media_path_str = media_path_str.replace("[", placeholder)
            media_path_str = media_path_str.replace("]", "[]]")
            media_path_str = media_path_str.replace(placeholder, "[[]")
        else:
            media_path_str = video_path

    else:
        media_path_str = video_path

    if not sys.platform == "win32" :
        media_path_str = escape(media_path_str)

    media_paths += glob(media_path_str)
    #print("media_paths = %s" %media_paths)

    if media_paths:
        if os.path.isfile(media_paths[0]):
            if check_file_type(media_paths[0], error_messages_callback=show_error_messages) == 'video':
                media_filepaths.append(media_paths[0])
                media_type = "video"
            elif check_file_type(media_paths[0], error_messages_callback=show_error_messages) == 'audio':
                media_filepaths.append(media_paths[0])
                media_type = "audio"

            else:
                invalid_media_filepaths.append(argpath)
                media_type = None

        else:
            not_exist_media_paths.append(media_paths[0])
            media_type = None

    if invalid_media_filepaths:
        msg = "{} is not valid video or audio file".format(invalid_media_filepaths[0])
        print(msg)
        sys.exit(0)

    if not_exist_media_paths:
        msg = "{} is not exist".format(not_exist_media_paths[0])
        print(msg)
        sys.exit(0)

    if not media_filepaths and not not_exist_media_paths:
        print("No any video file matching filename you typed")
        sys.exit(0)

    subtitle_paths = []
    not_exist_subtitle_paths = []
    invalid_subtitle_paths = []
    valid_subtitle_paths = []
    subtitle_path_str = ""

    if (not ("*" and "?") in str(args.subtitle_file_path)):
        fpath = Path(args.subtitle_file_path)
        #print("fpath = %s" %fpath)
        if not os.path.isfile(fpath):
            not_exist_subtitle_paths.append(args.subtitle_file_path)
            #print(str(fpath) + " is not exist")

    if sys.platform == "win32":
        if ("[" or "]") in str(subtitle_path):
            placeholder = "#TEMP#"
            subtitle_path_str = str(subtitle_path)
            subtitle_path_str = subtitle_path_str.replace("[", placeholder)
            subtitle_path_str = subtitle_path_str.replace("]", "[]]")
            subtitle_path_str = subtitle_path_str.replace(placeholder, "[[]")
        else:
            subtitle_path_str = subtitle_path

    else:
        subtitle_path_str = subtitle_path

    if not sys.platform == "win32" :
        subtitle_path_str = escape(subtitle_path_str)

    subtitle_paths += glob(subtitle_path_str)

    if subtitle_paths:
        if (not os.path.isfile(subtitle_paths[0])) and (not "*" in subtitle_path_str) and (not "?" in subtitle_path_str):
            not_exist_subtitle_paths.append(subtitle_paths[0])

        if os.path.isfile(subtitle_paths[0]):
            if is_valid_srt_file(subtitle_paths[0], error_messages_callback=show_error_messages):
                valid_subtitle_paths.append(subtitle_paths[0])
            else:
                invalid_subtitle_paths.append(subtitle_paths[0])
        else:
            not_exist_subtitle_paths.append(subtitle_paths[0])

    if invalid_subtitle_paths:
        msg = "{} is not a valid SRT subtitle file".format(invalid_subtitle_paths[0])
        print(msg)

    if not_exist_subtitle_paths:
        msg = "{} is not exist".format(not_exist_subtitle_paths[0])
        print(msg)

    if not valid_subtitle_paths and not not_exist_subtitle_paths:
        print("No any SRT subtitle file matching filename you typed")

    if media_filepaths and valid_subtitle_paths and output_path:
        base, ext = os.path.splitext(media_filepaths[0])
        result = render_media_with_subtitle(media_filepaths[0], media_type, ext, valid_subtitle_paths[0], output_path)

    if result and os.path.isfile(result):
        print("Rendered video created at      : {}".format(output_path))

if __name__ == '__main__':
    sys.exit(main())
