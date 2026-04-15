import streamlit as st
import os
from google import genai
from PIL import Image
from dotenv import load_dotenv
load_dotenv()
key=os.environ.get("API_KEY")

client=genai.Client(api_key=key)


with st.sidebar:
    st.write(f"controls sidebar")
    st.write("upload max images 3")
    upload_images= st.file_uploader(
        "upload",
        type=["jpg","png","jpeg"],
        accept_multiple_files=True
    )
    pil_generated_images=[]             
    if upload_images and len(upload_images)<3:
        col=st.columns(len(upload_images))
        for i, img in enumerate(upload_images):
            with col[i]:
                image=Image.open(img)
                pil_generated_images.append(image)
                for img in pil_generated_images:
                    st.write(img)
    
    else:
        st.error("please upload your image")
    options=st.selectbox(
        "Your options",
        ["Hints","Solution with Code"]
    )
    button=st.button("Debug code")

with st.container():
    st.title("Welcome to the AI based code debugger")
    st.divider()
    
    if button:
        if not options:
            st.error("Select your options")
        elif not upload_images:
            st.error("Please select your images")
        else:
            with st.spinner("AI is working"):
                response= client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=[f"{pil_generated_images} and {options} make solutions with markdown based on options"]
                )
                st.write(response.text)


    


