CREATE VIEW dod_dashboard
AS
SELECT 
	wp.*,
	hf.controllable_expenses,
	hf.cost_of_sales,
	hf.occupancy_expenses,
	oa.main_course_total,
	oa.beverages_total,
	oa.desert_total
	
FROM weekly_planner wp

LEFT JOIN historical_finances hf
	ON wp.date = hf.date
	AND wp.account_id = hf.account_id
LEFT JOIN order_analyzer oa
	ON wp.date = oa.date
	AND wp.account_id = oa.account_id