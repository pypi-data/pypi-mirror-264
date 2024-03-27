CREATE TABLE `function_models` (
	`id`    	BIGINT(32) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`name`  	VARCHAR(256) NOT NULL UNIQUE,
	`content`    VARCHAR(1024) NOT NULL,
	`description`  VARCHAR(1024) NOT NULL,
	`available`    TINYINT(1) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

