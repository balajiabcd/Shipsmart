-- Milestone #39: Delivery Events Table Migration

DROP TABLE IF EXISTS delivery_events CASCADE;

CREATE TABLE delivery_events (
    event_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    event_type VARCHAR(30) NOT NULL,
    location_id VARCHAR(10),
    driver_id VARCHAR(10),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_event_type CHECK (event_type IN ('created', 'picked_up', 'in_transit', 'out_for_delivery', 'delivered', 'failed_attempt')),
    CONSTRAINT fk_events_order FOREIGN KEY (order_id) REFERENCES orders(order_id),
    CONSTRAINT fk_events_driver FOREIGN KEY (driver_id) REFERENCES drivers(driver_id),
    CONSTRAINT fk_events_location FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

CREATE INDEX idx_delivery_events_order ON delivery_events(order_id);
CREATE INDEX idx_delivery_events_timestamp ON delivery_events(timestamp);
CREATE INDEX idx_delivery_events_driver ON delivery_events(driver_id);
CREATE INDEX idx_delivery_events_type ON delivery_events(event_type);

COMMENT ON TABLE delivery_events IS 'Order delivery event tracking';