import sqlite3
import urllib.request
from bs4 import BeautifulSoup
import re
import os
import PyPDF2

#this will fetch the pdfs from the URL
def fetchincidents():
    req = urllib.request.urlopen('http://normanpd.normanok.gov/content/daily-activity')
    inc = req.read()
    inc.decode('utf-8')
    soup = BeautifulSoup(inc, "html.parser")
    for tag in soup.findAll('a', href=True):
        pdfs = str(tag)
        match = re.compile(r'\d{4}-\d{2}-\d{2}\sDaily Incident')
        test = match.search(pdfs)
        if ".pdf" in pdfs and test:
            print(True)
            print(tag)
            current = urllib.request.urlopen('http://normanpd.normanok.gov/' + tag['href'])
            newpath = "normanpdPDFs"
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            f = open(newpath + "/" + test.group() + ".pdf", "wb")
            f.write(current.read())
            f.close()


def extractincidents():
    incidents = []
    def getPDFContent(path):
        content = ""
        pdf = PyPDF2.PdfFileReader(open(path, "rb"))
        for i in range(pdf.getNumPages()):
            content += pdf.getPage(i).extractText()
        content = " ".join(content.replace("\xa0", " ").strip().split())
        exp = r'(\d{1,2}/\d{1,2}/\d{4}\s\d{1,2}:\d{1,2})\s(\d{4}-\d{8})\s(.+?(?=\s[A-Z][a-z]{1,9}))\s(.+?(?=OK\d+|\d+))'
        l = re.compile(exp).split(content)
        return l
    for filenames in os.listdir("./normanpdPDFs"):
        inc = getPDFContent("./normanpdPDFs/" + filenames)
        inc = inc[1:]
        incidents.extend(inc)
    incidents = [incidents[x:x+5] for x in range(0, len(incidents), 5)]
    print(incidents)
# creates the normanpd database
def createdb():
    # creates a connection to a db called normanpd
    # if the db isn't already created it will create a new one.
    conn = sqlite3.connect('normanpd.db')
    conn.execute('''CREATE TABLE incidents
    (id INTEGER, number TEXT, data_time TEXT, location TEXT, nature TEXT, ORI TEXT)''')



extractincidents()
