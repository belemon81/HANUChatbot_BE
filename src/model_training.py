from src.data_collecting import collect_data
from src.data_processing import process_data
from src.data_storing import store_data

# original training
data = collect_data('../documents/test.csv')
process_data(data, '../documents/embedded_test.csv')
store_data('../documents/embedded_test.csv')

# new data layer
# new_data = collect_data('../documents/new_test.csv')
# process_data(new_data, '../documents/new_embedded_test.csv')
