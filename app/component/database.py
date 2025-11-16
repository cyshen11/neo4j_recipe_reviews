from neo4j import GraphDatabase

class Database():
    def __init__(self, uri: str,username: str, password: str):
        self.driver = GraphDatabase.driver(
            uri=uri
            ,auth=(username, password)
        )

    def generate_query(self, cypher_filename: str):
        try:
            with open(f'cypher/{cypher_filename}', 'r') as file:
                query = file.read()
            return query
        except FileNotFoundError:
            print(f"Error: The file '{cypher_filename}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def run_cypher(self, query: str, database: str) -> dict:
        with self.driver.session() as session:
            results = session.run(query=query, database=database)
            df = results.to_df()
        return df
        