
import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Content Generator",
    layout="wide"
)

st.title("🚀 AI Content Generator")
st.write("Generate Blogs, LinkedIn Posts, Captions, Emails and more")

topic = st.text_input("Enter Topic")

technology = st.selectbox(
    "Select Technology",
    [
        "Python",
        "React",
        "MERN",
        "NodeJS",
        "FastAPI",
        "AI",
        "GenAI"
    ]
)

content_type = st.selectbox(
    "Content Type",
    [
        "LinkedIn Post",
        "Blog",
        "Instagram Caption",
        "Twitter Post",
        "Email",
        "YouTube Description"
    ]
)

tone = st.selectbox(
    "Tone",
    [
        "Professional",
        "Technical",
        "Friendly",
        "Casual",
        "Marketing"
    ]
)

generate = st.button("Generate Content")

if generate:
    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        try:
            with st.spinner("Generating Content..."):
                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json={
                        "topic": topic,
                        "technology": technology,
                        "content_type": content_type,
                        "tone": tone
                    },
                    timeout=120
                )

            # Check HTTP status
            response.raise_for_status()

            # Check whether the response contains valid JSON
            try:
                result = response.json()
            except requests.exceptions.JSONDecodeError:
                st.error("Backend returned an invalid JSON response.")
                st.code(response.text or "Empty response")
                st.stop()

            # Display generated content
            if "content" in result:
                if result.get("generation_mode") == "offline":
                    st.caption(
                        "Offline draft generated. Add a valid Groq API key to enable AI generation."
                    )
                else:
                    st.success("AI content generated successfully!")
                st.subheader("Generated Content")
                st.text_area(
                    "Output",
                    value=result["content"],
                    height=400
                )
            else:
                st.error("The backend response does not contain 'content'.")
                st.json(result)

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to the backend. "
                "Make sure your FastAPI server is running on port 8000."
            )

        except requests.exceptions.Timeout:
            st.error("The request timed out. Please try again.")

        except requests.exceptions.HTTPError as e:
            st.error(f"Backend HTTP error: {e}")
            st.code(response.text)

        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
