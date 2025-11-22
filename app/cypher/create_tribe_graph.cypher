/**
 * Header Comment: User Co-Comment Graph Projection
 * 
 * Purpose:
 * Creates a projected in-memory graph representation of user relationships based on shared recipe commenting.
 * This projection identifies users who comment on the same recipes and weights their connections by 
 * the number of recipes they both commented on.
 * 
 * Returns:
 * A projected graph named 'userCoComment' containing:
 * - Nodes: All users in the database
 * - Edges: Weighted connections between users who co-commented on recipes
 * - Edge Weight: Count of shared recipes commented on by both users
 * 
 * Use Case:
 * This graph can be used for community detection, user similarity analysis, and recommendation systems.
 */

CALL gds.graph.project.cypher(
  'userCoComment',
  // Node projection: Select all USER nodes and use their internal Neo4j IDs
  'MATCH (u:USER) RETURN id(u) AS id',
  // Relationship projection: Find user pairs connected through shared recipe comments
  'MATCH (u1:USER)-[:POSTED]-(:COMMENT)-[:BELONGS_TO]->(r:RECIPE)
    MATCH (u2:USER)-[:POSTED]-(:COMMENT)-[:BELONGS_TO]->(r) 
    WITH r, u1, u2 WHERE u1 <> u2  // Filter out self-loops (same user)
    RETURN id(u1) AS source, id(u2) AS target, count(r) AS weight'  // Weight = number of shared recipes
);