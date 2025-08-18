from neo4j import GraphDatabase

class Database():
    def __init__(self, uri: str,username: str, password: str):
        self.driver = GraphDatabase.driver(
            uri=uri
            ,auth=(username, password)
        )

    def run_cypher(self, cypher_filename: str, database: str):
        try:
            with open(f'cypher/{cypher_filename}', 'r') as file:
                query = file.read()

            return self.driver.execute_query(
                query_=query
                ,database=database
            ) 
        except FileNotFoundError:
            print(f"Error: The file '{cypher_filename}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        