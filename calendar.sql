CREATE TABLE IF NOT EXISTS `users`(
	`user_id` VARCHAR (32),
	`email` VARCHAR (30) NOT NULL,
	`password` VARCHAR(80) NOT NULL,
	PRIMARY KEY(`user_id`)
) engine = InnoDB default CHARACTER SET = utf8 collate = utf8_general_ci;

CREATE TABLE IF NOT EXISTS `events` (
	`event_id` VARCHAR (32),
	`event_name` VARCHAR(255) NOT NULL,
	`event_time` DATETIME,
	PRIMARY KEY(`event_id`)
) engine = InnoDB default CHARACTER SET = utf8 collate = utf8_general_ci;

CREATE TABLE IF NOT EXISTS `tags` (
	`tag_id` VARCHAR (32),
	`tag_name` VARCHAR(255) NOT NULL,
	`event_id` VARCHAR (32) NOT NULL,
	`activated` BOOLEAN NOT NULL,
	PRIMARY KEY(`tag_id`),
	FOREIGN KEY (`event_id`) references `events` (`event_id`) ON DELETE CASCADE
) engine = InnoDB default CHARACTER SET = utf8 collate = utf8_general_ci;

CREATE TABLE IF NOT EXISTS `users_events` (
	`user_id` VARCHAR (32) NOT NULL,
	`event_id` VARCHAR (32) NOT NULL,
	PRIMARY KEY(`user_id`, `event_id`),
	FOREIGN KEY (`user_id`) references `users` (`user_id`) ON DELETE CASCADE,
	FOREIGN KEY (`event_id`) references `events` (`event_id`) ON DELETE CASCADE
) engine = InnoDB default CHARACTER SET = utf8 collate = utf8_general_ci;

