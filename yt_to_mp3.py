import json
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os 

def download_youtube_video(youtube_link, output_path):
    yt = YouTube(youtube_link)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(output_path)
    return stream.default_filename

def convert_to_mp3(video_filename, output_path):
    video_clip = VideoFileClip(video_filename)
    mp3_filename = output_path + video_filename.split('.')[0] + ".mp3"
    video_clip.audio.write_audiofile(mp3_filename)
    return mp3_filename

def my_yt_func(youtube_link, output_path):
    yt = YouTube(youtube_link)
    # extract only audio 
    video = yt.streams.filter(only_audio=True).first() 

    # check for destination to save file 
    #print("Enter the destination (leave blank for current directory)") 
    destination = output_path #str(input(">> ")) or '.'

    # download the file 
    out_file = video.download(output_path=destination) 

    # save the file 
    base, ext = os.path.splitext(out_file) 
    new_file = base + '.mp3'
    os.rename(out_file, new_file) 

    # result of success 
    print(yt.title + " has been successfully downloaded.")

def load_links_from_json(filename):
    with open(filename, 'r') as f:
        youtube_links = json.load(f)
    return youtube_links

if __name__ == "__main__":
    json_file = 'list_to_link.json' #input("Enter the JSON file containing YouTube links: ")
    output_folder = 'output/' #input("Enter the folder path to save MP3 files: ")

    youtube_links = load_links_from_json(json_file)

    for track_name, youtube_link in youtube_links.items():
        print(f"Downloading and converting: {track_name}")
        my_yt_func(youtube_link, output_folder)
        # video_filename = download_youtube_video(youtube_link, output_folder)
        # try:
        #     mp3_filename = convert_to_mp3(output_folder + video_filename, output_folder)
        #     print(f"{track_name} converted to MP3: {mp3_filename}")
        # except: # KeyError:
        #     print(f"Error: Video fps information not found for {track_name}. Skipping...")
