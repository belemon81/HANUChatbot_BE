import pandas as pd

from src.test import client


# import tiktoken


# def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
#     encoding = tiktoken.get_encoding(encoding_name)
#     num_tokens = len(encoding.encode(string))
#     return num_tokens


# Calculate cost of embedding num_tokens: https://openai.com/pricing
# def get_embedding_cost(num_tokens):
#     return num_tokens / 1000 * 0.0005


# Calculate total cost of embedding all content in the dataframe
# def get_total_embeddings_cost(documents):
#     total_tokens = 0
#     for doc in documents:
#         total_tokens += num_tokens_from_string(doc)
#     total_cost = get_embedding_cost(total_tokens)
#     return total_cost


# def normalize_l2(x):
#     x = np.array(x)
#     if x.ndim == 1:
#         norm = np.linalg.norm(x)
#         if norm == 0:
#             return x
#         return x / norm
#     else:
#         norm = np.linalg.norm(x, 2, axis=1, keepdims=True)
#         return np.where(norm == 0, x, x / norm)


def get_embedding(text, model='text-embedding-3-small'):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model, encoding_format="float").data[0].embedding[:256]


def combine_values(row):
    combined_parts = []
    for col in row.index:
        value = row[col]
        if not pd.isna(value):
            combined_parts.append(f"{col}: {value}")
    return "; ".join(combined_parts)


def process_data(data, to_path):
    data['Combined'] = data.apply(combine_values, axis=1)
    data['Embedding'] = data.Content.apply(lambda text: get_embedding(text))
    data.to_csv(to_path, index=False)

# data = collect_data('../documents/test.csv')
# process_data(data, '../documents/embedded_test.csv')
# data = pd.read_csv('../documents/embedded_test.csv')
# print(data)
