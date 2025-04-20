import streamlit as st
import streamlit.components.v1 as stc
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import base64
import os

# Vectorization
def vectorize_text_to_cosine(df):
    df['combined_features'] = (
        df['course_title'] + " " + df['subject'] + " " + df['level'] + " " + df['course_description']
    )
    count_vect = CountVectorizer(stop_words='english')
    cv_mat = count_vect.fit_transform(df['combined_features'])
    cosine_sim_mat = cosine_similarity(cv_mat)
    return cosine_sim_mat

# Course recommendation logic
def get_recommendation(title, cosine_sim_mat, df, num_of_rec=10):
    course_indices = pd.Series(df.index, index=df['course_title']).drop_duplicates()
    idx = course_indices[title]
    sim_scores = list(enumerate(cosine_sim_mat[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    selected_indices = [i[0] for i in sim_scores[1:num_of_rec+1]]
    selected_scores = [i[1] for i in sim_scores[1:num_of_rec+1]]

    result_df = df.iloc[selected_indices].copy()
    result_df['similarity_score'] = selected_scores
    return result_df

# Suggest similar course titles if not found
def search_term_if_not_found(term, df):
    return df[df['course_title'].str.contains(term, case=False, na=False)]

# HTML template for result display
RESULT_TEMP = """
<div style="width:90%;height:100%;margin:10px;padding:10px;position:relative;border-radius:10px;
box-shadow:0 0 15px 5px #ccc; background-color: #f0f9ff; border-left: 5px solid #6c6c6c;">
<h4>{}</h4>
<p><strong>📈 Similarity Score:</strong> {:.2f}</p>
<p><strong>🔗 Link:</strong> <a href="{}" target="_blank">Course URL</a></p>
<p><strong>💲 Price:</strong> {}</p>
<p><strong>🧑‍🎓 Students:</strong> {}</p>
<img src="{}" width="100%" height="150">
</div>
"""

# Render each course using HTML block
def render_course(row):
    return RESULT_TEMP.format(
        row['course_title'],
        row['similarity_score'],
        row['url'],
        row['price'],
        row['num_subscribers'],
        row['image_url']
    )

# Main recommend tab
def load_recommend_tab(df):
    # Load study.gif
    gif_path = os.path.join(os.path.dirname(__file__), 'image', 'study.gif')
    with open(gif_path, "rb") as gif_file:
        gif_bytes = gif_file.read()
        encoded_gif = base64.b64encode(gif_bytes).decode()

    # Sidebar filters
    subject_filter = st.sidebar.multiselect("Filter by Subject", sorted(df['subject'].dropna().unique()))
    level_filter = st.sidebar.multiselect("Filter by Level", sorted(df['level'].dropna().unique()))
    num_of_rec = st.sidebar.slider("Number of Recommendations", 4, 20, 7)

    # Filter dataset
    filtered_df = df.copy()
    if subject_filter:
        filtered_df = filtered_df[filtered_df['subject'].isin(subject_filter)]
    if level_filter:
        filtered_df = filtered_df[filtered_df['level'].isin(level_filter)]

    if filtered_df.empty:
        st.warning("No courses found with selected filters.")
        return

    filtered_df = filtered_df.reset_index(drop=True)
    cosine_sim_mat = vectorize_text_to_cosine(filtered_df)

    # Layout: Left (input & results), Right (GIF)
    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("📚 Course Recommendation")
        st.markdown("### 🔍 Recommend Similar Courses")

        search_term = st.text_input("Enter Course Title")

        if st.button("Recommend"):
            if search_term not in filtered_df['course_title'].values:
                st.warning("Course not found.")
                st.info("Suggested Options:")
                st.dataframe(search_term_if_not_found(search_term, filtered_df))
            else:
                results = get_recommendation(search_term, cosine_sim_mat, filtered_df, num_of_rec)
                for _, row in results.iterrows():
                    stc.html(render_course(row), height=400)

    with right_col:
        st.markdown(f"""
        <img src="data:image/gif;base64,{encoded_gif}" style="height: 500px; width: auto;" />
    """, unsafe_allow_html=True)

