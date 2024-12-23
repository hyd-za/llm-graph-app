import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import plotly.express as px

# Load environment variables from .env file (for API key)
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize LangChain's ChatOpenAI model using the API key
llm = ChatOpenAI(
    model="gpt-4o-mini",  # or "gpt-4" if available
    openai_api_key=openai_api_key,
    temperature=0.7,
)

# Function to load the CSV file
def load_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        return None

# Function to generate a prompt based on user query and CSV data
def generate_prompt(user_query, csv_data):
    csv_string = csv_data.head().to_string(index=False)
    prompt = f"""
    You are given a dataset in CSV format (here, only the first five rows are shown):
    
    {csv_string}

    Your response should ONLY be the python code [NOTHING ELSE is allowed]. 
    Keep in mind that the data is already read using pandas as csv_data. Create a temporary copy onto another variable copy_data for your needs.

    You are free to perform any data cleaning to resolve issues - like badly named columns, column data types, etc.
    
    If a chart/graph is requested: Please ONLY use Plotly for creating the chart. Exclude fig.show() at the end of the code.

    If something other than a chart is requested: Just generate a python code and make sure to store the result in a variable 'result' as a clear string (add new lines if needed) with a tiny explanation.
    
    Now, answer this question based on this dataset: {user_query}
    """
    return prompt

# Main Streamlit app
def main():
    st.title("Dynamic Data Query App with LLM and Plotly")
    
    # File uploader for CSV
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    
    if uploaded_file is not None:
        # Load the uploaded CSV file
        csv_data = pd.read_csv(uploaded_file)
        st.write("Preview of the uploaded data:")
        st.dataframe(csv_data.head())
        
        # Input for user query
        user_query = st.text_area("Enter your prompt for the graph", 
                                  placeholder="e.g., Generate Python code for a bar chart showing portfolio allocation.")
        # Inside the Streamlit app:
        if st.button("Generate Response"):
            with st.spinner("Processing..."):
                # Generate the prompt and get the response
                prompt = generate_prompt(user_query, csv_data)
                response = llm([HumanMessage(content=prompt)])

            # Check if the response contains a Python code (for graph generation)
            if "fig" in response.content:  # This indicates it's generating a chart
                st.subheader("Generated Python Code for Chart:")
                st.code(response.content, language='python')

                # Execute the generated code dynamically to get the Plotly chart
                try:
                    # Define a local execution context
                    local_context = {"csv_data": csv_data, "pd": pd, "px": px}
                    exec(response.content.strip("```").lstrip("python"), local_context)
                    
                    # Capture and display the Plotly graph
                    st.subheader("Generated Graph:")
                    st.plotly_chart(local_context["fig"])
                except Exception as e:
                    st.error(f"Error executing the generated code: {e}")
            
            else:
                # Display the text response for non-graph queries
                # st.subheader("Generated Answer:")
                # st.write(response.content)
                st.subheader("Generated Python Code:")
                st.code(response.content, language='python')

                # Execute the generated code dynamically to get the Plotly chart
                try:
                    # Define a local execution context
                    local_context = {"csv_data": csv_data, "pd": pd, "px": px}
                    exec(response.content.strip("```").lstrip("python"), local_context)
                    st.subheader("Generated Answer:")
                    st.write(local_context['result'])
                    
                    # Capture and display the Plotly graph
                    # st.plotly_chart(local_context["fig"])
                except Exception as e:
                    st.error(f"Error executing the generated code: {e}")

# Run the app
if __name__ == "__main__":
    main()
