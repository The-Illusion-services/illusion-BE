<h3>Project Title:<strong>Illusion Academy: AI-Powered Internal Corporate Training Software for Web 3 Companies</strong></h3> 

<em>Illusion Academy is designed to provide an all-in-one solution for Web 3 companies looking to streamline internal corporate training. The platform offers a suite of tools tailored for:</em>
<ul>
<li>Recruitment Testing: Helping recruiters assess candidates during the interview process.</li>
<li>Educational Resources: Delivering teachings, lectures, and computer-based testing (CBT).</li>
<li>Internal Training: Allowing companies to conduct in-house training efficiently.</li>
</ul>

<h4>Table of Contents</h4>
<ul type="square">
<li>Installation</li>
<li>Usage</li>
<li>API Endpoints</li>
<li>Technologies Used</li>
<li>Contributing</li>
<li>License</li>
</ul>
<h3>Installation</h3>
For the installation of the project;
<ol>
<li>clone the project directory from:<br>
<em><strong>git clone https://github.com/The-Illusion-services/illusion-BE.git</strong></em>
 </li>
<li>Navigate to the project directory in your local machine <br>
<strong><em>cd your_repo_name</strong></em>
 </li>
<li>Create a virtual environment and activate it:<br>
<strong><em>python -m venv venv<br>
source venv/bin/activate  # On Windows use `venv\Scripts\activate` # to activate the virtual environment </strong></em>
 </li>
<li> install the require packages from requirements.txt<br>
<strong><em> pip install -r requirements.txt</strong></em>
 </li>
<li>set up the database by running:<br>
 <strong><em> python manage.py migrate</strong></em>
 </li>
</ol>
Usage
For usage of the project, use the command
<strong><em>python manage.py runserver</strong></em>

The APIs will be available at <a href="https://illusion-6ga5.onrender.com/docs/"> https://illusion-6ga5.onrender.com/docs/ </a>

API Endpoints
The follwoing are API Endpoints 

assignments 
POST /assignments/create/: To create assignments by instructors
POST /assignments/submit/{user_id}: To submite assignments by candidates
PUT /assignments/update/{id}/: full update of the assignment (put)
PATCH /assignments/update/{id}/: Partial update of the assignment(patch)

certifications
GET /certifications/: List of certificates
POST /certifications/create: Create certificates
GET /certifications/{id}: read individual certificate

courses
GET /courses/: List of courses
POST /courses/enrol: create course enrolment
GET /courses/{course_id}/assignments/: course assignment list
GET /courses/{course_id}/enrollments/: course enrolment list
POST /create-course/: create course 
POST /create-module/: create course modules
GET /modules/: list of modules
PUT /update-module/{id}/: update full detail modules(put)
PATCH /update-module/{id}/: update partial details modules(patch)


google-signup
POST /google-signup/: signup using google api

lessons
GET /lessons/: list of lessons
PUT /lessons/progress/{id}/: lesson progress update(put)
PATCH /lessons/progress/{id}/: lesson progress partial update(patch)

login
POST /login/: create login
GET /protected/: protected list

quizzes
GET /quizzes/: list of quizzes
POST /quizzes/create/: create quizzes
POST /quizzes/submit/: submit quiz by candidates
GET /quizzes/{id}/: read individual quiz

register
POST /register/: create new user

resources
GET /resources/: list of resources
POST /resources/create/: create resources

Technologies Used
sgiref
certifi
charset-normalizer
coreapi
coreschema
Django
django-rest-framework
django-rest-swagger
djangorestframework
djangorestframework-simplejwt
django-cors-headers
python-decouple
django-cors-headers
python-decouple
drf-yasg
idna
inflection
itypes
Jinja2
MarkupSafe
openapi-codec
packaging
pillow
psycopg
psycopg2
PyJWT
gunicorn
python-dotenv
pytz
PyYAML
requests
simplejson
sqlparse
typing_extensions
tzdata
uritemplate
urllib3

Contributing


License
