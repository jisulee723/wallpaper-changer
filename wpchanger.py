import os
import tempfile
import requests
import wget
import win32api
import win32con
import win32gui
from PIL import Image
from bs4 import BeautifulSoup


# 이미지 url 얻기
def get_url(pick):
    if pick == 1:
        # 게시글 주소 스크래핑
        resp = requests.get('http://www.bukedu.or.kr/user/nd51910.do')
        soup = BeautifulSoup(resp.text, 'html.parser')
        anchors = [text for text in [link.get('href') for link in soup.find_all('a')] if text.startswith("javascript")]

        # 이미지 주소 스크래핑
        resp = requests.get('http://www.bukedu.or.kr/user/nd51910.do?View&pageSV=&boardNo=' + anchors[0][-11:-3])
        soup = BeautifulSoup(resp.text, 'html.parser')
        images = [str(image)[10:-12] for image in soup.select("tbody img")]

        return "http://www.bukedu.or.kr" + images[0]
    elif pick == 2:
        return "https://raw.githubusercontent.com/jisulee723/wallpaper-changer/master/images/defaultImage.jpg"
    elif pick == 3:
        print("이미지 주소를 입력하세요: ", end="")
        url = input()
        return url


# 바탕화면 설정
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


# path 설정 및 폴더 체크
temp_dir = tempfile.TemporaryDirectory()
file_path = temp_dir.__enter__()
bg = "bg.png"
image_path = os.path.join(file_path, bg)

# 바탕화면 선택
print("Step1. 바탕화면을 골라주세요")
print("------------------------------------------------------------------------------------------------")
print("1) 식단표")
print("2) 기본 바탕화면")
print("3) 이미지 주소 직접 입력")
print("------------------------------------------------------------------------------------------------")
while True:
    print("\n입력1: ", end="")
    pickBg = int(input())
    if pickBg not in (1, 2, 3):
        print("잘못된 값을 입력했습니다")
        continue
    wget.download(get_url(pickBg), image_path)
    break

# 적용방식 선택
print("\n\nStep2. 적용 방식을 골라주세요")
print("------------------------------------------------------------------------------------------------")
print("1) 채우기")
print("2) 맞춤")
print("3) 확대")
print("4) 바둑판식 배열")
print("5) 가운데")
print("6) 스팬")
print("------------------------------------------------------------------------------------------------")
while True:
    print("\n입력2: ", end="")
    pickStyle = int(input())
    if pickStyle not in (1, 2, 3, 4, 5, 6):
        print("잘못된 값을 입력했습니다")
        continue
    break

# 작은 이미지를 크게 사용하는 것이라면
if pickStyle in (1, 6):
    # 이미지 리사이즈
    base_image = Image.open(image_path)
    resize_image = base_image.resize((1920, 1080))
    resize_image.save(image_path)

# 바탕화면으로 변경
set_wallpaper(image_path, pickStyle)

# 사용한 이미지와 디렉토리 삭제
temp_dir.cleanup()
