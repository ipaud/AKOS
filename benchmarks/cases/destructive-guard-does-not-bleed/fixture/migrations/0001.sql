-- reviewed: column unused since v2, see PR #123
ALTER TABLE orders DROP COLUMN legacy_status;

DROP TABLE temp_import_staging;
