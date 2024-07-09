import os
import pandas as pd
from openai import OpenAI
import streamlit as st
from groq import Groq

# initialize the Groq client
def initialize_groq_client(api_key):
    return Groq(api_key=api_key)

 # Define a function to count words in the input
def count_words(input_text):
    return len(input_text.split())

# llama3 70b generate chat completion
def llama3_generate(available_teachers, available_rooms):
    if len(available_teachers) > 60 or len(available_rooms) > 60:
        return "One or both of the DataFrames exceed the maximum row limit of 60. Cannot process the request."
    os.environ['GROQ_API_KEY'] = st.session_state['groq_api_key']
    api_key = os.environ.get("GROQ_API_KEY")

    client = initialize_groq_client(api_key)
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f'''
                    As an expert assistant, your task is to create a timetable that efficiently assigns available rooms to teachers and students based on their free times. This timetable should be presented in a table format, clearly detailing who is free during each time interval and their assigned room.
                    Dont need to explain anything and generate any text explanation. I want the just table as an output according to following output format for gievn reqirements.

                    Output Format:
                    - Columns: Time, Room Name 1, Room Name 2, etc.
                    - 'Time' column: List time intervals during which the assignments are relevant.
                    - Each 'Room Name' column: Should contain entries formatted as 'TeacherName/StudentName1/studentName2/so on based on given input data'. If a room is free during a specific time slot, indicate the assignment with teacher and student name list; if not, mark it as 'X'.

                    Ensure the table is constructed with precise alignment to the given schedules, maintaining accurate correspondence between students and teachers as detailed in the data. Dont need to explain any irrelevant text explanation.

                    Schedules Provided:
                    - Teacher's Schedule: Columns represent teacher names. Entries under each teacher name list the students assigned to them.
                    - Room's Schedule: Columns represent room names. An empty entry indicates availability; 'X' indicates the room is not available.

                    Please construct the table based on the following data:
                    Teacher's Schedule: {available_teachers}
                    Room's Schedule: {available_rooms}
                    '''
                }
            ],
            model="llama3-70b-8192",
        )
        response_content = chat_completion.choices[0].message.content
        return response_content
    except Exception as e:
        return f"An error occurred: {str(e)}"

def openai_generate(available_teachers, available_rooms):
    if len(available_teachers) > 100 or len(available_rooms) > 100:
        return "One or both of the DataFrames exceed the maximum row limit of 100. Cannot process the request."
    os.environ['OPENAI_API_KEY'] = st.session_state['openai_api_key']
    client_openai = OpenAI()

    system_role = f'''
                    As an expert assistant, your task is to create a timetable that efficiently assigns available rooms to teachers and students based on their free times. This timetable should be presented in a table format, clearly detailing who is free during each time interval and their assigned room.
                    Dont need to explain anything and generate any text explanation. I want the just table as an output according to following output format for gievn reqirements.

                    Output Format:
                    - Columns: Time, Room Name 1, Room Name 2, etc.
                    - 'Time' column: List time intervals during which the assignments are relevant.
                    - Each 'Room Name' column: Should contain entries formatted as 'TeacherName/StudentName1/studentName2/so on based on given input data'. If a room is free during a specific time slot, indicate the assignment with teacher and student name list; if not, mark it as 'X'.

                    Ensure the table is constructed with precise alignment to the given schedules, maintaining accurate correspondence between students and teachers as detailed in the data. Dont need to explain any irrelevant text explanation.

                    Schedules Provided:
                    - Teacher's Schedule: Columns represent teacher names. Entries under each teacher name list the students assigned to them.
                    - Room's Schedule: Columns represent room names. An empty entry indicates availability; 'X' indicates the room is not available.

                    Please construct the table based on the following data:
                    Teacher's Schedule: {available_teachers}
                    Room's Schedule: {available_rooms}
                    '''
    input = f'''
    Kindly follow the following output format to built the table according to Rooms and Teachers Data and your generated table must be correct and your output generated table should be created after alot of thinking and create a 100 percent corrected table using Rooms and Teachers Data without any error and clash in time table with teachers/students with other in room assignment according to Rooms and Teachers Data.
    Output Format:
                - Columns: Time, Room Name 1, Room Name 2, etc.
                - 'Time' column: List time intervals during which the assignments are relevant.
                - Each 'Room Name' column: Should contain entries formatted as 'TeacherName/StudentName1/studentName2/so on based on given input data'. If a room is free during a specific time slot, indicate the assignment with teacher and student name list; if not, mark it as 'X'.

    Ensure the table is constructed with precise alignment to the given schedules, maintaining accurate correspondence between students and teachers as detailed in the data. Dont need to explain any irrelevant text explanation.
    Rooms and Teachers Data:

    Schedules Provided:
    - Teacher's Schedule: Columns represent teacher names. Entries under each teacher name list the students assigned to them.
    - Room's Schedule: Columns represent room names. An empty entry indicates availability; 'X' indicates the room is not available.

    Please construct the table based on the following data:
    Teacher's Schedule: {available_teachers}
    Room's Schedule: {available_rooms}
                    '''

    messages = [
        {"role": "system", "content": system_role},
        {"role": "user", "content": input}
    ]

    # Use the chat completion endpoint
    response = client_openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages
    )

    return response.choices[0].message.content

def generate(available_teachers, available_rooms, model_choice):
    try:
        if model_choice == 'Groq Model':
            return llama3_generate(available_teachers, available_rooms)
        elif model_choice == 'OpenAI Model':
            return openai_generate(available_teachers, available_rooms)
    except Exception as e:
        return f"Error during generation: {str(e)} 🚨"

def llama3_recommendation(available_teachers, available_rooms, generated_table):
    if len(available_teachers) > 60 or len(available_rooms) > 60:
        return "One or both of the DataFrames exceed the maximum row limit of 60. Cannot process the request."
    os.environ['GROQ_API_KEY'] = st.session_state['groq_api_key']
    api_key = os.environ.get("GROQ_API_KEY")

    client = initialize_groq_client(api_key)
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f'''
                    You will act like a intelligent assistant to gave the good recommendation on timetable setting for the given rooms teachers and students.
                    
                    As an expert assistant, your task is to gave some recommendation on the created timetable for the given rooms and teachers and students. You will check the timetable correctly and gave recommendation on the generated 
                    timetable for the rooms and teachers and student on different timestamps. You will suggest the good solutions and i want the optimize in proper and professional way. Use the easy words and dont need to explain any irrelevant text.

                    Kindly gave the recommendaton in professional and use the proper headings and i want good and professonal recommendation to improve this timetable more.
                    Here is provided timetable that is generated for the given information of rooms and teachers and students.
                    generated timetable:
                    {generated_table}
                    
                    Information of students, teachers and rooms
                    Analyze the following data:
                    Teacher's Schedule: {available_teachers}
                    Room's Schedule: {available_rooms}
                    '''
                }
            ],
            model="llama3-70b-8192",
        )
        response_content = chat_completion.choices[0].message.content
        return response_content
    except Exception as e:
        return f"An error occurred: {str(e)}"

def openai_recommendation(available_teachers, available_rooms, generated_table):
    if len(available_teachers) > 100 or len(available_rooms) > 100:
        return "One or both of the DataFrames exceed the maximum row limit of 100. Cannot process the request."
    os.environ['OPENAI_API_KEY'] = st.session_state['openai_api_key']
    client_openai = OpenAI()
    system_role = f'''
                    You will act like a intelligent assistant to gave the good recommendation on timetable setting for the given rooms teachers and students. Your gtask is to analyze the timetable that is built for the free rooms on timestamps for teachers and student and then check the raw the information and then some suggestion some changes.                    
                    As an expert assistant, your task is to gave some recommendation on the created timetable for the given rooms and teachers and students. You will check the timetable correctly and gave recommendation on the generated 
    timetable for the rooms and teachers and student on different timestamps. You will suggest the good solutions and i want the optimize in proper and professional way. Use the easy words and dont need to explain any irrelevant text.
          
                    Kindly gave the recommendaton in professional and use the proper headings and i want good and professonal recommendation to improve this timetable more.
                    Here is provided timetable that is generated for the given information of rooms and teachers and students.
                    generated timetable:
                    {generated_table}
                    
                    Information of students, teachers and rooms
                    Analyze the following data:
                    Teacher's Schedule: {available_teachers}
                    Room's Schedule: {available_rooms}
                    '''
    input = f'''
    As an expert assistant, your task is to gave some recommendation on the created timetable for the given rooms and teachers and students. You will check the timetable correctly and gave recommendation on the generated 
    timetable for the rooms and teachers and student on different timestamps. You will suggest the good solutions and i want the optimize in proper and professional way. Use the easy words and dont need to explain any irrelevant text.
                    
    Kindly gave the recommendaton in professional and use the proper headings and i want good and professonal recommendation to improve this timetable more.

    Here is provided timetable that is generated for the given information of rooms and teachers and students.
    generated timetable:
    {generated_table}
    
    Information of students, teachers and rooms
    Analyze the following data:
    Teacher's Schedule: {available_teachers}
    Room's Schedule: {available_rooms}
                    '''

    messages = [
        {"role": "system", "content": system_role},
        {"role": "user", "content": input}
    ]

    # Use the chat completion endpoint
    response = client_openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages
    )

    return response.choices[0].message.content
def get_recommendation(available_teachers, available_rooms, generated_table, model_choice):
    try:
        if model_choice == 'Groq Model':
            return llama3_recommendation(available_teachers, available_rooms, generated_table)
        elif model_choice == 'OpenAI Model':
            return openai_recommendation(available_teachers, available_rooms, generated_table)
    except Exception as e:
        return f"Error during generation: {str(e)} 🚨"

def llama3_mistakes(available_teachers, available_rooms, generated_table):
    if len(available_teachers) > 60 or len(available_rooms) > 60:
        return "One or both of the DataFrames exceed the maximum row limit of 60. Cannot process the request."
    os.environ['GROQ_API_KEY'] = st.session_state['groq_api_key']
    api_key = os.environ.get("GROQ_API_KEY")

    client = initialize_groq_client(api_key)
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f'''
                    As an expert assistant, your task is to find the mistakes from the generated timetable for the rooms, teachers and students. I want find out mistakes and i want the list of mistakes and and output should be following
                    Your task is to analyze the timetable and raw data then detect the mistakes if there is no mistakes then then add the message no mistakes found in solution and mistakes heading if found then explain it in list and solution in solution heading.
                    
                    Kindly follow the output format to generate a response and dont need to explain any irrelevant text and i want full optimize response. Your response should be professional.
            
                    Here is provided timetable that is generated for the given information of rooms and teachers and students.
                    generated timetable:
                    {generated_table}
                    
                    Information of students, teachers and rooms
                    Analyze the following data:
                    Teacher's Schedule: {available_teachers}
                    Room's Schedule: {available_rooms}
                    
                    Output format:
                    mistakes:
                    write list of mistakes here
                     if there is no mistakes then then add the message no mistakes found if found then explain it in list.
        
                    solution:
                    write solution of mistakes here
                    '''
                }
            ],
            model="llama3-70b-8192",
        )
        response_content = chat_completion.choices[0].message.content
        return response_content
    except Exception as e:
        return f"An error occurred: {str(e)}"

def openai_mistakes(available_teachers, available_rooms, generated_table):
    if len(available_teachers) > 100 or len(available_rooms) > 100:
        return "One or both of the DataFrames exceed the maximum row limit of 100. Cannot process the request."
    os.environ['OPENAI_API_KEY'] = st.session_state['openai_api_key']
    client_openai = OpenAI()
    system_role = f'''
                    As an expert assistant, your task is to find the mistakes from the generated timetable for the rooms, teachers and students. I want find out mistakes and i want the list of mistakes and and output should be following
                    Your task is to analyze the timetable and raw data then detect the mistakes if there is no mistakes then then add the message no mistakes found in solution and mistakes heading if found then explain it in list and solution in solution heading.
                    
                    Kindly follow the output format to generate a response and dont need to explain any irrelevant text and i want full optimize response. Your response should be professional.
            
                    Here is provided timetable that is generated for the given information of rooms and teachers and students.
                    generated timetable:
                    {generated_table}
                    
                    Information of students, teachers and rooms
                    Analyze the following data:
                    Teacher's Schedule: {available_teachers}
                    Room's Schedule: {available_rooms}
                    
                    Output format:
                    mistakes:
                    write list of mistakes here
                     if there is no mistakes then then add the message no mistakes found if found then explain it in list.
        
                    solution:
                    write solution of mistakes here
                    '''
    input = f'''
     Your task is to analyze the timetable and raw data then detect the mistakes if there is no mistakes then then add the message no mistakes found in solution and mistakes heading if found then explain it in list and solution in solution heading.
    
    Kindly follow the output format to generate a response and dont need to explain any irrelevant text and i want full optimize response. Your response should be professional.

    Here is provided timetable that is generated for the given information of rooms and teachers and students.
    generated timetable:
    {generated_table}
    
    Information of students, teachers and rooms
    Analyze the following data:
    Teacher's Schedule: {available_teachers}
    Room's Schedule: {available_rooms}
    
    Output format:
    mistakes:
    write list of mistakes here
     if there is no mistakes then then add the message no mistakes found if found then explain it in list.

    solution:
    write solution of mistakes here
                    '''

    messages = [
        {"role": "system", "content": system_role},
        {"role": "user", "content": input}
    ]

    # Use the chat completion endpoint
    response = client_openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages
    )

    return response.choices[0].message.content

def get_mistakes(available_teachers, available_rooms, generated_table, model_choice):
    try:
        if model_choice == 'Groq Model':
            return llama3_mistakes(available_teachers, available_rooms, generated_table)
        elif model_choice == 'OpenAI Model':
            return openai_mistakes(available_teachers, available_rooms, generated_table)
    except Exception as e:
        return f"Error during generation: {str(e)} 🚨"

def custom_llama3_generate(available_teachers, available_rooms, basic_info, teacher_info, room_info, output_format):
    if len(available_teachers) > 60 or len(available_rooms) > 60:
        return "One or both of the DataFrames exceed the maximum row limit of 60. Cannot process the request."
    os.environ['GROQ_API_KEY'] = st.session_state['groq_api_key']
    api_key = os.environ.get("GROQ_API_KEY")

    client = initialize_groq_client(api_key)
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f'''
                    Act like a timetable generatorand you will generate a  correct and allign with requirements timetable.
                    As an expert assistant, your task is to create a timetable that efficiently assigns available rooms to teachers and students based on their free times. This timetable should be presented in a table format, clearly detailing who is free during each time interval and their assigned room.
                    Dont need to explain anything and generate any text explanation. I want the just table as an output according to following output format for gievn reqirements.
                    here is basic info that you will use to define the timetable and follow the time table format to generate table
                    basic_info:
                    {basic_info}
                    here is output format that you wil use to generate table.
                    Output Format:
                    {output_format}

                    Ensure the table is constructed with precise alignment to the given schedules, maintaining accurate correspondence between students and teachers as detailed in the data. Dont need to explain any irrelevant text explanation.
                    here is teacher, student and room information explanation
                    Schedules Provided:
                    - Teacher's Schedule: {teacher_info}
                    - Room's Schedule: {room_info}
                    
                    Please construct the table based on the following data:
                    Teacher's Schedule: {available_teachers}
                    Room's Schedule: {available_rooms}
                    
                    Use the following format to generate a response and dont need to add any irrelevant text explanation
                    OUTPUT FORMAT:
                    
                    {output_format}
                    '''
                }
            ],
            model="llama3-70b-8192",
        )
        response_content = chat_completion.choices[0].message.content
        return response_content
    except Exception as e:
        return f"An error occurred: {str(e)}"

def custom_openai_generate(available_teachers, available_rooms, basic_info, teacher_info, room_info, output_format):
    if len(available_teachers) > 100 or len(available_rooms) > 100:
        return "One or both of the DataFrames exceed the maximum row limit of 100. Cannot process the request."
    os.environ['OPENAI_API_KEY'] = st.session_state['openai_api_key']
    client_openai = OpenAI()
    system_role = f'''
    Act like a timetable generatorand you will generate a  correct and allign with requirements timetable.
    As an expert assistant, your task is to create a timetable that efficiently assigns available rooms to teachers and students based on their free times. This timetable should be presented in a table format, clearly detailing who is free during each time interval and their assigned room.
    Dont need to explain anything and generate any text explanation. I want the just table as an output according to following output format for gievn reqirements.
    here is basic info that you will use to define the timetable and follow the time table format to generate table
    basic_info:
    {basic_info}
    here is output format that you wil use to generate table.
    Output Format:
    {output_format}

    Ensure the table is constructed with precise alignment to the given schedules, maintaining accurate correspondence between students and teachers as detailed in the data. Dont need to explain any irrelevant text explanation.
    here is teacher, student and room information explanation
    Schedules Provided:
    - Teacher's Schedule: {teacher_info}
    - Room's Schedule: {room_info}
    
    Please construct the table based on the following data:
    Teacher's Schedule: {available_teachers}
    Room's Schedule: {available_rooms}
                    
                    '''
    input = f'''
    As an expert assistant, your task is to create a timetable that efficiently assigns available rooms to teachers and students based on their free times. This timetable should be presented in a table format, clearly detailing who is free during each time interval and their assigned room.
    Dont need to explain anything and generate any text explanation. I want the just table as an output according to following output format for gievn reqirements.
    here is basic info that you will use to define the timetable and follow the time table format to generate table
    basic_info:
    {basic_info}
    here is output format that you wil use to generate table.
    Output Format:
    {output_format}

    Ensure the table is constructed with precise alignment to the given schedules, maintaining accurate correspondence between students and teachers as detailed in the data. Dont need to explain any irrelevant text explanation.
    here is teacher, student and room information explanation
    Schedules Provided:
    - Teacher's Schedule: {teacher_info}
    - Room's Schedule: {room_info}
    
    Please construct the table based on the following data:
    Teacher's Schedule: {available_teachers}
    Room's Schedule: {available_rooms}
    
    Use the following format to generate a response and dont need to add any irrelevant text explanation
    OUTPUT FORMAT:
    
    {output_format}
    '''

    messages = [
        {"role": "system", "content": system_role},
        {"role": "user", "content": input}
    ]

    # Use the chat completion endpoint
    response = client_openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages
    )

    return response.choices[0].message.content

def custom_generate(available_teachers, available_rooms, basic_info, teacher_info, room_info, output_format, model_choice):
    try:
        if model_choice == 'Groq Model':
            return custom_llama3_generate(available_teachers, available_rooms, basic_info, teacher_info, room_info, output_format)
        elif model_choice == 'OpenAI Model':
            return custom_openai_generate(available_teachers, available_rooms, basic_info, teacher_info, room_info, output_format)
    except Exception as e:
        return f"Error during generation: {str(e)} 🚨"


def change_table_llama3_generate(available_teachers, available_rooms, generated_table, changing):
    if len(available_teachers) > 60 or len(available_rooms) > 60:
        return "One or both of the DataFrames exceed the maximum row limit of 60. Cannot process the request."
    os.environ['GROQ_API_KEY'] = st.session_state['groq_api_key']
    api_key = os.environ.get("GROQ_API_KEY")

    client = initialize_groq_client(api_key)
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f'''
    Generate a output table with marko=down and dont add any irrelevnt text explanation and i want the markdown format table and dont addd any irrelevant text explanation
    Act like a intelligent assistant to generate atimetable with given changings
    As an expert assistant, your task is to analyze the following changings and change the timetable with same syntax and dont need to explain any irrelevant text and just generate a timetable. I want to implement the following
    changing in the generated timetable and dont need to explain any text explanation and output should be tiemtable with following changing and here is raw data mention that we use to create a time table and you can use it as a context. I want to generate 
    a timetable with given changingchanges
    Changing that should be implemented:
    changing:
    {changing}
    Here is provided timetable that is generated for the given information of rooms and teachers and students.
    generated timetable:
    {generated_table}

    Information of students, teachers and rooms
    Analyze the following data:
    Teacher's Schedule: {available_teachers}
    Room's Schedule: {available_rooms}
                    '''
                }
            ],
            model="llama3-70b-8192",
        )
        response_content = chat_completion.choices[0].message.content
        return response_content
    except Exception as e:
        return f"An error occurred: {str(e)}"

def change_table_openai_generate(available_teachers, available_rooms, generated_table, changing):
    if len(available_teachers) > 100 or len(available_rooms) > 100:
        return "One or both of the DataFrames exceed the maximum row limit of 100. Cannot process the request."
    os.environ['OPENAI_API_KEY'] = st.session_state['openai_api_key']
    client_openai = OpenAI()
    system_role = f'''
    Act like a intelligent assistant to generate atimetable with given changings
    As an expert assistant, your task is to analyze the following changings and change the timetable with same syntax and dont need to explain any irrelevant text and just generate a timetable. I want to implement the following
    changing in the generated timetable and dont need to explain any text explanation and output should be tiemtable with following changing and here is raw data mention that we use to create a time table and you can use it as a context. I want to generate 
    a timetable with given changing
    Changing that should be implemented:
    changing:
    {changing}
    Here is provided timetable that is generated for the given information of rooms and teachers and students.
    generated timetable:
    {generated_table}

    Information of students, teachers and rooms
    Analyze the following data:
    Teacher's Schedule: {available_teachers}
    Room's Schedule: {available_rooms}
                    '''
    input = f'''
     As an expert assistant, your task is to analyze the following changings and change the timetable with same syntax and dont need to explain any irrelevant text and just generate a timetable. I want to implement the following
    changing in the generated timetable and dont need to explain any text explanation and output should be tiemtable with following changing and here is raw data mention that we use to create a time table and you can use it as a context. I want to generate 
    a timetable with given changing
    Changing that should be implemented:
    changing:
    {changing}
    Here is provided timetable that is generated for the given information of rooms and teachers and students.
    generated timetable:
    {generated_table}

    Information of students, teachers and rooms
    Analyze the following data:
    Teacher's Schedule: {available_teachers}
    Room's Schedule: {available_rooms}
                    '''

    messages = [
        {"role": "system", "content": system_role},
        {"role": "user", "content": input}
    ]

    # Use the chat completion endpoint
    response = client_openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages
    )

    return response.choices[0].message.content
def get_change_timetable(available_teachers, available_rooms, generated_table, changing, model_choice):
    try:
        if model_choice == 'Groq Model':
            return change_table_llama3_generate(available_teachers, available_rooms, generated_table, changing)
        elif model_choice == 'OpenAI Model':
            return change_table_openai_generate(available_teachers, available_rooms, generated_table, changing)
    except Exception as e:
        return f"Error during generation: {str(e)} 🚨"
# Streamlit app setup
st.set_page_config(page_title="Timetable Generator 🏫", page_icon="📅")
st.title('🏫 Timetable Generator 🏫')

# Sidebar for model options
with st.sidebar:
    st.header('Settings 🛠️')
    model_choice = st.selectbox('Select Model:', ('Groq Model', 'OpenAI Model'))
    if 'api_keys_set' not in st.session_state:
        st.session_state['api_keys_set'] = False

    if not st.session_state['api_keys_set']:
        st.session_state['groq_api_key'] = st.text_input('Enter Groq API Key', type="password")
        st.session_state['openai_api_key'] = st.text_input('Enter OpenAI API Key', type="password")
        if st.button('Set API Keys'):
            if st.session_state['groq_api_key'] and st.session_state['openai_api_key']:
                st.session_state['api_keys_set'] = True
                st.success('API Keys set successfully! 🗝️')
            else:
                st.error('Please enter both API keys. 🔑')


    if st.session_state.get('api_keys_set', False):
        # Navigation buttons with emojis
        if st.button('Read Me 📘'):
            st.session_state['page'] = 'Read Me'
        if st.button('Generate TimeTable 📚'):
            st.session_state['page'] = 'Generate TimeTable'
        if st.button('Generate Custom TimeTable 🛠️'):
            st.session_state['page'] = 'Generate Custom Time table'
        if st.button('Check Mistakes 🕵️'):
            st.session_state['page'] = 'Check Mistakes'
        if st.button('Recommendation 📈'):
            st.session_state['page'] = 'Recommendation'
        if st.button('Change Timetable 🔄'):
            st.session_state['page'] = 'Change TimeTable'

# Main page actions based on sidebar navigation
if 'page' in st.session_state:
    if st.session_state['page'] == 'Read Me':
        st.subheader('About the Timetable Generator 📘')
        st.markdown("""
           ## 📘 About the Timetable Generator
           The Timetable Generator is a versatile application designed to automate the creation, customization, and optimization of academic or organizational timetables. This tool is perfect for educational institutions, businesses, and any organizations needing structured scheduling solutions.

           ## 🔑 How to Use
           - **Set API Keys:** Start by entering your Groq and OpenAI API keys to activate the underlying models that power the timetable generation and optimization processes.
           - **Generate Timetable:** Simply upload your CSV files containing teacher and room data to automatically generate a comprehensive timetable.
           - **Generate Custom Timetable:** Tailor your timetable by providing additional parameters. This feature allows you to adjust the timetable based on specific needs and constraints.
           - **Check Mistakes:** Utilize the application to analyze your generated timetables for any potential scheduling conflicts or errors, ensuring optimal organization.
           - **Recommendation:** Get actionable insights and recommendations on how to optimize your timetable for maximum efficiency and effectiveness.
           - **Create New Timetable:** This new feature allows you to start from scratch, inputting data manually or uploading a timetable that meets new or changing requirements.

           ## 🌟 Features
           - **Easy CSV uploads:** Streamline data management with simple CSV uploads for teacher and room information.
           - **Real-time generation:** Leverage real-time processing to instantly generate and modify timetables with complete conflict detection and resolution.
           - **Customization options:** Adapt the timetable to meet unique organizational needs with extensive customization tools.
           - **Advanced AI integration:** Employ cutting-edge AI technologies from Groq and OpenAI to enhance the accuracy and efficiency of your timetables.

           This application is designed to simplify your scheduling tasks, reduce errors, and optimize resource allocation across your organization.
        """, unsafe_allow_html=True)


    elif st.session_state['page'] == 'Generate TimeTable':
        st.subheader('Upload Data and Generate Timetable 📚')
        teachers_file = st.file_uploader("Upload Teachers CSV 📚", type=['csv'])
        rooms_file = st.file_uploader("Upload Rooms CSV 🏢", type=['csv'])

        # Button to generate timetable
        if st.button('Generate Timetable 🚀', help="Click to generate the timetable using selected model"):
            if teachers_file and rooms_file:
                available_teachers = pd.read_csv(teachers_file)
                available_rooms = pd.read_csv(rooms_file)

                with st.spinner('Generating timetable 💭💭💭'):
                    results = generate(available_teachers, available_rooms, model_choice)
                    st.markdown(results)
            else:
                st.error('Please upload both CSV files and ensure all required fields are filled. 🚨')

    elif st.session_state['page'] == 'Generate Custom Time table':
        st.subheader('Generate a Custom Time Table 🛠️')

        # Define text areas with emoji in placeholder
        basic_info = st.text_area('Enter your basic info 📝', placeholder="Please enter at least 100 words...")
        teacher_info = st.text_area('Enter your teacher info 🧑‍🏫', placeholder="Please enter at least 100 words...")
        room_info = st.text_area('Enter your room info 🏢', placeholder="Please enter at least 100 words...")
        output_format = st.text_area('Enter your output format 🗂️', placeholder="Please enter at least 100 words...")

        teachers_file = st.file_uploader("Upload Teachers CSV 📚", type=['csv'])
        rooms_file = st.file_uploader("Upload Rooms CSV 🏢", type=['csv'])

        # Button to generate timetable
        if st.button('Generate Timetable 🚀', help="Click to generate the timetable using selected model"):
            # Check for file uploads and sufficient text length
            if teachers_file and rooms_file and all(
                    count_words(text) >= 100 for text in [basic_info, teacher_info, room_info, output_format]):
                available_teachers = pd.read_csv(teachers_file)
                available_rooms = pd.read_csv(rooms_file)

                with st.spinner('Generating timetable 💭'):
                    results = custom_generate(available_teachers, available_rooms, basic_info, teacher_info, room_info,
                                              output_format, model_choice)
                    st.success("Timetable generated successfully! 🎉")
                    st.markdown(results)
            else:
                error_message = 'Please upload both CSV files and ensure all required fields contain at least 100 words. 🚨'
                st.error(error_message)


    # Handling different pages based on user selection

    elif st.session_state['page'] == 'Check Mistakes':

        st.subheader('Check for Mistakes in the Timetable 🕵️')

        generated_table = st.text_area('Enter your generated timetable',
                                       placeholder="📄 Paste your timetable data here...")

        teachers_file = st.file_uploader("Upload Teachers CSV 📚", type=['csv'])

        rooms_file = st.file_uploader("Upload Rooms CSV 🏢", type=['csv'])

        if st.button('Get Mistakes 🕵️'):

            if teachers_file and rooms_file and generated_table:

                available_teachers = pd.read_csv(teachers_file)

                available_rooms = pd.read_csv(rooms_file)

                with st.spinner('Analyzing mistakes...'):

                    results = get_mistakes(available_teachers, available_rooms, generated_table, model_choice)

                    st.success("Analysis complete! Here are the findings: ✅")

                    st.markdown(results)

            else:

                st.error('Please upload both CSV files and provide the generated timetable text. 🚨')


    elif st.session_state['page'] == 'Recommendation':

        st.subheader('Get Recommendations for Timetable Optimization 📊')

        generated_table = st.text_area('Enter your generated timetable',
                                       placeholder="📄 Paste your timetable data here...")

        teachers_file = st.file_uploader("Upload Teachers CSV 📚", type=['csv'])

        rooms_file = st.file_uploader("Upload Rooms CSV 🏢", type=['csv'])

        if st.button('Get Recommendation 🚀'):

            if teachers_file and rooms_file and generated_table:

                available_teachers = pd.read_csv(teachers_file)

                available_rooms = pd.read_csv(rooms_file)

                with st.spinner('Generating recommendations...'):

                    results = get_recommendation(available_teachers, available_rooms, generated_table, model_choice)

                    st.success("Recommendations generated successfully! 🌟")

                    st.markdown(results)

            else:

                st.error('Please upload both CSV files and provide the generated timetable text. 🚨')


    elif st.session_state['page'] == 'Change TimeTable':

        st.subheader('Modify Timetable 🛠️')

        generated_table: str | None = st.text_area('Enter your generated timetable',
                                       placeholder="📄 Paste your timetable data here...")

        changes = st.text_area('Specify Changes to Apply', placeholder="🔄 Describe the changes to apply...")

        teachers_file = st.file_uploader("Upload Teachers CSV 📚", type=['csv'])

        rooms_file = st.file_uploader("Upload Rooms CSV 🏢", type=['csv'])

        if st.button('Apply Changes 🚀'):

            if teachers_file and rooms_file and generated_table and changes:

                available_teachers = pd.read_csv(teachers_file)

                available_rooms = pd.read_csv(rooms_file)

                with st.spinner('Applying changes to the timetable...'):
                    results = get_change_timetable(available_teachers, available_rooms, generated_table, changes, model_choice)


                    st.success("Timetable updated successfully! 🌟")

                    st.markdown(results)

            else:

                st.error(
                    'Please upload both CSV files, provide the generated timetable text, and describe the changes. 🚨')
else:
    if st.session_state.get('api_keys_set', False):
        st.write("Welcome! Please select an option from the sidebar. 🚀")
    else:
        st.write("Welcome to the Timetable Generator! Set the API keys to unlock the functionalities. 🔐")

