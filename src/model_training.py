# original training
from src.data_collecting import collect_data
from src.data_processing import get_chunked_data, process_data
from src.data_storing import store_data

data = collect_data('../documents/test.csv')
chunked_data = get_chunked_data(data)
process_data(chunked_data, '../documents/embedded_test.csv')
store_data('../documents/embedded_test.csv', 'test')

# data = collect_data('../documents/test.csv')
# chunked_data = get_chunked_data(data)
# process_data(chunked_data, '../documents/embedded_test.csv')
# store_data('../documents/embedded_test.csv', 'test')
