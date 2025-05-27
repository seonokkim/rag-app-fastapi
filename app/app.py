import streamlit as st
from datetime import datetime
from database.vector_store import VectorStore
from services.synthesizer import Synthesizer
from timescale_vector import client

# Initialize VectorStore
vec = VectorStore()

# Page config
st.set_page_config(
    page_title="FAQ Search System",
    page_icon="🔍",
    layout="wide"
)

# Title and description
st.title("📈 Stock Trading FAQ Assistant")
st.markdown("""
This application helps you find answers to common stock trading questions using natural language.
Filter by category to find specific trading-related information.
""")

# Sidebar for filters
st.sidebar.header("Search Filters")

# Category filter
categories = [
    "All",
    "Trading Strategies",
    "Trading Strategy",
    "Trading Basics",
    "Trading Concepts",
    "Trading Tools",
    "Trading Options",
    "Technical Analysis",
    "Fundamental Analysis",
    "Market Indicators",
    "Market Structure",
    "Market Function",
    "Market Theory",
    "Market Benchmarks",
    "Market Cycles",
    "Market Anomalies",
    "Risk Management",
    "Order Types",
    "Brokerage Accounts",
    "Options Strategy",
    "Portfolio Management",
    "Investment Options",
    "Investment Types",
    "Company Analysis",
    "Financial Metrics",
    "Price Metrics",
    "Earnings Analysis",
    "Economic Impact",
    "Industry Basics",
    "Corporate Finance",
    "Derivatives",
    "Dividend Types",
    "International Investing",
    "International Risk",
    "International Access",
    "Account Types",
    "Advanced Trading",
    "Advanced Strategy",
    "Advanced Risk",
    "High-Risk Investing",
    "Employee Benefits",
    "Tax Rules",
    "Wealth Building",
    "Research Tools",
    "Analysis Methods"
]

selected_category = st.sidebar.selectbox("Select Category", categories)

# Date range filter
st.sidebar.subheader("Date Range")
use_date_filter = st.sidebar.checkbox("Use Date Filter")

if use_date_filter:
    start_date = st.sidebar.date_input("Start Date", datetime(2024, 1, 1))
    end_date = st.sidebar.date_input("End Date", datetime(2024, 12, 31))
    time_range = (datetime.combine(start_date, datetime.min.time()),
                 datetime.combine(end_date, datetime.max.time()))
else:
    time_range = None

# Use session state to store the current query
if 'query' not in st.session_state:
    st.session_state.query = ''

# Main search interface
st.header("Search FAQ")
query = st.text_input("Enter your question:", key="main_query_input", value=st.session_state.query, placeholder="e.g., What is a stock?")

# Add example questions
st.markdown("**Or try these examples:**")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("What is a bond?"):
        st.session_state.query = "What is a bond?"
        st.rerun()

with col2:
    if st.button("What is technical analysis?"):
        st.session_state.query = "What is technical analysis?"
        st.rerun()

with col3:
    if st.button("What is risk management?"):
        st.session_state.query = "What is risk management?"
        st.rerun()

if query:
    # Prepare search parameters
    search_params = {
        "limit": 3,
        "time_range": time_range if use_date_filter else None
    }
    
    # Add category filter if selected
    if selected_category != "All":
        search_params["metadata_filter"] = {"category": selected_category}
    
    # Perform search
    with st.spinner("Searching..."):
        results = vec.search(query, return_dataframe=False, **search_params)
        
        # Generate response
        response = Synthesizer.generate_response(question=query, context=results)
        
        # Display results
        st.subheader("Answer")
        st.write(response.answer)
        
        # Display thought process in an expander
        with st.expander("View Thought Process"):
            for thought in response.thought_process:
                st.write(f"- {thought}")
        
        # Display context sufficiency
        st.info(f"Context Sufficiency: {'✅ Sufficient' if response.enough_context else '⚠️ Insufficient'}")
        
        # Display raw results in an expander
        with st.expander("View Raw Search Results"):
            for i, result in enumerate(results, 1):
                st.markdown(f"**Result {i}**")
                # Create columns for better layout
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Display the main content
                    st.markdown("**Question & Answer:**")
                    st.write(result[2])  # content is at index 2
                
                with col2:
                    # Display metadata
                    st.markdown("**Metadata:**")
                    metadata = result[1]  # metadata is at index 1
                    st.write(f"Category: {metadata.get('category', 'N/A')}")
                    st.write(f"Created: {metadata.get('created_at', 'N/A')}")
                    st.write(f"Similarity: {result[4]:.2f}")  # distance is at index 4
                
                st.markdown("---")

# Footer
st.markdown("---")
st.markdown("2025 Seonok Kim") 