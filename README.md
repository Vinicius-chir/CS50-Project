# Agenda
#### Video Demo:  <https://www.youtube.com/watch?v=Ytu5s19VUl4>
#### Description:

app.py:
    The appy.py file is the core of a Flask-based web application designed to function as a task management system. It allows users to register, log in, create tasks, mark tasks as completed,
view their task history, and log out. The application is built with a focus on user authentication, task organization, and secure session management.
Below is a detailed explanation of what the code does:
    The application starts by importing necessary libraries and modules, such as Flask for the web framework, SQL from the cs50 library for database interactions,and werkzeug.security
for password hashing and verification. The Flask application is initialized with app = Flask(__name__), and session management is configured to use the filesystem for storing session data.
This ensures that user sessions are maintained securely across requests. The database is set up to use SQLite3, with the connection established via db = SQL("sqlite:///project.db").
    The index route is the main page of the application, accessible only to logged-in users (enforced by the @login_required decorator). When a user accesses this route via a GET request, the
application retrieves all tasks associated with the user from the database, sorted by deadline, and renders them in the menu.html template. If the user submits a form via a POST request
(e.g., to delete or complete a task), the application processes the request. If the "delete" button is clicked, the task is removed from the database. If the "approve" button is clicked, the
task is marked as completed by moving it to the history table, and the current date is recorded as the completion date. The updated list of tasks is then rendered in the template.
    The register route allows new users to create an account. When accessed via a GET request, it renders the register.html template, which contains a registration form. When the form is
submitted via a POST request, the application validates the input. It ensures that the username, password, and confirmation fields are provided and that the password matches the confirmation. It also checks if the username is already taken by querying the database. If all validations pass, the password is hashed for security, and the new user is inserted into the users table. The user is
then automatically logged in by setting their user_id in the session, and they are redirected to the index page.
    The login route allows existing users to log in. When accessed via a GET request, it renders the login.html template, which contains a login form. When the form is submitted via a POST
request, the application validates the input. It ensures that both the username and password are provided. It then queries the database to check if the username exists and verifies the password
using check_password_hash. If the credentials are valid, the user is logged in by setting their user_id in the session, and they are redirected to the index page. If the credentials are
invalid, an error message is displayed.
    The logout route clears the user's session, effectively logging them out. It then redirects the user to the login page, ensuring they cannot access protected routes without re-authenticating.
    The add task route allows logged-in users to create new tasks. When accessed via a GET request, it renders the add.html template, which contains a form for entering task details.
When the form is submitted via a POST request, the application validates the input. It ensures that both the task title and deadline are provided. The task is then inserted into the
tasks table, along with the current date as the creation date. The user is redirected to the index page to view their updated task list.
    The history route allows logged-in users to view their completed tasks. When accessed via a GET request, it retrieves all tasks from the history table associated with the user,
sorted by completion date in descending order, and renders them in the history.html template. If the user submits a form via a POST request
the specified history entry is removed from the database, and the updated list of completed tasks is rendered in the template.

helper.py:
This file provides two key utilities for the Flask app:
login_required: A decorator that ensures only logged-in users can access specific routes by checking the session for user_id.
error: A function that renders an error template with a custom message and status code for error handling.

project.db:
The database consists of three tables:
users: Stores user data (user_id, USERNAME, PASSWORD).
tasks: Stores tasks (task_id, user_id, TITLE, DESCRIPTION, DEADLINE, CREATED), linked to users.
history: Stores completed tasks (history_id, user_id, TITLE, DESCRIPTION, DEADLINE, FINISHED), also linked to users.

Templates(add.html, error.html, history.html, login.html, menu.html, register.html, tasks.html):
Its where I store the code of the html pages, being menu.html the main one.

Static (error.png, darkmode.js, style.css):
    This CSS file styles a web application, enabling dark mode with CSS variables, organizing layouts using Flexbox, and customizing tables, buttons, and spacing. It includes a theme
switch button with dynamic icon visibility and ensures responsive, visually consistent design across the app.
    darkmode.js this code toggles dark mode on a webpage. It checks localStorage for a darkmode setting and applies it. Clicking the themeSwitch button enables or disables dark mode,
updating the body class and localStorage accordingly.
    error.png is the image that its displayed when something went wrong.
