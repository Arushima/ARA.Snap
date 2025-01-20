from phi.agent import Agent
# from phi.model.groq import Groq
from  phi.tools.duckduckgo import DuckDuckGo
from phi.tools.file import FileTools
from dotenv import load_dotenv
import os
from pathlib import Path
from phi.agent import Agent, RunResponse
from phi.model.google import Gemini


load_dotenv()
dir='data2'
path = Path(dir)


# 2. Requirement Analysis Agent
Requirement_analysis_agent = Agent(
    name='requirement_analysis_agent',
    role='Analyze the user-provided prompt to extract the key requirements for the landing page.',
    tools=[],
    model=Gemini(id="gemini-2.0-flash-exp", api_key=os.getenv("GOOGLE_API")),
    verbose=True,
    instructions=[
        "Understand and parse the user's prompt to extract key features and layout requirements.",
        "Break down the requirements into structured tasks for subsequent agents.",
        "Identify the target audience and style based on the provided details.",
        "Prepare a summary of the requirements for use by other agents."
    ],
    show_tool_calls=True,
    markdown=True
)

# 3. Web Search Agent
Web_search_agent = Agent(
    name='web_search_agent',
    role='Search for design inspiration and ideas online to enhance the landing page design.',
    tools=[DuckDuckGo()],
    model=Gemini(id="gemini-2.0-flash-exp", api_key=os.getenv("GOOGLE_API")),
    verbose=True,
    instructions=[
        "Perform web searches using DuckDuckGo to find examples and ideas relevant to the project requirements.",
        "Focus on trending design elements, layouts, and aesthetics that match the user's brief.",
        "Analyze and summarize the collected design inspirations.",
        "Provide actionable suggestions to the design_agent for incorporation into the landing page wireframe.",
        "Ensure that the suggestions align with accessibility and usability standards."
    ],
    show_tool_calls=True,
    markdown=True
)

# 4. Design Agent
Design_agent = Agent(
    name='design_agent',
    role='Create the design layout and wireframe for the landing page.',
    tools=[],
    model=Gemini(id="gemini-2.0-flash-exp", api_key=os.getenv("GOOGLE_API")),
    verbose=True,
    instructions=[
        "Use the requirements provided by the requirement_analysis_agent.",
        "Incorporate web search results provided by the web_search_agent.",
        "Generate a written visual layout including sections, headers, footers, and placeholders for images and text.",
        "Export the layout as a wireframe file for review."
    ],
    show_tool_calls=True,
    markdown=True
)

# 5. Content Generation Agent
Content_generation_agent = Agent(
    name='content_generation_agent',
    role='Generate textual content for the landing page based on user input and the requirements.',
    tools=[],
    model=Gemini(id="gemini-2.0-flash-exp", api_key=os.getenv("GOOGLE_API")),
    verbose=True,
    instructions=[
        "Generate engaging and concise textual content for each section of the landing page.",
        "Align the content with the brand's voice and tone as inferred from the prompt.",
        "Provide alternative content options for A/B testing if required."
    ],
    show_tool_calls=True,
    markdown=True
)

# 6. Code Generator Agent
Code_generator_agent = Agent(
    name='code_generator_agent',
    role='Write the landing page code using HTML, CSS, and JavaScript.',
    tools=[FileTools(base_dir=path, read_files=True, list_files=True, save_files=True)],
    model=Gemini(id="gemini-2.0-flash-exp", api_key=os.getenv("GOOGLE_API")),
    verbose=True,
    instructions=[
        "Take the design and content inputs from the design_agent and content_generation_agent.",
        "Write clean, modular, and responsive HTML, CSS, and JavaScript code.",
        "Incorporate animations or interactive elements as needed.",
        "Save the final code files for publication."
    ],
    show_tool_calls=True,
    markdown=True
)

# 7. Quality Assurance Agent
Quality_assurance_agent = Agent(
    name='quality_assurance_agent',
    role='Review and test the generated code and content.',
    tools=[FileTools(base_dir=path, read_files=True, list_files=True,save_files=True)],
    model=Gemini(id="gemini-2.0-flash-exp", api_key=os.getenv("GOOGLE_API")),
    verbose=True,
    instructions=[
        "Validate the code for syntax errors and responsiveness.",
        "Provide a report of issues and suggestions for improvement."
    ],
    show_tool_calls=True,
    markdown=True
)

Multiple_agent = Agent(
    team=[
        Requirement_analysis_agent,
        Web_search_agent,
        Design_agent,
        Content_generation_agent,
        Code_generator_agent,
        Quality_assurance_agent
    ],
    verbose=False,
    instructions=[
        "The requirement_analysis_agent will analyze the user's prompt and extract key requirements.",
        "The web_search_agent will perform online searches for design inspiration.",
        "The design_agent will create the wireframe based on requirements and search results.",
        "The content_generation_agent will generate textual content for each section of the landing page.",
        "The code_generator_agent will write HTML, CSS, and JavaScript code based on the design and content.",
        "The quality_assurance_agent will review the generated code and content for errors and improvements.",
        "Save the final html, css and javascript code files."
    ],
    tools=[DuckDuckGo(), FileTools(base_dir=path, read_files=True, list_files=True,save_files=True)],
    show_tool_calls=True,
    model=Gemini(id="gemini-2.0-flash-exp", api_key=os.getenv("GOOGLE_API")),
    stream=True
)

combined_agent = Agent(
    name='designer_and_coder',
    role='Analyze user requirements, create a detailed design plan, and generate the final landing page code.',
    tools=[DuckDuckGo(), FileTools(base_dir=path, read_files=True, list_files=True, save_files=True)],
    model=Gemini(id="gemini-2.0-flash-exp", api_key=os.getenv("GOOGLE_API")),
    verbose=False,
    instructions=[
        # Design Planning Phase
        "1. Read and analyze the user's prompt thoroughly to extract specific requirements, such as the purpose of the landing page, target audience, preferred themes, colors, and layout preferences.",
        "2. Use DuckDuckGo to research and gather inspiration from existing landing pages relevant to the given topic. Focus on identifying best practices for layout, typography, color usage, and visual hierarchy.",
        "3. Determine a suitable layout structure for the landing page, including the placement of the header, hero section, main content, call-to-action buttons, and footer. Ensure the layout supports a logical flow and user engagement.",
        "4. Develop a cohesive color scheme that aligns with the user’s requirements and the intended theme: ",
        "   - Select a primary color to set the tone (e.g., vibrant for energetic pages, muted for professional ones).",
        "   - Choose complementary secondary and accent colors to enhance the design while maintaining harmony.",
        "   - Ensure sufficient contrast between text and background for readability.",
        "Add placeholder images where necessary, take them from the web or https://picsum.photos .",
        "5. Plan the typography for the page: ",
        "   - Use a font for headings that conveys the desired tone (e.g., bold for emphasis, playful for informal).",
        "   - Select a legible and professional font for body text with appropriate size and spacing.",
        "   - Maintain consistent typography hierarchy throughout the page.",
        "6. Plan textual content placement, such as headings, subheadings, body text, and calls-to-action, ensuring clarity and alignment with the user’s goals.",
        "7. Document all design decisions in a detailed plan, specifying the color scheme, font choices, layout structure, and content arrangement. Include examples or references wherever possible.",
        
        # Code Generation Phase
        "8. Translate the design plan into HTML and CSS code: ",
        "   - Write semantic HTML for the structure of the landing page.",
        "   - Use CSS to implement styling, including layout, typography, colors, and spacing.",
        "   - Ensure the design is responsive and works well on different screen sizes.",
        "9. Align all elements, such as headings, sections, and buttons, precisely as described in the design plan, paying attention to margins, padding, and alignment.",
        "10. Validate the HTML and CSS code for errors, ensuring compliance with web standards and cross-browser compatibility.",
        
        # File Management
        "11. Save the HTML code in a file named 'index.html' and the CSS code in a file named 'styles.css'. Ensure the files are saved in the specified directory structure.",
        "12. If required, create additional resources like placeholder images or JSON data files and organize them in the appropriate folders.",
        
        # Final Checks
        "13. Conduct a final review to verify that the implemented design matches the user’s requirements and the design plan.",
        "14. Prepare the project for handoff, including ensuring all files are named appropriately and well-organized for ease of use."
    ],
    show_tool_calls=False,
    markdown=True
)

# Web_search_agent.print_response(user_prompt)
def get_code(prompt):
    response=combined_agent.run(prompt)
    return response.content