SELECT 
	DATE(ch.dining_date) as date,
	c.account_id,
	SUM(CASE WHEN course_type
		IN('other')
		THEN c.total 
		END) AS "main_course_total",
	SUM(CASE WHEN course_type
		IN('beverages')
		THEN c.total
		END) AS "beverages_total",
	SUM(CASE WHEN course_type
		IN('dessert')
		THEN c.total 
		END) AS "desert_total"
FROM courses c
LEFT JOIN checks ch
	ON c.check_id = ch.check_id
GROUP BY 
	DATE(ch.dining_date),
	c.account_id