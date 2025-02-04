import streamlit as st
import google.generativeai as genai
import os 
import webbrowser
from PIL import Image 
from main import get_code
genai.configure(api_key=os.getenv("GOOGLE_API"))
llm = genai.GenerativeModel("gemini-2.0-flash-exp")
sinput='''You have perfect vision and pay great attention to detail which makes you an expert at building single page apps using Tailwind, HTML and JS.
    You take screenshots of a reference web page from the user, and then build single page apps 
    using Tailwind, HTML and JS.

    - Make sure the app looks exactly like the screenshot.
    - Do not leave out smaller UI elements. Make sure to include every single thing in the screenshot.
    - Pay close attention to background color, text color, font size, font family, 
    padding, margin, border, etc. Match the colors and sizes exactly.
    - In particular, pay attention to background color and overall color scheme.
    - Use the exact text from the screenshot.
    - Do not add comments in the code such as "<!-- Add other navigation links as needed -->" and "<!-- ... other news items ... -->" in place of writing the full code. WRITE THE FULL CODE.
    - Make sure to always get the layout right (if things are arranged in a row in the screenshot, they should be in a row in the app as well)
    - Repeat elements as needed to match the screenshot. For example, if there are 15 items, the code should have 15 items. DO NOT LEAVE comments like "<!-- Repeat for each news item -->" or bad things will happen.
    - For images, use placeholder images from https://picsum.photos and include a detailed description of the image in the alt text so that an image generation AI can generate the image later.

    In terms of libraries,

    - Use this script to include Tailwind: <script src="https://cdn.tailwindcss.com"></script>
    - You can use Google Fonts
    - Font Awesome for icons: <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"></link>

    Return only the full code in <html></html> tags.'''
def stream_code(llm,image,input=sinput):
    res=llm.generate_content([input,image],stream=True,generation_config={"max_output_tokens":4096})
    with open("data2/vision.html", "w", encoding= "utf-8")as file:

        for chunk in res:
            # generated_code=generated_code+chunk.candidates[0].content.parts[0].text
            file.write(chunk.candidates[0].content.parts[0].text)
            yield chunk.candidates[0].content.parts[0].text
def show_html():
    with open("data2/index.html", "r", encoding="utf-8") as file:
        return file.read()
# Set up the Streamlit app
st.set_page_config("ARA_Snap", page_icon="random", layout="wide")
st.title("LandScape AI")
tab1, tab2=st.tabs(["Vision2Code", "Prompt2Code"])

with tab1:
    uploaded_file = st.file_uploader("Choose an Image file (sample picture or hand drawn layout)", accept_multiple_files=False, type=["jpg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width =True)
        generate = st.button("Generate!")
        if generate:
            st.write_stream(stream_code(llm,image))
    else:
        st.markdown("""# Project Submission Details

### *Project Description:*
- *Project Title:* A.R.A Snap
- *Objective:*  
  A.R.A Snap automates landing page creation using AI-driven agents, generating structured, responsive, and visually appealing designs from user prompts or images with minimal effort.
- *Overview:*  
  This system leverages Agentic AI Technology and Gemini LLM to streamline web development. It breaks down the design process into specialized agents, ensuring high-quality HTML, CSS, and JavaScript generation. With AI-powered requirement analysis, web search, and content generation, A.R.A Snap simplifies landing page creation while maintaining design consistency and efficiency.
   Key functionalities include:

- **AI-powered landing page generation** from textual prompts or reference images.  
- **Automated web search** for gathering design inspiration.  
- **Structured HTML, CSS, and JavaScript code generation** using AI.  
- **Integrated quality assurance** for debugging and performance validation.  
- **User-friendly Streamlit interface** for seamless interaction.  

 By combining generative AI, structured workflows, and automation, A.R.A Snap significantly reduces development time while ensuring professional, high-quality landing pages.

### *Project Created By:*
| *Name*          | *Roll Number* | *Email Address*               |
|--------------------|-----------------|---------------------------------|
| Arushima Chauhan   | 21BCON239       | arushima.21bcon239@jecrcu.edu.in|
| Akansha Bhargava   | 21BCON244       | akansha.21bcon244@jecrcu.edu.in |
| Ruchika Choudhary  | 22BCON1107      | ruchika.22bcom1017@jecrcu.edu.in|

- *Name of Mentor:*  Dr. Shivangi Dheer 
- *Submitted To:* Dr. Shashi Sharma  
 """)


with tab2:
    prompt=st.text_input('Enter the prompt to generate your landing page', placeholder="eg. ad for a recruiting agency looking for actors, use appropriate colours and font styles")

    b=st.button('generate code') 
    if b:
        st.markdown("Please wait")
        # Show a spinner during a process
        with st.spinner(text='In progress'):
            shit=get_code(prompt)
            st.success('Done')
        html_code=show_html()
        st.code(html_code, language="html")
        st.balloons()
        st.toast('TADA!!!!')

