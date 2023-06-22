-- Create and populate calendar table
DROP PROCEDURE IF EXISTS FillCalendar;
DROP TABLE IF EXISTS calendar;

CREATE TABLE calendar (
	date datetime NOT NULL PRIMARY KEY,
    weekstart datetime AS (DATE_ADD(date, INTERVAL (-DAYOFWEEK(date)) DAY)),
	monthstart datetime AS (DATE_ADD(date, INTERVAL (1-DAYOFMONTH(date)) DAY))
);

DELIMITER &&
	CREATE PROCEDURE FillCalendar (start_date DATE, end_date DATE)
    BEGIN
		DECLARE crt_date DATE;
		SET crt_date = start_date;
		WHILE crt_date <= end_date DO
			INSERT IGNORE INTO calendar (date) VALUES (crt_date);
			SET crt_date = DATE_ADD(crt_date, INTERVAL(1) DAY);
		END WHILE;
    END&&
DELIMITER ;

CALL FillCalendar('2020-01-01', '2023-12-31');

SELECT *
FROM calendar;