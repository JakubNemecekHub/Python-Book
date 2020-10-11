from bs4 import BeautifulSoup
from os import scandir
import subprocess
from pprint import pprint

files = scandir("/home/jakub/Prog/Book/p-g-wodehouse_a-prefects-uncle/src/epub/text")

names = []
for file in files:
    if "chapter" in file.name:
        #print(file.path)
        with open(file.path, "r", encoding="utf8") as chapter:
            soup = BeautifulSoup(chapter, "html.parser")

            # hgroup = soup.new_tag("hgroup")
            # ch_number = soup.new_tag("h2")
            # ch_name = soup.new_tag("h2")
            # for tag in soup.find_all("h2"):
            #     try:
            #         numbers_and_names = tag.string.split(" — ")
            #         ch_number.string = numbers_and_names[0]
            #         ch_number["epub:type"] = "ordinal"
            #         ch_name.string = numbers_and_names[1]
            #         ch_name["epub:type"] = "title"
            #         hgroup.contents = [ch_number, ch_name]
            #         tag.replace_with(hgroup)
            #     except:
            #         print("Problém:", file.name)

            for tag in soup.find_all("h2"):
                try:
                    subprocess.call(["se", "titlecase", tag.string])
                    # titlecase = subprocess.Popen(["se", "titlecase", "-n", tag.string], stdin= subprocess.PIPE, stdout= subprocess.PIPE)
                    # print(str(titlecase.communicate()[0]).strip())
                except:
                    pass

            # [tag.decompose() for tag in soup.find_all(["div", "br", "hr", "a"])]
            # [tag.decompose() for tag in soup.find_all("p") if tag.string == "\n"]

        # with open(file.path, "w", encoding="utf8") as chapter:
        #     chapter.write(str(soup))



# subprocess.call(["se", "titlecase", "5⁠—FARNIE GETS INTO TROUBLE⁠—"])
