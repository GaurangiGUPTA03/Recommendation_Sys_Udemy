


import streamlit as st
import os
import base64
import pandas as pd

def load_home_tab(df):
    st.title("Course Recommendation App")

    # Paths and titles
    image_folder = os.path.join(os.path.dirname(__file__), 'image')
    image_files = ['Business_Finance.gif', 'Graphic_Design.gif', 'Musical_Instruments.gif', 'web_Dev.gif']
    image_titles = ['Business Finance', 'Graphic Design', 'Musical Instruments', 'Web Development']
    image_paths = [os.path.join(image_folder, file) for file in image_files]

    st.markdown("### 🌟 Course Highlights by Category")
    cols = st.columns(4)
    selected_subject = None

    for i, col in enumerate(cols):
        try:
            base64_gif = image_to_base64(image_paths[i])
            col.markdown(f'''
                <style>
                    .hover-img {{
                        transition: transform 0.3s ease, box-shadow 0.3s ease;
                        border-radius: 10px;
                    }}
                    .hover-img:hover {{
                        transform: scale(1.1);
                        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
                    }}
                </style>
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <img src="data:image/gif;base64,{base64_gif}" class="hover-img" style="height: 180px; width: auto;" />
                </div>
            ''', unsafe_allow_html=True)

            # Show only one clearly labeled button
            with col:
             st.markdown(" ")  # spacing
             offset, btn_col = st.columns([1, 2])  # 1: left spacing, 2: button area
             with btn_col:
                if st.button(image_titles[i], key=image_titles[i]):
                 selected_subject = image_titles[i]


        except Exception as e:
            col.warning(f"Image not found: {image_files[i]}")

    st.markdown("---")

    # Show filtered or default course table
    if selected_subject:
        st.subheader(f"📘 Courses in {selected_subject}")
        filtered = df[df['subject'] == selected_subject]
        if not filtered.empty:
            st.dataframe(filtered[['course_title', 'subject', 'level', 'price', 'num_subscribers']])
        else:
            st.info("No courses available for this category.")
    else:
        st.markdown("### 🔍 Preview of Available Courses")
        st.dataframe(df[['course_title', 'subject', 'level', 'price', 'num_subscribers']].head(10))


# Base64 converter
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()
