What kinds of analytics question can be answered with this graph data model? 

- Nodes 
    - COMMENT
        - created_at: time at which the comment was posted as unix timestamp 
        - reply_count: number of replies to the comment
        - thumbs_up: number of up-votes the comment has received
        - thumbs_down: number of down-votes the comment has received 
        - stars: the score on a 1 to 5 scale that the user gave to the recipe. A score of 0 means that no score was given
        - best_score: score of the comment, likely used by the site the help determine the order the comments appear in
        - text: the text content of the comment	
    - RECIPE
        - recipe_number: placement of the recipe on the top 100 recipes list
        - recipe_name: name of the recipe the comment was posted on
    - USER
        - user_name: name of the user
        - user_reputation: internal score of the site, roughly roughly quantifying the past behaviour of the user

- Relationships
    - USER - [POSTED] -> COMMENT
    - COMMENT - [BELONGS_TO] -> RECIPE