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
st.title("🔍 FAQ Search System")
st.markdown("""
This application allows you to search through our FAQ database using natural language.
You can filter results by category, date range, and more.
""")

# Sidebar for filters
st.sidebar.header("Search Filters")

# Category filter
categories = [
    "All",
    "Shipping",
    "Order Management",
    "Returns",
    "Payment",
    "Product Information",
    "Customer Support",
    "Services",
    "Pricing",
    "Account Management",
    "Rewards",
    "Communication",
    "Company Information",
    "Privacy"
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

# Main search interface
st.header("Search FAQ")
query = st.text_input("Enter your question:", placeholder="e.g., What are your shipping options?")

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
st.markdown("Built with Streamlit • Powered by TimescaleDB and OpenAI") 