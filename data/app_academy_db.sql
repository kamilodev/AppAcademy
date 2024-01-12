CREATE DATABASE IF NOT EXISTS `app_academy_db`;
USE `app_academy_db`;

DROP TABLE IF EXISTS `classes`;
CREATE TABLE `classes` (
	`id_classes` int NOT NULL AUTO_INCREMENT,
	`name` varchar(45) NOT NULL,
	`id_packs` int NOT NULL,
	PRIMARY KEY (`id_classes`),
	UNIQUE KEY `id_classes_UNIQUE` (`id_classes`),
	KEY `id_packs_idx` (`id_packs`)
) ENGINE = InnoDB AUTO_INCREMENT = 16 DEFAULT CHARSET = utf8mb3;
LOCK TABLES `classes` WRITE;
INSERT INTO `classes`
VALUES (0, 'Bachata', 1),
(1, 'Salsa', 1),
(2, 'Kizomba', 1),
(3, 'Estilo para todos', 2),
(4, 'Lady style', 3),
(5, 'Role rotation', 1),
(6, 'Pilates', 2),
(7, 'Yoga', 2),
(8, 'Flamenco', 3),
(9, 'Zouk', 2);
UNLOCK TABLES;
DROP TABLE IF EXISTS `courses`;
CREATE TABLE `courses` (
	`id_courses` int NOT NULL AUTO_INCREMENT,
	`id_classes` int NOT NULL,
	`id_levels` int NOT NULL,
	`id_professors` varchar(15) NOT NULL,
	`max_students` int NOT NULL,
	`prices` decimal(10, 2) NOT NULL,
	PRIMARY KEY (`id_courses`),
	UNIQUE KEY `id_courses_UNIQUE` (`id_courses`),
	KEY `id_professors_idx` (`id_professors`),
	KEY `id_classes_idx` (`id_classes`),
	KEY `id_levels_idx` (`id_levels`),
	CONSTRAINT `id_classes` FOREIGN KEY (`id_classes`) REFERENCES `classes` (`id_classes`),
	CONSTRAINT `id_levels` FOREIGN KEY (`id_levels`) REFERENCES `levels` (`id_levels`),
	CONSTRAINT `id_professors` FOREIGN KEY (`id_professors`) REFERENCES `professors` (`id_professors`)
) ENGINE = InnoDB AUTO_INCREMENT = 39 DEFAULT CHARSET = utf8mb3;
LOCK TABLES `courses` WRITE;
INSERT INTO `courses`
VALUES (0, 0, 0, '1', 10, 35.00),
(1, 0, 1, '1', 10, 35.00),
(2, 0, 2, '1', 10, 35.00),
(3, 0, 3, '1', 10, 35.00),
(4, 0, 0, '2', 10, 35.00),
(5, 0, 1, '2', 10, 35.00),
(6, 0, 2, '2', 10, 35.00),
(7, 0, 3, '2', 10, 35.00),
(8, 0, 0, '3', 10, 35.00),
(9, 0, 1, '3', 10, 35.00),
(10, 0, 2, '3', 10, 35.00),
(11, 0, 3, '3', 10, 35.00),
(12, 0, 0, '4', 10, 35.00),
(13, 0, 1, '4', 10, 35.00),
(14, 0, 2, '4', 10, 35.00),
(15, 0, 3, '4', 10, 35.00),
(16, 0, 0, '5', 10, 35.00),
(17, 0, 1, '5', 10, 35.00),
(18, 0, 2, '5', 10, 35.00),
(19, 0, 3, '5', 10, 35.00),
(20, 1, 1, '1', 10, 35.00),
(21, 1, 2, '1', 10, 35.00),
(22, 1, 1, '2', 10, 35.00),
(23, 1, 2, '2', 10, 35.00),
(24, 2, 1, '1', 10, 35.00),
(25, 2, 2, '1', 10, 35.00),
(26, 2, 3, '1', 10, 35.00),
(27, 3, 4, '5', 10, 40.00),
(28, 4, 4, '4', 10, 40.00),
(29, 5, 1, '1', 10, 35.00),
(30, 5, 2, '1', 10, 35.00),
(31, 6, 4, '6', 10, 40.00),
(32, 7, 4, '6', 10, 40.00),
(33, 8, 4, '7', 10, 40.00),
(34, 9, 1, '5', 10, 40.00),
(35, 9, 2, '5', 10, 40.00),
(36, 3, 4, '3', 10, 30.00),
(37, 0, 4, '1', 10, 40.00);
UNLOCK TABLES;
DROP TABLE IF EXISTS `discounts`;
CREATE TABLE `discounts` (
	`id_discounts` int NOT NULL,
	`discounts` decimal(2, 2) NOT NULL,
	PRIMARY KEY (`id_discounts`),
	UNIQUE KEY `id_discounts_UNIQUE` (`id_discounts`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb3;
LOCK TABLES `discounts` WRITE;
INSERT INTO `discounts`
VALUES (0, 0.00),
(1, 0.50),
(2, 0.75),
(3, 0.10);
UNLOCK TABLES;
DROP TABLE IF EXISTS `inscriptions`;
CREATE TABLE `inscriptions` (
	`id_inscriptions` int NOT NULL AUTO_INCREMENT,
	`id_students` varchar(15) NOT NULL,
	`observation` varchar(200) DEFAULT NULL,
	`date_inscription` date NOT NULL,
	`discount_family` decimal(2, 2) NOT NULL,
	PRIMARY KEY (`id_inscriptions`),
	UNIQUE KEY `id_inscriptions_UNIQUE` (`id_inscriptions`),
	KEY `id_students_idx` (`id_students`),
	CONSTRAINT `id_students` FOREIGN KEY (`id_students`) REFERENCES `students` (`id_students`)
) ENGINE = InnoDB AUTO_INCREMENT = 100 DEFAULT CHARSET = utf8mb3;
LOCK TABLES `inscriptions` WRITE;
INSERT INTO `inscriptions`
VALUES (
		73,
		'41123887J',
		'Sin observaciones',
		'2023-07-25',
		0.00
	),
(
		74,
		'41123887J',
		'Sin observaciones',
		'2023-07-25',
		0.00
	),
(
		75,
		'41123887J',
		'Sin observaciones',
		'2023-07-25',
		0.00
	),
(
		76,
		'41123887J',
		'Sin observaciones',
		'2023-07-25',
		0.00
	),
(
		77,
		'41123887J',
		'Sin observaciones',
		'2023-07-25',
		0.00
	),
(
		95,
		'41123887J',
		'Sin observaciones',
		'2023-07-26',
		0.00
	),
(
		96,
		'67543009P',
		'Sin observaciones',
		'2023-07-26',
		0.00
	),
(
		97,
		'41123887J',
		'Sin observaciones',
		'2023-07-26',
		0.10
	),
(
		99,
		'41123887J',
		'Sin observaciones',
		'2023-07-26',
		0.00
	);
UNLOCK TABLES;
DROP TABLE IF EXISTS `inscriptions_detail`;
CREATE TABLE `inscriptions_detail` (
	`id_inscriptions` int NOT NULL,
	`id_courses` int NOT NULL,
	`unit_price` float NOT NULL,
	`aply_discount` decimal(2, 2) DEFAULT NULL,
	`status` tinyint DEFAULT NULL,
	PRIMARY KEY (`id_inscriptions`, `id_courses`),
	KEY `id_courses_idx` (`id_courses`),
	KEY `id_inscriptions_idx` (`id_inscriptions`),
	CONSTRAINT `id_courses` FOREIGN KEY (`id_courses`) REFERENCES `courses` (`id_courses`),
	CONSTRAINT `id_inscriptions` FOREIGN KEY (`id_inscriptions`) REFERENCES `inscriptions` (`id_inscriptions`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb3;
LOCK TABLES `inscriptions_detail` WRITE;
INSERT INTO `inscriptions_detail`
VALUES (73, 20, 35, 0.00, 1),
(73, 25, 35, 0.00, 1),
(73, 27, 40, 0.00, 1),
(73, 30, 35, 0.00, 1),
(74, 31, 40, 0.00, 1),
(74, 33, 40, 0.00, 0),
(75, 34, 40, 0.00, 1),
(76, 7, 35, 0.00, 1),
(76, 9, 35, 0.00, 1),
(77, 14, 35, 0.00, 1),
(77, 19, 35, 0.00, 1),
(95, 18, 35, 0.00, 1),
(95, 37, 40, 0.00, 1),
(96, 10, 35, 0.00, 0),
(97, 29, 35, 0.00, 1),
(99, 28, 40, 0.00, 0);
UNLOCK TABLES;
DROP TABLE IF EXISTS `levels`;
CREATE TABLE `levels` (
	`id_levels` int NOT NULL AUTO_INCREMENT,
	`name` varchar(45) NOT NULL,
	PRIMARY KEY (`id_levels`),
	UNIQUE KEY `id_levels_UNIQUE` (`id_levels`)
) ENGINE = InnoDB AUTO_INCREMENT = 11 DEFAULT CHARSET = utf8mb3;
LOCK TABLES `levels` WRITE;
INSERT INTO `levels`
VALUES (0, 'Cero'),
(1, 'Iniciacion'),
(2, 'Medio'),
(3, 'Avanzado'),
(4, 'Único'),
(7, 'super'),
(8, 'super super'),
(10, 'string');
UNLOCK TABLES;
DROP TABLE IF EXISTS `packs`;
CREATE TABLE `packs` (
	`id_packs` int NOT NULL AUTO_INCREMENT,
	`name` varchar(45) NOT NULL,
	PRIMARY KEY (`id_packs`),
	UNIQUE KEY `id_packs_UNIQUE` (`id_packs`)
) ENGINE = InnoDB AUTO_INCREMENT = 4 DEFAULT CHARSET = utf8mb3;
LOCK TABLES `packs` WRITE;
INSERT INTO `packs`
VALUES (1, 'pack mar'),
(2, 'pack otros'),
(3, 'no pack');
UNLOCK TABLES;
--
-- Table structure for table `professors`
--

DROP TABLE IF EXISTS `professors`;
CREATE TABLE `professors` (
	`id_professors` varchar(15) NOT NULL,
	`first_name` varchar(45) NOT NULL,
	`last_name` varchar(45) NOT NULL,
	`phone` varchar(45) NOT NULL,
	`email` varchar(45) NOT NULL,
	PRIMARY KEY (`id_professors`),
	UNIQUE KEY `id_professors_UNIQUE` (`id_professors`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb3;
LOCK TABLES `professors` WRITE;
INSERT INTO `professors`
VALUES (
		'1',
		'Mar',
		'Campos',
		'665432112',
		'mar@appacademy.com'
	),
('10', 'Sara', 'string', 'string', 'string'),
(
		'2',
		'Flor',
		'Baín',
		'698765342',
		'flor@appacademy.com'
	),
(
		'3',
		'Alvaro',
		'Montes',
		'688097546',
		'alvaro@appacademy.com'
	),
(
		'4',
		'Marifé',
		'Anaya',
		'611989002',
		'marife@appacademy.com'
	),
(
		'5',
		'Nayara',
		'Torres',
		'623476879',
		'nayara@appacademy.com'
	),
(
		'6',
		'Nieves',
		'Córdoba',
		'690075421',
		'nieves@appacademy.com'
	),
(
		'7',
		'Sofía',
		'Pérez',
		'765098345',
		'sofia@appacademy.com'
	);
UNLOCK TABLES;
DROP TABLE IF EXISTS `students`;
CREATE TABLE `students` (
	`id_students` varchar(15) NOT NULL,
	`first_name` varchar(45) NOT NULL,
	`last_name` varchar(45) NOT NULL,
	`phone` varchar(45) NOT NULL,
	`email` varchar(45) NOT NULL,
	`age` int DEFAULT NULL,
	`id_familiar` json DEFAULT NULL,
	`status` tinyint DEFAULT NULL,
	`familiar` varchar(15) DEFAULT NULL,
	PRIMARY KEY (`id_students`),
	UNIQUE KEY `id_students_UNIQUE` (`id_students`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb3;
LOCK TABLES `students` WRITE;
INSERT INTO `students`
VALUES (
		'21444565C',
		'Martha',
		'Blanco',
		'643999835',
		'martha@gmail.com',
		31,
		'[0, \"556889742S\"]',
		1,
		'0'
	),
(
		'41123887J',
		'Andres',
		'Parrado',
		'655445656',
		'andres@gmail.com',
		30,
		'[0, \"86743549U\", \"67543009P\"]',
		1,
		'0'
	),
(
		'55434555N',
		'Maria',
		'Garcia',
		'766555454',
		'maria@gmail.com',
		20,
		'0',
		1,
		'0'
	),
(
		'556889742S',
		'Jorge',
		'Diaz',
		'600912432',
		'jorge@gmail.com',
		33,
		'0',
		1,
		'21444565C'
	),
(
		'64554776R',
		'Carlos',
		'Martin',
		'600912432',
		'carlos@gmail.com',
		33,
		'[0, \"73464758W\"]',
		1,
		'0'
	),
(
		'67543009P',
		'Miguel',
		'Hernandez',
		'709881273',
		'miguel@gmail.com',
		32,
		'0',
		1,
		'0'
	),
(
		'73464758W',
		'Fernando',
		'Martin',
		'600912432',
		'carlos@gmail.com',
		33,
		'0',
		1,
		'64554776R'
	),
(
		'78234655G',
		'Carmen',
		'Rueda',
		'798003115',
		'carmen@gmail.com',
		39,
		'0',
		1,
		'0'
	),
(
		'86743549U',
		'Javier',
		'Torres',
		'678321654',
		'javier@gmail.com',
		40,
		'[0, \"78234655G\"]',
		1,
		'0'
	);
UNLOCK TABLES;
--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
	`id_users` int NOT NULL AUTO_INCREMENT,
	`nombre` varchar(45) NOT NULL,
	`password` varchar(255) NOT NULL,
	PRIMARY KEY (`id_users`),
	UNIQUE KEY `id_users_UNIQUE` (`id_users`)
) ENGINE = InnoDB AUTO_INCREMENT = 38 DEFAULT CHARSET = utf8mb3;
LOCK TABLES `users` WRITE;
INSERT INTO `users`
VALUES (1, 'Mar', '123'),
(10, 'Sara', '246');
UNLOCK TABLES;