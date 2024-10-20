import streamlit as st
from PIL import Image
import io
import base64
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Groq LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.2-11b-vision-preview"
)

def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def get_styling_advice(image):
    base64_image = image_to_base64(image)
    
    messages = [
        HumanMessage(content=[
            {
                "type": "text",
                "text": "You are a professional fashion stylist with an eye for trends and a knack for personalizing outfits. Here's an image of a clothing item. Please provide styling advice for different occasions and settings. Consider factors like accessories, complementary pieces, and appropriate contexts."
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"
                }
            }
        ])
    ]
    
    try:
        response = llm.invoke(messages)
        return response.content, False
    except Exception as e:
        if "rate limit" in str(e).lower():
            return "Rate limit exceeded. Please subscribe for more requests.", True
        else:
            return f"An error occurred: {str(e)}", False

def main():
    st.set_page_config(page_title="Fashion Stylist AI", page_icon="👔", layout="wide")
    
    st.title("👔 Fashion Stylist AI")
    st.subheader("Upload an image of a clothing item for styling advice!")

    if 'rate_limited' not in st.session_state:
        st.session_state.rate_limited = False

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Get Styling Advice", disabled=st.session_state.rate_limited):
            with st.spinner("Analyzing your fashion item..."):
                advice, rate_limited = get_styling_advice(image)
            st.markdown("## Styling Advice")
            st.write(advice)
            
            if rate_limited:
                st.session_state.rate_limited = True
                st.error("You've reached the request limit. Subscribe for more!")
                st.button("Subscribe Now", type="primary")

if __name__ == "__main__":
    main()