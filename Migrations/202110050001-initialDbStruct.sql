CREATE TABLE IF NOT EXISTS scores (
    id int PRIMARY KEY AUTO_INCREMENT,
    gridSize varchar(20) NOT NULL,
    turnCount int NOT NULL,
    startTime varchar(30) NOT NULL,
    endTime varchar(30) NOT NULL
)