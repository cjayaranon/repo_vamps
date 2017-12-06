This is a Django powered website developed on a Python virtual environment. When deploying please proceed according to your machine specifications.

Linux/Ubuntu
[note] Your machine must have pip installed first.
		Run steps 7 to 13 for first instance of usage of this system.
1. Open terminal
2. Go to the directory containing the folder 'bin'
3. Run 'activate'
4. Go to the directory where 'requirements.txt' is located
5. Run 'pip install -r requirements.txt'
6. Go to the directory containing 'manage.py'
7. Run 'python manage.py makemigrations Users'
8. Run 'python manage.py migrate Users'
9. Run 'python manage.py createsuperuser' and input the necessary information.
10. Run 'python manage.py makemigrations clients'
11. Run 'python manage.py migrate clients'
12. Run 'python manage.py makemigrations'
13. Run 'python manage.py migrate' to migrate the models as a whole
14. Run 'python manage.py runserver <IP Address>:<port>
15. Open browser and type the <IP Address>:<port>

Windows
[note] Your machine must have Python 2 installed first. This will also install pip.
1. Open command line
2. Go to the directory containing the folder 'bin'
3. Run 'activate'
4. Go to the directory where 'requirements.txt' is located
5. Run 'pip install -r requirements.txt'
6. Go to the directory containing 'manage.py'
7. Run 'python manage.py makemigrations Users'
8. Run 'python manage.py migrate Users'
9. Run 'python manage.py createsuperuser' and input the necessary information.
10. Run 'python manage.py makemigrations clients'
11. Run 'python manage.py migrate clients'
12. Run 'python manage.py makemigrations'
13. Run 'python manage.py migrate' to migrate the models as a whole
14. Run 'python manage.py runserver <IP Address>:<port>
15. Open browser and type the <IP Address>:<port>

For the documentation files go to:
a. System user manual go to https://drive.google.com/open?id=1F_Y_xkom5ceYfvelP0C9kdJXG0zZ6BWi
b. Systems Analysis Document go to https://drive.google.com/open?id=0BykxFqwrA7BBMTZzVDhUNHhqM00
