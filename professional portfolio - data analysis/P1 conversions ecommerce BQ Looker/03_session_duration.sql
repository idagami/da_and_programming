WITH base AS (
    SELECT CONCAT(
            user_pseudo_id,
            (
                SELECT value.int_value
                FROM UNNEST(event_params)
                WHERE key = 'ga_session_id'
            )
        ) AS user_session_id,
        MIN(timestamp_micros(event_timestamp)) AS session_start_ts,
        MAX(timestamp_micros(event_timestamp)) AS session_end_ts
    FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
    WHERE event_name IN (
            'session_start',
            'view_item',
            'add_to_cart',
            'begin_checkout',
            'add_shipping_info',
            'add_payment_info',
            'purchase'
        )
    GROUP BY user_session_id
)
SELECT user_session_id,
    session_start_ts,
    session_end_ts,
    TIMESTAMP_DIFF(session_end_ts, session_start_ts, SECOND) AS session_duration_seconds,
    DATE(session_start_ts) AS session_date
FROM base;