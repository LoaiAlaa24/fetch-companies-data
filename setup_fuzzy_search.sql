-- Enable the pg_trgm extension for fuzzy text matching
-- This extension provides functions and operators for determining the similarity of text based on trigram matching

CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Drop existing index if it exists and recreate it
-- This ensures the index is properly configured for trigram matching
DROP INDEX IF EXISTS idx_european_companies_name_trgm;

-- Create a GIN index on the name column for faster fuzzy searches
-- This index will significantly improve performance for similarity queries on millions of records
CREATE INDEX idx_european_companies_name_trgm
ON european_companies USING gin (name gin_trgm_ops);

-- Optional: Create a GiST index as an alternative (GIN is usually faster for this use case)
-- CREATE INDEX IF NOT EXISTS idx_european_companies_name_gist
-- ON european_companies USING gist (name gist_trgm_ops);

-- Set the similarity threshold (default is 0.3, but you can adjust this)
-- This can also be set per-session in your application
-- SELECT set_limit(0.95);  -- 95% similarity

-- Test the fuzzy search functionality
-- Example query:
-- SELECT name, similarity(name, 'Google') as score
-- FROM european_companies
-- WHERE similarity(name, 'Google') >= 0.95
-- ORDER BY score DESC
-- LIMIT 10;
