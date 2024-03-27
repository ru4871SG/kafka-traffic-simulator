-- Keyspace: traffic, Table: toll_events
CREATE TABLE IF NOT EXISTS traffic.toll_events (
    event_time timestamp,
    vehicle_id int,
    vehicle_type text,
    plaza_id smallint,
    PRIMARY KEY ((vehicle_id), vehicle_type, plaza_id));