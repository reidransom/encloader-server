Goal
====

The goal of this project is to create a web app that will allow computers 
(primarily) on the local network to encode and upload videos for the 
web.

The main problem this project aims to fix is the situation where you have
multiple content producers or editors needing to push video to the same place 
or places.  For example a post production company may have multiple Avid or 
Final Cut editors posting video to the same website for review and approval.  
Rather than configuring export settings for each editing application, 
installing FTP software, configuring FTP shortcuts, giving out passwords,
and training people on this process (not to mention how slow these applications
can be at exporting video for the web), you could have them export same as
source Quicktimes or Quicktime references and send them a link to a page where
they can upload the video and let Encloader take care of the rest.

This project should have similar functionality as Apple Compressor except that 
the user interface should be *much* simpler because the user should only see
presets which have been created by an Administrator type person.

Requirements
============

* Python 2.5+ - http://python.org/ (2.5 requires simplejson)
* Bottle - http://bottle.paws.de/
* Paste - http://pythonpaste.org/ *Recommended*
* HandbrakeCLI - http://handbrake.fr/downloads2.php

Install
=======

Assuming you have Python 2.5+, Bottle and Paste installed, download
HandbrakeCLI and place the binary in the encloader/handbrake folder.  Then cd
into the handbrake folder and run::

    python encloadd.py

Then visit http://localhost:8000/ in your web browser to start encloading!
