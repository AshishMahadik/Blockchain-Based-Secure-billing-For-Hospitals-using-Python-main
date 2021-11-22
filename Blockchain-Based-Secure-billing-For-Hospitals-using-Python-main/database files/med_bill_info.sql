-- MySQL dump 10.13  Distrib 8.0.25, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: med
-- ------------------------------------------------------
-- Server version	8.0.25

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

--
-- Table structure for table `bill_info`
--

DROP TABLE IF EXISTS `bill_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bill_info` (
  `prev_hash` varchar(64) DEFAULT NULL,
  `p_id` varchar(20) DEFAULT NULL,
  `bill_no` varchar(45) DEFAULT NULL,
  `bill_file` longblob,
  `c_hash` varchar(64) DEFAULT NULL,
  UNIQUE KEY `c_hash_UNIQUE` (`c_hash`),
  UNIQUE KEY `prev_hash_UNIQUE` (`prev_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bill_info`
--

LOCK TABLES `bill_info` WRITE;
/*!40000 ALTER TABLE `bill_info` DISABLE KEYS */;
INSERT INTO `bill_info` VALUES ('0','0','0',_binary 'this is genesis file for the blockchain','3795438c28848778e3dc8d29e8e7d2158af08d2a9209496092232d91049e380d'),('3795438c28848778e3dc8d29e8e7d2158af08d2a9209496092232d91049e380d','2108140119','50104',_binary '==================================================================  PATIENT ID : 2108140119					BILL NO : 50104\r\n PATIENT NAME : Sourabh Jamdade					CONTACT NO : 9021143570\r\n==================================================================\r\n   Medicine		                 Description		             		  QTY	                   Price\r\n-----------------------------------------------------------------------------------------------------------------------\r\n  Creatine                                      Protin					                     2		                   2400.0\r\n  Creatine                                      Protin					                     4		                   4800.0\r\n\r\n==================================================================\r\n  Total: 							               Rs.7200.0\r\n','3bb92d217284678d0d3454b3a86282e78c0c906898d75d3cbbc170c5789d4d1a');
/*!40000 ALTER TABLE `bill_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-08-18 22:52:14
