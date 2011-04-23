#!/usr/bin/env python
# -*- coding: utf-8 -*-


import cgi
import cgitb
import os
import time

#from time import gmtime, strftime

cgitb.enable()


def printform():
    prefilldict = {}
    prefilldict["IPaddresse"] = cgi.escape(os.environ["REMOTE_ADDR"])
    prefilldict["Useragent"] =  cgi.escape(os.environ["HTTP_USER_AGENT"])
    prefilldict["thetime"] = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())


    print """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="de">
<head>
<title>TroLUG Anmeldung</title>
<meta name="author" content="Jonas Stein" />
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
</head>

<body>
<form action="anmeldung.py" method="post">
<pre>
Rufname (z.B. Marie): <input type="text" name="tlfrufname" size="40" /> 
Der Rufname wird in der Liste der Anmeldungen öffentlich angezeigt.

Name (z.B. Curie): <input type="text" name="tlfname" size="40" /> 
keine Phantasienamen.


<input type="radio" name="tlfskill" value="0"> Ich möchte mich für den Termin abmelden 

Ich möchte mich für den Termin anmelden und meine Vorkenntnisse zum angekündigten Thema sind
    <input type="radio" name="tlfskill" value="1" checked> keine 
    <input type="radio" name="tlfskill" value="2"> ein grober Überblick 
    <input type="radio" name="tlfskill" value="3"> sehr tiefgehend


Mailadresse:  <input type="text" name="tlfcomment" size="40" /> 
(wenn eingetragen wird eine Bestätigungsmail gesendet)

Anmerkung:    <input type="text" name="tlfcomment" size="40" /> 

Ihre IP:      <input type="text" name="tlfshowip" value="%(IPaddresse)s" readonly size="15">
Datum (GMT):  <input type="text" name="tlfshowthetime" value="%(thetime)s" readonly size="40">
Browser:      <input type="text" name="tlfshowbrowser" value="%(Useragent)s" readonly size="40">


Es werden nur die hier sichtbaren Daten auf dem Webserver gespeichert.
Nach dem Absenden erscheint nochmal eine Zusammenfassung.

Spamschutz: Wieviel ist 3+1 ...

         <input type="submit" value="Anmelden" />

</pre>
</form>
</body>
</html>
""" %(prefilldict)


def dataisok(form):
    """checks if all data is entered in the right syntax"""
    if "tlfshowip" not in form:
        return False
    else: 
        return True


def printsaveddata(datadict):
    print """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="de">
<head>
<title>TroLUG Anmeldung</title>
<meta name="author" content="Jonas Stein" />
<meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
</head>

<body>

<h3>Herzlich willkommen %(tlfname)s!</h3>
Die Anmeldung war erfolgreich.

</body>
</html>
"""%(datadict)




if __name__ == '__main__':

    form = cgi.FieldStorage()

    datadict={}
    for value in ("tlfname","tlfcomment"):
        datadict[value] = form.getvalue(value)


    print 'Content-type: text/html\n\n'


    if dataisok(form)==False:
        printform()
    else:
        printsaveddata(datadict)


    
  
