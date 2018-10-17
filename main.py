from PIL import Image
import pytesseract
import os
from os import walk
from pyquery import PyQuery


class Scraper():

    def __init__(self, email, html_path):
        self.email = email
        self.html_path = html_path
        self.full_name = ""
        self.research = ""
        self.education = ""
        self.homepage = ""


    def Start(self):
        # The name can be found by parsing this part of the code in the html
        # <h3 class="heading-title pull-left">
        i = 0
        name = []
        cleaned_name = []
        full_name = ""

        research = []
        education = []
        homepage = ""

        isname = False
        isresearch = False
        iseducation = False
        # I is there for us to be able to read 3 lines that contain the name of the person
        with open(self.html_path, "r") as txt:
            lines = txt.readlines()
            for line in lines:
                if i != 0:
                    if isname:
                        name.append(line)

                    if isresearch:
                        research.append(line)

                    if iseducation:
                        education.append(line)


                    i -= 1
                if i == 0:
                    isname = False
                    isresearch = False
                    iseducation = False

                if '<h3 class="panel-title">Education</h3>' in line:
                    i = 2
                    iseducation = True

                if '<h3 class="panel-title">Research Interests</h3>' in line:
                    i = 2
                    isresearch = True

                if '<h3 class="heading-title pull-left">' in line:
                    i = 9
                    isname = True

                if 'Homepage' in line:
                    homepage = line

            if homepage:
                pq = PyQuery(homepage.strip())
                tag = pq('a')
                print("Homepage: {}".format(tag.attr('href')))
                self.homepage = tag.attr('href')


            for line in education:
                if line.strip() != "</div>":
                    pq = PyQuery(line.strip())
                    tag = pq('p')
                    print("Education: {}".format(tag.text()))
                    self.education = tag.text()

            # This part is for getting the research
            for line in research:
                if line.strip() != "</div>":
                    pq = PyQuery(line.strip())
                    tag = pq('p')
                    print("Research interests: {}".format(tag.text()))
                    self.research = tag.text()

            # This part is for getting the name
            for thing in name:
                if not thing.isspace():
                    cleaned_name.append(thing.rstrip().replace(" ", ""))
            for word in cleaned_name:
                full_name += word

            print(full_name)
            self.full_name = full_name


    def Cleanup(self):
        # This writes the csv
        with open("output.txt", "a") as txt:
            txt.write("\nEmail: {}, Fullname: {}, Research interests: {}, Education: {}, Homepage: {}".format(self.email, self.full_name, self.research, self.education, self.homepage))



# --------------- This is a machine learning model detecting the emails
# If any errors happen it is probably because you havent installed pytesseract the right way
# Make sure you have the libraries installed like this pip install pillow pytesseract
# Here you can find a way to install the remaining parts of pytesseract
# https://stackoverflow.com/questions/42831662/python-install-tesseract-for-windows-7

files = []
for (dirpath, dirnames, filenames) in walk("html"):
    files.extend(filenames)
    break

print("Analyzing these files: {}".format(files))
for file in files:
    print("\n")
    print("Working on {}".format(file))
    image = Image.open('html/{}_files/a.png'.format(file[:-5]), mode='r')
    print("Found email: {}".format(pytesseract.image_to_string(image)))

# ----------------------------------------------- #

    engine = Scraper(pytesseract.image_to_string(image), "html/{}".format(file))
    engine.Start()
    engine.Cleanup()
