SELECT
    farm_id,
    SUM(quantity_g) AS total_quantity_g
FROM fact_harvest
GROUP BY farm_id
ORDER BY total_quantity_g DESC;
