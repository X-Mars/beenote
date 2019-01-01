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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'运维部'),(2,'运营部');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add user',6,'add_newuser'),(22,'Can change user',6,'change_newuser'),(23,'Can delete user',6,'delete_newuser'),(24,'Can view user',6,'view_newuser'),(25,'Can add roles',7,'add_roles'),(26,'Can change roles',7,'change_roles'),(27,'Can delete roles',7,'delete_roles'),(28,'Can view roles',7,'view_roles'),(29,'Can add note',8,'add_note'),(30,'Can change note',8,'change_note'),(31,'Can delete note',8,'delete_note'),(32,'Can view note',8,'view_note'),(33,'Can add note book',9,'add_notebook'),(34,'Can change note book',9,'change_notebook'),(35,'Can delete note book',9,'delete_notebook'),(36,'Can view note book',9,'view_notebook');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
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
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_oauth_newuser_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_oauth_newuser_id` FOREIGN KEY (`user_id`) REFERENCES `oauth_newuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2018-12-29 12:13:56.479783','1','Note object (1)',1,'[{\"added\": {}}]',8,1),(2,'2018-12-29 12:18:14.678408','2','liuyongkang',1,'[{\"added\": {}}]',6,1),(3,'2018-12-29 12:18:29.048223','2','liuyongkang',2,'[{\"changed\": {\"fields\": [\"name\", \"is_staff\", \"is_superuser\"]}}]',6,1),(4,'2018-12-29 12:18:38.039974','1','users',1,'[{\"added\": {}}]',7,1),(5,'2018-12-29 12:18:43.295614','2','admin',1,'[{\"added\": {}}]',7,1),(6,'2018-12-29 12:19:11.992439','1','NoteBook object (1)',1,'[{\"added\": {}}]',9,1),(7,'2018-12-29 12:20:43.252167','1','Note object (1)',2,'[{\"changed\": {\"fields\": [\"notebook\"]}}]',8,1),(8,'2018-12-29 12:20:49.584846','1','Note object (1)',2,'[{\"changed\": {\"fields\": [\"user\"]}}]',8,1),(9,'2018-12-29 12:29:45.558927','1','Note object (1)',2,'[]',8,1),(10,'2018-12-29 12:39:42.495321','2','liuyongkang-刘永康',2,'[{\"changed\": {\"fields\": [\"roles\"]}}]',6,1),(11,'2018-12-29 12:40:03.501235','1','admin-管理员',2,'[{\"changed\": {\"fields\": [\"name\", \"roles\", \"last_login\"]}}]',6,1),(12,'2018-12-29 12:41:20.301829','2','liuyongkang-刘永康',2,'[{\"changed\": {\"fields\": [\"email\", \"last_login\"]}}]',6,1),(13,'2018-12-29 12:47:07.797583','1','运维部',1,'[{\"added\": {}}]',3,1),(14,'2018-12-29 12:47:13.624470','2','运营部',1,'[{\"added\": {}}]',3,1),(15,'2018-12-29 13:19:52.906162','1','admin-管理员',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',6,1),(16,'2018-12-30 06:15:38.434077','2','升级-管理员',1,'[{\"added\": {}}]',9,1),(17,'2018-12-31 11:18:17.032525','2','如何快速致富-管理员-text-运维',1,'[{\"added\": {}}]',8,1),(18,'2018-12-31 12:27:41.397974','2','如何快速致富-管理员-text-运维',2,'[{\"changed\": {\"fields\": [\"text\"]}}]',8,1),(19,'2018-12-31 12:27:47.473379','1','运维开发分享-刘永康-text-运维',2,'[{\"changed\": {\"fields\": [\"text\"]}}]',8,1),(20,'2018-12-31 13:08:05.010349','2','如何快速致富-管理员-markdown-运维',2,'[{\"changed\": {\"fields\": [\"type\"]}}]',8,1),(21,'2018-12-31 13:08:09.394045','1','运维开发分享-刘永康-markdown-运维',2,'[{\"changed\": {\"fields\": [\"type\"]}}]',8,1),(22,'2019-01-01 02:23:02.488351','2','如何快速致富-管理员-text-运维',2,'[{\"changed\": {\"fields\": [\"type\"]}}]',8,1),(23,'2019-01-01 02:25:06.122982','2','如何快速致富-管理员-text-运维',2,'[{\"changed\": {\"fields\": [\"text\"]}}]',8,1),(24,'2019-01-01 02:28:43.285430','2','如何快速致富-管理员-text-运维',2,'[{\"changed\": {\"fields\": [\"text\"]}}]',8,1),(25,'2019-01-01 04:56:14.281490','4','Note object (4)',3,'',8,1),(26,'2019-01-01 04:56:14.288832','3','Note object (3)',3,'',8,1),(27,'2019-01-01 05:01:09.070042','1','运维-管理员',2,'[{\"changed\": {\"fields\": [\"user\"]}}]',9,1),(28,'2019-01-01 05:01:23.697450','1','运维开发分享-管理员-markdown-运维',2,'[{\"changed\": {\"fields\": [\"text\", \"user\"]}}]',8,1),(29,'2019-01-01 06:07:58.097884','9','dddd-管理员-text-运维',3,'',8,1),(30,'2019-01-01 06:07:58.101407','8','ddd-管理员-text-运维',3,'',8,1),(31,'2019-01-01 06:07:58.106972','7','dddd-管理员-text-升级',3,'',8,1),(32,'2019-01-01 06:08:22.545628','2','huoxingxiaoliu-火星小刘',2,'[{\"changed\": {\"fields\": [\"username\", \"name\", \"last_login\"]}}]',6,1),(33,'2019-01-01 06:08:48.886614','2','huoxingxiaoliu-火星小刘',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',6,1),(34,'2019-01-01 06:09:20.234757','1','admin-管理员',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',6,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(8,'bee','note'),(9,'bee','notebook'),(4,'contenttypes','contenttype'),(6,'oauth','newuser'),(7,'oauth','roles'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'bee','0001_initial','2018-12-29 12:06:29.688677'),(2,'contenttypes','0001_initial','2018-12-29 12:06:29.769348'),(3,'contenttypes','0002_remove_content_type_name','2018-12-29 12:06:29.832519'),(4,'auth','0001_initial','2018-12-29 12:06:30.084719'),(5,'auth','0002_alter_permission_name_max_length','2018-12-29 12:06:30.112989'),(6,'auth','0003_alter_user_email_max_length','2018-12-29 12:06:30.119941'),(7,'auth','0004_alter_user_username_opts','2018-12-29 12:06:30.128937'),(8,'auth','0005_alter_user_last_login_null','2018-12-29 12:06:30.135644'),(9,'auth','0006_require_contenttypes_0002','2018-12-29 12:06:30.137491'),(10,'auth','0007_alter_validators_add_error_messages','2018-12-29 12:06:30.144495'),(11,'auth','0008_alter_user_username_max_length','2018-12-29 12:06:30.150992'),(12,'auth','0009_alter_user_last_name_max_length','2018-12-29 12:06:30.157583'),(13,'oauth','0001_initial','2018-12-29 12:06:30.583918'),(14,'admin','0001_initial','2018-12-29 12:06:30.671279'),(15,'admin','0002_logentry_remove_auto_add','2018-12-29 12:06:30.684565'),(16,'admin','0003_logentry_add_action_flag_choices','2018-12-29 12:06:30.697367'),(17,'sessions','0001_initial','2018-12-29 12:06:30.743790'),(18,'oauth','0002_auto_20181229_2006','2018-12-29 12:07:19.760517'),(19,'oauth','0003_auto_20181229_2007','2018-12-29 12:07:19.888996'),(20,'bee','0002_auto_20181229_2010','2018-12-29 12:10:16.882980'),(21,'oauth','0004_auto_20181229_2010','2018-12-29 12:10:17.088646'),(22,'bee','0003_notebook_create_time','2018-12-29 12:16:11.219946'),(23,'oauth','0005_auto_20181229_2016','2018-12-29 12:16:11.235337'),(24,'bee','0004_auto_20181229_2017','2018-12-29 12:17:38.809642'),(25,'oauth','0006_auto_20181229_2017','2018-12-29 12:17:38.823640'),(26,'bee','0005_auto_20181231_2108','2018-12-31 13:08:49.438539'),(27,'oauth','0007_auto_20181231_2108','2018-12-31 13:08:49.453995');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('akh3h07c2jti92kds0os7siwy3hznmim','MDY0MjY5YTBlYjhhNWFiYmFhOGU4MWIyZTQ1NjE0ZTU2ODI5YTdmMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyMWYzOGYyZGMwYWQ3MzQ4OTAxY2I4ZmQ1NWNjZTY2MTUwMDk4MzRkIn0=','2019-01-15 06:09:20.246380');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
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
INSERT INTO `oauth_newuser` VALUES (1,'pbkdf2_sha256$120000$Yxh661Skb7Hf$GhMZFY32GWSAqb5w5nRAZakPPtcDu/8HVqwRRBVZdpQ=','2019-01-01 04:35:08.167985',1,'admin','','','xtlyk@126.com',1,1,'2018-12-29 12:07:00.000000','管理员','508d803f84c340eba5b3989336da65bb'),(2,'pbkdf2_sha256$120000$UU9LtVIXxIXd$P369ELIASw/iHeWFJwQrQPPGorsOKA7OjSp2q5LSugw=','2018-12-29 13:09:00.000000',1,'huoxingxiaoliu','','','xtlyk@126.com',1,1,'2018-12-29 12:18:00.000000','火星小刘','1b847ea202854ff7b8877f7ab6c888c5');
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

-- Dump completed on 2019-01-01 14:12:01
