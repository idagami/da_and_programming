create schema if not exists public;

create table public.salaries (
    work_year integer
    , experience_level text
    , employment_type text
    , job_title text
    , salary integer
    , salary_currency text
    , salary_in_usd integer
    , employee_residence text
    , remote_ratio integer
    , company_location text
    , company_size text
);

copy public.salaries
from '/Users/irenka/irenka_docs/tech/Studying/SQL/self_study/salaries_dataset/salaries.csv'
delimiter ','
csv header;

