
import streamlit as st
from sqlalchemy import text
from database import engine
from sql_generator import generate_sql

# Configure Streamlit Page
st.set_page_config(
    page_title="AI SQL Query Helper",
    page_icon="🤖",
    layout="wide"
)

# Project Title
st.title("🤖 AI-Powered English to SQL Query Generator")

st.write(
    "Convert English questions into SQL queries "
    "and retrieve results from your MySQL database."
)

st.divider()

# User Input
st.subheader("Ask Your Database")

question = st.text_input(
    "Enter your question:",
    placeholder="Show all employees earning more than 50000"
)

# Generate SQL Button
if st.button("Generate SQL", type="primary"):

    if question.strip():

        try:
            # Generate SQL Query
            with st.spinner("Generating SQL..."):
                sql_query = generate_sql(question)

            # Display SQL Query
            st.subheader("Generated SQL")
            st.code(sql_query, language="sql")

            # Basic SELECT Check
            normalized_sql = sql_query.strip().rstrip(";")

            if not normalized_sql.upper().startswith("SELECT"):

                st.error("Only SELECT queries are allowed.")

            else:

                # Execute SQL Query
                with st.spinner("Executing query..."):

                    with engine.connect() as connection:

                        result = connection.execute(
                            text(normalized_sql)
                        )

                        rows = result.fetchall()
                        columns = result.keys()

                # Display Result
                st.subheader("Query Result")

                if rows:

                    result_data = [
                        dict(zip(columns, row))
                        for row in rows
                    ]

                    st.dataframe(
                        result_data,
                        use_container_width=True
                    )

                    st.success(
                        f"Query executed successfully! "
                        f"{len(rows)} rows returned."
                    )

                else:

                    st.info("No records found.")

        except Exception as error:

            st.error(f"Error: {error}")

    else:

        st.warning("Please enter a question.")

# Footer
st.divider()

st.caption(
    "Python | MySQL | LangChain | OpenAI API"
)

