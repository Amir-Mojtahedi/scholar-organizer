# ScholarOrganizer
https://gitlab.com/serhiyfed/scholar-organizer

## Live Demo
[http://10.172.13.162:8000/](http://10.172.13.162:8000/)

## Contributors
- Serhiy Fedurtsya (2135229)
- Mohamed Loutfi (2141950)
- Amirreza Mojtahedi (2133044)

## Development
1. Install Python 3.7 or greater.
2. Setup and activate your virtual envinronment.
3. Install requirements using `pip install -r requirements.txt`
4. Set DBUSER and set DBPWD environment variables for the PDBORA19C database
5. Setup the database by running the `setup.sql` script.
6. Run the flask app for debugging using `flask --app CoursePlannerApp --debug run`

## Deployment
1. Install Python 3.7 or greater.
2. Setup and activate your virtual envinronment.
3. Install requirements using `pip install -r requirements.txt`
4. Set DBUSER and set DBPWD environment variables for the PDBORA19C database
5. Setup the database by running the `setup.sql` script.
6. Allow the port desired through your firewall.
7. Run the command `gunicorn -w 2 -b 0.0.0.0:8000 'CoursePlannerApp:create_app()'`