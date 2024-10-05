
# Illusion Academy: AI-Powered Internal Corporate Training Software for Web 3 Companies

_Illusion Academy is designed to provide an all-in-one solution for Web 3 companies looking to streamline internal corporate training. The platform offers a suite of tools tailored for:_

- Recruitment Testing: Helping recruiters assess candidates during the interview process.
- Educational Resources: Delivering teachings, lectures, and computer-based testing (CBT).
- Internal Training: Allowing companies to conduct in-house training efficiently.

## Table of Contents

- Installation
- Usage
- API Endpoints
- Technologies Used
- Contributing
- License

## Installation

For the installation of the project:

1. Clone the project directory from:  
   `git clone https://github.com/The-Illusion-services/illusion-BE.git`
   
2. Navigate to the project directory in your local machine  
   `cd your_repo_name`
   
3. Create a virtual environment and activate it:  
   `python -m venv venv`  
   `source venv/bin/activate`  # On Windows use `venv\Scripts\activate` to activate the virtual environment
   
4. Install the required packages from `requirements.txt`:  
   `pip install -r requirements.txt`
   
5. Set up the database by running:  
   `python manage.py migrate`

## Usage

For usage of the project, use the command  
`python manage.py runserver`

The APIs will be available at: [https://illusion-6ga5.onrender.com/docs/](https://illusion-6ga5.onrender.com/docs/)

## API Endpoints

### Assignments

- **POST** `/assignments/create/`: To create assignments by instructors  
- **POST** `/assignments/submit/{user_id}`: To submit assignments by candidates  
- **PUT** `/assignments/update/{id}/`: Full update of the assignment  
- **PATCH** `/assignments/update/{id}/`: Partial update of the assignment  

### Certifications

- **GET** `/certifications/`: List of certificates  
- **POST** `/certifications/create`: Create certificates  
- **GET** `/certifications/{id}`: Read individual certificate  

### Courses

- **GET** `/courses/`: List of courses  
- **POST** `/courses/enrol`: Create course enrolment  
- **GET** `/courses/{course_id}/assignments/`: Course assignment list  
- **GET** `/courses/{course_id}/enrollments/`: Course enrolment list  
- **POST** `/create-course/`: Create course  
- **POST** `/create-module/`: Create course modules  
- **GET** `/modules/`: List of modules  
- **PUT** `/update-module/{id}/`: Full update of modules  
- **PATCH** `/update-module/{id}/`: Partial update of modules  

### Google Signup

- **POST** `/google-signup/`: Signup using Google API  

### Profile

- **GET** `/profile/`: Profile list  
- **PATCH** `/profile/{id}`: Update profile  

### Lessons

- **GET** `/lessons/`: List of lessons  
- **PUT** `/lessons/progress/{id}/`: Lesson progress update  
- **PATCH** `/lessons/progress/{id}/`: Lesson progress partial update  

### Login

- **POST** `/login/`: Create login  
- **GET** `/protected/`: Protected list  

### Quizzes

- **GET** `/quizzes/`: List of quizzes  
- **POST** `/quizzes/create/`: Create quizzes  
- **POST** `/quizzes/submit/`: Submit quiz by candidates  
- **GET** `/quizzes/{id}/`: Read individual quiz  

### Register

- **POST** `/register/`: Create new user  

### Resources

- **GET** `/resources/`: List of resources  
- **POST** `/resources/create/`: Create resources  

## Technologies Used

- Python
- Django

## Contributing

We welcome contributions to improve **Illusion Academy**! As this project was initially developed during a hackathon, we're excited to see how it can grow with community input.

### Reporting Issues

If you encounter any bugs or have suggestions for improvements:

- Check the Issues page to see if it has already been reported.
- If not, open a new issue. Please provide:
  - A clear title and description
  - As much relevant information as possible
  - A code sample or an executable test case demonstrating the issue, if applicable

### Suggesting Enhancements

We're open to ideas! If you have suggestions for new features:

- Open a new issue on the Issues page.
- Use a clear and descriptive title.
- Provide a detailed description of the proposed feature.
- Explain why this enhancement would be useful to most users.

### Pull Requests

We actively welcome your pull requests:

- Fork the repo and create your branch from main.
- If you've added code that should be tested, add tests.
- If you've changed APIs, update the documentation.
- Ensure the test suite passes.
- Make sure your code lints.
- Issue that pull request!

### Coding Style

Please adhere to the coding style used throughout the project. In general:

- Follow PEP 8 for Python code.
- Use 4 spaces for indentation rather than tabs.
- Use docstrings for functions and classes.

## License

By contributing, you agree that your contributions will be licensed under the same license that covers this project (see LICENSE file).

## Questions?

If you have any questions about contributing, feel free to ask. We're here to help!  
Thank you for your interest in improving **Illusion Academy**!

## License

This project is licensed under the terms of the [LICENSE file].
