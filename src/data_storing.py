import numpy as np
import pandas as pd
import psycopg2

from pgvector.psycopg2 import register_vector


#  TODO: create database
def create_database(conn):
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'hanu_chatbot'")
        exists = cur.fetchone()
        if not exists:
            cur.execute("CREATE DATABASE hanu_chatbot")
            cur.execute("GRANT ALL PRIVILEGES ON DATABASE hanu_chatbot TO postgres")
    conn.autocommit = False


# TODO: create extension
def create_extension(conn):
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
    register_vector(conn)
    conn.commit()


# TODO: create table

def create_table(conn, table_name):
    with conn.cursor() as cur:
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id bigserial primary key,  
                content text, 
                embedding vector(256)
            );
        """)
    conn.commit()


# TODO: load data from file to tables
def load_data(conn, from_file, table_name):
    # process_data('../documents/embedded_test.csv', '../documents/embedded_test.csv')
    data = pd.read_csv(from_file)
    data_list = [(row['Combined'], np.array(eval(row['Embedding']))) for index, row in data.iterrows()]
    with conn.cursor() as cur:
        cur.executemany(f"""
            INSERT INTO {table_name} (content, embedding)
            VALUES (%s, %s)
            """, data_list)
    conn.commit()


# TODO: create index
def create_index(conn, table_name):
    with conn.cursor() as cur:
        cur.execute(f"""
            CREATE INDEX ON {table_name} USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
        """)
    conn.commit()


# TODO: store data
def store_data(from_file, table_name):
    conn = psycopg2.connect(database='postgres', user='postgres', password='postgres', host='localhost', port=23050)
    create_database(conn)
    conn = psycopg2.connect(database='hanu_chatbot', user='postgres', password='postgres', host='localhost', port=23050)
    create_extension(conn)

    create_table(conn, table_name)
    create_index(conn, table_name)
    load_data(conn, from_file, table_name)

# store_data('../documents/embedded_test.csv', 'test')
