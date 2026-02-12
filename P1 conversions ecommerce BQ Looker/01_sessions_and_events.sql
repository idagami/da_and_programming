WITH session_start AS (
    SELECT timestamp_micros(event_timestamp) as event_date,
        traffic_source.source AS source,
        traffic_source.medium AS medium,
        traffic_source.name AS campaign,
        event_name,
        geo.country AS country,
        device.category AS device,
        device.language AS language,
        device.operating_system AS os,
        user_pseudo_id,
        CONCAT(
            user_pseudo_id,
            (
                SELECT value.int_value
                FROM UNNEST(event_params)
                WHERE key = 'ga_session_id'
            )
        ) AS user_session_id,
        REGEXP_EXTRACT(
            (
                SELECT value.string_value
                FROM e.event_params
                WHERE KEY = 'page_location'
            ),
            r '(?:https:\/\/)?[^\/]+\/(.*)'
        ) AS landing_page
    FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` e
    WHERE event_name = 'session_start'
),
events AS (
    SELECT timestamp_micros(event_timestamp) as event_date,
        traffic_source.source AS source,
        traffic_source.medium AS medium,
        traffic_source.name AS campaign,
        event_name,
        geo.country AS country,
        device.category AS device,
        device.language AS language,
        device.operating_system AS os,
        CONCAT(
            user_pseudo_id,
            (
                SELECT value.int_value
                FROM UNNEST(event_params)
                WHERE key = 'ga_session_id'
            )
        ) AS user_session_id,
        REGEXP_EXTRACT(
            (
                SELECT value.string_value
                FROM e.event_params
                WHERE KEY = 'page_location'
            ),
            r '(?:https:\/\/)?[^\/]+\/(.*)'
        ) AS landing_page
    FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` e
    WHERE event_name IN (
            'session_start',
            'view_item',
            'add_to_cart',
            'begin_checkout',
            'add_shipping_info',
            'add_payment_info',
            'purchase'
        )
)
SELECT ss.user_session_id,
    ev.event_name,
    ev.event_date,
    ev.source,
    ev.medium,
    ev.campaign,
    ev.landing_page,
    ev.country,
    ev.device,
    ev.language,
    ev.os
FROM session_start ss
    LEFT JOIN events ev ON ss.user_session_id = ev.user_session_id
ORDER BY event_date DESC;