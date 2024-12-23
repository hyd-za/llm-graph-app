# llm-graph-app
This project is a Streamlit-based application that leverages the LangChain `ChatOpenAI` model to dynamically generate Python code based on user queries and uploaded CSV data. The app can produce Plotly visualizations or other Python outputs by interpreting user prompts.

---

## Features

- **CSV File Upload**: Allows users to upload CSV files for analysis.
- **Dynamic Code Generation**: Uses LangChain's LLM to generate Python code for data manipulation and visualization based on user prompts.
- **Interactive Visualizations**: Creates dynamic, interactive Plotly charts without requiring users to write code.
- **Error Handling**: Gracefully handles errors in CSV reading, prompt generation, and code execution.

---

## Installation

### Prerequisites

1. **Python 3.8 or higher**
2. Required Python packages:
   - `streamlit`
   - `pandas`
   - `python-dotenv`
   - `langchain`
   - `openai`
   - `plotly`

### Setup

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone <repository_url>
   cd <project_directory>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

4. Run the Streamlit application:
   ```bash
   streamlit run initial_app.py
   ```

---

## Usage

1. **Upload a CSV File**:
   - Use the file uploader to upload a dataset in CSV format.
   - The app displays a preview of the uploaded data.

2. **Enter a Prompt**:
   - Provide a text prompt describing the desired analysis or visualization (e.g., "Generate a bar chart of sales by region.").

3. **Generate Code and Outputs**:
   - Click the "Generate Response" button.
   - The app generates Python code and displays it.
   - If the code generates a Plotly chart, it will be rendered directly in the app.

4. **Non-Chart Queries**:
   - For queries that don't result in a visualization, the app processes and displays the output in text format.

---

## How It Works

1. **Prompt Generation**:
   - Extracts a preview of the uploaded CSV data (first five rows) to create a structured prompt.
   - Combines user queries with the preview to guide the LLM in generating Python code.

2. **LLM Interaction**:
   - Sends the generated prompt to LangChain's ChatOpenAI model.
   - Receives Python code as the response.

3. **Dynamic Execution**:
   - Executes the generated Python code in a controlled environment.
   - Captures and displays results, including Plotly charts and textual outputs.

---

## File Structure

- **`intial_app.py`**: Main Streamlit application file.
- **`.env`**: Stores the OpenAI API key.
- **`requirements.txt`**: Lists required Python packages.
