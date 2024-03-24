Welcome to the Blogly Project!

To run the Blogly project on your local machine, follow these steps:

1. Clone the repository:
   git clone [repository_url]
   
2. Navigate to the project directory:
   cd Blogly
   
3. Create and activate a virtual environment:
   python3 -m venv venv
   source venv/bin/activate (for Unix/Mac)
   venv\Scripts\activate (for Windows)
   
4. Install dependencies:
   pip install -r requirements.txt
   
5. Set up the database:
   python -i model.py
   >>> db.create_all()

6. Run the Flask application:
   python app.py
   
7. Open your web browser and visit http://localhost:5000/ to access the platform.

That's it! You're now ready to explore and interact with the Blogly project.
