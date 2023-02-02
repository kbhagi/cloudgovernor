-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: botinsights.cluster-ctg6xsmiyb1e.ap-south-1.rds.amazonaws.com    Database: BotInsights
-- ------------------------------------------------------
-- Server version	5.7.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
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

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '';

--
-- Table structure for table `Tasks`
--

DROP TABLE IF EXISTS `Tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Tasks` (
  `TaskId` varchar(50) NOT NULL,
  `TaskStatus` varchar(20) DEFAULT NULL,
  `TaskType` varchar(20) NOT NULL,
  `DateTime` varchar(30) DEFAULT NULL,
  `FindingId` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`TaskId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Tasks`
--

LOCK TABLES `Tasks` WRITE;
/*!40000 ALTER TABLE `Tasks` DISABLE KEYS */;
INSERT INTO `Tasks` VALUES ('0dd48727-b2b1-4fba-ac32-1586c6abbb41','Success','Suppression','Mon, 20 Sep 2021 16:59:16 GMT','arn:aws:s3:::exposed-bucket/s3-bucket-policy-allows-public-access-check'),('bcc22495-84c2-46a8-9c56-23bb9bcf182f','Success','Remediation','Sat, 14 Aug 2021 05:02:32 GMT','arn:aws:s3:::exposed-bucket/s3-bucket-policy-allows-public-access-check'),('bcfa4d6c-0f87-467f-8a22-ba5dae572a91','Success','Suppression','Sat, 14 Aug 2021 05:03:51 GMT','arn:aws:s3:::exposed-bucket/s3-bucket-policy-allows-public-access-check'),('f9a1ca75-9451-44fa-9a26-08cf440f2962','Success','Remediation','Mon, 20 Sep 2021 16:57:59 GMT','arn:aws:s3:::exposed-bucket/s3-bucket-policy-allows-public-access-check');
/*!40000 ALTER TABLE `Tasks` ENABLE KEYS */;
UNLOCK TABLES;
