from openai import OpenAI
import json
import pandas as pd

# Initialize OpenAI client with API key
api_key = "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"
client = OpenAI(api_key=api_key)

# Function to generate JSON response using LLM
def generate_llm_response(tableau_response):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": f"""
                You are a helpful assistant designed to generate JSON answers based on Tableau data. Explore the data and derive key insights to answer user questions.
                
                Assuming you receive data from Tableau in the below JSON format:
                {tableau_response}
                
                User can ask any kind of questions:
                1. How many rows are there?
                2. What is this sheet 1 about?
                
                Example 1:
                User: What is the average salary?
                Prompt: The average salary is ((50000+60000)/2)
                
                Example 2:
                User: What is the total salary?
                Prompt: {{"Total Salary": 50000+60000}}
                
                Example 3:
                User: How many employees have a salary above 55000?
                Prompt: {{
                    "Employees Above 55000": [
                        {{
                            "Employee ID": 2,
                            "First Name": "Jane",
                            "Last Name": "Smith"
                        }}
                    ]
                }}
                
                Example 4:
                User: What is this sheet 1 about?
                Prompt: This sheet contains employee information with columns such as Employee ID, First Name, Last Name, Age, Salary, and Joining Date.
                """
            },
            {"role": "user", "content": "show me salary"}
        ]
    )
    return response.choices[0].message.content

# Function to load JSON data from file and generate LLM response
def process_json_file_and_generate_response(file_path):
    try:
        # Load JSON data from file
        with open(file_path, 'r') as json_file:
            tableau_response = json.load(json_file)
    except FileNotFoundError:
        print("Error: JSON file not found.")
        tableau_response = {}  # Set an empty response if file not found or invalid JSON

    # Generate JSON response using LLM
    llm_response = generate_llm_response(tableau_response)
    print(llm_response)
    return llm_response
    

# Function to display output in a table format
def display_output_as_table(llm_response):
    # Assuming llm_response is a JSON string containing tabular data
    # Parse the JSON string to a Python dictionary
    output_data = json.loads(llm_response)
    # Extract the list of employee names from the dictionary
    employee_names = output_data.get('Employee Names', [])
    # Convert the data to a DataFrame for easier display
    df = pd.DataFrame(employee_names)

    # Display the DataFrame as a table
    print(df)

# Example usage
file_path = 'shows_data.json'
llm_response = process_json_file_and_generate_response(file_path)

# Display the output as a table
display_output_as_table(llm_response)
