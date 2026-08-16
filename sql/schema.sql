CREATE TABLE IF NOT EXISTS fact_harvest (
    harvest_id BIGINT PRIMARY KEY,
    farm_id TEXT NOT NULL,
    house_id TEXT NOT NULL,
    harvest_date DATE NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL,
    client_id TEXT NOT NULL,
    crop_name TEXT NOT NULL,
    crop_category TEXT NOT NULL,
    quantity_g NUMERIC NOT NULL CHECK (quantity_g > 0),
    validation_status TEXT NOT NULL,
    validation_reason TEXT
);

CREATE TABLE IF NOT EXISTS quarantine_harvest (
    quarantine_id BIGSERIAL PRIMARY KEY,
    harvest_id BIGINT,
    farm_raw TEXT,
    house_id TEXT,
    harvest_date DATE,
    client_raw TEXT,
    crop_raw TEXT,
    quantity_g NUMERIC,
    validation_reason TEXT NOT NULL,
    quarantined_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
