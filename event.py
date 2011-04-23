#!/usr/bin/python2.5
# -*- coding: utf-8 -*-

"""USAGE: 
"""

__version__ = 0.03
__author__ = "Jonas Stein"




import MySQLdb
# import sys
# import time
import cgi
import cgitb
import ConfigParser

cgitb.enable()


def printhead():
    print """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="de">
<head>
<title>TroLUG Anmeldung</title>
<meta name="author" content="Jonas Stein" />
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<link rel="stylesheet" media="screen" type="text/css" href="event.css" />
</head>
"""


def starttable():
    print """
<table border="1" class="inline">
"""

def endtable():
    print """
</table>
"""

def startbody():
    print """
<body>
<!-- start dokuwiki block -->
<div class="dokuwiki">
"""

def endbody():
    print """

</div>
<!-- end dokuwiki block -->

</body>
</html>
"""




def main():

    config = ConfigParser.ConfigParser()
    config.read('trolug.cfg')

    conn = MySQLdb.connect (host = config.get('mysql','host'),
                            user = config.get('mysql','user'), 
                            passwd = config.get('mysql','passwd'),
                            db = config.get('mysql','db'))
    cursor = conn.cursor ()
    cursor.execute ("SELECT VERSION()")
    row = cursor.fetchone ()
    
    printhead()
    print("""
<h1> Termine der TroLUG </h1>

""")

#     	maxreg 	link 	tutor 	organisation 	kategorie 	anforderungen 	isanmeldungnotwendig 	issondertermin
    sqlabfrage =("""
SELECT * 
FROM `event` 
WHERE `anfangszeit` > '1998-01-02 21:30:08'
ORDER BY `anfangszeit` ASC
LIMIT 0 , 30 
""")

    cursor.execute(sqlabfrage)
    eventlist = cursor.fetchall() 
    starttable()

    print("""
<th> Datum </th>
<th> Thema </th>
<th> Dozent </th>
<th> Anmeldung </th>
""")

# Hole jetzt die Spaltennamen
    Spaltennamen = [ ]
    for Spalte in cursor.description:
        Spaltennamen.append(Spalte[0])
    
    for event in eventlist:
        # Erzeuge ein dictionary der Form Spaltenname:Wert fuer jede Datenzeile
        dbantwort = dict(zip(Spaltennamen,event))

        print("<tr>")
        print("""
<td> %(anfangszeit)s </td>
<td> <a href="%(link)s">%(thema)s </a></td>
<td> %(tutor)s (%(organisation)s) </td>
<td> %(kategorie)s </td>
""")  % dict(dbantwort)


        print("</td>")

        print("</tr>")

    endtable()


    endbody()


    cursor.close ()
    conn.close ()



# TODO: liste muss anderes FORMAT bekommen
if __name__ == '__main__':
    main()
