#!/usr/bin/env python
# encoding: utf-8

import os
import re
import logging
import requests

class InsPic:
    """
    Download picture from instagram.
    args:
        [url]: picture's url
        [path]: image storage place, default is where .py file at.
    """
    proxy = {
        'http': "socks5://127.0.0.1:1080",
        'https': "socks5://127.0.0.1:1080"
    }
    headers = {
        "origin": "https://www.instagram.com",
        "user-agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
        )
    }

    def __init__(self, url, path=os.path.abspath(__file__)):
        self.url = url
        self.path = path

    def parse(self):
        html = requests.get(self.url, proxies=self.proxy).text
        self.image_url = re.findall("og:image.+=\"(.+)\"", html)[0]
        return self.image_url or False

    def download(self):
        self.image_path = self.path = self.image_url.split('?')[0][-14:]
        with open(self.image_path, 'w') as image:
            image_content = requests.get(self.image_url,
                                         proxies=self.proxy).content
            image.write(image_content)

    def run(self):
        logging.basicConfig(level=logging.INFO,
                            format="%(levelname)s: %(message)s")
        image_url = self.parse()
        if image_url:
            logging.info("parse succeed, image url {0}.".format(image_url))
            self.download()
            logging.info("storage image at {}.".format(self.image_path))
        else:
            logging.warn("image url not found.")

    def __str__(self):
        return """
            instagram url: {0}
            image url: {1}
            """.format(self.url, self.image_url)

    __repr__ = __str__

if __name__ == "__main__":
    url = "https://www.instagram.com/p/BNuR3KSlnY6/"
    nasa = InsPic(url)
    nasa.run()
