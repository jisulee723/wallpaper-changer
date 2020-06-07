import os
import requests
import wget
import win32api
import win32con
import win32gui
from PIL import Image
from bs4 import BeautifulSoup


def set_wallpaper(path, fill_type=1):
    tile = "0"
    if fill_type == 4:
        fill_type = 5
        tile = "1"
    fill_dict = {
        1: "10",
        2: "6",
        3: "2",
        5: "0",
        6: "22"
    }
    style = fill_dict[fill_type]
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                                "Control Panel\\Desktop", 0,
                                win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, style)
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, tile)
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, path, 1 | 2)
    win32api.RegCloseKey(key)


# 폴더 체크
if not os.path.exists("D:\\Downloads"):
    os.mkdir("D:\\Downloads")
file_path = "D:\\Downloads\\bg.png"

# 선택창 띄우기
print("Step1. 바탕화면을 골라주세요")
print("------------------------------------------------------------------------------------------------")
print("1) 식단표")
print("2) 기본 바탕화면")
print("------------------------------------------------------------------------------------------------")
print("\n입력: ", end="")
pickBg = int(input())
print("\n\nStep2. 적용 방식을 골라주세요")
print("------------------------------------------------------------------------------------------------")
print("1) 채우기")
print("2) 맞춤")
print("3) 확대")
print("4) 바둑판식 배열")
print("5) 가운데")
print("6) 스팬")
print("------------------------------------------------------------------------------------------------")
print("\n입력: ", end="")
pickStyle = int(input())

if pickBg == 1:
    # 게시글 주소 스크래핑
    resp = requests.get('http://www.bukedu.or.kr/user/nd51910.do')
    soup = BeautifulSoup(resp.text, 'html.parser')
    anchors = [text for text in [link.get('href') for link in soup.find_all('a')] if text.startswith("javascript")]

    # 이미지 주소 스크래핑
    resp = requests.get('http://www.bukedu.or.kr/user/nd51910.do?View&pageSV=&boardNo=' + anchors[0][-11:-3])
    soup = BeautifulSoup(resp.text, 'html.parser')
    images = [str(image)[10:-12] for image in soup.select("tbody img")]

    # 이미지 다운로드
    wget.download("http://www.bukedu.or.kr" + images[0], file_path)
else:
    # 이미지 다운로드
    wget.download("https://raw.githubusercontent.com/jisulee723/wallpaper-changer/master/images/defaultImage.jpg", file_path)

# 작은 이미지를 크게 사용하는 것이라면
if pickStyle in (1, 6):
    # 이미지 리사이즈
    image = Image.open(file_path)
    resize_image = image.resize((1920, 1080))
    resize_image.save(file_path)

# 바탕화면으로 변경
set_wallpaper(file_path, pickStyle)

# 사용한 이미지 삭제
os.remove(file_path)
