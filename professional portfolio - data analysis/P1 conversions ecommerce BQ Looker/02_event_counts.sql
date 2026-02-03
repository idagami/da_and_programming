WITH all_events AS (
    SELECT event_name,
        user_pseudo_id,
        (
            SELECT value.int_value
            FROM UNNEST(event_params)
            WHERE key = 'ga_session_id'
        ) AS ga_session_id
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
),
valid_sessions AS (
    SELECT user_pseudo_id,
        ga_session_id
    FROM all_events
    WHERE event_name = 'session_start'
        AND ga_session_id IS NOT NULL
),
filtered_events AS (
    SELECT ae.event_name
    FROM all_events ae
        JOIN valid_sessions vs ON ae.user_pseudo_id = vs.user_pseudo_id
        AND ae.ga_session_id = vs.ga_session_id
)
SELECT event_name,
    COUNT(*) AS event_count
FROM filtered_events
GROUP BY event_name
ORDER BY event_count DESC;