/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.11-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: proyecto
-- ------------------------------------------------------
-- Server version	10.11.11-MariaDB-0+deb12u1

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can view log entry',1,'view_logentry'),
(5,'Can add permission',2,'add_permission'),
(6,'Can change permission',2,'change_permission'),
(7,'Can delete permission',2,'delete_permission'),
(8,'Can view permission',2,'view_permission'),
(9,'Can add group',3,'add_group'),
(10,'Can change group',3,'change_group'),
(11,'Can delete group',3,'delete_group'),
(12,'Can view group',3,'view_group'),
(13,'Can add user',4,'add_user'),
(14,'Can change user',4,'change_user'),
(15,'Can delete user',4,'delete_user'),
(16,'Can view user',4,'view_user'),
(17,'Can add content type',5,'add_contenttype'),
(18,'Can change content type',5,'change_contenttype'),
(19,'Can delete content type',5,'delete_contenttype'),
(20,'Can view content type',5,'view_contenttype'),
(21,'Can add session',6,'add_session'),
(22,'Can change session',6,'change_session'),
(23,'Can delete session',6,'delete_session'),
(24,'Can view session',6,'view_session'),
(25,'Can add server1',7,'add_server1'),
(26,'Can change server1',7,'change_server1'),
(27,'Can delete server1',7,'delete_server1'),
(28,'Can view server1',7,'view_server1'),
(29,'Can add backup config',8,'add_backupconfig'),
(30,'Can change backup config',8,'change_backupconfig'),
(31,'Can delete backup config',8,'delete_backupconfig'),
(32,'Can view backup config',8,'view_backupconfig'),
(33,'Can add captcha store',9,'add_captchastore'),
(34,'Can change captcha store',9,'change_captchastore'),
(35,'Can delete captcha store',9,'delete_captchastore'),
(36,'Can view captcha store',9,'view_captchastore'),
(37,'Can add otp code',10,'add_otpcode'),
(38,'Can change otp code',10,'change_otpcode'),
(39,'Can delete otp code',10,'delete_otpcode'),
(40,'Can view otp code',10,'view_otpcode'),
(41,'Can add otp attempt',11,'add_otpattempt'),
(42,'Can change otp attempt',11,'change_otpattempt'),
(43,'Can delete otp attempt',11,'delete_otpattempt'),
(44,'Can view otp attempt',11,'view_otpattempt'),
(45,'Can add otp intento',11,'add_otpintento'),
(46,'Can change otp intento',11,'change_otpintento'),
(47,'Can delete otp intento',11,'delete_otpintento'),
(48,'Can view otp intento',11,'view_otpintento'),
(49,'Can add Servicio Configurado en Servidor',12,'add_servicioconfigurado'),
(50,'Can change Servicio Configurado en Servidor',12,'change_servicioconfigurado'),
(51,'Can delete Servicio Configurado en Servidor',12,'delete_servicioconfigurado'),
(52,'Can view Servicio Configurado en Servidor',12,'view_servicioconfigurado'),
(53,'Can add Servidor Linux',13,'add_servidor'),
(54,'Can change Servidor Linux',13,'change_servidor'),
(55,'Can delete Servidor Linux',13,'delete_servidor'),
(56,'Can view Servidor Linux',13,'view_servidor');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES
(1,'pbkdf2_sha256$1000000$yirrqjxWIUFrCmb6k6hNUH$Wg5hda1cfLcdr59BZoXzTl8uD2L+jHsmpiQyTK8++P8=','2025-06-02 09:37:49.982944',1,'admin','','','admin@example.com',1,1,'2025-04-28 12:08:25.097644'),
(2,'pbkdf2_sha256$1000000$96RCyqcLPq9OoUmmPFIrEp$iIzY1sEVc+vLu16n5aPCWEh7SeJKIPKVY/ybHNVQxBY=','2025-05-29 15:51:59.513706',1,'oscar','','','oscar@example.com',1,1,'2025-05-29 15:50:34.291463');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backend_otpcode`
--

DROP TABLE IF EXISTS `backend_otpcode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `backend_otpcode` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(10) NOT NULL,
  `creado` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `backend_otpcode_user_id_43bc5e17_fk_auth_user_id` (`user_id`),
  CONSTRAINT `backend_otpcode_user_id_43bc5e17_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backend_otpcode`
--

LOCK TABLES `backend_otpcode` WRITE;
/*!40000 ALTER TABLE `backend_otpcode` DISABLE KEYS */;
/*!40000 ALTER TABLE `backend_otpcode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backend_otpintento`
--

DROP TABLE IF EXISTS `backend_otpintento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `backend_otpintento` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `intentos` int(11) NOT NULL,
  `bloqueado` datetime(6) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `direccion_ip` char(39) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `backend_otpintento_user_id_direccion_ip_5f6ed684_uniq` (`user_id`,`direccion_ip`),
  KEY `backend_otpintento_user_id_1ce97fb4` (`user_id`),
  CONSTRAINT `backend_otpintento_user_id_1ce97fb4_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backend_otpintento`
--

LOCK TABLES `backend_otpintento` WRITE;
/*!40000 ALTER TABLE `backend_otpintento` DISABLE KEYS */;
INSERT INTO `backend_otpintento` VALUES
(28,5,'2025-05-22 17:08:07.710875',1,NULL),
(56,3,'2025-06-02 09:37:59.925299',2,'127.0.0.1');
/*!40000 ALTER TABLE `backend_otpintento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backend_server1`
--

DROP TABLE IF EXISTS `backend_server1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `backend_server1` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `ip` varchar(15) NOT NULL,
  `avala` varchar(100) NOT NULL,
  `usuario_remoto` varchar(50) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `detalles` longtext DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backend_server1`
--

LOCK TABLES `backend_server1` WRITE;
/*!40000 ALTER TABLE `backend_server1` DISABLE KEYS */;
/*!40000 ALTER TABLE `backend_server1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backend_servicioconfigurado`
--

DROP TABLE IF EXISTS `backend_servicioconfigurado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `backend_servicioconfigurado` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre_servicio_remoto` varchar(100) NOT NULL,
  `descripcion_personalizada` longtext NOT NULL,
  `estado_conocido` varchar(20) NOT NULL,
  `puerto_monitorizar` int(10) unsigned DEFAULT NULL CHECK (`puerto_monitorizar` >= 0),
  `comando_verificar_estado` longtext NOT NULL,
  `comando_levantar` longtext NOT NULL,
  `comando_bajar` longtext NOT NULL,
  `comando_reiniciar` longtext NOT NULL,
  `habilitado_para_gestion` tinyint(1) NOT NULL,
  `ultima_comprobacion_estado` datetime(6) DEFAULT NULL,
  `log_ultima_accion` longtext NOT NULL,
  `fecha_configuracion` datetime(6) NOT NULL,
  `ultima_actualizacion_config` datetime(6) NOT NULL,
  `configurado_por_id` int(11) DEFAULT NULL,
  `servidor_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `backend_servicioconfigur_servidor_id_nombre_servi_20b4cd15_uniq` (`servidor_id`,`nombre_servicio_remoto`),
  KEY `backend_servicioconf_configurado_por_id_e6f961e1_fk_auth_user` (`configurado_por_id`),
  CONSTRAINT `backend_servicioconf_configurado_por_id_e6f961e1_fk_auth_user` FOREIGN KEY (`configurado_por_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `backend_servicioconf_servidor_id_ffd856af_fk_backend_s` FOREIGN KEY (`servidor_id`) REFERENCES `backend_servidor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backend_servicioconfigurado`
--

LOCK TABLES `backend_servicioconfigurado` WRITE;
/*!40000 ALTER TABLE `backend_servicioconfigurado` DISABLE KEYS */;
INSERT INTO `backend_servicioconfigurado` VALUES
(1,'bind9.service','servidor dns','inactivo',NULL,'','','','',1,'2025-05-26 10:35:38.737448','','2025-05-26 10:35:22.219181','2025-05-26 10:35:38.737560',1,1);
/*!40000 ALTER TABLE `backend_servicioconfigurado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backend_servidor`
--

DROP TABLE IF EXISTS `backend_servidor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `backend_servidor` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `direccion_host` varchar(255) NOT NULL,
  `usuario_remoto` varchar(50) NOT NULL,
  `ssh_port` int(10) unsigned NOT NULL CHECK (`ssh_port` >= 0),
  `clave_ssh_configurada` tinyint(1) NOT NULL,
  `detalles_adicionales` longtext DEFAULT NULL,
  `fecha_registro` datetime(6) NOT NULL,
  `ultima_modificacion` datetime(6) NOT NULL,
  `registrado_por_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `backend_servidor_registrado_por_id_62980f8d_fk_auth_user_id` (`registrado_por_id`),
  CONSTRAINT `backend_servidor_registrado_por_id_62980f8d_fk_auth_user_id` FOREIGN KEY (`registrado_por_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backend_servidor`
--

LOCK TABLES `backend_servidor` WRITE;
/*!40000 ALTER TABLE `backend_servidor` DISABLE KEYS */;
INSERT INTO `backend_servidor` VALUES
(1,'prueba','192.168.11.129','oscar',22,1,'','2025-05-26 09:24:46.557394','2025-05-26 09:24:46.557418',1);
/*!40000 ALTER TABLE `backend_servidor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `captcha_captchastore`
--

DROP TABLE IF EXISTS `captcha_captchastore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `captcha_captchastore` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `challenge` varchar(32) NOT NULL,
  `response` varchar(32) NOT NULL,
  `hashkey` varchar(40) NOT NULL,
  `expiration` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hashkey` (`hashkey`)
) ENGINE=InnoDB AUTO_INCREMENT=350 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `captcha_captchastore`
--

LOCK TABLES `captcha_captchastore` WRITE;
/*!40000 ALTER TABLE `captcha_captchastore` DISABLE KEYS */;
INSERT INTO `captcha_captchastore` VALUES
(339,'NILF','nilf','212285fdeed300b8b5f3cc74ebeb6a3543d34ed1','2025-06-02 09:38:32.064641'),
(340,'EQGG','eqgg','09bf2420d4f952f53140289ef3b188bc319a25f0','2025-06-02 09:39:12.947543'),
(345,'NFJV','nfjv','57bcc86b1f3a3331e78dc173b2b60771dce65a84','2025-06-02 09:41:13.850698'),
(349,'WHPA','whpa','b0b2027e0fd74fb89d8c905b27b8bd77f059f216','2025-06-02 09:42:55.567229');
/*!40000 ALTER TABLE `captcha_captchastore` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES
(1,'admin','logentry'),
(3,'auth','group'),
(2,'auth','permission'),
(4,'auth','user'),
(8,'backend','backupconfig'),
(10,'backend','otpcode'),
(11,'backend','otpintento'),
(7,'backend','server1'),
(12,'backend','servicioconfigurado'),
(13,'backend','servidor'),
(9,'captcha','captchastore'),
(5,'contenttypes','contenttype'),
(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES
(1,'contenttypes','0001_initial','2025-04-28 12:03:21.111616'),
(2,'auth','0001_initial','2025-04-28 12:03:22.224059'),
(3,'admin','0001_initial','2025-04-28 12:03:22.454217'),
(4,'admin','0002_logentry_remove_auto_add','2025-04-28 12:03:22.465283'),
(5,'admin','0003_logentry_add_action_flag_choices','2025-04-28 12:03:22.474452'),
(6,'contenttypes','0002_remove_content_type_name','2025-04-28 12:03:22.616970'),
(7,'auth','0002_alter_permission_name_max_length','2025-04-28 12:03:22.712462'),
(8,'auth','0003_alter_user_email_max_length','2025-04-28 12:03:22.767252'),
(9,'auth','0004_alter_user_username_opts','2025-04-28 12:03:22.777034'),
(10,'auth','0005_alter_user_last_login_null','2025-04-28 12:03:22.859707'),
(11,'auth','0006_require_contenttypes_0002','2025-04-28 12:03:22.863652'),
(12,'auth','0007_alter_validators_add_error_messages','2025-04-28 12:03:22.872389'),
(13,'auth','0008_alter_user_username_max_length','2025-04-28 12:03:22.924393'),
(14,'auth','0009_alter_user_last_name_max_length','2025-04-28 12:03:22.974455'),
(15,'auth','0010_alter_group_name_max_length','2025-04-28 12:03:23.038178'),
(16,'auth','0011_update_proxy_permissions','2025-04-28 12:03:23.048630'),
(17,'auth','0012_alter_user_first_name_max_length','2025-04-28 12:03:23.098334'),
(18,'backend','0001_initial','2025-04-28 12:03:23.334667'),
(19,'backend','0002_server1_delete_backupconfig_delete_server','2025-04-28 12:03:23.420615'),
(20,'backend','0003_rename_server1_server','2025-04-28 12:03:23.465522'),
(21,'backend','0004_backupconfig','2025-04-28 12:03:23.670979'),
(22,'backend','0005_server1_delete_backupconfig_delete_server','2025-04-28 12:03:23.753136'),
(23,'backend','0006_backupconfig','2025-04-28 12:03:23.976090'),
(24,'backend','0007_remove_server1_exitoso','2025-04-28 12:03:24.035882'),
(25,'backend','0008_auto_20231206_1935','2025-04-28 12:03:24.148524'),
(26,'backend','0009_remove_backupconfig_server_origen','2025-04-28 12:03:24.257061'),
(27,'backend','0010_backupconfig_server_remitente','2025-04-28 12:03:24.354707'),
(28,'backend','0011_alter_backupconfig_server_remitente','2025-04-28 12:03:24.508400'),
(29,'backend','0012_rename_server_remitente_backupconfig_server_re','2025-04-28 12:03:24.766576'),
(30,'backend','0013_rename_server_re_backupconfig_server_remitente','2025-04-28 12:03:24.958796'),
(31,'backend','0014_backupconfig_comando_cron','2025-04-28 12:03:25.015014'),
(32,'backend','0015_auto_20231224_0356','2025-04-28 12:03:25.132769'),
(33,'backend','0016_auto_20231225_1531','2025-04-28 12:03:25.241314'),
(34,'backend','0017_alter_backupconfig_comando_cron','2025-04-28 12:03:25.288994'),
(35,'backend','0018_alter_backupconfig_comando_cron','2025-04-28 12:03:25.336309'),
(36,'backend','0019_auto_20231225_1551','2025-04-28 12:03:25.447096'),
(37,'sessions','0001_initial','2025-04-28 12:03:25.575802'),
(38,'captcha','0001_initial','2025-05-05 09:49:32.831741'),
(39,'captcha','0002_alter_captchastore_id','2025-05-05 09:49:32.837518'),
(40,'backend','0020_otpcode','2025-05-19 04:14:11.388427'),
(41,'backend','0021_otpattempt','2025-05-19 06:39:40.396360'),
(42,'backend','0022_delete_backupconfig','2025-05-19 10:22:46.262853'),
(43,'backend','0023_rename_locked_until_otpattempt_bloqueado_and_more','2025-05-19 16:57:36.039672'),
(44,'backend','0024_rename_otpattempt_otpintento','2025-05-19 17:15:57.171254'),
(45,'backend','0025_rename_code_otpcode_codigo_otpintento_direccion_ip_and_more','2025-05-26 00:58:46.022815'),
(46,'backend','0026_servidor_servicioconfigurado','2025-05-26 08:56:31.030730');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES
('0dxb359kxuifgw4aowgr0ku1vy0h684z','eyJwcmVhdXRoX3VzZXJfaWQiOjF9:1uH3s9:Q2_AquHQZ3LD7kYGfHKkApmMgaoavCEh_LQfM1M7WFg','2025-05-19 17:11:53.958713'),
('2f8g91vu3cfdm2u4crni1so9ohlq23ul','.eJxVjDsOwjAQBe_iGlnrb2xKes5g7fqDA8iW4qRC3B0ipYD2zcx7sYDbWsM28hLmxM5MsNPvRhgfue0g3bHdOo-9rctMfFf4QQe_9pSfl8P9O6g46rfW5IpKwls00YPyiM6CymTATFlLA44UuViUt5OhIjVFKQRZDQhgYmHvD9F5N2E:1uEOST:LcNrhIgA6nKeeRqvvTpJyYbiPXYQcgyPZOPoBnEs9b4','2025-05-12 08:34:21.819624'),
('30egiobyhphxy0dx6jtb8o9y740vqsyp','eyJwcmVhdXRoX3VzZXJfaWQiOjF9:1uGvBs:lA_DLEJJiGKa3VHwaWp6VhZi8D_B84zxutXgZWLDPd8','2025-05-19 07:55:40.171122'),
('3byxq6bzclsu9yyphuszcvjs2viokac3','eyJwcmVhdXRoX3VzZXJfaWQiOjF9:1uGxrq:6MaUL3Zjd_OriCITKH8ShpUQHPhsDDfhH9WV8kV6G7U','2025-05-19 10:47:10.227282'),
('4gs3zvqqssi7xj6rv1hu0mjiprmkj3xf','.eJxVjDsOwjAQBe_iGlnrb2xKes5g7fqDA8iW4qRC3B0ipYD2zcx7sYDbWsM28hLmxM5MsNPvRhgfue0g3bHdOo-9rctMfFf4QQe_9pSfl8P9O6g46rfW5IpKwls00YPyiM6CymTATFlLA44UuViUt5OhIjVFKQRZDQhgYmHvD9F5N2E:1uGyBb:9vqr9Cvv9DBs9LZZpYk_Sqx7Asoj5I7hac589OxfkL4','2025-05-19 11:07:35.577619'),
('56sn1qk7mpkyoxbqhekppoyb4a140990','eyJwcmVhdXRoX3VzZXJfaWQiOjF9:1uGvTw:pc5TiI2IvUc9QThX5RIROLJFz-XMIopi4fBtTSAVTl0','2025-05-19 08:14:20.780608'),
('5sclna4fobnr16cj29e7wc0w8eosr99x','eyJwcmVhdXRoX3VzZXJfaWQiOjF9:1uJMkD:eZjgWNUa6fCrgCB6nxfsPxM9Ejo5OZXYtKDFzCpUDzA','2025-05-26 01:45:13.210589'),
('6l21t74tkeyqyo0jjqkuc975y4zlyk0q','.eJxVjDsOwjAQBe_iGlnrb2xKes5g7fqDA8iW4qRC3B0ipYD2zcx7sYDbWsM28hLmxM5MsNPvRhgfue0g3bHdOo-9rctMfFf4QQe_9pSfl8P9O6g46rfW5IpKwls00YPyiM6CymTATFlLA44UuViUt5OhIjVFKQRZDQhgYmHvD9F5N2E:1uJTz8:1Carthu6hWJsSjDVTWB7MBzBtPG6kOe4ZAl7ACNug7A','2025-05-26 09:29:06.737020'),
('6npp0qpqgx0uommmak6dqdc1rojchls9','eyJwcmVhdXRoX3VzZXJfaWQiOjF9:1uGruh:Y-STYeguFATvZm6KEb40Wm3s7Bfhig-ol3038jEkRYA','2025-05-19 04:25:43.853955'),
('8e2szdw4mi0rhe1ubdrzdoqn8w1exyuv','eyJwcmVhdXRoX3VzZXJfaWQiOjF9:1uJMWu:wInhFvEfdIJCsizugfTbpmwU3luXWepMjc7J-PwJsf0','2025-05-26 01:31:28.522189'),
('9rzeyr67ko3b2rt5trmydmv8ujkbhqta','.eJxVjDsOwjAQBe_iGlnrb2xKes5g7fqDA8iW4qRC3B0ipYD2zcx7sYDbWsM28hLmxM5MsNPvRhgfue0g3bHdOo-9rctMfFf4QQe_9pSfl8P9O6g46rfW5IpKwls00YPyiM6CymTATFlLA44UuViUt5OhIjVFKQRZDQhgYmHvD9F5N2E:1uBscT:6OjphWT7T6HuJaB5PGrYIOdhRdFuvmG6j3yN0YwuJAI','2025-05-05 10:10:17.362324'),
('drivp0nnu6i2ud428otbsqxn2trhq5fh','.eJxVjDsOwjAQBe_iGlnrb2xKes5g7fqDA8iW4qRC3B0ipYD2zcx7sYDbWsM28hLmxM5MsNPvRhgfue0g3bHdOo-9rctMfFf4QQe_9pSfl8P9O6g46rfW5IpKwls00YPyiM6CymTATFlLA44UuViUt5OhIjVFKQRZDQhgYmHvD9F5N2E:1uJUhe:kTLaX9rQxpFnxcJABt98bso7uDOoJ8iPL-vC5yRbrgg','2025-05-26 10:15:06.355597'),
('f228nyzjlx0i5irozmael36u15z4b063','.eJxVjDsOwjAQBe_iGlnrb2xKes5g7fqDA8iW4qRC3B0ipYD2zcx7sYDbWsM28hLmxM5MsNPvRhgfue0g3bHdOo-9rctMfFf4QQe_9pSfl8P9O6g46rfW5IpKwls00YPyiM6CymTATFlLA44UuViUt5OhIjVFKQRZDQhgYmHvD9F5N2E:1uJSvd:OIXaomjbNFmZSVotFfwcJMiJ5qgw8turyaW8DjxwnqI','2025-05-26 08:21:25.498826'),
('fcojn17f9c7lutru3cshhwtcn0355vg5','.eJxVjDsOwjAQBe_iGlm24x-U9DmDtd5d4wBypDipEHeHSCmgfTPzXiLBtta0dV7SROIitDj9bhnwwW0HdId2myXObV2mLHdFHrTLcSZ-Xg_376BCr9_aOQrWQjzrWBCU4wCW0A0GQGUTTCxGMw-ePYKO6NEGVwiKCk5lq0m8P-YOOCU:1u9NR6:g23BzevIxZnL5l2Vqu1tR6xPZdP6F8Hd00vPZHRZE8E','2025-04-28 12:28:12.357995'),
('iit7r07qnmaxa29g8hquxnfpgzxvird7','eyJwcmVhdXRoX3VzZXJfaWQiOjF9:1uGuDt:6A_rFH6JsSveaLDd43e3JNLiRnS6SmU8aA9TIG5lkwE','2025-05-19 06:53:41.827380'),
('ir9g6vll3libiuivba9wlotn4jumuvrx','.eJxVjDsOwjAQBe_iGlm24x-U9DmDtd5d4wBypDipEHeHSCmgfTPzXiLBtta0dV7SROIitDj9bhnwwW0HdId2myXObV2mLHdFHrTLcSZ-Xg_376BCr9_aOQrWQjzrWBCU4wCW0A0GQGUTTCxGMw-ePYKO6NEGVwiKCk5lq0m8P-YOOCU:1u9QdZ:1RQK_S0dGyJLWb1FASQdWcLlbrVrr4ijLqXm0db9W5g','2025-04-28 15:53:17.754818'),
('l1z4ja3ra9wofy9585cwfzem8qe85gmx','eyJwcmVhdXRoX3VzZXJfaWQiOjF9:1uGw3k:NZUk5D917vNxJ00TLBZaASjQlqQd6MQR3-LRfDlH_LA','2025-05-19 08:51:20.952646'),
('meemhk8scg2t6qx5pqsqzs27q07r57x8','eyJwcmVhdXRoX3VzZXJfaWQiOjF9:1uGwLg:Gd8J2_PnSodbyGqFiMMP6Htw0Rj-q8eLJ5TBwCEW5eQ','2025-05-19 09:09:52.672362'),
('o124x0llcv1oudoxuhtsvj3onbg4gsl5','.eJxVjDsOwjAQBe_iGlnrb2xKes5g7fqDA8iW4qRC3B0ipYD2zcx7sYDbWsM28hLmxM5MsNPvRhgfue0g3bHdOo-9rctMfFf4QQe_9pSfl8P9O6g46rfW5IpKwls00YPyiM6CymTATFlLA44UuViUt5OhIjVFKQRZDQhgYmHvD9F5N2E:1uJV7e:CVZdhRy8XjTApip8O8kbGQPrh8nIgzSsUqEX5mTYglc','2025-05-26 10:41:58.065663'),
('o5q9bl9c7cgn82vne3av4p6ym1zuxzga','.eJxVjDsOwjAQBe_iGlnrb2xKes5g7fqDA8iW4qRC3B0ipYD2zcx7sYDbWsM28hLmxM5MsNPvRhgfue0g3bHdOo-9rctMfFf4QQe_9pSfl8P9O6g46rfW5IpKwls00YPyiM6CymTATFlLA44UuViUt5OhIjVFKQRZDQhgYmHvD9F5N2E:1uEXhF:RUzVOauUnVXzj-1rdaRP9mvEeTUlqL0LsuAgcMaaM9M','2025-05-12 18:26:13.886300'),
('ohk9y60dftb0fyt8n1e7xrj6b7k05rt6','.eJxVjDsOwjAQBe_iGlnrb2xKes5g7fqDA8iW4qRC3B0ipYD2zcx7sYDbWsM28hLmxM5MsNPvRhgfue0g3bHdOo-9rctMfFf4QQe_9pSfl8P9O6g46rfW5IpKwls00YPyiM6CymTATFlLA44UuViUt5OhIjVFKQRZDQhgYmHvD9F5N2E:1uJOzj:A0PuFAzZ5p8av6xeqYJxMzHRTvD29RoJ8rnXEU0lSCc','2025-05-26 04:09:23.686258'),
('pl4h3lf0f3ijeytrrzvh4w2uyir2pb06','eyJwcmVhdXRoX3VzZXJfaWQiOjF9:1uGwKF:bft6wD0RxWEec28nKUFNLjx-J3jUnyGDpfo1qMBJIuA','2025-05-19 09:08:23.179723'),
('s1sk8kj6k4g0w9fdyzge2yxnbzoap5iv','.eJxVjDsOwjAQBe_iGlnrb2xKes5g7fqDA8iW4qRC3B0ipYD2zcx7sYDbWsM28hLmxM5MsNPvRhgfue0g3bHdOo-9rctMfFf4QQe_9pSfl8P9O6g46rfW5IpKwls00YPyiM6CymTATFlLA44UuViUt5OhIjVFKQRZDQhgYmHvD9F5N2E:1uJUPG:7TZDJ_oE6CScxFpvw6pg6aeKlm180y_fPJK2POfVUY8','2025-05-26 09:56:06.044309'),
('sfu6j3r5ommqcny8co92vcxd79uxz4hv','.eJxVjDsOwjAQBe_iGlnrb2xKes5g7fqDA8iW4qRC3B0ipYD2zcx7sYDbWsM28hLmxM5MsNPvRhgfue0g3bHdOo-9rctMfFf4QQe_9pSfl8P9O6g46rfW5IpKwls00YPyiM6CymTATFlLA44UuViUt5OhIjVFKQRZDQhgYmHvD9F5N2E:1uJa2g:h5IfsTvpTLLEkWzq3EdLu8a-YBDhLFZ87hnpOJuoYqE','2025-05-26 15:57:10.829810'),
('wozd8yvqv3o33skk7f8nulx4jct4uo8q','.eJxVjDsOwjAQBe_iGlnrb2xKes5g7fqDA8iW4qRC3B0ipYD2zcx7sYDbWsM28hLmxM5MsNPvRhgfue0g3bHdOo-9rctMfFf4QQe_9pSfl8P9O6g46rfW5IpKwls00YPyiM6CymTATFlLA44UuViUt5OhIjVFKQRZDQhgYmHvD9F5N2E:1uJOo3:h2eIHfM_Jup5u7O8BT7LNVsLb9MpKTWmLQVJjBhN0u0','2025-05-26 03:57:19.460031'),
('x6pl7htbzxy7fvobyikcistf6tw8qxk6','.eJxVjDsOwjAQBe_iGlnrb2xKes5g7fqDA8iW4qRC3B0ipYD2zcx7sYDbWsM28hLmxM5MsNPvRhgfue0g3bHdOo-9rctMfFf4QQe_9pSfl8P9O6g46rfW5IpKwls00YPyiM6CymTATFlLA44UuViUt5OhIjVFKQRZDQhgYmHvD9F5N2E:1uJU9K:9t7RzwYajMUKoAd644SRJw9puRqZC80FzGRFQhrvYA0','2025-05-26 09:39:38.785258'),
('ynifzupw587ec2iarkyby0xsjmgz19tk','eyJwcmVhdXRoX3VzZXJfaWQiOjF9:1uH4FU:5SfH8DeDO2dNFed4SeiZ-pL-Bsh1ODr_8aiE0Px9zIs','2025-05-19 17:36:00.631051'),
('ysrznqpg768wynakcnw8mh018ag7p0u4','.eJxVjDsOwjAQBe_iGlm24x-U9DmDtd5d4wBypDipEHeHSCmgfTPzXiLBtta0dV7SROIitDj9bhnwwW0HdId2myXObV2mLHdFHrTLcSZ-Xg_376BCr9_aOQrWQjzrWBCU4wCW0A0GQGUTTCxGMw-ePYKO6NEGVwiKCk5lq0m8P-YOOCU:1u9Nt6:lwsrMEA2aoOBgVDbfcJ8WKlNPbPaXeCn_4qAVHdi0_A','2025-04-28 12:57:08.648740'),
('z46e4mhpa7q0tf9x9ueecxtbnbm9yg0b','.eJxVjDsOwjAQBe_iGlnrb2xKes5g7fqDA8iW4qRC3B0ipYD2zcx7sYDbWsM28hLmxM5MsNPvRhgfue0g3bHdOo-9rctMfFf4QQe_9pSfl8P9O6g46rfW5IpKwls00YPyiM6CymTATFlLA44UuViUt5OhIjVFKQRZDQhgYmHvD9F5N2E:1uGrxV:iXydRUPBpPKa8jVMW04xHLl5Bl709vofDzbVZDXpgww','2025-05-19 04:28:37.866156'),
('zwzv38o1hhxtnom1vg0y591ir5iskzu1','.eJxVjDsOwjAQBe_iGlnrb2xKes5g7fqDA8iW4qRC3B0ipYD2zcx7sYDbWsM28hLmxM5MsNPvRhgfue0g3bHdOo-9rctMfFf4QQe_9pSfl8P9O6g46rfW5IpKwls00YPyiM6CymTATFlLA44UuViUt5OhIjVFKQRZDQhgYmHvD9F5N2E:1uJUsZ:ZBIdFhtblb3TOONmBEeJoxx3uQGHwGRqgr0KYi0H584','2025-05-26 10:26:23.777551');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-02  5:19:57
