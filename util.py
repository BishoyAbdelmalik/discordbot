import requests


def is_url_image(image_url):
   image_formats = ("image/png", "image/jpeg", "image/jpg")
   r = requests.head(image_url)
   if r.headers["content-type"] in image_formats:
      return True
   return False


def get_yt_url(v_id: str):
    return "https://www.youtube.com/watch?v="+v_id

def get_url(url: str):
    import json
    import validators
    from youtube_search import YoutubeSearch
    if not validators.url(url):
        youtube_search = YoutubeSearch(url, max_results=1).to_json()
        youtube_search = json.loads(youtube_search)
        v_id = youtube_search["videos"][0]["id"]
        url = get_yt_url(v_id)
    elif "list" in url or "playlist" in url:
        pass
        # with youtube_dl.YoutubeDL({}) as ydl:
        # 	result=ydl.extract_info(url, download=False)
        # if 'entries' in result:
        # 	# Can be a playlist or a list of videos
        # 	video = result['entries']
        # 	#loops entries to grab each video_url
        # 	for j, item in enumerate(video):
        # 		video = result['entries'][j]["webpage_url"]
        # 		url=video
    return url