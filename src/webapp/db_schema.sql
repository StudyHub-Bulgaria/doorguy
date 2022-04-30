-- MariaDB dump 10.19  Distrib 10.5.12-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: doorguy_dev
-- ------------------------------------------------------
-- Server version	10.5.12-MariaDB-0+deb11u1

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
-- Table structure for table `customer_accounts`
--

DROP TABLE IF EXISTS `customer_accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_accounts` (
  `customer_id` int(11) DEFAULT NULL,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(256) DEFAULT NULL,
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `customer_accounts_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_accounts`
--

LOCK TABLES `customer_accounts` WRITE;
/*!40000 ALTER TABLE `customer_accounts` DISABLE KEYS */;
INSERT INTO `customer_accounts` VALUES (1,'ivan','$2b$12$ECEilCLfWSmkv5JpnLOSjOPmk.d7mI5/g2sgKqTF3SYqL41B7Bj5e'),(29,'kiro14',''),(30,'kiro14',''),(31,'kiro14',''),(32,'kiro14',''),(33,'kiro14',''),(38,'kiro14','$2b$12$m/vAFHy0iVzMGGspYwNxuORGIjtFXoiqp.8en220sbIw0/s5mySs2'),(39,'kiro14','$2b$12$zlXCdK3mDoOL/WZzx.W1NOPZaDsWaohKaWblCUP26N/HXg4ta6XfO'),(40,'kiro14','$2b$12$xas0GDPMh0M3baAgzfvn0eDlpVh.bjuP4LIkGOm15qFjugH2.Pqbi'),(41,'kiro14','$2b$12$0WZXmdJUC8YB9LBLstNYmejbE8qcbpfoFTZLMJi04ahW8Qqmi74ky'),(42,'kiro14','$2b$12$wt7xmmgATp3fMJ2xorGSG.e15B9K0JMC1.w2hn9FCiNH/MNoYpHRW'),(43,'kiro14','$2b$12$3E4OqjmNL02zyggNC4FeyO9nCbE5MdrasKXQPEEw2htsxgqicLFoe'),(44,'kiro14','$2b$12$0DmzJqr7r.yuMJVgHGgrReCLNdGrRtxC2EsDyHjLdjOB0eBMEHwle'),(45,'kiro14','$2b$12$FY9L8DhV718UFDQFlNft1Ob0tJBystbiDdPKLKTTYZhNS8c4HXnBK');
/*!40000 ALTER TABLE `customer_accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_payments`
--

DROP TABLE IF EXISTS `customer_payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_payments` (
  `customer_id` int(11) DEFAULT NULL,
  `timestamp` bigint(20) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `subscription_type` int(11) DEFAULT NULL,
  KEY `customer_payments_FK` (`customer_id`),
  KEY `customer_payments_FK_1` (`subscription_type`),
  CONSTRAINT `customer_payments_FK` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`),
  CONSTRAINT `customer_payments_FK_1` FOREIGN KEY (`subscription_type`) REFERENCES `subscription_types` (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_payments`
--

LOCK TABLES `customer_payments` WRITE;
/*!40000 ALTER TABLE `customer_payments` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer_payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_subscriptions`
--

DROP TABLE IF EXISTS `customer_subscriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_subscriptions` (
  `customer_id` int(11) DEFAULT NULL,
  `is_valid` tinyint(1) DEFAULT NULL,
  `subscription_type` int(11) DEFAULT NULL,
  `validity_start` bigint(20) DEFAULT NULL,
  `validity_end` bigint(20) DEFAULT NULL,
  KEY `customer_id` (`customer_id`),
  KEY `customer_subscriptions_FK` (`subscription_type`),
  CONSTRAINT `customer_subscriptions_FK` FOREIGN KEY (`subscription_type`) REFERENCES `subscription_types` (`type`),
  CONSTRAINT `customer_subscriptions_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_subscriptions`
--

LOCK TABLES `customer_subscriptions` WRITE;
/*!40000 ALTER TABLE `customer_subscriptions` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer_subscriptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `university` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `zkteco_id` int(11) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'Sofia uni','Petrov','Ivan',143,'05583412','angel@studyhub.bg'),(2,NULL,NULL,'Хитър Петър',NULL,NULL,NULL),(7,'Petrov Uni',NULL,'Pesho',715,'666','ivancho@abv.bg'),(29,'kiro_uni',NULL,'kiro_14',0,'08895143512','kiro@abv.bg'),(30,'kiro_uni',NULL,'kiro_14',0,'08895143512','kiro@abv.bg'),(31,'kiro_uni',NULL,'kiro_14',0,'08895143512','kiro@abv.bg'),(32,'kiro_uni',NULL,'kiro_14',0,'08895143512','kiro@abv.bg'),(33,'kiro_uni',NULL,'kiro_14',0,'08895143512','kiro@abv.bg'),(34,'kiro_uni',NULL,'kiro_14',0,'08895143512','kiro@abv.bg'),(35,'kiro_uni',NULL,'kiro_14',0,'08895143512','kiro@abv.bg'),(36,'kiro_uni',NULL,'kiro_14',0,'08895143512','kiro@abv.bg'),(37,'kiro_uni',NULL,'kiro_14',0,'08895143512','kiro@abv.bg'),(38,'kiro_uni',NULL,'kiro_14',0,'08895143512','kiro@abv.bg'),(39,'kiro_uni',NULL,'kiro_14',0,'08895143512','kiro@abv.bg'),(40,'kiro_uni',NULL,'kiro_14',0,'08895143512','kiro@abv.bg'),(41,'kiro_uni',NULL,'kiro_14',0,'08895143512','kiro@abv.bg'),(42,'kiro_uni',NULL,'kiro_14',0,'08895143512','kiro@abv.bg'),(43,'kiro_uni',NULL,'kiro_14',0,'08895143512','kiro@abv.bg'),(44,'kiro_uni',NULL,'kiro_14',0,'08895143512','kiro@abv.bg'),(45,'kiro_uni',NULL,'kiro_14',0,'08895143512','kiro@abv.bg');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doors`
--

DROP TABLE IF EXISTS `doors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `doors` (
  `door_id` int(11) NOT NULL,
  `door_name` varchar(100) DEFAULT NULL,
  `door_ip` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`door_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doors`
--

LOCK TABLES `doors` WRITE;
/*!40000 ALTER TABLE `doors` DISABLE KEYS */;
INSERT INTO `doors` VALUES (1,'Front Door External','192.168.1.x'),(2,'Front Door Internal','192.168.1.x'),(3,'Back Door Internal','192.168.1.x'),(4,'Back Door External','192.168.1.x');
/*!40000 ALTER TABLE `doors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entry_logs`
--

DROP TABLE IF EXISTS `entry_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entry_logs` (
  `timestamp` timestamp NULL DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `door_id` int(11) DEFAULT NULL,
  KEY `door_id` (`door_id`),
  KEY `entry_logs_user_id_IDX` (`user_id`) USING BTREE,
  CONSTRAINT `entry_logs_FK` FOREIGN KEY (`user_id`) REFERENCES `customers` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `entry_logs_ibfk_1` FOREIGN KEY (`door_id`) REFERENCES `doors` (`door_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entry_logs`
--

LOCK TABLES `entry_logs` WRITE;
/*!40000 ALTER TABLE `entry_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `entry_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subscription_types`
--

DROP TABLE IF EXISTS `subscription_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subscription_types` (
  `type` int(11) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  PRIMARY KEY (`type`),
  KEY `card_type` (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subscription_types`
--

LOCK TABLES `subscription_types` WRITE;
/*!40000 ALTER TABLE `subscription_types` DISABLE KEYS */;
INSERT INTO `subscription_types` VALUES (1,'Daily pass, 24 hours.',5),(2,'Weekly pass, 24/7 for 7 days',15),(3,'Monthly pass, 24/7 for 30 days.',30),(4,'Non-student monthly pass, 24/7 for 30 days.',50),(5,'Semester pass, 24/7 for full semester.',90);
/*!40000 ALTER TABLE `subscription_types` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-04-30 16:00:48
