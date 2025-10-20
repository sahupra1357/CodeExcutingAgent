import logging
from registry.agents.file_access_agent import FileAccessAgent
from registry.agents.python_code_exec_agent import PythonCodeExecAgent

# Set up debug logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

prompt = """Use the file traffic_accidents.csv for your analysis. The column names are:
Variable	Description
accidents	Number of recorded accidents, as a positive integer.
traffic_fine_amount	Traffic fine amount, expressed in thousands of USD.
traffic_density	Traffic density index, scale from 0 (low) to 10 (high).
traffic_lights	Proportion of traffic lights in the area (0 to 1).
pavement_quality	Pavement quality, scale from 0 (very poor) to 5 (excellent).
urban_area	Urban area (1) or rural area (0), as an integer.
average_speed	Average speed of vehicles in km/h.
rain_intensity	Rain intensity, scale from 0 (no rain) to 3 (heavy rain).
vehicle_count	Estimated number of vehicles, in thousands, as an integer.
time_of_day	Time of day in 24-hour format (0 to 24).
accidents	traffic_fine_amount
"""

print("set up: ")
print(prompt)

print(" Setting up the agents...")

file_ingest_agent = FileAccessAgent()

data_analysis_agent = PythonCodeExecAgent(model_name="o3-mini", reasoning_effort="high")

print("Understanding the content of the file...")

file_ingest_agent_output = file_ingest_agent.task(prompt)
print("File Ingest Agent Output: ", file_ingest_agent_output)

data_analysis_agent.add_context(prompt)
data_analysis_agent.add_context(file_ingest_agent_output)

while True:
    print("Type your question related to the data in the file. Type 'exit' to quit.")
    user_input = input("Your question: ")
    if user_input.lower() == 'exit':
        print("Exiting the program.")
        break

    print("user input: ", user_input)

    data_analysis_agent_output = data_analysis_agent.task(user_input)

    print("Data Analysis Agent Output: ")
    print(data_analysis_agent_output)
          
