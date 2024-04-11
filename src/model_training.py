# original training
import os

from src.data_collecting import collect_data
from src.data_processing import get_chunked_data, process_data
from src.data_storing import store_data, init_database, init_table


# TODO: prepare database and directory (for embeddings)
def prepare(database_name):
    # create directory to store embedded data (for later reference)
    try:
        os.makedirs('..\\documents\\embedded_data')
        print("Directory for embedded data created successfully!")
    except FileExistsError:
        print("Directory for embedded data already exists.")

    # init database and tables
    init_database(database_name)


# TODO: load corpus and save it to vector database
def load_corpus(database_name, chatbot_name):
    # init table to store data embedded
    init_table(database_name, chatbot_name)
    # get all files in folder
    directory_path = '..\\documents\\' + chatbot_name  # e.g. folder ../documents/educational_program
    csv_files = [os.path.join(directory_path, filename) for filename in os.listdir(directory_path) if
                 filename.endswith(".csv")]
    for csv_file in csv_files:
        data = collect_data(csv_file)
        chunked_data = get_chunked_data(data)
        # store embedded data to new file (for later reference)
        filepath, extension = os.path.splitext(csv_file)
        filename = os.path.basename(filepath)
        new_file = os.path.join('..\\documents\\embedded_data', f'{filename}_embedded{extension}')
        process_data(chunked_data, new_file)
        store_data(new_file, database_name, chatbot_name)


prepare('hanu_chatbot')
load_corpus('hanu_chatbot', 'educational_program')
# load_corpus('hanu_chatbot', 'public_administration')





