//
// Purpose: This query identifies common "commenting paths" or sequences of recipes that users comment on.
// It starts with a given recipe and finds all users who commented on it. Then, for those users, it reconstructs
// the chronological sequence of all other recipes they have commented on. Finally, it aggregates these paths
// to find sequences that are shared by more than one user, which can reveal common user journeys or interests.
//
// Returns:
// - commenting_path: A list of recipe names representing a chronological commenting sequence shared by multiple users.
// - user_count: The number of users who share this exact commenting path.
//

// Step 1: Find all users who commented on the initial target recipe.
MATCH (r1:RECIPE) <- [:BELONGS_TO] - (c1:COMMENT) - [:POSTED] - (u:USER)
WHERE r1.recipe_name = '{recipe}'

// Step 2: For those users, find all *other* recipes they have commented on.
MATCH (u)-[:POSTED]-(c2:COMMENT)-[:BELONGS_TO]->(r2:RECIPE)
// Ensure we are not re-matching the same comment or recipe from the first step.
WHERE c2 <> c1
AND r2 <> r1

// Step 3: For each user, gather all their comments (the initial one and all others) into a single collection.
// This is a data preparation step to facilitate chronological sorting.
WITH u.user_name AS user,
    r1.recipe_name AS recipe1,
    c1.created_at AS created1,
    // Collect all other comments into a list of objects, each containing the recipe name and comment timestamp.
    COLLECT({recipe: r2.recipe_name, created: c2.created_at}) AS other_comments

// Combine the initial comment with the list of other comments.
WITH user,
    [{recipe: recipe1, created: created1}] + other_comments AS comments

// Step 4: Unwind the collection and order the comments chronologically to build the user's path.
UNWIND comments AS c
WITH user, c.recipe AS recipe, c.created AS created
ORDER BY user, created

// Step 5: Re-aggregate the sorted recipes for each user to form their unique, ordered commenting path.
WITH user,
    // Collect the distinct recipe names in the order established by the previous clause.
    COLLECT(DISTINCT recipe) AS commenting_path

// Step 6: Group by the identical paths and count how many users share each one.
WITH commenting_path,
    COUNT(user) AS user_count
// Filter for paths shared by more than one user to find common behavioral patterns.
WHERE user_count > 1

// Step 7: Return the common paths and their corresponding user counts, ordered by popularity.
RETURN
    commenting_path,
    user_count
ORDER BY user_count DESC
;