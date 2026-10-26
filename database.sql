-- IRCTC Railway Ticketing System - Database Schema
-- Run: mysql -u root -p < database.sql

CREATE DATABASE IF NOT EXISTS railway_db;
USE railway_db;

-- Trains table: stores train details and seat availability
CREATE TABLE IF NOT EXISTS trains (
    train_no        VARCHAR(10)  NOT NULL,
    train_name      VARCHAR(100) NOT NULL,
    source          VARCHAR(50)  NOT NULL,
    destination     VARCHAR(50)  NOT NULL,
    fare            DECIMAL(10, 2) NOT NULL,
    total_seats     INT          NOT NULL,
    available_seats INT          NOT NULL,
    PRIMARY KEY (train_no),
    CHECK (fare >= 0),
    CHECK (total_seats >= 0),
    CHECK (available_seats >= 0),
    CHECK (available_seats <= total_seats)
);

-- Bookings table: one row per passenger; same PNR groups up to 4 passengers
CREATE TABLE IF NOT EXISTS bookings (
    booking_id      INT          NOT NULL AUTO_INCREMENT,
    pnr             VARCHAR(20)  NOT NULL,
    train_no        VARCHAR(10)  NOT NULL,
    passenger_name  VARCHAR(100) NOT NULL,
    passenger_age   INT          NOT NULL,
    status          ENUM('CONFIRMED', 'CANCELLED') NOT NULL DEFAULT 'CONFIRMED',
    PRIMARY KEY (booking_id),
    INDEX idx_pnr (pnr),
    FOREIGN KEY (train_no) REFERENCES trains(train_no)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CHECK (passenger_age > 0 AND passenger_age <= 120)
);
