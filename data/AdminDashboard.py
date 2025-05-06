import streamlit as st

def load_admin_dashboard(df):  # Accept df, even if not used
    st.title("🛠️ Admin Dashboard")

    tableau_url = "https://public.tableau.com/app/profile/aditi.jain7249/viz/UdemyAdmindashboard/Dashboard1?publish=yes"

    st.markdown("View the admin dashboard by clicking the link below:")
    st.markdown(f"[🔗 Open Tableau Admin Dashboard]({tableau_url})", unsafe_allow_html=True)