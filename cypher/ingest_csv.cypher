:param {
  // Define the file path root and the individual file names required for loading.
  // https://neo4j.com/docs/operations-manual/current/configuration/file-locations/
  file_path_root: 'file:///', // Change this to the folder your script can access the files at.
  file_0: 'recipe.csv',
  file_1: 'user.csv',
  file_2: 'comment.csv'
};

// CONSTRAINT creation
// -------------------
//
// Create node uniqueness constraints, ensuring no duplicates for the given node label and ID property exist in the database. This also ensures no duplicates are introduced in future.
//
// NOTE: The following constraint creation syntax is generated based on the current connected database version 2025.7.1.
CREATE CONSTRAINT `comment_id_COMMENT_uniq` IF NOT EXISTS
FOR (n: `COMMENT`)
REQUIRE (n.`comment_id`) IS UNIQUE;
CREATE CONSTRAINT `recipe_code_RECIPE_uniq` IF NOT EXISTS
FOR (n: `RECIPE`)
REQUIRE (n.`recipe_code`) IS UNIQUE;
CREATE CONSTRAINT `user_id_USER_uniq` IF NOT EXISTS
FOR (n: `USER`)
REQUIRE (n.`user_id`) IS UNIQUE;

:param {
  idsToSkip: []
};

// NODE load
// ---------
//
// Load nodes in batches, one node label at a time. Nodes will be created using a MERGE statement to ensure a node with the same label and ID property remains unique. Pre-existing nodes found by a MERGE statement will have their other properties set to the latest values encountered in a load file.
//
// NOTE: Any nodes with IDs in the 'idsToSkip' list parameter will not be loaded.
LOAD CSV WITH HEADERS FROM ($file_path_root + $file_2) AS row
WITH row
WHERE NOT row.`comment_id` IN $idsToSkip AND NOT row.`comment_id` IS NULL
CALL {
  WITH row
  MERGE (n: `COMMENT` { `comment_id`: row.`comment_id` })
  SET n.`comment_id` = row.`comment_id`
  SET n.`recipe_code` = toInteger(trim(row.`recipe_code`))
  SET n.`user_id` = row.`user_id`
  SET n.`created_at` = toInteger(trim(row.`created_at`))
  SET n.`reply_count` = toInteger(trim(row.`reply_count`))
  SET n.`thumbs_up` = toInteger(trim(row.`thumbs_up`))
  SET n.`thumbs_down` = toInteger(trim(row.`thumbs_down`))
  SET n.`stars` = toInteger(trim(row.`stars`))
  SET n.`best_score` = toInteger(trim(row.`best_score`))
  SET n.`text` = row.`text`
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_0) AS row
WITH row
WHERE NOT row.`recipe_code` IN $idsToSkip AND NOT toInteger(trim(row.`recipe_code`)) IS NULL
CALL {
  WITH row
  MERGE (n: `RECIPE` { `recipe_code`: toInteger(trim(row.`recipe_code`)) })
  SET n.`recipe_code` = toInteger(trim(row.`recipe_code`))
  SET n.`recipe_number` = toInteger(trim(row.`recipe_number`))
  SET n.`recipe_name` = row.`recipe_name`
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_1) AS row
WITH row
WHERE NOT row.`user_id` IN $idsToSkip AND NOT row.`user_id` IS NULL
CALL {
  WITH row
  MERGE (n: `USER` { `user_id`: row.`user_id` })
  SET n.`user_id` = row.`user_id`
  SET n.`user_name` = row.`user_name`
  SET n.`user_reputation` = toInteger(trim(row.`user_reputation`))
} IN TRANSACTIONS OF 10000 ROWS;


// RELATIONSHIP load
// -----------------
//
// Load relationships in batches, one relationship type at a time. Relationships are created using a MERGE statement, meaning only one relationship of a given type will ever be created between a pair of nodes.
LOAD CSV WITH HEADERS FROM ($file_path_root + $file_2) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `USER` { `user_id`: row.`user_id` })
  MATCH (target: `COMMENT` { `comment_id`: row.`comment_id` })
  MERGE (source)-[r: `POSTED`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_2) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `COMMENT` { `comment_id`: row.`comment_id` })
  MATCH (target: `RECIPE` { `recipe_code`: toInteger(trim(row.`recipe_code`)) })
  MERGE (source)-[r: `BELONGS_TO`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;
