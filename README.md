# Blaster
Web application for improved BLAST local DNA sequence alignment.
This is my first web application created with using python3 and Django framework. It combines simple blog/forum and integrated 
script for massive DNA sequence alignment (was part of my diploma work in biotech:) with using NCBI BLAST+ algorithms in it. It allows
to compare many vs many sequences and outputting analysis results into .xlsx spreadsheet for better data visualization. Script allows
user to choose cut-off and sortning results parameters in simple user interface in Django web app.
## Some features of Blaster web app:
  * Ready to use: https://blaster-inf.tk/blaster/About/
  * Deployed to digitalocean droplet (Ubuntu 18.04) with PostgreSQL database
  * Added API which inherits all functionality available in front end
  * Common design with using Bootstrap 4
  * User registration with confirmation via email (unique one-time use link)
  * Oauth2.0 user registration/login with facebook and google (connect/disconnect)
  * Simple user profile with editing possibility
  * Questions/answers section with possibility to comment, edit, delete
  * Custom form validation, user image/file input validation (size, extension, mime type)
  * Created mostly with using mixed class based views
  * User permissions (editing, deleting, seeing) validation
  * Customized pagination
  * Custom middleware

## API endpoints:
>#### User management:
  * https://blaster-inf.tk/blaster-api/users/crud/  -- (GET --> get list of users, POST --> create user (password double check), sends verification email, )
  * https://blaster-inf.tk/blaster-api/users/crud/**user_id**/ -- (GET --> get user, PUT/PATCH/DELETE --> change user data (password double check, authentication needed)
  * https://blaster-inf.tk/blaster-api/users/token-auth/ -- obtain authentication token, username and passwors is required
>#### BLAST analysis:
  * https://blaster-inf.tk/blaster-api/tool/io/  -- (POST method is allowed only, accepts sequences, analysis set of parameters)
>#### Questions and answers:
  * https://blaster-inf.tk/blaster-api/questions/  -- (GET --> questions list, POST(if authenticated) --> add question)
  * https://blaster-inf.tk/blaster-api/questions/**id**/  -- (GET --> get question, PUT/PATCH/DELETE(if authenticated) --> change question, delete)
  * https://blaster-inf.tk/blaster-api/questions/**id**/comments  -- (GET --> get question comments, POST(if authenticated) --> add comment)
  * https://blaster-inf.tk/blaster-api/questions/**id**/comments/**comment_id**/  -- (GET --> get question comment, PUT/DELETE(if authenticated) --> change comment, delete)
## Packages used in this project:
  * Widget tweaks, Biopython, Xlsxwriter, Pyunpack, Patool, Magic, Django REST Framework, Django allauth.
 
  
