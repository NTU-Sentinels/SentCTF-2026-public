/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.8.6-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: legacy_portal
-- ------------------------------------------------------
-- Server version	11.8.6-MariaDB-5ubuntu0.1 from Ubuntu

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;
DROP DATABASE IF EXISTS legacy_portal;
CREATE DATABASE legacy_portal;
USE legacy_portal;

CREATE USER IF NOT EXISTS 'portaluser'@'localhost' IDENTIFIED BY 'portalpass';

GRANT ALL PRIVILEGES ON legacy_portal.* TO 'portaluser'@'localhost';

FLUSH PRIVILEGES;

--
-- Table structure for table `announcements`
--

DROP TABLE IF EXISTS `announcements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `announcements` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) DEFAULT NULL,
  `body` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `announcements`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `announcements` WRITE;
/*!40000 ALTER TABLE `announcements` DISABLE KEYS */;
INSERT INTO `announcements` VALUES
(1,'Migration','Legacy portal scheduled for retirement.');
/*!40000 ALTER TABLE `announcements` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `employees` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `employees` WRITE;
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
INSERT INTO `employees` VALUES
(4,'John Tan','School of Computer Science and Engineering','john.tan@ntu.edu.sg'),
(5,'Sarah Lim','School of Electrical and Electronic Engineering','sarah.lim@ntu.edu.sg'),
(6,'Daniel Lee','Finance Office','daniel.lee@ntu.edu.sg'),
(7,'Marcus Ong','Human Resources','marcus.ong@ntu.edu.sg'),
(8,'Rachel Koh','Library','rachel.koh@ntu.edu.sg'),
(9,'Benjamin Chua','IT Services','benjamin.chua@ntu.edu.sg'),
(10,'Cheryl Ng','School of Mechanical and Aerospace Engineering','cheryl.ng@ntu.edu.sg'),
(11,'Jason Lim','Admissions Office','jason.lim@ntu.edu.sg'),
(12,'Melissa Tan','Student Affairs','melissa.tan@ntu.edu.sg'),
(13,'David Goh','Facilities Management','david.goh@ntu.edu.sg'),
(14,'Alex Wong','Office of Information Technology','alex.wong@ntu.edu.sg'),
(15,'Emily Chen','School of Civil and Environmental Engineering','emily.chen@ntu.edu.sg'),
(16,'Kevin Tan','School of Biological Sciences','kevin.tan@ntu.edu.sg'),
(17,'Grace Lim','School of Physical and Mathematical Sciences','grace.lim@ntu.edu.sg'),
(18,'Ryan Koh','School of Chemistry, Chemical Engineering and Biotechnology','ryan.koh@ntu.edu.sg'),
(19,'Olivia Ng','Lee Kong Chian School of Medicine','olivia.ng@ntu.edu.sg'),
(20,'Nicholas Teo','Graduate College','nicholas.teo@ntu.edu.sg'),
(21,'Sophia Goh','Office of Academic Services','sophia.goh@ntu.edu.sg'),
(22,'Aaron Chia','Research Support Office','aaron.chia@ntu.edu.sg'),
(23,'Hannah Ong','Office of Finance','hannah.ong@ntu.edu.sg'),
(24,'Justin Ho','University Advancement Office','justin.ho@ntu.edu.sg'),
(25,'Michelle Yeo','Centre for IT Services','michelle.yeo@ntu.edu.sg'),
(26,'Samuel Low','Office of Campus Housing','samuel.low@ntu.edu.sg'),
(27,'Vanessa Tay','Office of Student Life','vanessa.tay@ntu.edu.sg'),
(28,'Darren Lim','School of Materials Science and Engineering','darren.lim@ntu.edu.sg'),
(29,'Jessica Chua','School of Humanities','jessica.chua@ntu.edu.sg'),
(30,'Ethan Tan','School of Social Sciences','ethan.tan@ntu.edu.sg'),
(31,'Nicole Seah','School of Art, Design and Media','nicole.seah@ntu.edu.sg'),
(32,'Bryan Ang','Centre for Career and Attachment','bryan.ang@ntu.edu.sg'),
(33,'Natalie Ho','Office of International Engagement','natalie.ho@ntu.edu.sg'),
(34,'Peter Chan','Legacy Systems Team','peter.chan@ntu.edu.sg'),
(35,'Linda Tan','Infrastructure Migration Office','linda.tan@ntu.edu.sg'),
(36,'Michael Goh','Database Administration','michael.goh@ntu.edu.sg'),
(37,'Rachel Lim','Cyber Security Office','rachel.lim@ntu.edu.sg');
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `internal_notes`
--

DROP TABLE IF EXISTS `internal_notes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `internal_notes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) DEFAULT NULL,
  `note` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `internal_notes`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `internal_notes` WRITE;
/*!40000 ALTER TABLE `internal_notes` DISABLE KEYS */;
INSERT INTO `internal_notes` VALUES
(1,'Migration Notes','Remove old staff portal before December'),
(2,'CTF Flag','sentCTF{all_r0ads_l3ad_t0_un10n}');
/*!40000 ALTER TABLE `internal_notes` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(1,'CCDSadmin','CCDSStaff1234!'),
(2,'thanos','Password123'),
(3,'staffadmin','Winter2024!');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-08-04 16:14:36
