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
<h3>Usage</h3>
For usage of the project, use the command<br>
<strong><em>python manage.py runserver</strong></em>

The APIs will be available at <a href="https://illusion-6ga5.onrender.com/docs/"> https://illusion-6ga5.onrender.com/docs/ </a>

<h3>API Endpoints</h3>
The follwoing are API Endpoints<br>

<h4>assignments</h4>
<strong><em>POST /assignments/create/: To create assignments by instructors</em></strong><br>
P<strong><em>OST /assignments/submit/{user_id}: To submite assignments by candidates</em></strong><br>
<strong><em>PUT /assignments/update/{id}/: full update of the assignment (put)</em></strong><br>
<strong><em>PATCH /assignments/update/{id}/: Partial update of the assignment(patch)</em></strong><br>

<h4>certifications</h4>
<strong><em>GET /certifications/: List of certificates</em></strong><br>
<strong><em>POST /certifications/create: Create certificates</em></strong><br>
<strong><em>GET /certifications/{id}: read individual certificate</em></strong><br>

<h4>courses</h4>
<strong><em>GET /courses/: List of courses</em></strong><br>
<strong><em>POST /courses/enrol: create course enrolment</em></strong><br>
<strong><em>GET /courses/{course_id}/assignments/: course assignment list</em></strong><br>
<strong><em>GET /courses/{course_id}/enrollments/: course enrolment list</em></strong><br>
<strong><em>POST /create-course/: create course </em></strong><br>
<strong><em>POST /create-module/: create course modules</em></strong><br>
<strong><em>GET /modules/: list of modules</em></strong><br>
<strong><em>PUT /update-module/{id}/: update full detail modules(put)</em></strong><br>
<strong><em>PATCH /update-module/{id}/: update partial details modules(patch)</em></strong><br>


<h4>google-signup</h4>
<strong><em>POST /google-signup/: signup using google api</em></strong><br>

<h4>profile</h4>
<strong><em>GET /profile/: profile list</em></strong><br>
<strong><em>PATCH /profile/{id}: profile list</em></strong><br>

<h4>lessons</h4>
<strong><em>GET /lessons/: list of lessons</em></strong><br>
<strong><em>PUT /lessons/progress/{id}/: lesson progress update(put)</em></strong><br>
<strong><em>PATCH /lessons/progress/{id}/: lesson progress partial update(patch)</em></strong><br>

<h4>login</h4>
<strong><em>POST /login/: create login</em></strong><br>
<strong><em>GET /protected/: protected list</em></strong><br>

<h4>quizzes</h4>
<strong><em>GET /quizzes/: list of quizzes</em></strong><br>
<strong><em>POST /quizzes/create/: create quizzes</em></strong><br>
<strong><em>POST /quizzes/submit/: submit quiz by candidates</em></strong><br>
<strong><em>GET /quizzes/{id}/: read individual quiz</em></strong><br>

<h4>register</h4>
<strong><em>POST /register/: create new user</em></strong><br>

<h4>resources</h4>
<strong><em>GET /resources/: list of resources</em></strong><br>
<strong><em>POST /resources/create/: create resources</em></strong><br>

<h3>Technologies Used</h3>
<ul type="square">
<li>sgiref</li>
<li>certifi</li>
<li>charset-normalizer</li>
<li>coreapi</li>
<li>coreschema</li>
<li>Django</li>
<li>django-rest-framework</li>
<li>django-rest-swagger</li>
<li>djangorestframework</li>
<li>djangorestframework-simplejwt</li>
<li>django-cors-headers</li>
<li>python-decouple</li>
<li>django-cors-headers</li>
<li>python-decouple</li>
<li>drf-yasg</li>
<li>idna</li>
<li>inflection</li>
<li>itypes</li>
<li>Jinja2</li>
<li>MarkupSafe</li>
<li>openapi-codec</li>
<li>packaging</li>
<li>pillow</li>
<li>psycopg</li>
<li>psycopg2</li>
<li>PyJWT</li>
<li>gunicorn</li>
<li>python-dotenv</li>
<li>pytz</li>
<li>PyYAML</li>
<li>requests</li>
<li>simplejson</li>
<li>sqlparse</li>
<li>typing_extensions</li>
<li>tzdata</li>
<li>uritemplate</li>
<li>urllib3</li>
</ul>
<h3>Contributing</h3>
<p>
We welcome contributions to improve <strong>Illusion Academy</strong>! As this project was initially developed during a hackathon, we're excited to see how it can grow with community input. Here's how you can contribute:
 </p>
<h3>Reporting Issues</h3>
If you encounter any bugs or have suggestions for improvements:<br>

Check the Issues page to see if it has already been reported.<br>
If not, open a new issue. Please provide:<br>
<ul>
<li>A clear title and description</li>
<li>As much relevant information as possible</li>
<li>A code sample or an executable test case demonstrating the issue, if applicable</li>
</ul>

<h3>Suggesting Enhancements</h3>
We're open to ideas! If you have suggestions for new features:
<ul type="arrow">
<li> Open a new issue on the Issues page.</li>
<li>Use a clear and descriptive title.</li>
<li>Provide a detailed description of the proposed feature.</li>
<li>Explain why this enhancement would be useful to most users.</li>
</ul>

<h3>Pull Requests</h3>
We actively welcome your pull requests:
<p>
Fork the repo and create your branch from main.
If you've added code that should be tested, add tests.
If you've changed APIs, update the documentation.
Ensure the test suite passes.
Make sure your code lints.
Issue that pull request!
</p>
<h4>Coding Style</h4>
Please adhere to the coding style used throughout the project. In general:
<ul type="square">
<li>Follow PEP 8 for Python code.</li>
<li>Use 4 spaces for indentation rather than tabs.</li>
<li>Use docstrings for functions and classes.</li>
</ul>
<strong>License</strong>:
By contributing, you agree that your contributions will be licensed under the same license that covers this project (see LICENSE file).

<h5>Questions?</h5>
If you have any questions about contributing, feel free to ask. We're here to help!
Thank you for your interest in improving  <strong>Illusion Academy</strong>!!
<h3>License</h3>