import pandas as pd
import tiktoken

from src.openai_client import client


# Calculate cost of embedding num_tokens: https://openai.com/pricing
# def get_embedding_cost(num_tokens):
#     return num_tokens / 1000000 * 0.5 # gpt-3.5-turbo


# Calculate total cost of embedding all content in the dataframe
# def get_total_embeddings_cost(documents):
#     total_tokens = 0
#     for doc in documents:
#         total_tokens += num_tokens_from_string(doc)
#     total_cost = get_embedding_cost(total_tokens)
#     return total_cost

# TODO: get number of tokens from a text
def get_num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


# TODO: chunk data to specific length of tokens
def get_chunked_data(data, max_tokens=666):  # ~ 500 words
    chunks = []
    ideal_size = int(max_tokens // (4 / 3))  # 1 token ~ 3/4 of a word

    for i in range(len(data.index)):
        content = data['Content'][i]
        token_len = get_num_tokens_from_string(content)
        if token_len <= max_tokens:
            chunks.append([data['Title'][i],
                           data['Summary'][i],
                           content,
                           data['URL'][i],
                           data['Contributor'][i]])
        else:
            # calculate total chunks can be split
            words = content.split()
            words = [w for w in words if w != ' ']
            total_words = len(words)
            chunks_len = total_words // ideal_size
            if total_words % ideal_size != 0:
                chunks_len += 1

            # split to chunks where chunk(start;end)
            start = 0
            end = ideal_size
            for j in range(chunks_len):
                if end > total_words:
                    end = total_words

                new_content = words[start:end]
                new_content_string = ' '.join(new_content)  # include ' ' again
                new_content_token_len = get_num_tokens_from_string(new_content_string)

                if new_content_token_len > 0:
                    chunks.append([data['Title'][i],
                                   data['Summary'][i],
                                   new_content_string,
                                   data['URL'][i],
                                   data['Contributor'][i]])

                start += ideal_size
                end += ideal_size
    print(f"-Chunked data content to {chunks.__len__()} chunks! (max: {max_tokens} tokens/chunk)")
    return pd.DataFrame(chunks, columns=['Title', 'Summary', 'Content', 'URL', 'Contributor'])


#  TODO: get embedding
def get_embedding(text, model='text-embedding-3-small'):
    text = text.replace('\n', ' ')
    return client.embeddings.create(input=[text], model=model, encoding_format='float').data[0].embedding[:256]


# TODO: combine values from multiple columns in data to one columns
def combine_values(row):
    combined_parts = []
    for col in row.index:
        value = row[col]
        if not pd.isna(value):
            combined_parts.append(f'{col}: {value}')
    return '\n'.join(combined_parts)


# TODO: process data and save to file
def process_data(data, to_file):
    # combined content with title, summary, url, and contributor
    data['Combined'] = data.apply(combine_values, axis=1)
    print("--Combined minor details to data content! (title, summary, url, contributor)")  # tokens varies under 1000

    data['Embedding'] = data.Combined.apply(lambda text: get_embedding(text))
    print("---Got embeddings of data from OPENAI client!")

    data.to_csv(to_file, index=False, encoding="utf-8")
    print(f"----Saved embeddings to {to_file}!")

# data = collect_data('../documents/test.csv')
# process_data(data, '../documents/embedded_test.csv')
# data = pd.read_csv('../documents/embedded_test.csv')
# print(data)
