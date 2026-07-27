import streamlit as st
from agent import query_business_agent

st.set_page_config(page_title="Monday.com BI Agent", layout="wide")

st.title("📊 Monday.com Executive BI Agent")
st.write("Ask founder-level questions across your Sales Pipeline and Work Orders boards.")

# Sidebar for Quick Actions
st.sidebar.header("Executive Shortcuts")
if st.sidebar.button("📋 Generate Leadership Update"):
    st.session_state["query_input"] = "Provide a high-level executive summary for leadership updates covering deal pipeline health, major operational updates, and data quality caveats."

user_input = st.text_input("Ask a business question:", key="query_input")

if st.button("Run Query") and user_input:
    with st.spinner("Analyzing Monday.com boards..."):
        answer = query_business_agent(user_input)
        st.markdown("### 💡 BI Insight")
        st.write(answer)