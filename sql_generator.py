
from langchain_ollama import ChatOllama
from sqlalchemy import inspect
from database import engine

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


def generate_sql(question):
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        schema = ""

        for table in tables:
            columns = inspector.get_columns(table)
            column_names = [
                column["name"] for column in columns
            ]

            schema += (
                f"\nTable: {table}\n"
                f"Columns: {', '.join(column_names)}\n"
            )

        prompt = f"""
You are an expert MySQL SQL developer.

Database schema:
{schema}

Convert this English question into a MySQL SELECT query.

Rules:
1. Generate only SELECT queries.
2. Use only the tables and columns in the schema.
3. Do not generate INSERT, UPDATE, DELETE or DROP queries.
4. Return only the SQL query without explanation.

Question: {question}

SQL Query:
"""

        response = llm.invoke(prompt)

        sql_query = response.content.strip()
        sql_query = sql_query.replace("```sql", "")
        sql_query = sql_query.replace("```", "")

        return sql_query.strip()

    except Exception as error:
        print("SQL Generation Error:", error)
        raise error


if __name__ == "__main__":
    question = input("Enter your English question: ")

    result = generate_sql(question)

    print("\nGenerated SQL Query:")
    print(result)


