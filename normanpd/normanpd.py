import sqlite3
import urllib.request
from bs4 import BeautifulSoup
import re
import os
import PyPDF2
from random import *

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
            newpath = os.getcwd() + "/normanpdPDFs"
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            f = open(newpath + "/" + test.group() + ".pdf", "wb")
            f.write(current.read())
            f.close()


# This goes through all of the pdf files in the folder
# And extracts the data for each incident in a list.
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

    for filenames in os.listdir(os.getcwd() + "/normanpdPDFs"):
        inc = getPDFContent(os.getcwd() + "/normanpdPDFs/" + filenames)
        inc = inc[1:]
        incidents.extend(inc)
    incidents = [incidents[x:x+5] for x in range(0, len(incidents), 5)]

    for i in range(len(incidents)):
        incidents[i].extend([i+1])

    return incidents


# creates the normanpd database
def createdb():
    # creates a connection to a db called normanpd
    # if the db isn't already created it will create a new one.
    conn = sqlite3.connect('normanpd.db')
    conn.execute('''CREATE TABLE incidents
    (date_time TEXT, number TEXT, location TEXT, nature TEXT, ori TEXT, id INTEGER)''')
    conn.close()


# Take the incidents from the list and add them to the database
def populatedb(incidents):
    conn = sqlite3.connect('normanpd.db')
    try:
        conn.executemany('''INSERT INTO incidents VALUES (?, ?, ?, ?, ?, ?)''', incidents)
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error")
    conn.close()


# Print out the number of rows in the db
def status(incidents):
    conn = sqlite3.connect('normanpd.db').cursor()
    conn.execute('SELECT COUNT(*) from incidents')
    count = conn.fetchone()
    print(count[0])
    for i in range(5):
        j = randint(1, len(incidents))
        conn.execute('''SELECT * from incidents WHERE id = ?''', (j,))
        rands = conn.fetchall()
        print(rands)





