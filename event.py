#!/usr/bin/python2.6
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

def htmleventlink(eventid):
    """returns a string with html code for a ical download-link to event id
    """
    
    return """<a href=event.py?geticalendar=%s>
<img src="calendar.png" alt="Termin im iCalendar Format"> 
</a>""" % eventid
    
    


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




def showcalendartable():

    config = ConfigParser.ConfigParser()
    config.read('trolug.cfg')

    conn = MySQLdb.connect (host = config.get('mysql','host'),
                            user = config.get('mysql','user'), 
                            passwd = config.get('mysql','passwd'),
                            db = config.get('mysql','db'))
    cursor = conn.cursor ()
#    cursor.execute ("SELECT VERSION()")
#    row = cursor.fetchone ()
    
    printhead()
    print("""
<h1> Termine der TroLUG </h1>

""")

# eventid 	anfangszeit 	schlusszeit 	anmeldeschluss 	thema 	maxreg 	link 	tutor
# organisation 	kategorie 	anforderungen 	isanmeldungnotwendig 	issondertermin

    cursor.execute("""SELECT * 
FROM `event` 
WHERE `anfangszeit` > '1998-01-02 21:30:08'
ORDER BY `anfangszeit` ASC
LIMIT 0 , 30 
""")

    eventlist = cursor.fetchall() 
    starttable()

    print("""
<th> .ics </th>
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
        print("""<td> %s </td>""") % htmleventlink(dbantwort['eventid'])
        print("""
<td> %(anfangszeit)s </td>
<td> <a href="%(link)s">%(thema)s </a></td>
<td> %(tutor)s (%(organisation)s) </td>
<td> %(kategorie)s </td>
""")  % dict(dbantwort)

        print("</td>")
        print("</tr>")

    endtable()
    print("""<h4> Legende </h4>
<img src="calendar.png" alt="Termin im iCalendar Format"> 
Termin im iCalendar Format herunterladen

<h4>Nächste Schritte</h4>
<ul> 
<li>Umlautproblem eliminieren </li>
<li>Sinnvolle Daten eingeben </li>
<li>.css ansehnlich gestalten </li>
<li>Anmeldeformular verlinken </li>
<li>Anmeldung: Initialen auflisten </li>
<li>Mail als Hash speichern </li>
</ul> 

""")
    endbody()

    cursor.close ()
    conn.close ()


def generatevcard(eventid):
    print("""Content-type: text/calendar
Content-Disposition: attachment; filename=trolug.ics
""")

    print("""
BEGIN:VCALENDAR
VERSION:2.0
PRODID:http://www.example.com/calendarapplication/
METHOD:PUBLISH
BEGIN:VEVENT
UID:%s@example.com
ORGANIZER;CN="Jonas Stein, TroLUG":MAILTO:news@jonasstein.de
SUMMARY:TroLUG Treffen
DESCRIPTION:Workshop zu Opensource
CLASS:PUBLIC
DTSTART:20001230T190000Z
DTEND:20001230T210000Z
DTSTAMP:20001230T190000Z
END:VEVENT
END:VCALENDAR
""") % eventid



def main():
    form = cgi.FieldStorage()
#    if "name" not in form or "addr" not in form:
    if "geticalendar" in form:
        generatevcard(form["geticalendar"].value)
    else: 
        showcalendartable()



# TODO: liste muss anderes FORMAT bekommen
if __name__ == '__main__':
    main()

 
