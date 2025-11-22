// create a projected user-user co-comment graph using Cypher projection
CALL gds.graph.project.cypher(
  'userCoComment',
  'MATCH (u:USER) RETURN id(u) AS id',
  'MATCH (u1:USER)-[:POSTED]-(:COMMENT)-[:BELONGS_TO]->(r:RECIPE)
    MATCH (u2:USER)-[:POSTED]-(:COMMENT)-[:BELONGS_TO]->(r) 
    WITH r, u1, u2 WHERE u1 <> u2
    RETURN id(u1) AS source, id(u2) AS target, count(r) AS weight'
);