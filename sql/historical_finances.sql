SELECT 
	DATE("timestamp") as "date",
	SUM(CASE WHEN "master_category"
	    IN ('controllable expenses')
	    THEN transactions.total
	    END) AS "controllable_expenses",
	SUM(CASE WHEN "master_category"
	    IN ('cost of sales')
	    THEN transactions.total
	    END) AS "cost_of_sales",
    SUM(CASE WHEN "master_category"
	    IN ('occupancy costs')
	    THEN transactions.total
	    END) AS "occupancy_expenses",
	account_id
FROM transactions
GROUP BY 
	DATE("timestamp"), 
	account_id