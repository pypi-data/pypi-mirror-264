CREATE TABLE `function_binding_models` (
	`id`    	BIGINT(32) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`name`  	VARCHAR(256) NOT NULL UNIQUE,
	`function_uid`	BIGINT(32) NOT NULL REFERENCES `function_models`(`id`),
	`function_declare_uid`	BIGINT(32) NOT NULL,
	`contract_uid`	BIGINT(32) NOT NULL,
	`available`    TINYINT(1) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
