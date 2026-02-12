This project focuses on analyzing product revenue metrics in the gaming industry. 
The goal was to build a multi-functional dashboard to track, visualize, and interpret revenue performance across 
different user segments, games, and time periods. It provides insights into user behavior, revenue growth, churn, 
and lifetime value (LTV), supporting data-driven decision-making for product managers, analysts, and company executives.

The dashboard was built using PostgreSQL for data processing and Tableau Public for visualization, 
allowing users to explore key metrics interactively without needing SQL knowledge.

Data Pipeline
The data comes from two sources:
games_payments – records of all purchases by users for three games.
games_paid_users – user metadata including language, age, and device information.

The SQL workflow includes the following steps:
Base Data (base_data) – combines payment data with user metadata, calculates first and last payment dates, and aggregates user-level information.
Monthly Revenue (monthly_revenue) – calculates monthly revenue, lifetime in days, and groups by user and game.
Periods (periods) – calculates past and next payment months and revenue, enabling churn and expansion/contraction analysis.

The dashboard is divided into three main parts:
KPI Cards – highlight key success metrics such as total revenue, MRR, churn rate, and new users.
Cohort Analysis – visualize revenue and retention for different user cohorts by language, age, device, and game.
Interactive Graphs – allow users to compare metrics by segments, identify top-performing players, and analyze revenue dynamics over time.