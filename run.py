import os
from langchain_community.chat_models import ChatOllama
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

def main():
    """
    Main function to set up and run the LangChain SQL Agent with a local Ollama model.
    """
    # --- 1. Define Database ---
    # The path to the SQLite database file created by the previous script.
    db_file = "music_library.db"

    # Check if the database file exists.
    if not os.path.exists(db_file):
        print(f"Error: Database file '{db_file}' not found.")
        print("Please run the 'create_dummy_db_script.py' first to create it.")
        return

    # Connect to the database
    db_uri = f"sqlite:///{db_file}"
    db = SQLDatabase.from_uri(db_uri)
    print(f"Connected to database: {db_uri}")
    print(f"Tables found: {db.get_usable_table_names()}")
    print("-" * 50)


    # --- 2. Instantiate LLM ---
    # Set up the connection to your local Ollama instance.
    # We now use ChatOllama to make the model compatible with the agent type.
    try:
        llm = ChatOllama(model="steamdj/mistral-cpu-only", base_url="http://localhost:11434")
        print("Ollama ChatOllama model has been instantiated.")
    except Exception as e:
        print(f"Error instantiating Ollama LLM. Is Ollama running? Error: {e}")
        return
    print("-" * 50)


    # --- 3. Create SQL Agent ---
    # This combines the LLM with the database connection and provides it with tools.
    # 'verbose=True' lets you see the agent's thought process in the terminal.
    agent_executor = create_sql_agent(
        llm=llm,
        db=db,
        agent_type="openai-tools",  # This agent type expects a Chat Model
        verbose=True
    )
    print("SQL Agent created successfully.")
    print("-" * 50)


    # --- 4. Interact with the Agent ---
    # Now you can ask questions in natural language.
    print("--- Starting Interaction ---")
    
    try:
        question0 = "Siapa yang kamu  kenal sebagai artis yang memiliki album 'A Night at the Opera'?"
        result0 = agent_executor.invoke({"input": question0})
        print("\n> Final Answer:", result0.get("output", "No output found."))

        # Example Question 1
        question1 = "How many artists are in the database?"
        result1 = agent_executor.invoke({"input": question1})
        print("\n> Final Answer:", result1.get("output", "No output found."))

        print("-" * 50)

        # Example Question 2
        question2 = "List the albums by Queen. How many are there?"
        result2 = agent_executor.invoke({"input": question2})
        print("\n> Final Answer:", result2.get("output", "No output found."))

        print("-" * 50)
        
        # Example Question 3
        question3 = "Which track is the longest in milliseconds? Which artist is it by?"
        result3 = agent_executor.invoke({"input": question3})
        print("\n> Final Answer:", result3.get("output", "No output found."))
        

    except Exception as e:
        print(f"\nAn error occurred while running the agent: {e}")


if __name__ == '__main__':
    main()
