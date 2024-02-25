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


def collect_data(from_path):
    data = pd.read_csv(from_path)
    data = data[["Title", "Summary", "Content", "URL", "Contributor"]]
    return data

# print(collect_data('../documents/test.csv'))
