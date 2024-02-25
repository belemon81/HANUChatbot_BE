import numpy as np
import pandas as pd
import psycopg2

from pgvector.psycopg2 import register_vector


def create_database(conn):
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'hanu_chatbot'")
        exists = cur.fetchone()
        if not exists:
            cur.execute("CREATE DATABASE hanu_chatbot")
            cur.execute("GRANT ALL PRIVILEGES ON DATABASE hanu_chatbot TO postgres")
    conn.autocommit = False


def create_extension(conn):
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
    register_vector(conn)
    conn.commit()


def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
                id bigserial primary key,  
                content text, 
                embedding vector(256)
            );
        """)
    conn.commit()


def load_data(conn, path):
    # process_data('../documents/embedded_test.csv', '../documents/embedded_test.csv')
    data = pd.read_csv(path)
    data_list = [(row['Combined'], np.array(eval(row['Embedding']))) for index, row in data.iterrows()]
    with conn.cursor() as cur:
        cur.executemany("""
            INSERT INTO embeddings (content, embedding)
            VALUES (%s, %s)
            """, data_list)
    conn.commit()


def create_index(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE INDEX ON embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
        """)
    conn.commit()


def store_data(from_path):
    conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="localhost", port=23050)
    create_database(conn)
    conn = psycopg2.connect(database="hanu_chatbot", user="postgres", password="postgres", host="localhost", port=23050)
    create_extension(conn)
    create_table(conn)
    create_index(conn)
    load_data(conn, from_path)


store_data('../documents/embedded_test.csv')
