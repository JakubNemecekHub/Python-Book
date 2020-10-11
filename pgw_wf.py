import subprocess
from bs4 import BeautifulSoup
from tools import get_chapters

def chapter_title(file):
    """
    Edit Chapter titles to the right format.
    Original:
        <h3><a id="I" name="I"/>I<br/>
			<br/>
			EXPERT OPINIONS</h3>
    New:
        <hgroup>
            <h2 epub:type="ordinal z3998:roman">I</h2>
    		<h2 epub:type="title">EXPERT OPINIONS</h2>
        </hgroup>
    """
    # Open file and load soup
    with open(file.path, "r", encoding="utf8") as chapter:
        soup = BeautifulSoup(chapter, "html.parser")

    # Locate and load data from old title
    for tag in soup.find_all("h3"):
        chapter_number = tag.contents[1]
        chapter_title = tag.contents[5].strip()

        # Create a new title
        try:
            hgroup = soup.new_tag("hgroup")
            chapter_number_tag = soup.new_tag("h2")
            chapter_number_tag["epub:type"] = "ordinal z3998:roman"
            chapter_number_tag.string = chapter_number
            chapter_title_tag = soup.new_tag("h2")
            chapter_title_tag["epub:type"] = "title"
            chapter_title_tag.string = chapter_title
            hgroup.contents = [chapter_number_tag, chapter_title_tag]
            tag.replace_with(hgroup)
        except:
            pass

    # Save edited soup into original file
    with open(file.path, "w", encoding="utf8") as chapter:
        chapter.write(str(soup))

def get_italics(file):
    """
    Print all <i> tags without attributes in file
    """
    # Open file and load soup
    with open(file.path, "r", encoding="utf8") as chapter:
        soup = BeautifulSoup(chapter, "html.parser")

    # go through all <i> tags
    for tag in soup.find_all("i"):
        if not (tag.has_attr("epub:type") or tag.has_attr("xml:lang")):
            print(tag)

def semantics(file):
    """
    Go throught file and find all <i> tag and show options:
        n - next
        em - change to em tag
        l "XX" - set xml:lang="XX"
        x - exit
    Original:
        “Don’t apologise to <i>me</i>,” said Allardyce disgustedly
        <i>seriatim</i>
        ??? <i>The Dark Horse</i>
    New:
        “Don’t apologise to <em>me</em>,” said Allardyce disgustedly
        <i xml:lang="la">seriatim</i>
        ??? <i>The Dark Horse</i> nebo <i epub:type="se:name.publication.book">The Dark Horse</i>
    """
    # Open file and load soup
    with open(file.path, "r", encoding="utf8") as chapter:
        soup = BeautifulSoup(chapter, "html.parser")

    # go through all <i> tags
    for tag in soup.find_all("i"):
        if not (tag.has_attr("epub:type") or tag.has_attr("xml:lang")):
            _action = input(f"{tag} | Select action [(n)ext, e(x)t, (e)m, (l)anguage, (p)ublication]: ")
            if _action == "n":
                continue
            elif _action == "x":
                break
            elif _action == "e":
                _new_tag = soup.new_tag("em")
                _new_tag.string = tag.string
                tag.replace_with(_new_tag)
            elif _action == "l":
                _language = input("Which language: ")
                # check if length is 2
                tag["xml:lang"] = _language
            elif _action == "p":
                _publication = input("Which publication [(m)agazine, (b)ook, (p)lay]: ")
                if _publication == "m":
                    tag["epub:type"] = "se:name.publication.magazine"
                elif _publication == "b":
                    tag["epub:type"] = "se:name.publication.book"
                elif _publication == "p":
                    tag["epub:type"] = "se:name.publication.play"

    # Save edited soup into original file
    with open(file.path, "w", encoding="utf8") as chapter:
        chapter.write(str(soup))

def delete_tag(file, tag_name):
    """ Delete all tags, even if they contain something """
    # Open file and load soup
    with open(file.path, "r", encoding="utf8") as chapter:
        soup = BeautifulSoup(chapter, "html.parser")

    # delete all tags
    [tag.decompose() for tag in soup.find_all(tag_name)]

    # Save edited soup into original file
    with open(file.path, "w", encoding="utf8") as chapter:
        chapter.write(str(soup))

def titlecacse(file):
    """ print names of chapters in titlecase into terminal """
    # Nevím jak dostat výsledek do proměnné
    with open(file.path, "r", encoding="utf8") as chapter:
        soup = BeautifulSoup(chapter, "html.parser")

        for tag in soup.find_all("hgroup"):
            _title = tag.contents[3].string
            try:
                subprocess.call(["se", "titlecase", _title])
                # titlecase = subprocess.Popen(["se", "titlecase", "-n", tag.string], stdin= subprocess.PIPE, stdout= subprocess.PIPE)
                # print(str(titlecase.communicate()[0]).strip())
            except:
                pass

def semantics(file, attr_name):
    """ Find all tags with given attributes """
    # Open file and load soup
    with open(file.path, "r", encoding="utf8") as chapter:
        soup = BeautifulSoup(chapter, "html.parser")

    # go through all <i> tags
    for tag in soup.find_all(True):
        if tag.has_attr(attr_name):
            print(tag)


if __name__ == "__main__":
    # Get all "chapter" files from src/epub/text
    chapters = get_chapters("/home/jakub/Prog/Book/p-g-wodehouse_the-white-feather/src/epub/text")
    for chapter in chapters:
        print(chapter.name)
        # chapter_title(chapter)
        # semantics(chapter)
        # get_italics(chapter)
        # delete_tag(chapter, "hr")
        # titlecacse(chapter)
        semantics(chapter, "class")
