{{ config(materialized='table') }}

-- On récupère les données brutes que Dagster a insérées
with source_data as (
    select
        cast(time as timestamp) as record_time,
        temperature_2m
    from {{ source('public', 'weather_hourly') }}
)

-- On calcule les statistiques par jour
select
    date(record_time) as date_jour,
    round(avg(temperature_2m)::numeric, 2) as temp_moyenne,
    min(temperature_2m) as temp_min,
    max(temperature_2m) as temp_max
from source_data
group by 1
order by 1