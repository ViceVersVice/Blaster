# Blaster
Web application for improved BLAST local sequence alignment
This is my first web application created with using python3 and Django framework. It combines in it blog/forum and integrated 
script for massive DNA sequence alignment (was part of my diploma work in biotech:) with using NCBI BLAST+ algorithms. It allows
to compare many vs many sequences and outputting analysis results into .xlsx spreadsheet for better data visualization. Script allows
user to choose cut-off and sortning results parameters in simple user interface in Django web app.
## Some features of Blaster web app:
  * Ready to use: http://blaster-inf.tk/blaster/About/
  * Deployed to digitalocean droplet (Ubuntu 18.04) with PostgreSQL database
  * Common design with using Bootstrap 4
  * User registration with enfirmation via email (unique one-time use link)
  * Simple user profile with editing possibility
  * Questions/answers section with possibility to comment, edit, delete
  * Custom form validation, user image/file input validation (size, extension, mime type)
  * Created mostly with using mixed class based views
  * User permissions (editing, deleting, seeing) validation
  * Customized pagination
  * Custom middleware
## Other packages used in this project:
  * Widget tweaks, Biopython, Xlsxwriter, Pyunpack, Patool, Magic, Git.
