import cv2
import numpy as np
import subprocess

# Function to download video using yt-dlp
def download_video(video_url):
    try:
        output_path = "downloaded_video.mp4"
        subprocess.run(
            ["yt-dlp", "-f", "best", "-o", output_path, video_url],
            check=True
        )
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Error downloading video: {e}")
        return None

# Function to extract the first frame as thumbnail
def extract_thumbnail(video_path):
    try:
        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()
        cap.release()
        if ret:
            return frame
        else:
            print("Failed to capture the frame from the video.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to analyze the thumbnail
def analyze_thumbnail(thumbnail):
    try:
        gray = cv2.cvtColor(thumbnail, cv2.COLOR_BGR2GRAY)
        mean_val = np.mean(gray)
        return mean_val
    except Exception as i:
        print(f"Error in analyzing thumbnail: {i}")
        return None

# Function to analyze the title
def analyze_text(title):
    title_keywords = title.split()
    return [word.lower() for word in title_keywords]

# Function to compare thumbnail and content 
def compare_thumbnail_content(thumbnail_analysis, content_analysis):
    relevant_keywords = ['episode', 'season', 'ft.', 'guest', 'special', 'live']
    title_keywords = set(content_analysis)
    return any(keyword.lower() in title_keywords for keyword in relevant_keywords)

def clickbait_analysis():
    video_url = input("Enter the YouTube video URL: ").strip()
    video_title = input("Enter the video title: ").strip()
    video_path = download_video(video_url)
    if video_path is not None:
        thumbnail = extract_thumbnail(video_path)
        if thumbnail is not None:
            thumbnail_analysis = analyze_thumbnail(thumbnail)
            content_analysis = analyze_text(video_title)
            if thumbnail_analysis is not None:
                result = compare_thumbnail_content(thumbnail_analysis, content_analysis)
                if result:
                    print("The thumbnail matches the content!")
                    print("The video is not a clickbait. ")
                else:
                    print("The thumbnail does not match the content.")
                    print("The video is a clickbait. ")
            else:
                print("Thumbnail analysis failed.")
        else:
            print("Unable to extract thumbnail from the video.")
    else:
        print("Video download failed.")

clickbait_analysis()