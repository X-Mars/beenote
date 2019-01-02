-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: localhost    Database: beenote
-- ------------------------------------------------------
-- Server version	5.7.24

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bee_note`
--

DROP TABLE IF EXISTS `bee_note`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bee_note` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(9999) NOT NULL,
  `text` longtext NOT NULL,
  `type` varchar(10) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `notebook_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `bee_note_user_id_f147d106_fk_oauth_newuser_id` (`user_id`),
  KEY `bee_note_notebook_id_cfb5c296_fk_bee_notebook_id` (`notebook_id`),
  CONSTRAINT `bee_note_notebook_id_cfb5c296_fk_bee_notebook_id` FOREIGN KEY (`notebook_id`) REFERENCES `bee_notebook` (`id`),
  CONSTRAINT `bee_note_user_id_f147d106_fk_oauth_newuser_id` FOREIGN KEY (`user_id`) REFERENCES `oauth_newuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bee_note`
--

LOCK TABLES `bee_note` WRITE;
/*!40000 ALTER TABLE `bee_note` DISABLE KEYS */;
INSERT INTO `bee_note` VALUES (1,'运维开发分享','### 运维开发分享1\r\n### 运维开发分享2\r\n### 运维开发分享3','markdown','2018-12-29 12:13:00.000000','2018-12-29 12:13:00.000000',1,1),(2,'如何快速致富','<p style=\"text-align: center;\">如何快速致富</p>\n<ol>\n<li><strong>1</strong></li>\n<li><strong>2</strong></li>\n<li><strong>3</strong></li>\n<li><strong>4</strong></li>\n<li>5</li>\n</ol>\n<p>&nbsp;</p>','text','2018-12-31 11:18:00.000000','2019-01-01 05:51:40.543000',1,1),(5,'来自火星的邮件','<p>你好，火星小刘！</p>','text','2019-01-01 04:55:14.993000','2019-01-01 04:59:12.115000',1,1),(6,'欢迎火星小刘。','### 欢迎火星小刘。','markdown','2019-01-01 05:02:55.933000','2019-01-01 05:02:55.933000',1,1);
/*!40000 ALTER TABLE `bee_note` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bee_notebook`
--

DROP TABLE IF EXISTS `bee_notebook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bee_notebook` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(10) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `create_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bee_notebook_user_id_c62242ed_fk_oauth_newuser_id` (`user_id`),
  CONSTRAINT `bee_notebook_user_id_c62242ed_fk_oauth_newuser_id` FOREIGN KEY (`user_id`) REFERENCES `oauth_newuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bee_notebook`
--

LOCK TABLES `bee_notebook` WRITE;
/*!40000 ALTER TABLE `bee_notebook` DISABLE KEYS */;
INSERT INTO `bee_notebook` VALUES (1,'运维',1,'2018-12-29 12:19:00.000000'),(2,'升级',1,'2018-12-30 06:15:00.000000');
/*!40000 ALTER TABLE `bee_notebook` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oauth_newuser`
--

DROP TABLE IF EXISTS `oauth_newuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oauth_newuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `name` varchar(150) NOT NULL,
  `jwt_secret` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth_newuser`
--

LOCK TABLES `oauth_newuser` WRITE;
/*!40000 ALTER TABLE `oauth_newuser` DISABLE KEYS */;
INSERT INTO `oauth_newuser` VALUES (1,'pbkdf2_sha256$120000$92c5c8vti1BM$uxvvVt+q+cpU6qP3gR5X2/11nniFnLPbzImtO+nPio0=','2019-01-02 12:31:03.253865',1,'admin','','','xtlyk@126.com',1,1,'2018-12-29 12:07:00.000000','管理员','d87539ffd86d4b7b89a26c1de6c9afa3'),(2,'pbkdf2_sha256$120000$UU9LtVIXxIXd$P369ELIASw/iHeWFJwQrQPPGorsOKA7OjSp2q5LSugw=','2018-12-29 13:09:00.000000',1,'huoxingxiaoliu','','','xtlyk@126.com',1,1,'2018-12-29 12:18:00.000000','火星小刘','1b847ea202854ff7b8877f7ab6c888c5');
/*!40000 ALTER TABLE `oauth_newuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oauth_newuser_groups`
--

DROP TABLE IF EXISTS `oauth_newuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oauth_newuser_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `newuser_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `oauth_newuser_groups_newuser_id_group_id_a4e081eb_uniq` (`newuser_id`,`group_id`),
  KEY `oauth_newuser_groups_group_id_540cf288_fk_auth_group_id` (`group_id`),
  CONSTRAINT `oauth_newuser_groups_group_id_540cf288_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `oauth_newuser_groups_newuser_id_2eaa6744_fk_oauth_newuser_id` FOREIGN KEY (`newuser_id`) REFERENCES `oauth_newuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth_newuser_groups`
--

LOCK TABLES `oauth_newuser_groups` WRITE;
/*!40000 ALTER TABLE `oauth_newuser_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `oauth_newuser_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oauth_newuser_roles`
--

DROP TABLE IF EXISTS `oauth_newuser_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oauth_newuser_roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `newuser_id` int(11) NOT NULL,
  `roles_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `oauth_newuser_roles_newuser_id_roles_id_3d82b4e6_uniq` (`newuser_id`,`roles_id`),
  KEY `oauth_newuser_roles_roles_id_a62e1032_fk_oauth_roles_id` (`roles_id`),
  CONSTRAINT `oauth_newuser_roles_newuser_id_0bd57cd0_fk_oauth_newuser_id` FOREIGN KEY (`newuser_id`) REFERENCES `oauth_newuser` (`id`),
  CONSTRAINT `oauth_newuser_roles_roles_id_a62e1032_fk_oauth_roles_id` FOREIGN KEY (`roles_id`) REFERENCES `oauth_roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth_newuser_roles`
--

LOCK TABLES `oauth_newuser_roles` WRITE;
/*!40000 ALTER TABLE `oauth_newuser_roles` DISABLE KEYS */;
INSERT INTO `oauth_newuser_roles` VALUES (2,1,2),(1,2,1);
/*!40000 ALTER TABLE `oauth_newuser_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oauth_newuser_user_permissions`
--

DROP TABLE IF EXISTS `oauth_newuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oauth_newuser_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `newuser_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `oauth_newuser_user_permi_newuser_id_permission_id_b5048a99_uniq` (`newuser_id`,`permission_id`),
  KEY `oauth_newuser_user_p_permission_id_a0034217_fk_auth_perm` (`permission_id`),
  CONSTRAINT `oauth_newuser_user_p_newuser_id_878af4f9_fk_oauth_new` FOREIGN KEY (`newuser_id`) REFERENCES `oauth_newuser` (`id`),
  CONSTRAINT `oauth_newuser_user_p_permission_id_a0034217_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth_newuser_user_permissions`
--

LOCK TABLES `oauth_newuser_user_permissions` WRITE;
/*!40000 ALTER TABLE `oauth_newuser_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `oauth_newuser_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oauth_roles`
--

DROP TABLE IF EXISTS `oauth_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oauth_roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `roles` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth_roles`
--

LOCK TABLES `oauth_roles` WRITE;
/*!40000 ALTER TABLE `oauth_roles` DISABLE KEYS */;
INSERT INTO `oauth_roles` VALUES (1,'users'),(2,'admin');
/*!40000 ALTER TABLE `oauth_roles` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-01-02 20:41:56
