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
-- Table structure for table `findings`
--

DROP TABLE IF EXISTS `findings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `findings` (
  `Id` varchar(40) NOT NULL,
  `Title` text NOT NULL,
  `Description` text NOT NULL,
  `FindingId` varchar(80) NOT NULL,
  `ResourceArn` varchar(30) NOT NULL,
  `Severity` varchar(20) NOT NULL,
  `WorkflowStatus` varchar(20) NOT NULL,
  `Status` varchar(20) NOT NULL,
  `CreatedAt` varchar(50) DEFAULT NULL,
  `Source` varchar(20) NOT NULL,
  `AccountNumber` varchar(50) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `findings`
--

LOCK TABLES `findings` WRITE;
/*!40000 ALTER TABLE `findings` DISABLE KEYS */;
INSERT INTO `findings` VALUES ('03a244d3-a54d-34b5-0a52-d8a338d5594c','[S3.4] S3 Bucket Policies should not allow public access to the bucket','S3 bucket xxxxxxx.com has a bucket policy attached and it does not allow public access.','arn:aws:s3:::xxxxxxx.com/s3-bucket-policy-allows-public-access-check','arn:aws:s3:::xxxxxxx.com','INFORMATIONAL','RESOLVED','PASSED','2021-06-26T18:05:26.136545+00:00','aws.securityhub','AccId'),('121792eb-5e85-3a57-96b0-c8e600181c86','[S3.4] S3 Bucket Policies should not allow public access to the bucket','S3 bucket exposed-bucket has a bucket policy attached that allows public access. Refer to the remediation instructions to remediate this behavior','arn:aws:s3:::exposed-bucket/s3-bucket-policy-allows-public-access-check','arn:aws:s3:::exposed-bucket','CRITICAL','Suppressed','FAILED','2021-08-07T06:23:13.377696+00:00','aws.securityhub','AccId'),('17507f23-3209-68b1-2050-0a86a4c8327c','[S3.4] S3 Bucket Policies should not allow public access to the bucket','S3 bucket xxxxxxx.com has a bucket policy attached and it does not allow public access.','arn:aws:s3:::xxxxxxx.com/s3-bucket-policy-allows-public-access-check','arn:aws:s3:::xxxxxxx.com','INFORMATIONAL','RESOLVED','PASSED','2021-06-26T18:05:26.136545+00:00','aws.securityhub','AccId'),('947defc0-554d-cc08-b978-d074af6f17b5','[S3.4] S3 Bucket Policies should not allow public access to the bucket','S3 bucket exposed-bucket has a bucket policy attached that allows public access. Refer to the remediation instructions to remediate this behavior','arn:aws:s3:::exposed-bucket/s3-bucket-policy-allows-public-access-check','arn:aws:s3:::exposed-bucket','CRITICAL','NEW','FAILED','2021-08-07T06:23:13.377696+00:00','aws.securityhub','AccId'),('d3709e74-6e9f-3db3-52b4-8eb44d8c6a36','[S3.4] S3 Bucket Policies should not allow public access to the bucket','S3 bucket exposed-bucket has a bucket policy attached that allows public access. Refer to the remediation instructions to remediate this behavior','arn:aws:s3:::exposed-bucket/s3-bucket-policy-allows-public-access-check','arn:aws:s3:::exposed-bucket','CRITICAL','Suppressed','FAILED','2021-08-07T06:23:13.377696+00:00','aws.securityhub','AccId'),('edd32579-7231-6e3b-4c4a-f4dc6a38ca7f','[S3.4] S3 Bucket Policies should not allow public access to the bucket','S3 bucket xxxxxxx.com has a bucket policy attached and it does not allow public access.','arn:aws:s3:::xxxxxxx.com/s3-bucket-policy-allows-public-access-check','arn:aws:s3:::xxxxxxx.com','INFORMATIONAL','RESOLVED','PASSED','2021-06-26T18:05:26.136545+00:00','aws.securityhub','AccId');
/*!40000 ALTER TABLE `findings` ENABLE KEYS */;
UNLOCK TABLES;
