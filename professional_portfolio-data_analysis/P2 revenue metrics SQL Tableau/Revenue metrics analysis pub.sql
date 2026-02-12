WITH base_data AS (
	SELECT gp.user_id,
		gp.payment_date,
		DATE_TRUNC('month', gp.payment_date)::DATE AS payment_month,
		gp.game_name,
		gp.revenue_amount_usd,
		gpu.language,
		gpu.has_older_device_model AS old_device,
		gpu.age::INT AS age,
		MIN(gp.payment_date) OVER (PARTITION BY gp.user_id) AS first_payment_date,
		MAX(gp.payment_date) OVER (PARTITION BY gp.user_id) AS last_payment_date
	FROM project.games_payments gp
		LEFT JOIN project.games_paid_users gpu ON gp.user_id = gpu.user_id
),
monthly_revenue AS (
	SELECT user_id,
		payment_month,
		game_name,
		(last_payment_date - first_payment_date)::INT AS lifetime_days,
		SUM(revenue_amount_usd) AS revenue,
		language,
		old_device,
		age
	FROM base_data
	GROUP BY user_id,
		payment_month,
		game_name,
		last_payment_date,
		first_payment_date,
		language,
		old_device,
		age
),
periods AS (
	SELECT user_id,
		payment_month,
		revenue,
		DATE(payment_month - INTERVAL '1' MONTH) AS previous_month,
		DATE(payment_month + INTERVAL '1' MONTH) AS next_month,
		LAG(revenue, 1) OVER (
			PARTITION BY user_id
			ORDER BY payment_month
		) AS past_month_revenue,
		LAG(payment_month, 1) OVER (
			PARTITION BY user_id
			ORDER BY payment_month
		) AS past_paid_month,
		LEAD(payment_month) OVER (
			PARTITION BY user_id
			ORDER BY payment_month
		) AS next_paid_month
	FROM monthly_revenue
),
metrics AS (
	SELECT user_id,
		payment_month,
		revenue as total_revenue,
		FIRST_VALUE(payment_month) OVER (
			PARTITION BY user_id
			ORDER BY payment_month
		) AS first_payment_month,
		COALESCE(
			CASE
				WHEN past_paid_month IS NULL THEN 1
			END,
			0
		) AS new_paid_users,
		CASE
			WHEN past_paid_month IS NULL THEN revenue
		END AS new_mrr,
		CASE
			WHEN next_paid_month IS NULL
			OR next_paid_month != next_month THEN 1
		END AS churned_users,
		CASE
			WHEN next_paid_month IS NULL
			OR next_paid_month != next_month THEN revenue
		END AS churned_revenue,
		CASE
			WHEN past_paid_month = previous_month
			AND revenue > past_month_revenue THEN revenue - past_month_revenue
		END AS expansion_revenue,
		CASE
			WHEN past_paid_month = previous_month
			AND revenue < past_month_revenue THEN revenue - past_month_revenue
		END AS contraction_revenue
	FROM periods
)
SELECT mr.user_id,
	mr.game_name,
	mr.lifetime_days,
	mr.payment_month,
	me.first_payment_month,
	me.total_revenue as mrr,
	me.new_paid_users,
	me.new_mrr,
	me.churned_users,
	me.churned_revenue,
	me.expansion_revenue,
	me.contraction_revenue,
	mr.language,
	mr.old_device,
	mr.age
FROM metrics me
	LEFT JOIN monthly_revenue mr ON me.user_id = mr.user_id
	AND me.payment_month = mr.payment_month
ORDER BY user_id,
	payment_month;