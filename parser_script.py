import urllib3
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
from io import BytesIO

if not os.path.exists("picts"):
    os.makedirs("picts")

with open("urls.txt", "r") as urls_file:
    urls = urls_file.read().splitlines()

http = urllib3.PoolManager()
for url in urls:
    response = http.request("GET", url)
    soup = BeautifulSoup(response.data, "html.parser", from_encoding="iso-8859-1")
    base_url = urlparse(url).scheme + "://" + urlparse(url).hostname
    for img in soup.find_all("img"):
        img_url = img.get("src")
        if not img_url or not (img_url.endswith(".jpg") or img_url.endswith(".webp") or img_url.endswith(".png")):
            continue
        if "http" not in img_url:
            img_url = base_url + img_url
        try:
            img_data = requests.get(img_url).content
            from PIL import Image
            with Image.open(BytesIO(img_data)) as img:
                width, height = img.size
                if width < 500 and height < 500:
                    continue
                image_path = "picts/" + img_url.split("/")[-1]
                old_image_path = "picts_old/" + img_url.split("/")[-1]
                if os.path.exists(old_image_path):
                    os.remove(image_path)
                    continue
                with open(image_path, "wb") as f:
                    f.write(img_data)
        except:
            print(f"Error downloading image: {img_url}")
            continue
print("I'm done!")