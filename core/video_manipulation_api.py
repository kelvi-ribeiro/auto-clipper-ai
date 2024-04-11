from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import *
import multiprocessing
import os

def cut_video(video, cuts):
    cut_segments = []
    for cut in cuts:
        start_time = cut.get("start")
        end_time = cut.get("end")
        if start_time < 0: 
            start_time = 0
        if end_time > video.duration:
            end_time = video.duration
            
        segment = video.subclip(start_time, end_time)
        cut_segments.append(segment)

    return cut_segments

def generate_video(combined_videos, times_of_each_keyword_spoken, dir_to_save, final_video_name, masks_config):
    cut_segments = []
    cut_segments = cut_video(combined_videos, times_of_each_keyword_spoken)
    if not cut_segments:
        print("No cuts found for the word passed")
    else:
        print(f"'{len(cut_segments)}' cuts were found in the video '{final_video_name}'")
        concatenated_videoclips = concatenate_videoclips(cut_segments) 
        if masks_config["flip"] is True:
            concatenated_videoclips = concatenated_videoclips.add_mask().rotate(180)
   
        concatenated_videoclips.write_videofile(f"{dir_to_save}{os.sep}{final_video_name}.mp4", threads=multiprocessing.cpu_count())
    return (len(cut_segments), sum(i['end'] - i['start']   for i in times_of_each_keyword_spoken))

def merge_videos(videos_paths):
    print(f"About to merge '{len(videos_paths)}' videos")
    videos = []
    for video_path in videos_paths:
        try:
            videos.append(VideoFileClip(video_path)) 
        except Exception as e:
            print(f"Error loading video: {e}")
            return None  
    ## TODO DAR UM JEITO DE FECHAR OS VÍDEOS, TEM ALGUNS CASOS QUE DÁ ERRO NO FINAL DO PROCESSO
    ## video.close
    if(len(videos) == 1):  
        return videos[0]

    return concatenate_videoclips(videos) 