# original training
import os

from src.data_collecting import collect_data
from src.data_processing import get_chunked_data, process_data
from src.data_storing import store_data, init_database

# create directory to store embedded data (for referring)
try:
    os.makedirs('../documents/embedded_data')
    print("Directory for embedded data created successfully!")
except FileExistsError:
    print("Directory for embedded data already exists.")
# init database
init_database('hanu_chatbot', 'test')
# train model
directory_path = '../documents/test'
csv_files = [os.path.join(directory_path, filename) for filename in os.listdir(directory_path) if
             filename.endswith(".csv")]
for csv_file in csv_files:
    data = collect_data(csv_file)
    chunked_data = get_chunked_data(data)

    filepath, extension = os.path.splitext(csv_file)
    filename = os.path.basename(filepath)
    new_file = os.path.join('../documents/embedded_data', f'{filename}_embedded{extension}')
    process_data(chunked_data, new_file)

    store_data(new_file, 'hanu_chatbot', 'test')
