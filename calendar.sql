CREATE TABLE IF NOT EXISTS `users`(
	`user_id` INTEGER AUTO_INCREMENT,
	`email` VARCHAR (30) NOT NULL,
	`password` VARCHAR(80) NOT NULL,
	PRIMARY KEY(`user_id`)
) engine = InnoDB default CHARACTER SET = utf8 collate = utf8_general_ci;

CREATE TABLE IF NOT EXISTS `events` (
	`event_id` INTEGER AUTO_INCREMENT,
	`event_name` VARCHAR(255) NOT NULL,
	`event_time` DATETIME,
	PRIMARY KEY(`event_id`)
) engine = InnoDB default CHARACTER SET = utf8 collate = utf8_general_ci;

CREATE TABLE IF NOT EXISTS `tags` (
	`tag_id` INTEGER AUTO_INCREMENT,
	`tag_name` VARCHAR(255) NOT NULL,
	`event_id` INTEGER NOT NULL,
	`activated` BOOLEAN NOT NULL,
	PRIMARY KEY(`tag_id`),
	FOREIGN KEY (`event_id`) references `events` (`event_id`) ON DELETE CASCADE
) engine = InnoDB default CHARACTER SET = utf8 collate = utf8_general_ci;

CREATE TABLE IF NOT EXISTS `users_events` (
	`user_id` INTEGER NOT NULL,
	`event_id` INTEGER NOT NULL,
	PRIMARY KEY(`user_id`, `event_id`),
	FOREIGN KEY (`user_id`) references `users` (`user_id`) ON DELETE CASCADE,
	FOREIGN KEY (`event_id`) references `events` (`event_id`) ON DELETE CASCADE
) engine = InnoDB default CHARACTER SET = utf8 collate = utf8_general_ci;
