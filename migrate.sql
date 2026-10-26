-- Run once if you already created the old bookings table (PNR as primary key):
-- mysql -u root -p railway_db < migrate.sql

USE railway_db;

ALTER TABLE bookings
    DROP PRIMARY KEY,
    ADD COLUMN booking_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST,
    ADD INDEX idx_pnr (pnr);
