Movie Review and Ranking Website
Welcome to the GitHub repository for the Movie Review and Ranking Website! This application provides a platform for movie enthusiasts to add, rate, review, and view a ranked list of movies based on user ratings.

Features
User Submissions: Users can submit movies they've watched, along with ratings and reviews.
Dynamic Movie Ranking: Movies are displayed in a ranking order, dynamically adjusted based on user ratings.
Interactive User Interface: Users can interact with the system through various operations like adding, editing, and reviewing movies.
Technology Stack
Python & Flask: The backend is built with Flask, a micro web framework written in Python.
HTML/CSS/JavaScript: Frontend development to create an engaging user interface.
SQLite: Lightweight database for storing and managing movie data.
Project Structure
main.py: The Flask application's main entry point. It includes route definitions and the core app setup.
requirements.txt: Lists all the Python dependencies required for the project.
templates/: Contains HTML files for rendering the web pages.
add.html: The form for adding new movies.
edit.html: Interface for editing movie details.
index.html: The main page displaying the ranked list of movies.
select.html: Page for selecting a movie to view or edit.
base.html: Base template that other templates extend.
static/: Directory for static files.
styles.css: Custom CSS for styling the website.
instance/: Contains the SQLite database file.
Code Design
The application is designed with a clear separation of concerns in mind:

Backend Logic: Handled by main.py, it includes Flask route definitions and interactions with the database.
Data Persistence: Managed by SQLite, providing a lightweight solution for data storage.
Frontend Presentation: HTML templates in the templates/ directory with accompanying CSS in the static/ directory ensure a user-friendly interface.
Modular Design: HTML templates use inheritance for a consistent and easily maintainable structure.

License
This project is open-source, available under the MIT License.

Contact
For more information or questions, feel free to open an issue on this repository.

