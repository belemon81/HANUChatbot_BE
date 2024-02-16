from data_processing import process_data
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
                embedding vector(256)
            );
        """)
    conn.commit()


def load_data(conn):
    with conn.cursor() as cur:
        doc_embeddings = process_data()
        for i, doc in enumerate(doc_embeddings):
            vector_list = list(doc_embeddings[i])  # Convert to list if an array type
            cur.execute("INSERT INTO embeddings (embedding) VALUES (%s)", (vector_list,))
    conn.commit()


def store_data():
    conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="localhost", port=23050)
    create_database(conn)
    conn = psycopg2.connect(database="hanu_chatbot", user="postgres", password="postgres", host="localhost", port=23050)
    create_extension(conn)
    create_table(conn)
    load_data(conn)


store_data()
