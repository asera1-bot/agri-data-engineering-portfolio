SELECT
    validation_status,
    validation_reason,
    COUNT(*) AS record_count
FROM fact_harvest
GROUP BY
    validation_status,
    validation_reason
ORDER BY record_count DESC;
