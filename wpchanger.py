import ctypes
import os
import requests
import wget
from PIL import Image
from bs4 import BeautifulSoup

# 게시글 주소 스크래핑
resp = requests.get('http://www.bukedu.or.kr/user/nd51910.do')
soup = BeautifulSoup(resp.text, 'html.parser')
anchors = [text for text in [link.get('href') for link in soup.find_all('a')] if text.startswith("javascript")]

# 이미지 주소 스크래핑
resp = requests.get('http://www.bukedu.or.kr/user/nd51910.do?View&pageSV=&boardNo=' + anchors[0][-11:-3])
soup = BeautifulSoup(resp.text, 'html.parser')
images = [str(image)[10:-12] for image in soup.select("tbody img")]

# 이미지 다운로드
if not os.path.exists("D:\\Downloads"):
    os.mkdir("D:\\Downloads")
file_path = "D:\\Downloads\\bg.png"  # 1
wget.download("http://www.bukedu.or.kr" + images[0], file_path)  # 2

# 이미지 리사이즈
image = Image.open(file_path)
resize_image = image.resize((1920, 1080))
resize_image.save(file_path)

# 이미지를 배경화면으로 지정
ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path, 3)  # 3

# 사용한 이미지 삭제
os.remove(file_path)  # 4