def collect_data():
    with open('../documents/test.txt', 'r') as f:
        text = f.read()
    paragraphs = text.split('\n')
    documents = []
    for paragraph in paragraphs:
        if paragraph.strip():
            documents.append(paragraph)

    return documents


# print(collect_data())
