import os
import boto3
import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine

PARQUET_DIR = "./parquet_files/"
DB_PASSWORD="MySecr3tPassWord"
DB_NAME="postgresdb"
DB_HOST="localhost"
DB_PORT="5432"
DB_USERNAME="postgres"
TABLE_NAME = "test_table"


DB_PASSWORD_DESTINATION="MySecr3tPassWordDESTINATION"
DB_NAME_DESTINATION="postgresdbDESTINATION"
DB_HOST_DESTINATION="localhostDESTINATION"
DB_PORT_DESTINATION="5432DESTINATION"
DB_USERNAME_DESTINATION="postgresDESTINATION"


S3_BUCKET_NAME = "demobucketplanit"
S3_OBJECT_KEY = "parquet_files/data.parquet"

os.makedirs(PARQUET_DIR, exist_ok=True)

def create_parquet_files():
    data = {
        "id": [5, 6, 7, 8],
        "name": ["chuñwa", "juluioi", "javier", "richard"],
        "age": [25, 20, 25, 24]
    }
    df = pd.DataFrame(data)
    parquet_path = os.path.join(PARQUET_DIR, "data.parquet")
    df.to_parquet(parquet_path, engine='pyarrow')
    print(f"Parquet file created at {parquet_path}")
    return parquet_path


def load_parquet_to_postgres(parquet_path):
    url_string = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(url_string)
    print(url_string[92:])
    engine = create_engine(url_string)
    conn = engine.connect()
    table = pq.read_table(parquet_path)
    df = table.to_pandas()
    df.to_sql(TABLE_NAME, conn, if_exists="append", index=False)
    print(f"Data loaded into PostgreSQL table '{TABLE_NAME}'")
    conn.close()


def upload_file_to_s3(file_path, bucket_name, object_key):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket_name, object_key)
        print(f"File uploaded to S3: s3://{bucket_name}/{object_key}")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")


if __name__ == "__main__":
    parquet_file = create_parquet_files()
    print('parquet file created')
    load_parquet_to_postgres(parquet_file)
    upload_file_to_s3(parquet_file, S3_BUCKET_NAME, S3_OBJECT_KEY)
