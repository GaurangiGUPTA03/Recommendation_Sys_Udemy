# import streamlit as st
# import streamlit.components.v1 as stc

# # Load dependencies
# import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# # Import chatbot module
# from chatbot import chatbot_interface

# # Load Dataset
# @st.cache_data
# def load_data():
#     df = pd.read_csv("data/udemy_courses.csv")
#     required_cols = ['course_title', 'subject', 'level']
#     optional_cols = ['course_description']

#     for col in required_cols:
#         if col not in df.columns:
#             raise ValueError(f"Required column '{col}' not found in dataset.")

#     df = df.dropna(subset=required_cols)

#     for col in optional_cols:
#         if col not in df.columns:
#             df[col] = ""
#         else:
#             df[col] = df[col].fillna("")

#     # Add placeholder image_url column
#     df['image_url'] = df['course_title'].apply(
#         lambda x: f"https://dummyimage.com/300x150/cccccc/000000.png&text={'+'.join(x.split()[:4])}"
#     )

#     return df


# # Vectorize + Cosine Similarity Matrix
# def vectorize_text_to_cosine(df):
#     df['combined_features'] = (
#         df['course_title'] + " " + df['subject'] + " " + df['level'] + " " + df['course_description']
#     )
#     count_vect = CountVectorizer(stop_words='english')
#     cv_mat = count_vect.fit_transform(df['combined_features'])
#     cosine_sim_mat = cosine_similarity(cv_mat)
#     return cosine_sim_mat


# # Recommendation System
# @st.cache_data
# def get_recommendation(title, cosine_sim_mat, df, num_of_rec=10):
#     course_indices = pd.Series(df.index, index=df['course_title']).drop_duplicates()
#     idx = course_indices[title]
#     sim_scores = list(enumerate(cosine_sim_mat[idx]))
#     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
#     selected_indices = [i[0] for i in sim_scores[1:num_of_rec+1]]
#     selected_scores = [i[1] for i in sim_scores[1:num_of_rec+1]]

#     result_df = df.iloc[selected_indices].copy()
#     result_df['similarity_score'] = selected_scores

#     return result_df


# # Search if course not found
# @st.cache_data
# def search_term_if_not_found(term, df):
#     result_df = df[df['course_title'].str.contains(term, case=False, na=False)]
#     return result_df


# # Template for course display
# RESULT_TEMP = """
# <div style="width:90%;height:100%;margin:10px;padding:10px;position:relative;border-radius:10px;
# box-shadow:0 0 15px 5px #ccc; background-color: #f0f9ff; border-left: 5px solid #6c6c6c;">
# <h4>{}</h4>
# <p><strong>📈 Similarity Score:</strong> {:.2f}</p>
# <p><strong>🔗 Link:</strong> <a href="{}" target="_blank">Course URL</a></p>
# <p><strong>💲 Price:</strong> {}</p>
# <p><strong>🧑‍🎓 Students:</strong> {}</p>
# <img src="{}" width="100%" height="150">
# </div>
# """

# def render_course(row):
#     return RESULT_TEMP.format(
#         row['course_title'],
#         row['similarity_score'],
#         row['url'],
#         row['price'],
#         row['num_subscribers'],
#         row['image_url']
#     )


# # Main App
# def main():
#     st.set_page_config(page_title="Course Recommender", layout="wide")
#     st.title("Course Recommendation App")

#     menu = ["Home", "Recommend", "Chatbot", "About"]
#     choice = st.sidebar.selectbox("Menu", menu)

#     df = load_data()

#     if choice == "Home":
#         st.subheader("Course Dataset Preview")
#         st.dataframe(df[['course_title', 'subject', 'level', 'price', 'num_subscribers']].head(10))

#     elif choice == "Recommend":
#         st.subheader("🔍 Recommend Similar Courses")

#         subject_filter = st.sidebar.multiselect("Filter by Subject", sorted(df['subject'].dropna().unique()))
#         level_filter = st.sidebar.multiselect("Filter by Level", sorted(df['level'].dropna().unique()))
#         num_of_rec = st.sidebar.slider("Number of Recommendations", 4, 20, 7)

#         filtered_df = df.copy()
#         if subject_filter:
#             filtered_df = filtered_df[filtered_df['subject'].isin(subject_filter)]
#         if level_filter:
#             filtered_df = filtered_df[filtered_df['level'].isin(level_filter)]

#         if filtered_df.empty:
#             st.warning("No courses found with selected filters.")
#             return

#         filtered_df = filtered_df.reset_index(drop=True)
#         cosine_sim_mat = vectorize_text_to_cosine(filtered_df)

#         search_term = st.text_input("Enter Course Title", "")

#         if st.button("Recommend"):
#             if search_term not in filtered_df['course_title'].values:
#                 st.warning("Course not found.")
#                 st.info("Suggested Options:")
#                 st.dataframe(search_term_if_not_found(search_term, filtered_df))
#             else:
#                 results = get_recommendation(search_term, cosine_sim_mat, filtered_df, num_of_rec)
#                 for _, row in results.iterrows():
#                     stc.html(render_course(row), height=400)

#     elif choice == "Chatbot":
#         chatbot_interface(df, render_course)

#     else:
#         st.subheader("About")
#         st.markdown("""
#         **Course Recommender App** built with:
#         - Streamlit 
#         - Pandas & Scikit-learn 
#         - Content-based filtering (cosine similarity)

#         Dataset: [Udemy Courses](https://www.udemy.com/)
#         """)


# if __name__ == '__main__':
#     main()








import streamlit as st

# Must come before any other Streamlit command!
st.set_page_config(page_title="Course Recommender", layout="wide")

import pandas as pd
import os
import base64

from chatbot import chatbot_interface
from Home import load_home_tab
from Recommend import load_recommend_tab
from Dashboard import load_dashboard_tab  # Ensure this function exists

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
    # Load data
    df = load_data()

    # Display GIF in sidebar
    try:
        gif_path = os.path.join("data", "image", "udemy.gif")
        encoded_gif = get_base64_gif(gif_path)
        st.sidebar.markdown(
            f"<img src='data:image/gif;base64,{encoded_gif}' style='width:100%; margin-bottom: 1rem;'>",
            unsafe_allow_html=True
        )
    except Exception as e:
        st.sidebar.warning(f"Could not load GIF: {e}")

    # Sidebar menu
    menu = ["Home", "Recommend", "Chatbot", "Dashboard", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Page navigation
    if choice == "Home":
        load_home_tab(df)

    elif choice == "Recommend":
        load_recommend_tab(df)

    elif choice == "Chatbot":
        from Recommend import render_course
        chatbot_interface(df, render_course)

    elif choice == "Dashboard":
        load_dashboard_tab(df)

    else:  # About
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









# import streamlit as st
# import pandas as pd
# import os
# import base64

# from chatbot import chatbot_interface
# from Home import load_home_tab
# from Recommend import load_recommend_tab
# from Dashboard import load_dashboard_tab


# @st.cache_data
# def load_data():
#     df = pd.read_csv("data/udemy_courses.csv")
#     required_cols = ['course_title', 'subject', 'level']
#     optional_cols = ['course_description']
#     for col in required_cols:
#         if col not in df.columns:
#             raise ValueError(f"Required column '{col}' not found in dataset.")
#     df = df.dropna(subset=required_cols)
#     for col in optional_cols:
#         if col not in df.columns:
#             df[col] = ""
#         else:
#             df[col] = df[col].fillna("")
#     df['image_url'] = df['course_title'].apply(
#         lambda x: f"https://dummyimage.com/300x150/cccccc/000000.png&text={'+'.join(x.split()[:4])}"
#     )
#     return df


# def get_base64_gif(gif_path):
#     with open(gif_path, "rb") as f:
#         data = f.read()
#     return base64.b64encode(data).decode("utf-8")


# def sidebar_menu():
#     st.sidebar.markdown("""
#         <link rel="stylesheet" href="https://cdn-uicons.flaticon.com/uicons-regular-rounded/css/uicons-regular-rounded.css">
#         <link rel="stylesheet" href="https://cdn-uicons.flaticon.com/uicons-thin-straight/css/uicons-thin-straight.css">
#         <link rel="stylesheet" href="https://cdn-uicons.flaticon.com/uicons-regular-straight/css/uicons-regular-straight.css">
#         <style>
#             .menu-item {
#                 padding: 10px 16px;
#                 font-size: 16px;
#                 color: #000000;
#                 border-radius: 6px;
#                 cursor: pointer;
#                 margin-bottom: 4px;
#                 display: flex;
#                 align-items: center;
#                 transition: background 0.2s;
#             }
#             .menu-item:hover {
#                 background-color: #e6e6e6;
#             }
#             .menu-item.active {
#                 background-color: #c7d2fe;
#                 font-weight: bold;
#             }
#             .menu-icon {
#                 margin-right: 12px;
#                 font-size: 18px;
#             }
#         </style>
#     """, unsafe_allow_html=True)

#     menu_items = {
#         "Home": "fi fi-rr-home",
#         "Recommend": "fi fi-rr-search",
#         "Chatbot": "fi fi-rr-chatbot-speech-bubble",
#         "Dashboard": "fi fi-ts-dashboard-panel",
#         "About": "fi fi-rs-info"
#     }

#     for key, icon in menu_items.items():
#         active_class = "active" if st.session_state.page == key else ""
#         # Create a unique key for each click handler
#         if st.sidebar.button(f"_{key}", key=f"navbtn_{key}"):
#             st.session_state.page = key
#         # Render the custom HTML that visually shows the list
#         st.sidebar.markdown(
#             f"""
#             <div class="menu-item {active_class}">
#                 <i class="{icon} menu-icon"></i> {key}
#             </div>
#             """,
#             unsafe_allow_html=True
#         )


# def main():
#     st.set_page_config(page_title="Course Recommender", layout="wide")

#     if "page" not in st.session_state:
#         st.session_state.page = "Home"

#     df = load_data()

#     # Sidebar GIF
#     try:
#         gif_path = os.path.join("data", "image", "udemy.gif")
#         encoded_gif = get_base64_gif(gif_path)
#         st.sidebar.markdown(
#             f"<img src='data:image/gif;base64,{encoded_gif}' style='width:100%; margin-bottom: 1rem;'>",
#             unsafe_allow_html=True
#         )
#     except:
#         pass

#     sidebar_menu()

#     page = st.session_state.page
#     if page == "Home":
#         load_home_tab(df)
#     elif page == "Recommend":
#         load_recommend_tab(df)
#     elif page == "Chatbot":
#         from Recommend import render_course
#         chatbot_interface(df, render_course)
#     elif page == "Dashboard":
#         load_dashboard_tab(df)
#     elif page == "About":
#         st.title("Welcome to the Course Recommendation System")
#         st.markdown("""
#         Use the **Recommend** tab to get personalized course suggestions, or try the **Chatbot** for conversational help!

#         ---
#         ### 🔍 About this App
#         Built with:
#         - Streamlit  
#         - Scikit-learn  
#         - Pandas  
#         - Udemy Dataset (content-based filtering)
#         """)


# if __name__ == '__main__':
#     main()
