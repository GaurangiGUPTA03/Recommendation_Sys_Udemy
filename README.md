-----------------------------------------📚 Course Recommendation System---------------------------------------------------------------------
An interactive web app to explore, recommend, and manage online courses using Streamlit, Pandas, and Scikit-learn. Designed for both users and admins with an intuitive interface.


🚀 Features
1) 🏠 Home

Preview the dataset with course title, subject, level, price, and number of subscribers.

2) 🎯 Course Recommender

Find similar courses using content-based filtering (title, subject, level, and description).

Filter by subject and difficulty level.

3) 📊 Dashboard (Admin & User)

Admin view: Visualize top-selling subjects, enrollment stats, and pricing trends.

User view: See course distribution and access analytics for informed decisions.

4) 🎨 Styled Interface

Enhanced visuals using custom HTML/CSS inside Streamlit.

-------------------------------💻 How to Run This Project---------------------------------------------------------------

-> Run Locally with Git

1. Clone the Repository
git clone https://github.com/your-username/course-recommender-app.git
cd course-recommender-app

2. Create a Virtual Environment
python -m venv venv
3. Activate the Virtual Environment
On Windows:
venv\Scripts\activate
On macOS/Linux:
source venv/bin/activate

4. Install Dependencies
pip install -r requirements.txt

5. Run the Application
python -m streamlit run data/app.py 

Then open the URL shown in your terminal (usually http://localhost:8501) in a browser.