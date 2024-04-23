import pandas as pd
import psycopg2

from pgvector.psycopg2 import register_vector


#  TODO: create database
def create_database(conn, database_name):
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (database_name,))
        exists = cur.fetchone()
        if not exists:
            cur.execute(f"CREATE DATABASE {database_name}")
            cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {database_name} TO postgres")
    conn.autocommit = False
    print(f"Database '{database_name}' created successfully!")


# TODO: initialize database
def init_database(database_name):
    postgres_conn = psycopg2.connect(database='postgres', user='postgres', password='postgres',
                                     host='localhost', port=5432)
    create_database(postgres_conn, database_name)
    postgres_conn.close()


# TODO: create extension
def create_extension(conn):
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
    register_vector(conn)
    conn.commit()
    print("Extension 'vector' created successfully!")


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
    print(f"Table '{table_name}' created successfully!")


# TODO: initialize table
def init_table(database_name, table_name):
    db_conn = psycopg2.connect(database=database_name, user='postgres', password='postgres',
                               host='localhost', port=5432)
    create_extension(db_conn)
    create_table(db_conn, table_name)
    create_index(db_conn, table_name)
    db_conn.close()


# TODO: create index
def create_index(conn, table_name):
    with conn.cursor() as cur:
        cur.execute(f"""
            CREATE INDEX ON {table_name} USING ivfflat (embedding vector_cosine_ops) WITH (lists = 10);
        """)
    conn.commit()
    print(f"Index for '{table_name}' created successfully!")


# TODO: load data from file to tables
def load_data(conn, from_file, table_name):
    data = pd.read_csv(from_file)
    data_list = [(row['Combined'], row['Embedding']) for index, row in data.iterrows()]
    with conn.cursor() as cur:
        cur.executemany(f"""
            INSERT INTO {table_name} (content, embedding)
            VALUES (%s, %s)
            """, data_list)
    conn.commit()
    print(f"-----Stored embeddings from {from_file} to table '{table_name}'!")


# TODO: store data to table in database
def store_data(from_file, database_name, table_name):
    db_conn = psycopg2.connect(database=database_name, user='postgres', password='postgres',
                               host='localhost', port=5432)
    load_data(db_conn, from_file, table_name)
    db_conn.close()
