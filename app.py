import streamlit as st
import requests
import json
import random
from dotenv import load_dotenv
import os


load_dotenv()

# Set page config
st.set_page_config(page_title="Your Go-To First Aid!", page_icon="👩‍⚕", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: lightyellow;
        color: rgb(88, 195, 240);
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: black;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: light blue;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        color: blue;
    }
    .chat-message.user {
        background-color: black;
    }
    .chat-message.bot {
        background-color: blue;
    }
    .chat-message .avatar {
      width: 20%;
    }
    .chat-message .avatar img {
      max-width: 78px;
      max-height: 78px;
      border-radius: 50%;
      object-fit: cover;
    }
    .chat-message .message {
      width: 80%;
      padding: 0 1.5rem;
    }
    h1, h2, h3 {
        color: #4CAF50;
    }
    .stAlert > div {
        color: white;
        background-color: purple;
    }
    </style>
    """, unsafe_allow_html=True)

# Gemini API key
api_key = os.getenv("api_key")

# Gemini API endpoint
api_url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"

def get_ai_response(user_input):
    try:
        data = {
            "contents": [{"parts": [{"text": user_input}]}]
        }
        
        response = requests.post(
            f"{api_url}?key={api_key}",
            headers={"Content-Type": "application/json"},
            data=json.dumps(data)
        )
        response.raise_for_status()
        
        result = response.json()
        if "candidates" in result and len(result["candidates"]) > 0:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "I'm sorry, but I couldn't generate a response. Could you please try rephrasing your question?"

    except Exception as e:
        return f"I apologize, but an error occurred while processing your request. Please try again later. Error: {str(e)}"

# Health tips
health_tips = [
    "Stay hydrated! Aim for 8 glasses of water a day.",
    "Practice mindfulness or meditation for 10 minutes daily.",
    "Take short breaks every hour if you sit for long periods.",
    "Incorporate colorful fruits and vegetables into your meals.",
    "Aim for 7-9 hours of sleep each night.",
    "Practice good hand hygiene to prevent infections.",
    "Stand up and stretch every hour to improve circulation.",
    "Try to get at least 30 minutes of moderate exercise daily.",
    "Limit processed foods and choose whole foods instead.",
    "Take time to relax and de-stress each day."
]

# Title and description
st.title("👨‍⚕️ MediBot: First Aid Simplified")
st.markdown("Your AI-powered health assistant for friendly advice and personalized health insights. Remember, in emergencies, always call your local emergency number immediately.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Chat with MediBot..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = get_ai_response(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar
with st.sidebar:
    st.sidebar.image(
    "https://d2jx2rerrg6sh3.cloudfront.net/images/Article_Images/ImageForArticle_22457_16516788730473249.jpg",
    width=300
)
    #st.image("https://www.google.com/imgres?q=health%20care%20bot&imgurl=https%3A%2F%2Fd2jx2rerrg6sh3.cloudfront.net%2Fimages%2FArticle_Images%2FImageForArticle_22457_16516788730473249.jpg&imgrefurl=https%3A%2F%2Fwww.news-medical.net%2Fhealth%2FThe-Pros-and-Cons-of-Healthcare-Chatbots.aspx&docid=IPNzNYqCrvR2sM&tbnid=2JbjtNyZwFgm4M&vet=12ahUKEwijuIGB0-iLAxXNUGwGHd9bBXEQM3oECBAQAA..i&w=2000&h=1000&hcb=2&ved=2ahUKEwijuIGB0-iLAxXNUGwGHd9bBXEQM3oECBAQAA", width=300)
    st.title("About MediBot")
    st.markdown(
        """
        **MediBot** is your trusted AI-powered health companion, designed to support your well-being with:

    - **Friendly, easy-to-understand health insights**  
    - **Possible causes of symptoms and immediate steps to take**  
    - **Personalized lifestyle and dietary recommendations**  
    - **Guidance on when to seek professional medical care**  

    **Important:** MediBot provides general health guidance but is **not** a replacement for professional medical advice.  
    Always consult a healthcare professional for accurate diagnosis and treatment.  

    **Your health matters—stay informed, stay well!**  
        """
    )
    st.warning("This is a demo application. The advice provided should not be considered as professional medical advice.")
    
    # Daily Health Tip
    st.subheader("🌟 Daily Health Tip")
    st.info(random.choice(health_tips))

# Footer
st.markdown("---")
st.markdown("Developed by Saara and Neelmani | © 2025")