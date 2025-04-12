import streamlit as st
import streamlit.components.v1 as stc

# Load dependencies
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load Dataset
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

    # Add placeholder image_url column
    df['image_url'] = df['course_title'].apply(
    lambda x: f"https://dummyimage.com/300x150/cccccc/000000.png&text={'+'.join(x.split()[:4])}"
)


    return df


# Vectorize + Cosine Similarity Matrix
def vectorize_text_to_cosine(df):
    df['combined_features'] = (
        df['course_title'] + " " + df['subject'] + " " + df['level'] + " " + df['course_description']
    )
    count_vect = CountVectorizer(stop_words='english')
    cv_mat = count_vect.fit_transform(df['combined_features'])
    cosine_sim_mat = cosine_similarity(cv_mat)
    return cosine_sim_mat


# Recommendation System
@st.cache_data
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


# Search if course not found
@st.cache_data
def search_term_if_not_found(term, df):
    result_df = df[df['course_title'].str.contains(term, case=False, na=False)]
    return result_df


# Template for course display
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


def render_course(row):
    return RESULT_TEMP.format(
        row['course_title'],
        row['similarity_score'],
        row['url'],
        row['price'],
        row['num_subscribers'],
        row['image_url']
    )


# Main App
def main():
    st.set_page_config(page_title="Course Recommender", layout="wide")
    st.title("Course Recommendation App")

    menu = ["Home", "Recommend", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    df = load_data()

    if choice == "Home":
        st.subheader("Course Dataset Preview")
        st.dataframe(df[['course_title', 'subject', 'level', 'price', 'num_subscribers']].head(10))

    elif choice == "Recommend":
        st.subheader("🔍 Recommend Similar Courses")

        subject_filter = st.sidebar.multiselect("Filter by Subject", sorted(df['subject'].dropna().unique()))
        level_filter = st.sidebar.multiselect("Filter by Level", sorted(df['level'].dropna().unique()))
        num_of_rec = st.sidebar.slider("Number of Recommendations", 4, 20, 7)

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

        search_term = st.text_input("Enter Course Title", "")

        if st.button("Recommend"):
            if search_term not in filtered_df['course_title'].values:
                st.warning("Course not found.")
                st.info("Suggested Options:")
                st.dataframe(search_term_if_not_found(search_term, filtered_df))
            else:
                results = get_recommendation(search_term, cosine_sim_mat, filtered_df, num_of_rec)
                for _, row in results.iterrows():
                    stc.html(render_course(row), height=400)

    else:
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
