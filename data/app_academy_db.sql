CREATE DATABASE  IF NOT EXISTS "app_academy_db" /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `app_academy_db`;
-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: app-academy-appacademy.aivencloud.com    Database: app_academy_db
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '0f8976d0-2020-11ee-b3a9-06534782e8ba:1-52,
d4d760c8-20cb-11ee-9ac8-0af620810800:1-738';

--
-- Table structure for table `classes`
--

DROP TABLE IF EXISTS `classes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `classes` (
  `id_classes` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `id_packs` int NOT NULL,
  PRIMARY KEY (`id_classes`),
  UNIQUE KEY `id_classes_UNIQUE` (`id_classes`),
  KEY `id_packs_idx` (`id_packs`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classes`
--

LOCK TABLES `classes` WRITE;
/*!40000 ALTER TABLE `classes` DISABLE KEYS */;
INSERT INTO `classes` VALUES (0,'Bachata',1),(1,'Salsa',1),(2,'Kizomba',1),(3,'Estilo para todos',2),(4,'Lady style',3),(5,'Role rotation',1),(6,'Pilates',2),(7,'Yoga',2),(8,'Flamenco',3),(9,'Zouk',2);
/*!40000 ALTER TABLE `classes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `id_courses` int NOT NULL AUTO_INCREMENT,
  `id_classes` int NOT NULL,
  `id_levels` int NOT NULL,
  `id_professors` varchar(15) NOT NULL,
  `max_students` int NOT NULL,
  `prices` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_courses`),
  UNIQUE KEY `id_courses_UNIQUE` (`id_courses`) /*!80000 INVISIBLE */,
  KEY `id_professors_idx` (`id_professors`),
  KEY `id_classes_idx` (`id_classes`),
  KEY `id_levels_idx` (`id_levels`),
  CONSTRAINT `id_classes` FOREIGN KEY (`id_classes`) REFERENCES `classes` (`id_classes`),
  CONSTRAINT `id_levels` FOREIGN KEY (`id_levels`) REFERENCES `levels` (`id_levels`),
  CONSTRAINT `id_professors` FOREIGN KEY (`id_professors`) REFERENCES `professors` (`id_professors`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES (0,0,0,'1',10,35.00),(1,0,1,'1',10,35.00),(2,0,2,'1',10,35.00),(3,0,3,'1',10,35.00),(4,0,0,'2',10,35.00),(5,0,1,'2',10,35.00),(6,0,2,'2',10,35.00),(7,0,3,'2',10,35.00),(8,0,0,'3',10,35.00),(9,0,1,'3',10,35.00),(10,0,2,'3',10,35.00),(11,0,3,'3',10,35.00),(12,0,0,'4',10,35.00),(13,0,1,'4',10,35.00),(14,0,2,'4',10,35.00),(15,0,3,'4',10,35.00),(16,0,0,'5',10,35.00),(17,0,1,'5',10,35.00),(18,0,2,'5',10,35.00),(19,0,3,'5',10,35.00),(20,1,1,'1',10,35.00),(21,1,2,'1',10,35.00),(22,1,1,'2',10,35.00),(23,1,2,'2',10,35.00),(24,2,1,'1',10,35.00),(25,2,2,'1',10,35.00),(26,2,3,'1',10,35.00),(27,3,4,'5',10,40.00),(28,4,4,'4',10,40.00),(29,5,1,'1',10,35.00),(30,5,2,'1',10,35.00),(31,6,4,'6',10,40.00),(32,7,4,'6',10,40.00),(33,8,4,'7',10,40.00),(34,9,1,'5',10,40.00),(35,9,2,'5',10,40.00),(36,3,4,'3',10,30.00),(37,0,4,'1',10,40.00);
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discounts`
--

DROP TABLE IF EXISTS `discounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `discounts` (
  `id_discounts` int NOT NULL,
  `discounts` decimal(2,2) NOT NULL,
  PRIMARY KEY (`id_discounts`),
  UNIQUE KEY `id_discounts_UNIQUE` (`id_discounts`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discounts`
--

LOCK TABLES `discounts` WRITE;
/*!40000 ALTER TABLE `discounts` DISABLE KEYS */;
INSERT INTO `discounts` VALUES (0,0.00),(1,0.50),(2,0.75),(3,0.10);
/*!40000 ALTER TABLE `discounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inscriptions`
--

DROP TABLE IF EXISTS `inscriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inscriptions` (
  `id_inscriptions` int NOT NULL AUTO_INCREMENT,
  `id_students` varchar(15) NOT NULL,
  `observation` varchar(200) DEFAULT NULL,
  `date_inscription` date NOT NULL,
  `discount_family` decimal(2,2) NOT NULL,
  PRIMARY KEY (`id_inscriptions`),
  UNIQUE KEY `id_inscriptions_UNIQUE` (`id_inscriptions`),
  KEY `id_students_idx` (`id_students`),
  CONSTRAINT `id_students` FOREIGN KEY (`id_students`) REFERENCES `students` (`id_students`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inscriptions`
--

LOCK TABLES `inscriptions` WRITE;
/*!40000 ALTER TABLE `inscriptions` DISABLE KEYS */;
INSERT INTO `inscriptions` VALUES (73,'41123887J','Sin observaciones','2023-07-25',0.00),(74,'41123887J','Sin observaciones','2023-07-25',0.00),(75,'41123887J','Sin observaciones','2023-07-25',0.00),(76,'41123887J','Sin observaciones','2023-07-25',0.00),(77,'41123887J','Sin observaciones','2023-07-25',0.00),(95,'41123887J','Sin observaciones','2023-07-26',0.00),(96,'67543009P','Sin observaciones','2023-07-26',0.00),(97,'41123887J','Sin observaciones','2023-07-26',0.10),(99,'41123887J','Sin observaciones','2023-07-26',0.00);
/*!40000 ALTER TABLE `inscriptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inscriptions_detail`
--

DROP TABLE IF EXISTS `inscriptions_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inscriptions_detail` (
  `id_inscriptions` int NOT NULL,
  `id_courses` int NOT NULL,
  `unit_price` float NOT NULL,
  `aply_discount` decimal(2,2) DEFAULT NULL,
  `status` tinyint DEFAULT NULL,
  PRIMARY KEY (`id_inscriptions`,`id_courses`),
  KEY `id_courses_idx` (`id_courses`) /*!80000 INVISIBLE */,
  KEY `id_inscriptions_idx` (`id_inscriptions`) /*!80000 INVISIBLE */,
  CONSTRAINT `id_courses` FOREIGN KEY (`id_courses`) REFERENCES `courses` (`id_courses`),
  CONSTRAINT `id_inscriptions` FOREIGN KEY (`id_inscriptions`) REFERENCES `inscriptions` (`id_inscriptions`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inscriptions_detail`
--

LOCK TABLES `inscriptions_detail` WRITE;
/*!40000 ALTER TABLE `inscriptions_detail` DISABLE KEYS */;
INSERT INTO `inscriptions_detail` VALUES (73,20,35,0.00,1),(73,25,35,0.00,1),(73,27,40,0.00,1),(73,30,35,0.00,1),(74,31,40,0.00,1),(74,33,40,0.00,0),(75,34,40,0.00,1),(76,7,35,0.00,1),(76,9,35,0.00,1),(77,14,35,0.00,1),(77,19,35,0.00,1),(95,18,35,0.00,1),(95,37,40,0.00,1),(96,10,35,0.00,0),(97,29,35,0.00,1),(99,28,40,0.00,0);
/*!40000 ALTER TABLE `inscriptions_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `levels`
--

DROP TABLE IF EXISTS `levels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `levels` (
  `id_levels` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`id_levels`),
  UNIQUE KEY `id_levels_UNIQUE` (`id_levels`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `levels`
--

LOCK TABLES `levels` WRITE;
/*!40000 ALTER TABLE `levels` DISABLE KEYS */;
INSERT INTO `levels` VALUES (0,'Cero'),(1,'Iniciacion'),(2,'Medio'),(3,'Avanzado'),(4,'Único'),(7,'super'),(8,'super super'),(10,'string');
/*!40000 ALTER TABLE `levels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `packs`
--

DROP TABLE IF EXISTS `packs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `packs` (
  `id_packs` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`id_packs`),
  UNIQUE KEY `id_packs_UNIQUE` (`id_packs`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `packs`
--

LOCK TABLES `packs` WRITE;
/*!40000 ALTER TABLE `packs` DISABLE KEYS */;
INSERT INTO `packs` VALUES (1,'pack mar'),(2,'pack otros'),(3,'no pack');
/*!40000 ALTER TABLE `packs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `professors`
--

DROP TABLE IF EXISTS `professors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `professors` (
  `id_professors` varchar(15) NOT NULL,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `phone` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  PRIMARY KEY (`id_professors`),
  UNIQUE KEY `id_professors_UNIQUE` (`id_professors`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `professors`
--

LOCK TABLES `professors` WRITE;
/*!40000 ALTER TABLE `professors` DISABLE KEYS */;
INSERT INTO `professors` VALUES ('1','Mar','Campos','665432112','mar@appacademy.com'),('10','Sara','string','string','string'),('2','Flor','Baín','698765342','flor@appacademy.com'),('3','Alvaro','Montes','688097546','alvaro@appacademy.com'),('4','Marifé','Anaya','611989002','marife@appacademy.com'),('5','Nayara','Torres','623476879','nayara@appacademy.com'),('6','Nieves','Córdoba','690075421','nieves@appacademy.com'),('7','Sofía','Pérez','765098345','sofia@appacademy.com');
/*!40000 ALTER TABLE `professors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES ('21444565C','Martha','Blanco','643999835','martha@gmail.com',31,'[0, \"556889742S\"]',1,'0'),('41123887J','Andres','Velasquez','655445656','andres@gmail.com',30,'[0, \"86743549U\", \"67543009P\"]',1,NULL),('55434555N','Camilo','Vanegas','766555454','camilo@gmail.com',20,'0',1,NULL),('556889742S','Jorge','Diaz','600912432','jorge@gmail.com',33,'0',1,'21444565C'),('64554776R','Carlos','Martin','600912432','carlos@gmail.com',33,'[0, \"73464758W\"]',1,'0'),('67543009P','Miguel','Hernandez','709881273','miguel@gmail.com',32,'0',1,NULL),('73464758W','Fernando','Martin','600912432','carlos@gmail.com',33,'0',1,'64554776R'),('78234655G','Carmen','Rueda','798003115','carmen@gmail.com',39,'0',1,NULL),('86743549U','Javier','Torres','678321654','javier@gmail.com',40,'[0, \"78234655G\"]',1,NULL);
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id_users` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id_users`),
  UNIQUE KEY `id_users_UNIQUE` (`id_users`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Mar','123'),(10,'Sara','246');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-07-26 10:52:10
