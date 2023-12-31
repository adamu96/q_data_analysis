/* 
Views for Analytics
*/
-- CREATE  OR REPLACE VIEW daily_all_data AS
SELECT c.date,
	e.*
FROM calendar c
LEFT JOIN emails e ON c.date = e.date_sent
WHERE c.date >= (SELECT MIN(date_sent) FROM emails)
	AND c.date <= (SELECT MAX(date_sent) FROM emails)
ORDER BY c.date;
DROP TABLE emails;

-- Three views for revenue analysis at different levels of granularity
CREATE OR REPLACE VIEW day_email_rev AS
SELECT c.date AS date,
	ROUND(SUM(e.revenue), 2) AS total_revenue
FROM calendar c
LEFT JOIN emails e
	ON c.date = e.date_sent
WHERE c.date >= (SELECT MIN(date_sent) FROM emails)
	AND c.date <= (SELECT MAX(date_sent) FROM emails)
GROUP BY c.date
ORDER BY c.date;


CREATE OR REPLACE VIEW week_email_rev AS
SELECT c.weekstart,
	ROUND(SUM(e.revenue), 2) AS total_revenue
FROM calendar c
LEFT JOIN emails e
	ON c.date = e.date_sent
WHERE c.date >= (SELECT MIN(date_sent) FROM emails)
	AND c.date <= (SELECT MAX(date_sent) FROM emails)
GROUP BY c.weekstart
ORDER BY c.weekstart;


CREATE OR REPLACE VIEW month_email_rev AS
SELECT c.monthstart AS month,
	ROUND(SUM(e.revenue), 2) AS total_revenue
FROM calendar c
LEFT JOIN emails e
	ON c.date = e.date_sent
WHERE c.date >= (SELECT MIN(date_sent) FROM emails)
	AND c.date <= (SELECT MAX(date_sent) FROM emails)
GROUP BY c.monthstart
ORDER BY c.monthstart;

drop view monthly_email_rev;

drop table emails;