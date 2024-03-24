Getting Started
To get started with Blogly, follow these steps:

Clone the repository:

bash
Copy code
git clone https://github.com/pattherogue/One-to-Many---Blogly.git
Navigate to the project directory:

bash
Copy code
cd One-to-Many---Blogly
Create and activate a virtual environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # for Unix/Mac
venv\Scripts\activate  # for Windows
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up the database:

bash
Copy code
python -i model.py
>>> db.create_all()
Run the Flask application:

bash
Copy code
python app.py
Open your web browser and visit http://localhost:5000/ to access the platform.

That's it! You're now ready to explore and interact with the Blogly project.
