

import streamlit as st

# Must come before any other Streamlit command!
st.set_page_config(page_title="Course Recommender", layout="wide")

import pandas as pd
import os
import base64

from chatbot import ChatBot
from Home import load_home_tab
from Recommend import load_recommend_tab
from AdminDashboard import load_admin_dashboard
from userDashboard import load_user_dashboard
  # Ensure this function exists

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/udemy_courses.csv")
    required_cols = ['course_title', 'subject', 'level']
    optional_cols = ['course_description']

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in dataset.")

    df = df.dropna(subset=required_cols)

    for col in optional_cols:
        if col not in df.columns:
            df[col] = ""
        else:
            df[col] = df[col].fillna("")

    df['image_url'] = df['course_title'].apply(
        lambda x: f"https://dummyimage.com/300x150/cccccc/000000.png&text={'+'.join(x.split()[:4])}"
    )
    return df


# Helper function to embed gif in sidebar
def get_base64_gif(gif_path):
    with open(gif_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode("utf-8")


def main():
    df = load_data()

    try:
        gif_path = os.path.join("data", "image", "udemy.gif")
        encoded_gif = get_base64_gif(gif_path)
        st.sidebar.markdown(
            f"<img src='data:image/gif;base64,{encoded_gif}' style='width:100%; margin-bottom: 1rem;'>",
            unsafe_allow_html=True
        )
    except Exception as e:
        st.sidebar.warning(f"Could not load GIF: {e}")

    menu = ["Home", "Recommend", "Chatbot", "Dashboard", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        load_home_tab(df)

    elif choice == "Recommend":
        load_recommend_tab(df)

    elif choice == "Chatbot":
        course_data = load_data()
        chatbot = ChatBot(course_data=course_data)
        chatbot.display_chat_interface()

    elif choice == "Dashboard":
        sub_menu = st.sidebar.radio("Select Dashboard", ["Admin Dashboard", "User Dashboard"])
        if sub_menu == "Admin Dashboard":
            load_admin_dashboard(df)
        else:
            load_user_dashboard(df)

    else:
        st.title("Welcome to the Course Recommendation System")
        st.write("Explore curated Udemy courses based on your interests, skill level, and subject preferences.")
        st.write("Use the **Recommend** tab to get personalized course suggestions or the **Chatbot** for natural language guidance.")
        st.subheader("About")
        st.markdown("""
        **Course Recommender App** built with:
        - Streamlit  
        - Pandas & Scikit-learn  
        - Content-based filtering (cosine similarity)  

        Dataset: [Udemy Courses](https://www.udemy.com/)
        """)



if __name__ == '__main__':
    main()









