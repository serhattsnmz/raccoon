import os
import re
import sys
import requests
import argparse
import textwrap
from bs4 import BeautifulSoup

"""
def __init__(self, url, index, output):
    self.web_url    = "http://slimhamdi.net/istanbul/demos/"
    self.index_path = "index-dark.html"
    self.save_path  = "content/"
    self.soup       = None
    os.makedirs(self.save_path, exist_ok=True)
"""

class WebPageDownloader:

    def __init__(self, url, index, output):
        self.web_url    = url
        self.index_path = index
        self.save_path  = output
        self.soup       = None
        os.makedirs(self.save_path, exist_ok=True)

    def get_page_content(self):
        print("Downloading main page...")

        if not self.index_path:
            r = requests.get(self.web_url)
            self.index_path = "index.html"
        else:
            r = requests.get(self.web_url + self.index_path)

        with open(self.save_path + self.index_path, "wb") as f:
            f.write(r.content)
            
        self.soup = BeautifulSoup(r.text, "html.parser")

    def download_file(self, url):
        if "http" in url:
            return

        _dir        = self.save_path + "/".join(url.split("/")[:-1])
        _filename   = (self.save_path + url).split("?")[0]
        _url        = self.web_url + url

        os.makedirs(_dir, exist_ok=True)
        _r = requests.get(_url)
        with open(_filename, "wb") as f:
            f.write(_r.content)

    def download_css_files(self):
        print("Downloading css files...")
        styles = self.soup.find_all("link")
        for style in styles:
            if "href" in style.attrs:
                self.download_file(style["href"])

    def download_script_files(self):
        print("Downloading script files...")
        script_links = self.soup.find_all("script")
        for script in script_links:
            if "src" in script.attrs:
                self.download_file(script["src"])

    def download_image_files(self):
        print("Downloading image files...")
        images = self.soup.find_all("img")
        for img in images:
            if "src" in img.attrs:
                self.download_file(img["src"])

    def download_video_sources(self):
        print("Downloading video files...")
        videos = self.soup.find_all("source")
        for video in videos:
            if "src" in video.attrs:
                self.download_file(video["src"])
    
    def find_css_urls(self):
        print("Downloading images and font in css files...")
        all_css_files = []
        for dirpath, dirnames, filenames in os.walk(self.save_path):
            for filename in filenames:
                if ".css" in filename or ".html" in filename:
                    all_css_files.append(f"{dirpath}/{filename}".replace("\\","/"))
        
        all_external_urls = []
        for css_file in all_css_files:
            with open(css_file, encoding="utf-8") as f:
                content = f.read()
            url_list = re.findall("url\([a-zA-Z0-9.\/\-?=,'\"]*\)", content)
            url_list = [k.replace("url(","").replace(")","").replace("'","").replace('"','').replace("../","") for k in url_list if "data:image" not in k]
            all_external_urls.extend(url_list)

        for url in all_external_urls:
            self.download_file(url)

class Helper:
    @staticmethod
    def parse_arguments():
        extra_help = textwrap.dedent("""\
        NOTE:
            "--url" parameter must define the base address which all css, js and the other files take as base address.

        EXAMPLE USAGE:
            python3 raccoon.py -u http://example.com
            python3 raccoon.py -u http://example.com -i index.html
            python3 raccoon.py -u http://example.com -i index.html -o site-files
        """)

        parser = argparse.ArgumentParser(description="Single page html downloader", epilog=extra_help, formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument("-u", "--url", metavar="", help="Html url base address", required=True)
        parser.add_argument("-i", "--index", metavar="", help="Html path")
        parser.add_argument("-o", "--output", metavar="", help="User username")
        args = parser.parse_args()

        url     = getattr(args, "url", None)
        index   = getattr(args, "index", None)
        output  = getattr(args, "output", None)

        if "http://" not in url and "https://" not in url:
            print("Invalid url format! Use http or https before domain name.")
            sys.exit(0);
        if url[-1] != "/":
            url += "/"

        if not output:
            output = "./output/"
        if output[-1] != "/":
            output += "/"
        
        return url, index, output

if __name__ == "__main__":

    url, index, output = Helper.parse_arguments()

    w = WebPageDownloader(url, index, output)
    w.get_page_content()
    w.download_css_files()
    w.download_script_files()
    w.download_image_files()
    w.download_video_sources()
    w.find_css_urls()
    print("Done.")