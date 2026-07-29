SELECT table_name, constraint_column_names
FROM duckdb_constraints()
WHERE constraint_type = 'PRIMARY KEY';