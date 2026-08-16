SELECT
    crop_name,
    SUM(quantity_g) AS total_quantity_g
FROM fact_harvest
GROUP BY crop_name
ORDER BY tatol_quantity_g DESC;
