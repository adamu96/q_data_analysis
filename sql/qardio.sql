CREATE TABLE emai_log (
	logid MEDIUMINT NOT NULL AUTO_INCREMENT,
    change_type VARCHAR(20),
    dt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (logid)
);

INSERT INTO email_log (change_type) VALUES ('insert');

SELECT * FROM email_log;

DELIMITER $$
	CREATE TRIGGER RemoveDuplicates
	AFTER INSERT ON emails
	FOR EACH ROW BEGIN
		INSERT INTO Emaillog
		VALUES (NEW.ID, OLD.Quantity, NEW.Quantity, TIMESTAMP);
	END$$
DELIMITER ;

LOAD DATA LOCAL INFILE '/Users/adamurquhart/data/qardio_data.csv'
INTO TABLE emails
FIELDS TERMINATED BY ','
IGNORE 1 ROWS;

 
SELECT date_sent,
	subscribers,
    recipients
FROM emails
ORDER BY recipients DESC;

