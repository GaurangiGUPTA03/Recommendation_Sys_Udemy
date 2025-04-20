import re
import streamlit as st




def chatbot_interface(df, render_course):
    st.subheader("🤖 Course Guidance Chatbot")

    # Keyword options
    available_subjects = df['subject'].dropna().str.lower().unique().tolist()
    available_levels = df['level'].dropna().str.lower().unique().tolist()

    # User input
    user_query = st.text_input("Ask me anything about courses (e.g., 'I want a beginner course in Python')")

    if st.button("Ask"):
        if not user_query.strip():
            st.warning("Please enter a question.")
            return

        query = user_query.lower()

        # Extract subject & level
        matched_subject = None
        for subj in available_subjects:
            if subj.lower() in query:
                matched_subject = subj
                break

        matched_level = None
        for lvl in available_levels:
            if lvl.lower() in query:
                matched_level = lvl
                break

        filtered_df = df.copy()

        if matched_subject:
            filtered_df = filtered_df[filtered_df['subject'].str.lower() == matched_subject]

        if matched_level:
            filtered_df = filtered_df[filtered_df['level'].str.lower() == matched_level]

        if filtered_df.empty:
            st.warning("🤷‍♂️ No exact matches found. Try different keywords.")
            st.info("Example queries: \n- Beginner course in Python\n- Advanced marketing course")
            return

        # Use cosine similarity to show top 5 from remaining
        cosine_sim_mat = vectorize_text_to_cosine(filtered_df)
        idx = 0  # Just use the first item as reference
        sim_scores = list(enumerate(cosine_sim_mat[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        selected_indices = [i[0] for i in sim_scores[1:6]]

        st.success(f"🎯 Showing top course suggestions for: {matched_subject or 'Any Subject'} | {matched_level or 'Any Level'}")
        for i in selected_indices:
            row = filtered_df.iloc[i]
            stc.html(render_course(row), height=400)
