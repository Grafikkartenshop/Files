-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: Grafikkartenshop
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Grafikkarte`
--

DROP TABLE IF EXISTS `Grafikkarte`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Grafikkarte` (
  `artikelNr` int(11) NOT NULL AUTO_INCREMENT,
  `modell` varchar(50) DEFAULT NULL,
  `hersteller` varchar(50) DEFAULT NULL,
  `marke` varchar(50) DEFAULT NULL,
  `vramGroesse` int(11) DEFAULT NULL,
  `speichertyp` varchar(50) DEFAULT NULL,
  `einkaufspreis` double DEFAULT NULL,
  `verkaufspreis` double DEFAULT NULL,
  `bestand` int(11) DEFAULT NULL,
  `shopID` int(11) DEFAULT NULL,
  PRIMARY KEY (`artikelNr`),
  KEY `shopID` (`shopID`),
  CONSTRAINT `Grafikkarte_ibfk_1` FOREIGN KEY (`shopID`) REFERENCES `Grafikkartenshop` (`shopID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Grafikkarte`
--

LOCK TABLES `Grafikkarte` WRITE;
/*!40000 ALTER TABLE `Grafikkarte` DISABLE KEYS */;
INSERT INTO `Grafikkarte` VALUES (1,'RTX 4080','NVIDIA','MSI',16,'GDDR6X',999.99,1299.99,4,1),(2,'RX 7900 XTX','AMD','GIGABYTE',24,'GDDR6',899.99,1049.99,6,1),(3,'Intel ARC B580','Intel','ASRock',12,'GDDR6',199.99,299.99,10,1),(4,'RTX 5060','NVIDIA','ASUS',8,'GDDR7',299.99,399.99,5,1);
/*!40000 ALTER TABLE `Grafikkarte` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Grafikkartenshop`
--

DROP TABLE IF EXISTS `Grafikkartenshop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Grafikkartenshop` (
  `shopID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `umsatz` double DEFAULT NULL,
  `budget` double DEFAULT NULL,
  PRIMARY KEY (`shopID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Grafikkartenshop`
--

LOCK TABLES `Grafikkartenshop` WRITE;
/*!40000 ALTER TABLE `Grafikkartenshop` DISABLE KEYS */;
INSERT INTO `Grafikkartenshop` VALUES (1,'Aura GPU',0,1000000);
/*!40000 ALTER TABLE `Grafikkartenshop` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-19 18:56:19
