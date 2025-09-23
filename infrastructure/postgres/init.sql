-- Initialize database with security settings
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create application user with limited privileges
CREATE USER app_user WITH PASSWORD 'change-this-app-password';

-- Grant necessary permissions
GRANT CONNECT ON DATABASE intelligence_db TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT CREATE ON SCHEMA public TO app_user;

-- Set up row level security
ALTER DATABASE intelligence_db SET row_security = on;

-- Create audit table for security monitoring
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    action VARCHAR(255) NOT NULL,
    table_name VARCHAR(255),
    record_id VARCHAR(255),
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create function for audit logging
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO audit_logs (action, table_name, record_id, old_values, created_at)
        VALUES (TG_OP, TG_TABLE_NAME, OLD.id::text, row_to_json(OLD), NOW());
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_logs (action, table_name, record_id, old_values, new_values, created_at)
        VALUES (TG_OP, TG_TABLE_NAME, NEW.id::text, row_to_json(OLD), row_to_json(NEW), NOW());
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO audit_logs (action, table_name, record_id, new_values, created_at)
        VALUES (TG_OP, TG_TABLE_NAME, NEW.id::text, row_to_json(NEW), NOW());
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Set up connection limits
ALTER USER postgres CONNECTION LIMIT 10;
ALTER USER app_user CONNECTION LIMIT 20;