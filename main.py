import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_ollama

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stTextInput>div>div>input {
        border: 2px solid #4a4a4a;
        border-radius: 8px;
        padding: 12px;
    }
    .stButton>button {
        background-color: #4a4a4a;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        border: none;
        font-weight: 500;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #333333;
        transform: translateY(-2px);
    }
    .stExpander {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .stTextArea>div>div>textarea {
        border-radius: 8px;
    }
    .title {
        color: #4a4a4a;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .success-message {
        color: #28a745;
        font-weight: 500;
    }
    .processing-message {
        color: #ffc107;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Main UI
st.markdown('<h1 class="title">🌐 AI Web Scraper</h1>', unsafe_allow_html=True)

# Sidebar for additional options
with st.sidebar:
    st.header("Settings")
    headless_mode = st.checkbox("Headless Mode", value=True)
    delay_time = st.slider("Page Load Delay (seconds)", 1, 20, 5)

# URL Input Section
with st.container():
    st.subheader("🔗 Enter Website URL")
    url = st.text_input("", placeholder="https://example.com", label_visibility="collapsed")

# Step 1: Scrape the Website
col1, col2 = st.columns([3, 1])
with col1:
    if st.button("🚀 Scrape Website", key="scrape"):
        if url:
            with st.spinner("🌐 Scraping website content..."):
                try:
                    # Scrape the website
                    dom_content = scrape_website(url)
                    body_content = extract_body_content(dom_content)
                    cleaned_content = clean_body_content(body_content)

                    # Store the DOM content in Streamlit session state
                    st.session_state.dom_content = cleaned_content
                    st.success("✅ Website scraped successfully!")
                except Exception as e:
                    st.error(f"❌ Error scraping website: {str(e)}")

# Display the DOM content
if "dom_content" in st.session_state:
    with st.expander("📄 View Scraped Content", expanded=False):
        st.code(st.session_state.dom_content, language='html')

    # Step 2: Ask Questions About the DOM Content
    st.divider()
    st.subheader("🔍 Parse Content")
    
    parse_description = st.text_area(
        "Describe what information you want to extract:",
        placeholder="e.g., 'Extract all product names and prices'",
        height=100
    )
    
    if st.button("✨ Parse Content", key="parse"):
        if parse_description:
            with st.spinner("🧠 Processing your request with AI..."):
                try:
                    # Parse the content with Ollama
                    dom_chunks = split_dom_content(st.session_state.dom_content)
                    parsed_result = parse_with_ollama(dom_chunks, parse_description)
                    
                    st.subheader("📋 Results")
                    st.markdown("---")
                    st.write(parsed_result)
                    st.markdown("---")
                except Exception as e:
                    st.error(f"❌ Error parsing content: {str(e)}")
        else:
            st.warning("⚠️ Please enter a description of what to parse")