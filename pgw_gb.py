import os
from bs4 import BeautifulSoup
from tools import get_chapters

def body_chapters():
    file_path = "/home/jakub/Prog/Book/p-g-wodehouse_the-white-feather/src/epub/text/body.xhtml"
    with open(file.path, "r", encoding="utf8") as chapter:
        soup = BeautifulSoup(chapter, "html.parser")
    tags_h2 = soup.find_all("h2")
    print(tags_h2)
