-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: localhost    Database: restaurant
-- ------------------------------------------------------
-- Server version	8.0.23

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
-- Table structure for table `ordertable`
--

DROP TABLE IF EXISTS `ordertable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordertable` (
  `orderno` int NOT NULL AUTO_INCREMENT,
  `paket` varchar(30) DEFAULT NULL,
  `quantity` varchar(30) DEFAULT NULL,
  `status` varchar(10) DEFAULT NULL,
  `doo` date DEFAULT NULL,
  `totalHarga` int DEFAULT NULL,
  `username` varchar(30) DEFAULT NULL,
  `notes` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`orderno`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordertable`
--

LOCK TABLES `ordertable` WRITE;
/*!40000 ALTER TABLE `ordertable` DISABLE KEYS */;
INSERT INTO `ordertable` VALUES (13,'B;C;A','1;2;3','ready','2021-04-25',247000,'abcde','abcde'),(14,'B;C','1;2','selesai','2021-04-25',110000,'abcde',''),(15,'B;C','1;1','selesai','2021-04-25',78000,'abcde',''),(16,'A;B','2;1','selesai','2021-04-25',124000,'abcde','Tambah 1'),(17,'A;B;C','4;4;4','selesai','2021-04-25',468000,'abcde','bjk'),(18,'A','1','ready','2021-04-28',10000,'cobapplj0',''),(19,'B','1','ready','2021-05-02',46000,'abcde',''),(20,'B','1','ready','2021-05-02',46000,'abcde',''),(21,'A;B','1;1','ready','2021-05-02',85000,'abcde',''),(22,'A;C','1;1','ready','2021-05-02',81000,'abcde',''),(23,'A','2','ready','2021-05-02',78000,'abcde',''),(24,'B','1','ready','2021-05-02',46000,'abcde',''),(25,'B','1','ready','2021-05-02',46000,'abcde',''),(26,'B','1','ready','2021-05-02',46000,'abcde',''),(27,'C','2','ready','2021-05-02',84000,'abcde',''),(28,'C','2','ready','2021-05-02',84000,'abcde',''),(29,'A;B','1;1','ready','2021-05-02',85000,'abcde',''),(30,'B;C','1;1','ready','2021-05-02',88000,'abcde',''),(32,'B;C','1;1','paid','2021-05-08',88000,'abcde',''),(33,'A;C','2;1','paid','2021-05-08',120000,'kelompokDAN81','ayamnya dada'),(34,'A;B','1;1','selesai','2021-05-08',85000,'kelompokDAN82','ayamnya dada');
/*!40000 ALTER TABLE `ordertable` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-08 23:52:04
