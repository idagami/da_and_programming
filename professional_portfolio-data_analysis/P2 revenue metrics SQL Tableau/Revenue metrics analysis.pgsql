-- good working code, monthly grouping
WITH monthly_revenue AS (
	SELECT gp.user_id,
		DATE_TRUNC('month', payment_date)::DATE as payment_month,
		gp.game_name,
		SUM(revenue_amount_usd) AS revenue,
		gpu.language,
		gpu.has_older_device_model AS old_device,
		gpu.age::INT AS age
	FROM project.games_payments gp
		LEFT JOIN project.games_paid_users gpu ON gp.user_id = gpu.user_id
	GROUP BY 1,
		2,
		3,
		5,
		6,
		7
	ORDER BY 1,
		2,
		3
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
SELECT mr.payment_month,
	SUM(me.total_revenue) as mrr,
	SUM(me.new_paid_users) as new_paid_users,
	SUM(me.new_mrr) as new_mrr,
	SUM(me.churned_users) AS churned_users,
	SUM(me.churned_revenue) AS churned_revenue,
	SUM(me.expansion_revenue) AS expansion_revenue,
	SUM(me.contraction_revenue) AS contraction_revenue
FROM metrics me
	LEFT JOIN monthly_revenue mr ON me.user_id = mr.user_id
	AND me.payment_month = mr.payment_month
GROUP BY 1
ORDER BY mr.payment_month;



-- good working code, userly grouping
WITH monthly_revenue AS (
	SELECT gp.user_id,
		DATE(payment_date) as paym_date,
		DATE_TRUNC('month', payment_date)::DATE as payment_month,
		gp.game_name,
		SUM(revenue_amount_usd) AS revenue,
		gpu.language,
		gpu.has_older_device_model AS old_device,
		gpu.age::INT AS age
	FROM project.games_payments gp
		LEFT JOIN project.games_paid_users gpu ON gp.user_id = gpu.user_id
	GROUP BY 1,
		2,
		3,
		4,
		6,
		7,
		8
	ORDER BY 1,
		2,
		3
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
	paym_date,
	mr.payment_month,
	me.first_payment_month,
	SUM(me.total_revenue) as mrr,
	SUM(me.new_paid_users) as new_paid_users,
	SUM(me.new_mrr) as new_mrr,
	SUM(me.churned_users) AS churned_users,
	SUM(me.churned_revenue) AS churned_revenue,
	SUM(me.expansion_revenue) AS expansion_revenue,
	SUM(me.contraction_revenue) AS contraction_revenue,
	mr.language,
	mr.old_device,
	mr.age
FROM metrics me
	LEFT JOIN monthly_revenue mr ON me.user_id = mr.user_id
	AND me.payment_month = mr.payment_month
GROUP BY 1,
	2,
	3,
	4,
	5,
	13,
	14,
	15
ORDER BY user_id,
	payment_month;



SELECT CONCAT(user_pseudo_id, '-', event_bundle_sequence_id) AS session_id,
	user_pseudo_id,
	event_bundle_sequence_id,
	event_name,
	DATETIME(TIMESTAMP_MICROS(event_timestamp)) AS event_time,
	(
		SELECT value.string_value
		FROM UNNEST(event_params)
		WHERE key = "page_location"
	) AS landing_page,
	device.category AS device_category,
	device.operating_system AS operating_system,
	device.language AS device_language,
	traffic_source.source AS traffic_source,
	traffic_source.medium AS traffic_medium,
	traffic_source.name AS traffic_campaign,
	(
		SELECT value.int_value
		FROM UNNEST(event_params)
		WHERE key = 'value'
	) AS revenue
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE event_name IN (
		'session_start',
		'view_item',
		'add_to_cart',
		'begin_checkout',
		'add_shipping_info',
		'add_payment_info',
		'purchase'
	) -- Malikas
	with monthly_payments as (
		select date_trunc('month', gp.payment_date)::date as payment_month,
			gp.user_id,
			gps.game_name,
			gps.age,
			gps.language,
			sum(gp.revenue_amount_usd) as total_month_revenue
		from project.games_payments gp
			left join project.games_paid_users gps on gps.user_id = gp.user_id
		group by 1,
			2,
			3,
			4,
			5
	),
	first_monthly_payment as(
		select payment_month,
			user_id,
			game_name,
			age,
			language,
			total_month_revenue,
			lag(payment_month) over (
				partition by user_id
				order by payment_month
			) AS previous_paid_month,
			date(payment_month + interval '1' month) as next_calendar_month,
			date(payment_month - interval '1' month) as previous_calendar_month,
			lead(payment_month) over (
				partition by user_id
				order by payment_month
			) as next_paid_month,
			lag(total_month_revenue) over (
				partition by user_id
				order by payment_month
			) as previous_paid_month_revenue
		from monthly_payments mp
	),
	agg_table as (
		select payment_month,
			user_id,
			game_name,
			age,
			language,
			total_month_revenue,
			case
				when fmp.previous_paid_month is null then fmp.total_month_revenue
			end as new_mrr,
			case
				when previous_paid_month is null then 1
				else 0
			end as new_paid_users,
			case
				when fmp.next_paid_month is null
				or fmp.next_paid_month != fmp.next_calendar_month then fmp.total_month_revenue
			end as churned_revenue,
			case
				when fmp.next_paid_month is null
				or fmp.next_paid_month != fmp.next_calendar_month then 1
			end as churned_users,
			case
				when fmp.next_paid_month is null
				or fmp.next_paid_month != fmp.next_calendar_month then fmp.next_calendar_month
			end as churn_month,
			case
				when fmp.previous_paid_month = fmp.previous_calendar_month
				and fmp.total_month_revenue > fmp.previous_paid_month_revenue then fmp.total_month_revenue - fmp.previous_paid_month_revenue
			end as expansion_revenue,
			case
				when fmp.previous_paid_month = fmp.previous_calendar_month
				and fmp.total_month_revenue < fmp.previous_paid_month_revenue then fmp.total_month_revenue - fmp.previous_paid_month_revenue
			end as contraction_revenue
		from first_monthly_payment fmp
	)
select payment_month,
	user_id,
	game_name,
	age,
	language,
	total_month_revenue,
	new_paid_users,
	new_mrr,
	churn_month,
	churned_users,
	churned_revenue,
	expansion_revenue,
	contraction_revenue
from agg_table;



-- mine good 1392 rows
WITH monthly_revenue AS (
	SELECT gp.user_id,
		DATE_TRUNC('month', payment_date)::DATE as payment_month,
		gp.game_name,
		SUM(revenue_amount_usd) AS revenue,
		gpu.language,
		gpu.has_older_device_model AS old_device,
		gpu.age::INT AS age
	FROM project.games_payments gp
		LEFT JOIN project.games_paid_users gpu ON gp.user_id = gpu.user_id
	GROUP BY 1,
		2,
		3,
		5,
		6,
		7
	ORDER BY 1,
		2,
		3
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
	mr.payment_month,
	me.first_payment_month,
	SUM(me.total_revenue) as mrr,
	SUM(me.new_paid_users) as new_paid_users,
	SUM(me.new_mrr) as new_mrr,
	SUM(me.churned_users) AS churned_users,
	SUM(me.churned_revenue) AS churned_revenue,
	SUM(me.expansion_revenue) AS expansion_revenue,
	SUM(me.contraction_revenue) AS contraction_revenue,
	mr.language,
	mr.old_device,
	mr.age
FROM metrics me
	LEFT JOIN monthly_revenue mr ON me.user_id = mr.user_id
	AND me.payment_month = mr.payment_month
GROUP BY 1,
	2,
	3,
	4,
	12,
	13,
	14
ORDER BY user_id,
	payment_month;




WITH monthly_revenue AS (
	SELECT 
		gp.user_id,
		DATE_TRUNC('month', payment_date)::DATE as payment_month,
		(MAX(payment_date)::DATE - MIN(payment_date)::DATE) AS lifetime_days,
		gp.game_name,
		SUM(revenue_amount_usd) AS revenue,
		gpu.language,
		gpu.has_older_device_model AS old_device,
		gpu.age::INT AS age
	FROM project.games_payments gp
		LEFT JOIN project.games_paid_users gpu ON gp.user_id = gpu.user_id
	GROUP BY 
		1,
		2,
		4,
		6, 7, 8
	ORDER BY 1,
		2,
		4
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
SELECT 
	mr.user_id,
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

-- final code
WITH base_data AS (
  SELECT 
    gp.user_id,
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
  SELECT
    user_id,
    payment_month,
    game_name,
    (last_payment_date - first_payment_date)::INT AS lifetime_days,
    SUM(revenue_amount_usd) AS revenue,
    language,
    old_device,
    age
  FROM base_data
  GROUP BY 
    user_id, payment_month, game_name, last_payment_date, first_payment_date, language, old_device, age
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
SELECT 
	mr.user_id,
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