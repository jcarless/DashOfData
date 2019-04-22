CREATE VIEW weekly_planner 
AS
SELECT
	DATE(checks.dining_date) as "date",
	SUM(checks.guests) as "guests",
	model_forecasts.guests as "guests_forecast",
	SUM(checks.total) as "revenue",
	checks.account_id
FROM checks
LEFT JOIN model_forecasts
	ON DATE(model_forecasts.forecast_date) = DATE(checks.dining_date)
	AND model_forecasts.model = 'sarimax'
	AND model_forecasts.target_variable = 'guests_log_diff'
	AND model_forecasts.parameter_id = 20
	
GROUP BY 
	DATE(checks.dining_date),
	DATE(model_forecasts.forecast_date),
	model_forecasts.guests,
	checks.account_id,
	model_forecasts.account_id
