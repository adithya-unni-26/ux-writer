import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define tonalities with their full descriptions
tonalities = {
    "Technical precision": "Emphasizes accuracy and detailed information.",
    "Developer-friendly": "Uses language and terminology familiar to developers.",
    "Concise and direct": "Provides information efficiently without unnecessary fluff.",
    "Empowering": "Encourages developers to take control and leverage the tool's capabilities.",
    "Problem-solving oriented": "Focuses on how the tool helps overcome challenges.",
    "Efficiency-focused": "Highlights time-saving and productivity-enhancing aspects.",
    "Educational": "Incorporates learning elements to help developers improve their skills.",
    "Command-line style": "Mimics the brevity and directness of command-line interfaces.",
    "Other": "Custom tonality"
}

def generate_ux_copy(component_description, ux_copy_type, tonality):
    prompt = f"""
    Generate UX copy for a devtool product based on the following:
    Component Description: {component_description}
    Type of UX Copy: {ux_copy_type}
    Desired Tonality: {tonality}

    Please provide 2-3 options for the requested UX copy.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a UX copy expert for devtool products."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

def main():
    st.set_page_config(page_title="Facets UX Writer", page_icon="✍️")
    st.title("Facets UX Writer")
    st.subheader("UX Copy Generator for Devtool Products")

    component_description = st.text_area("Description of the component:", 
                                         help="Provide a brief description of the component, including its purpose and functionality")
    
    ux_copy_type = st.selectbox("Type of UX copy required:",
                                ["Tooltips", "Toast messages", "Subheadings", "Error messages", 
                                 "Empty state", "Onboarding messages", "Loading messages", 
                                 "Success messages", "Other"],
                                help="Select the type of UX copy you need")
    
    if ux_copy_type == "Other":
        ux_copy_type = st.text_input("Please specify the type of UX copy:")

    selected_tonality = st.selectbox("Desired tonality:",
                                     list(tonalities.keys()),
                                     help="Select the desired tone for the UX copy")
    
    if selected_tonality == "Other":
        custom_tonality = st.text_input("Please specify the desired tonality:")
        tonality_description = custom_tonality
    else:
        tonality_description = tonalities[selected_tonality]

    if st.button("Generate UX Copy"):
        if component_description and ux_copy_type and selected_tonality:
            with st.spinner("Generating UX copy..."):
                try:
                    ux_copy = generate_ux_copy(component_description, ux_copy_type, tonality_description)
                    st.success("UX copy generated successfully!")
                    st.subheader("Generated UX Copy Options:")
                    st.write(ux_copy)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.error("Please fill out all fields before submitting.")

if __name__ == "__main__":
    main()