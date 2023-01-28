-- MariaDB dump 10.19  Distrib 10.6.10-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: paradise_database
-- ------------------------------------------------------
-- Server version	10.6.10-MariaDB-1+b1

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
-- Current Database: `paradise_database`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `paradise_database` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `paradise_database`;

--
-- Table structure for table `badges`
--

DROP TABLE IF EXISTS `badges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `badges` (
  `badge_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb3 NOT NULL,
  `description` varchar(255) CHARACTER SET utf8mb3 NOT NULL DEFAULT 'no description',
  `icon` varchar(255) CHARACTER SET utf8mb3 NOT NULL,
  PRIMARY KEY (`badge_id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `icon` (`icon`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `badges`
--

LOCK TABLES `badges` WRITE;
/*!40000 ALTER TABLE `badges` DISABLE KEYS */;
INSERT INTO `badges` VALUES (1,'founder','the bot founder\'s badge','<:founder:1033761115567562873>'),(2,'developer','badge for those involved in bot development','<a:developer:1033732985054318612>'),(3,'halloweenAward','halloween event badge','<a:halloween:1032777226397175920>'),(4,'christmas','christmas event badge','<:christmas:1059147339014623353>'),(5,'year2023','badge for new year\'s event 2023','<a:2023:1059150117577437234>');
/*!40000 ALTER TABLE `badges` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `guilds`
--

DROP TABLE IF EXISTS `guilds`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `guilds` (
  `guild_id` varchar(50) CHARACTER SET utf8mb3 NOT NULL,
  `name` varchar(50) CHARACTER SET utf8mb3 DEFAULT NULL,
  `prefix` varchar(3) CHARACTER SET utf8mb3 NOT NULL DEFAULT '$',
  `lang` varchar(10) CHARACTER SET utf8mb3 NOT NULL DEFAULT 'en',
  `spam` varchar(3) CHARACTER SET utf8mb3 NOT NULL DEFAULT 'yes',
  `channel` varchar(50) CHARACTER SET utf8mb3 DEFAULT NULL,
  `announcementsChannel` varchar(50) CHARACTER SET utf8mb3 DEFAULT NULL,
  `prefixVC` varchar(3) CHARACTER SET utf8mb3 DEFAULT NULL,
  PRIMARY KEY (`guild_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guilds`
--

LOCK TABLES `guilds` WRITE;
/*!40000 ALTER TABLE `guilds` DISABLE KEYS */;
INSERT INTO `guilds` VALUES ('1005889989315416094','Bot tester 2','$','en','yes',NULL,NULL,'-'),('704895895485022290','GAYSHIN BOH','$','ja','yes','ud83cudf10speak-bot',NULL,NULL),('717451610254606386','Bot tester','$','it','no','bot-vc','annunci',NULL),('996535243441975326','Paradise!','$','it','no',NULL,NULL,'-');
/*!40000 ALTER TABLE `guilds` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventories`
--

DROP TABLE IF EXISTS `inventories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventories` (
  `user_id` varchar(50) CHARACTER SET utf8mb3 NOT NULL,
  `badge_id` int(11) NOT NULL,
  `received` date DEFAULT NULL,
  PRIMARY KEY (`user_id`,`badge_id`),
  KEY `fk_inventories_badges` (`badge_id`),
  CONSTRAINT `fk_inventories_badges` FOREIGN KEY (`badge_id`) REFERENCES `badges` (`badge_id`),
  CONSTRAINT `fk_inventories_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventories`
--

LOCK TABLES `inventories` WRITE;
/*!40000 ALTER TABLE `inventories` DISABLE KEYS */;
INSERT INTO `inventories` VALUES ('1009982111983358053',5,'2023-01-01'),('1010481872347877426',5,'2023-01-01'),('332253032324792321',5,'2023-01-01'),('471022051973660673',5,'2023-01-01'),('533014724569333770',1,'2022-10-20'),('533014724569333770',2,'2022-10-20'),('533014724569333770',3,'2022-10-31'),('533014724569333770',4,'2022-12-25'),('533014724569333770',5,'2023-01-01'),('587662332214247489',5,'2023-01-01'),('778014834419171359',5,'2023-01-01'),('916822446852694126',5,'2023-01-01'),('932262008345219072',4,'2022-12-25'),('932262008345219072',5,'2023-01-01');
/*!40000 ALTER TABLE `inventories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `items` (
  `item_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb3 NOT NULL,
  `description` varchar(255) CHARACTER SET utf8mb3 NOT NULL DEFAULT 'no description',
  `icon` varchar(255) CHARACTER SET utf8mb3 NOT NULL,
  PRIMARY KEY (`item_id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `icon` (`icon`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items`
--

LOCK TABLES `items` WRITE;
/*!40000 ALTER TABLE `items` DISABLE KEYS */;
INSERT INTO `items` VALUES (1,'robux','bot coin','<:robux:1010974169552404551>'),(2,'cat','a cute kitten','<a:catto:1012052395435499550>'),(3,'old_house','An old house that can save you from criminals discreetly','<:oldhouse:1012052537198776430>'),(4,'modern_house','An old house that can save you from criminals effectively','<:modernhouse:1012052596120367236>'),(5,'wallet','you don\'t pay commissions, what more do you want? just one each','<a:wallet:1012053408263438396>');
/*!40000 ALTER TABLE `items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jobs`
--

DROP TABLE IF EXISTS `jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jobs` (
  `work_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb3 NOT NULL,
  `description` varchar(255) CHARACTER SET utf8mb3 NOT NULL DEFAULT 'no description',
  PRIMARY KEY (`work_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobs`
--

LOCK TABLES `jobs` WRITE;
/*!40000 ALTER TABLE `jobs` DISABLE KEYS */;
INSERT INTO `jobs` VALUES (1,'banker','the banker\'s job allows you to print coins'),(2,'criminal','the criminal\'s job allows you to steal coins from other people'),(3,'petSeller','pet seller\'s job allows you to sell cuddly kittens');
/*!40000 ALTER TABLE `jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `noWords`
--

DROP TABLE IF EXISTS `noWords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `noWords` (
  `word_id` int(11) NOT NULL AUTO_INCREMENT,
  `word` varchar(50) CHARACTER SET utf8mb3 NOT NULL,
  PRIMARY KEY (`word_id`),
  UNIQUE KEY `word` (`word`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `noWords`
--

LOCK TABLES `noWords` WRITE;
/*!40000 ALTER TABLE `noWords` DISABLE KEYS */;
INSERT INTO `noWords` VALUES (7,'down'),(10,'froci'),(12,'frociazzi'),(5,'frocio'),(13,'hitler'),(14,'mussolini'),(9,'negracci'),(4,'negraccio'),(8,'negri'),(2,'negro'),(1,'nigga'),(3,'nigger'),(11,'ritardati'),(6,'ritardato');
/*!40000 ALTER TABLE `noWords` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pokedex`
--

DROP TABLE IF EXISTS `pokedex`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pokedex` (
  `user_id` varchar(50) CHARACTER SET utf8mb3 NOT NULL,
  `item_id` int(11) NOT NULL,
  `amount` int(11) DEFAULT 0,
  PRIMARY KEY (`user_id`,`item_id`),
  KEY `fk_pokedex_items` (`item_id`),
  CONSTRAINT `fk_pokedex_items` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`),
  CONSTRAINT `fk_pokedex_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pokedex`
--

LOCK TABLES `pokedex` WRITE;
/*!40000 ALTER TABLE `pokedex` DISABLE KEYS */;
INSERT INTO `pokedex` VALUES ('1009982111983358053',1,41),('1010481872347877426',1,5),('1017805142948593825',1,44),('332253032324792321',1,129),('471022051973660673',1,481),('471022051973660673',4,1),('471022051973660673',5,1),('473651113166635018',1,152),('473651113166635018',2,1),('533014724569333770',1,80),('533014724569333770',2,15),('533014724569333770',3,1),('533014724569333770',4,2),('533014724569333770',5,1),('587662332214247489',1,372),('592669756415279104',1,82),('594868896629260305',1,18),('630324319620431872',1,67),('630324319620431872',2,2),('711210565611159592',1,6),('766966489265340426',1,1),('778014834419171359',1,523),('778014834419171359',2,1),('812054020197449750',1,9),('815311962497220668',1,50),('889035646222606348',1,1),('889268113265274901',1,1),('916822446852694126',1,837),('916822446852694126',2,11),('916822446852694126',4,1),('932262008345219072',1,12),('932262008345219072',2,1),('938234430051479572',1,5),('945044201714905199',1,53),('953800430926827611',1,194),('985292622354599957',1,1);
/*!40000 ALTER TABLE `pokedex` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles` (
  `role_id` varchar(50) CHARACTER SET utf8mb3 NOT NULL,
  `name` varchar(50) CHARACTER SET utf8mb3 NOT NULL,
  `price` int(11) NOT NULL,
  `guild_id` varchar(50) CHARACTER SET utf8mb3 NOT NULL,
  PRIMARY KEY (`role_id`),
  KEY `fk_roles_guilds` (`guild_id`),
  CONSTRAINT `fk_roles_guilds` FOREIGN KEY (`guild_id`) REFERENCES `guilds` (`guild_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `user_id` varchar(50) CHARACTER SET utf8mb3 NOT NULL,
  `firstname` varchar(50) CHARACTER SET utf8mb3 DEFAULT 'no firstname',
  `lastname` varchar(50) CHARACTER SET utf8mb3 DEFAULT 'no lastname',
  `blacklist` datetime DEFAULT NULL,
  `work_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  KEY `fk_users_jobs` (`work_id`),
  CONSTRAINT `fk_users_jobs` FOREIGN KEY (`work_id`) REFERENCES `jobs` (`work_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('1009982111983358053','no firstname','no lastname',NULL,NULL),('1010481872347877426','no firstname','no lastname',NULL,NULL),('1017805142948593825','no firstname','no lastname',NULL,NULL),('332253032324792321','no firstname','no lastname',NULL,NULL),('471022051973660673','no firstname','no lastname',NULL,1),('473651113166635018','no firstname','no lastname',NULL,NULL),('533014724569333770','Hikki','Hikigaya',NULL,3),('587662332214247489','no firstname','no lastname',NULL,NULL),('592669756415279104','no firstname','no lastname',NULL,NULL),('594868896629260305','no firstname','no lastname',NULL,NULL),('630324319620431872','no firstname','no lastname',NULL,NULL),('711210565611159592','no firstname','no lastname',NULL,NULL),('766966489265340426','no firstname','no lastname',NULL,NULL),('778014834419171359','no firstname','no lastname',NULL,NULL),('812054020197449750','no firstname','no lastname',NULL,NULL),('815311962497220668','no firstname','no lastname',NULL,NULL),('889035646222606348','no firstname','no lastname',NULL,NULL),('889268113265274901','no firstname','no lastname',NULL,NULL),('916822446852694126','no firstname','no lastname',NULL,NULL),('932262008345219072','no firstname','no lastname',NULL,3),('938234430051479572','no firstname','no lastname',NULL,NULL),('945044201714905199','no firstname','no lastname',NULL,NULL),('953800430926827611','no firstname','no lastname',NULL,NULL),('985292622354599957','no firstname','no lastname',NULL,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-01-27 23:24:29
