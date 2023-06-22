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
	AFTER INSERT ON email_data
	FOR EACH ROW BEGIN
		INSERT INTO Emaillog
		VALUES (NEW.ID, OLD.Quantity, NEW.Quantity, TIMESTAMP);
	END$$
DELIMITER ;

LOAD DATA LOCAL INFILE '/Users/adamurquhart/data/qardio_data.csv'
INTO TABLE email_data
FIELDS TERMINATED BY ','
IGNORE 1 ROWS;

 
SELECT date_sent,
	subscribers,
    recipients
FROM email_data
ORDER BY recipients DESC;

