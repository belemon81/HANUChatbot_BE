import pandas as pd


# def collect_data():
#     with open('../documents/test.txt', 'r') as f:
#         text = f.read()
#     paragraphs = text.split('\n')
#     documents = []
#     for paragraph in paragraphs:
#         if paragraph.strip():
#             documents.append(paragraph)
#     return documents


# TODO: collect data from csv file
def collect_data(from_file):
    data = pd.read_csv(from_file)
    data = data[['Title', 'Summary', 'Content', 'URL', 'Contributor']]
    print("Collected data from " + from_file)
    return data

# print(collect_data('../documents/test.csv'))
