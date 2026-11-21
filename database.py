
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load Environment Variables
load_dotenv()

# MySQL Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "company_db")

# Database Connection URL
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Create Database Engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# Test Database Connection
def test_connection():

    try:

        with engine.connect() as connection:

            connection.execute(text("SELECT 1"))

        print("MySQL Database Connected Successfully!")

        return True

    except Exception as error:

        print("Database Connection Failed!")
        print(error)

        return False


# Execute SQL Query
def execute_query(sql_query):

    try:

        normalized_sql = sql_query.strip().rstrip(";")

        if not normalized_sql.upper().startswith("SELECT"):

            raise ValueError(
                "Only SELECT queries are allowed."
            )

        with engine.connect() as connection:

            result = connection.execute(
                text(normalized_sql)
            )

            rows = result.fetchall()
            columns = result.keys()

            return [
                dict(zip(columns, row))
                for row in rows
            ]

    except Exception as error:

        print("Query Execution Error:", error)

        return None


# Run Database Connection Test
if __name__ == "__main__":

    test_connection()

