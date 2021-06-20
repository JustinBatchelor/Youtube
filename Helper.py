from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
from pathlib import Path

seconds_in_minute = 60
seconds_in_hour = seconds_in_minute * 60


def hoursToSeconds(hours):
    return int(hours) * seconds_in_hour


def minutesToSeconds(minutes):
    return int(minutes) * seconds_in_minute


def getLink():
    return YouTube(input("Please enter the youtube link here: "))


def getStartTime():
    return input("Please enter the start time of the clip you are trying to create [format 00:00:00]: ")


def getDuration():
    return input("Please enter the duration of the clip in seconds: ")


def convertTimeToSeconds(starttime):
    return int(starttime[-2:]) + minutesToSeconds(starttime[3:4]) + hoursToSeconds(starttime[0:1])


def sortList(mp4_list):
    max = []
    current_max = 0
    for video in mp4_list:
        video_res = video.resolution
        if not (video_res is None):
            resolution = int(str(video.resolution).replace("p", ""))
            if resolution > current_max:
                max.append(video)
    return max[0]


def checkPath():
    if not os.path.isdir(os.path.join(Path.home(), "Videos", "Youtube")):
        os.mkdir(os.path.join(Path.home(), "Videos", "Youtube"))


def formatClipName(title, dir):
    clip_count = 0
    while True:
        clip_name = formatYoutubeTitle(title) + "_clip_{}.mp4".format(clip_count)
        if not os.path.isfile(os.path.join(dir, clip_name)):
            return os.path.join(dir, clip_name)
        clip_count += 1


def formatYoutubeTitle(title):
    return str(title).replace(" ", "_")


def userLoop():
    try:
        youtube = getLink()
        video = sortList(youtube.streams.filter(file_extension='mp4').all())
        checkPath()
        _dir = os.path.join(Path.home(), "Videos", "Youtube")
        _path = os.path.join(_dir, (formatYoutubeTitle(youtube.title) + ".mp4"))
        _formatted_title = formatYoutubeTitle(youtube.title)
        if os.path.isfile(_path):
            print("Seems we have already downloaded this file.")
        else:
            youtube.streams.get_by_itag(video.itag).download(output_path=_dir,
                                                             filename=_formatted_title)
        if input("Would you like to clip this video? [Y/n]: ").lower() == "y":
            start_time = convertTimeToSeconds(getStartTime())
            duration = int(getDuration())

            with VideoFileClip(_path) as clip:
                new = clip.subclip(start_time, (start_time + duration))
                clip_name = formatClipName(youtube.title, _dir)
                new.write_videofile(os.path.join(_dir, clip_name), audio_codec='aac')

    except Exception as e:
        print(e)
