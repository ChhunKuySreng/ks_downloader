import os
import re
import requests
from moviepy.editor import VideoFileClip, concatenate_videoclips
from tqdm import tqdm
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

class KuaishouDownload:
    def __init__(self, user_id, download_dir_path):
        self.download_dir_path = download_dir_path
        self.user_id = user_id
        # self.cookie = 'kpf=PC_WEB; clientid=3; did=web_f05060d6067c69d1927877f59838fb40; didv=1709519762000; kpn=KUAISHOU_VISION'
        self.cookie = input('Cookie : ')
        self.max_videos = input('Enter Maximum Downloads Or (Press Enter To Download All): ')
        if self.max_videos:
            self.max_videos = int(self.max_videos)
        else:
            self.max_videos = None
        self.videos_downloads_path = os.path.join(self.download_dir_path, "videos_downloads")
        if not os.path.exists(self.videos_downloads_path):
            os.makedirs(self.videos_downloads_path)

    def set_user_id(self):
        try:
            url = 'https://www.kuaishou.com/graphql'
            headers = {
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.9,km;q=0.8',
                'Connection': 'keep-alive',
                'Content-Length': '662',
                'content-type': 'application/json',
                'Cookie': self.cookie,
                'Host': 'www.kuaishou.com',
                'Origin': url,
                'Referer': url,
                'sec-ch-ua': 'Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': 'Windows',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            }
            payload = {
                'operationName': "graphqlSearchUser",
                'query': "query graphqlSearchUser($keyword: String, $pcursor: String, $searchSessionId: String) {\n  visionSearchUser(keyword: $keyword, pcursor: $pcursor, searchSessionId: $searchSessionId) {\n    result\n    users {\n      fansCount\n      photoCount\n      isFollowing\n      user_id\n      headurl\n      user_text\n      user_name\n      verified\n      verifiedDetail {\n        description\n        iconType\n        newVerified\n        musicCompany\n        type\n        __typename\n      }\n      __typename\n    }\n    searchSessionId\n    pcursor\n    __typename\n  }\n}\n",
                'variables': {'keyword': self.user_id},
            }
            proxy = {'http': None, 'https': None}
            request_url_id = requests.post(url=url, json=payload, headers=headers, verify=False, proxies=proxy)
            p_0 = re.compile(r'"user_id":".*?"')
            self.user_id = p_0.findall(request_url_id.text)[0][11:-1]
            print('User_Id_Is : ', self.user_id)
        except:
            print('please wait, we are fixing the problem')
            self.set_user_id()

    def get_video_downloaded(self, pcursor=None):
        url = 'https://www.kuaishou.com/graphql'
        headers = {
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9,km;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '1784',
            'content-type': 'application/json',
            'Cookie': self.cookie,
            'Host': 'www.kuaishou.com',
            'Origin': url,
            'Referer': url,
            'sec-ch-ua': 'Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        payload = {
            'operationName': "visionProfilePhotoList",
            'query': "fragment photoContent on PhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment recoPhotoFragment on recoPhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    ...recoPhotoFragment\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nquery visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n",
            'variables': {'userId': self.user_id, 'pcursor': pcursor, 'page': "profile"}
        }
        try:
            video_counter = 0  # Define video_counter here
            while True:
                request_url = requests.post(url=url, json=payload, headers=headers)
                request_data = request_url.json()
                if request_url.status_code == 200:
                    feeds = request_data.get('data', {}).get('visionProfilePhotoList', {}).get('feeds', [])
                    if not feeds:
                        break
                    for index, feed in enumerate(feeds):
                        photo = feed.get('photo', {})
                        if photo:
                            video_name = photo.get('originCaption', '')
                            video_url = photo.get('photoH265Url', '')
                            if video_name and video_url:
                                video_counter += 1
                                if self.max_videos is not None and video_counter > self.max_videos:
                                    return  # Stop downloading more videos
                                self.download_video(video_name, video_url, video_counter)
                    pcursor = request_data.get('data', {}).get('visionProfilePhotoList', {}).get('pcursor')
                    if not pcursor:
                        break
                    # Update payload with new pcursor
                    payload['variables']['pcursor'] = pcursor
        except Exception as e:
            print('Error:', e)


    def concatenate_videos(self, request_url_list, remove_rest=False):
        data_path = os.path.join(self.download_dir_path, self.user_id)
        suffix = '.mp4'
        save_path = os.path.join(data_path, f"{self.user_id} compilation.mp4")
        file_names = []
        for root, files in os.walk(data_path):
            files.sort()
            for file in files:
                if os.path.splitext(file)[1] == suffix:
                    filePath = os.path.join(root, file)
                    video = VideoFileClip(filePath)
                    file_names.append(video)
        clip = concatenate_videoclips(file_names)
        clip.to_videofile(save_path, fps=60, remove_temp=False)
        if remove_rest:
            for i in range(len(request_url_list)):
                os.remove(os.path.join(data_path, f"{self.user_id}{i + 1}.mp4"))

    def download_video(self, video_name, video_url, video_counter):
        try:
            file_name = f'{video_counter}.{video_name}.mp4'
            user_folder_path = os.path.join(self.videos_downloads_path, self.user_id)
            if not os.path.exists(user_folder_path):
                os.makedirs(user_folder_path)
            file_path = os.path.join(user_folder_path, file_name)
            if os.path.exists(file_path):
                print(f'Skipping: {file_name} - Already downloaded')
                return

            video_content = requests.get(video_url, stream=True, verify=False)
            total_size = int(video_content.headers.get('content-length', 0))
            block_size = 1024  # 1 KB
            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
            with open(file_path, mode='wb') as f:
                for data in video_content.iter_content(block_size):
                    progress_bar.update(len(data))
                    f.write(data)
            progress_bar.close()

            print(f'Downloaded: {file_name}')
        except Exception as e:
            print(f'Error downloading {video_name}: {e}')

    def run_download(self, make_compilation=False, remove_rest=False):
        self.get_video_downloaded()
        if make_compilation:
            request_url_list = []
            self.concatenate_videos(request_url_list, remove_rest=remove_rest)

if __name__ == "__main__":
    print("Example --> User ID : 3xbuci3a79pcr8k")
    print("Example --> Cookie : kpf=PC_WEB; clientid=3; did=web_f05060d6067c69d1927877f59838fb40; didv=1709519762000; kpn=KUAISHOU_VISION")
    while True:
        user_id_list = [input("User ID : ")]
        for user_id in user_id_list:
            downloader = KuaishouDownload(user_id, download_dir_path=os.getcwd())
            downloader.run_download(make_compilation=False, remove_rest=False)
            input("Press Enter to continue...")