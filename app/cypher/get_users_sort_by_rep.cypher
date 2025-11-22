MATCH (u:USER)
RETURN u.user_name AS user_name, u.user_reputation AS user_reputation
ORDER BY u.user_reputation DESC