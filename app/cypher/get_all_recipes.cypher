/**
 * Header Comment: Retrieve All Recipes
 * 
 * Purpose:
 * Fetches all recipes from the database in alphabetical order.
 * This query provides a simple way to explore the recipe catalog and is useful for 
 * data validation, exploratory data analysis, and understanding the recipe domain.
 * 
 * Returns:
 * A sorted list of all recipe names in the database.
 * - Column: recipe_name (string) - The name of each recipe
 */

// Query all RECIPE nodes and extract their recipe_name property
MATCH (r:RECIPE) RETURN r.recipe_name AS recipe_name 
// Sort results alphabetically for easier exploration and comparison
ORDER BY recipe_name;