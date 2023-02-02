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
-- Table structure for table `remediation`
--

DROP TABLE IF EXISTS `remediation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `remediation` (
  `Id` varchar(40) NOT NULL,
  `Title` varchar(80) NOT NULL,
  `Description` varchar(80) NOT NULL,
  `DocumentName` varchar(50) NOT NULL,
  `Bucket` varchar(30) NOT NULL,
  `Arguments` varchar(80) NOT NULL,
  `ObjectKey` varchar(30) NOT NULL,
  `AutomationAssumeRole` varchar(80) NOT NULL,
  `AccountId` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `remediation`
--

LOCK TABLES `remediation` WRITE;
/*!40000 ALTER TABLE `remediation` DISABLE KEYS */;
INSERT INTO `remediation` VALUES ('9c166897-2336-43ab-a0cb-ce26a14ad466','[S3.4] S3 Bucket Policies should not allow public access to the bucket','Put private ACL on a bucket to remove public read or write access ','KB-AWS-ExecuteScript','sbotplaybooks','{ \"s3BucketName\": \"\", \"findingId\": \"\" }','S3_PrivateACL_Playbook.py','arn:aws:iam::AccId:role/StoreBotInsightsLambda',AccId);
/*!40000 ALTER TABLE `remediation` ENABLE KEYS */;
UNLOCK TABLES;
