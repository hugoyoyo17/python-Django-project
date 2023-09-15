-- MySQL dump 10.13  Distrib 8.0.27, for Linux (x86_64)
--
-- Host: localhost    Database: miumiushop
-- ------------------------------------------------------
-- Server version	8.0.27

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

--
-- Table structure for table `goods_brand`
--

DROP TABLE IF EXISTS `goods_brand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `goods_brand` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goods_brand`
--

LOCK TABLES `goods_brand` WRITE;
/*!40000 ALTER TABLE `goods_brand` DISABLE KEYS */;
INSERT INTO `goods_brand` VALUES (1,'切爾思','2023-05-24 17:33:54.924722','2023-05-24 17:33:54.925515'),(2,'沛瑞思','2023-05-24 17:34:22.840430','2023-05-24 17:34:22.840489'),(3,'哈里斯','2023-05-24 17:34:40.845620','2023-05-24 17:34:40.845657');
/*!40000 ALTER TABLE `goods_brand` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `goods_catalog`
--

DROP TABLE IF EXISTS `goods_catalog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `goods_catalog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(10) NOT NULL,
  `product_for` varchar(10) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goods_catalog`
--

LOCK TABLES `goods_catalog` WRITE;
/*!40000 ALTER TABLE `goods_catalog` DISABLE KEYS */;
INSERT INTO `goods_catalog` VALUES (1,'飼料','狗','2023-05-24 17:35:04.011678','2023-05-24 17:35:04.011716'),(2,'飼料','貓','2023-05-24 17:35:11.317471','2023-05-24 17:35:11.317514'),(3,'罐頭','狗','2023-05-24 17:35:22.588783','2023-05-24 17:35:22.588823'),(4,'罐頭','貓','2023-05-24 17:35:29.944331','2023-05-24 17:35:29.944369'),(5,'零食','狗','2023-05-24 17:35:36.265530','2023-05-24 17:35:36.265568'),(6,'零食','貓','2023-05-24 17:35:46.596293','2023-05-24 17:35:46.596376');
/*!40000 ALTER TABLE `goods_catalog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `goods_sale_attr_value`
--

DROP TABLE IF EXISTS `goods_sale_attr_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `goods_sale_attr_value` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `spu_sale_attr_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `goods_sale_attr_valu_spu_sale_attr_id_0b44357f_fk_goods_spu` (`spu_sale_attr_id`),
  CONSTRAINT `goods_sale_attr_valu_spu_sale_attr_id_0b44357f_fk_goods_spu` FOREIGN KEY (`spu_sale_attr_id`) REFERENCES `goods_spu_sale_attr` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goods_sale_attr_value`
--

LOCK TABLES `goods_sale_attr_value` WRITE;
/*!40000 ALTER TABLE `goods_sale_attr_value` DISABLE KEYS */;
INSERT INTO `goods_sale_attr_value` VALUES (1,'2KG','2023-05-24 19:47:26.342657','2023-05-24 19:47:26.342694',1),(2,'6.8KG','2023-05-24 19:47:41.094066','2023-05-24 19:47:41.094102',1),(3,'12KG','2023-05-24 19:48:11.991641','2023-05-24 19:48:11.991677',1),(4,'2KG','2023-05-25 08:31:42.421082','2023-05-25 08:31:42.421117',2),(5,'6.8KG','2023-05-25 08:32:43.188233','2023-05-25 08:32:43.188267',2),(6,'12KG','2023-05-25 08:33:15.581277','2023-05-25 08:33:15.581313',2),(7,'羊肉口味','2023-05-25 08:36:31.602403','2023-05-25 08:36:31.602439',3),(8,'雞肉口味','2023-05-25 08:37:58.896693','2023-05-25 08:37:58.896728',3),(9,'羊肉口味','2023-05-25 08:39:48.355862','2023-05-25 08:39:48.355893',4),(10,'雞肉口味','2023-05-25 08:40:38.298974','2023-05-25 08:40:38.299006',4),(11,'1罐','2023-05-25 08:46:00.809538','2023-05-25 08:46:00.809629',5),(12,'一盒6入','2023-05-25 08:47:39.014974','2023-05-25 08:47:39.015007',5),(13,'1罐','2023-05-25 08:49:05.102068','2023-05-25 08:49:05.102103',6),(14,'1盒6入','2023-05-25 08:49:53.877910','2023-05-25 08:49:53.877945',6);
/*!40000 ALTER TABLE `goods_sale_attr_value` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `goods_sku`
--

DROP TABLE IF EXISTS `goods_sku`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `goods_sku` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `caption` varchar(100) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `cost_price` decimal(10,2) NOT NULL,
  `market_price` decimal(10,2) NOT NULL,
  `sales` int NOT NULL,
  `comments` int NOT NULL,
  `is_launched` tinyint(1) NOT NULL,
  `default_image_url` varchar(100) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `spu_id` bigint NOT NULL,
  `stock_number` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `goods_sku_spu_id_9392246b_fk_goods_spu_id` (`spu_id`),
  CONSTRAINT `goods_sku_spu_id_9392246b_fk_goods_spu_id` FOREIGN KEY (`spu_id`) REFERENCES `goods_spu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goods_sku`
--

LOCK TABLES `goods_sku` WRITE;
/*!40000 ALTER TABLE `goods_sku` DISABLE KEYS */;
INSERT INTO `goods_sku` VALUES (2,'老犬飼料 長壽配方 低過敏 小顆粒 狗飼料','2KG',600.00,850.00,850.00,81,0,1,'sku/dog_feed_At1woIA.jpg','2023-05-24 19:57:51.725406','2023-06-28 12:28:08.192561',1,19),(3,'老犬飼料 長壽配方 低過敏 小顆粒 狗飼料','6.8KG',1800.00,2100.00,2100.00,100,0,1,'sku/dog_feed_qlRiwGJ.jpg','2023-05-24 20:24:53.867285','2023-06-27 10:14:06.068570',1,0),(4,'老犬飼料 長壽配方 低過敏 小顆粒 狗飼料','12KG',3100.00,3400.00,3400.00,0,0,1,'sku/dog_feed_A2Ke8sL.jpg','2023-05-24 20:31:39.365159','2023-06-27 10:14:19.693986',1,50),(5,'火雞+雞肉 挑嘴全齡 貓飼料','2KG',600.00,850.00,850.00,20,0,1,'sku/cat_feed_qBx67ef.jpg','2023-05-25 08:31:49.101631','2023-06-27 10:14:31.872851',2,80),(6,'火雞+雞肉 挑嘴全齡 貓飼料','6.8KG',1800.00,2100.00,2100.00,50,0,1,'sku/cat_feed_9Bkd8TT.jpg','2023-05-25 08:32:45.554463','2023-05-26 18:56:13.920163',2,50),(7,'火雞+雞肉 挑嘴全齡 貓飼料','12KG',3100.00,3400.00,3400.00,40,0,1,'sku/cat_feed_Z0KqQuQ.jpg','2023-05-25 08:33:18.165371','2023-06-17 22:02:27.130558',2,10),(8,'愛犬機能餐罐 100g','羊肉口味',20.00,30.00,30.00,0,0,1,'sku/dog_can_lamb_0suu8Wp.jpg','2023-05-25 08:36:40.499046','2023-05-25 17:58:41.348798',3,500),(9,'愛犬機能餐罐 100g','雞肉口味',20.00,30.00,30.00,0,0,1,'sku/dog_can_chicken_sdCQrp7.jpg','2023-05-25 08:38:01.202854','2023-05-25 08:38:01.202891',3,0),(10,'愛貓機能餐罐 100g','羊肉口味',20.00,30.00,30.00,0,0,1,'sku/cat_can_lamb_BuEm5Or.jpg','2023-05-25 08:39:52.808554','2023-05-25 17:59:21.281797',4,500),(11,'愛貓機能餐罐 100g','雞肉口味',20.00,30.00,30.00,0,0,1,'sku/cat_can_chicken_RDfGHje.jpg','2023-05-25 08:40:40.040868','2023-05-25 17:59:33.346465',4,500),(12,'狗狗凍乾零食-毛鱗魚60g','1罐',200.00,280.00,280.00,200,0,1,'sku/dog_snack_YjP1m91.jpg','2023-05-25 08:46:03.620791','2023-05-25 19:08:47.745082',5,800),(13,'狗狗凍乾零食-毛鱗魚60g','1盒6入',1000.00,1200.00,1200.00,20,0,1,'sku/dog_snack_nRsUX0X.jpg','2023-05-25 08:47:43.108465','2023-05-25 19:08:47.753180',5,30),(14,'貓咪凍乾零食-鱈魚 60g','1罐',200.00,280.00,280.00,0,0,1,'sku/cat_snack_WewlzV4.png','2023-05-25 08:49:07.426870','2023-05-25 18:01:15.484822',6,1000),(15,'貓咪凍乾零食-鱈魚 60g','1盒6入',1000.00,1200.00,1200.00,0,0,1,'sku/cat_snack_p1jQOdq.png','2023-05-25 08:49:55.592889','2023-07-09 10:07:11.754242',6,50);
/*!40000 ALTER TABLE `goods_sku` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `goods_sku_comment`
--

DROP TABLE IF EXISTS `goods_sku_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `goods_sku_comment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `score` int NOT NULL,
  `comment_text` longtext NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `sku_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `goods_sku_comment_sku_id_6834aac3_fk_goods_sku_id` (`sku_id`),
  CONSTRAINT `goods_sku_comment_sku_id_6834aac3_fk_goods_sku_id` FOREIGN KEY (`sku_id`) REFERENCES `goods_sku` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goods_sku_comment`
--

LOCK TABLES `goods_sku_comment` WRITE;
/*!40000 ALTER TABLE `goods_sku_comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `goods_sku_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `goods_sku_image`
--

DROP TABLE IF EXISTS `goods_sku_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `goods_sku_image` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `sku_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `goods_sku_image_sku_id_c00116ee_fk_goods_sku_id` (`sku_id`),
  CONSTRAINT `goods_sku_image_sku_id_c00116ee_fk_goods_sku_id` FOREIGN KEY (`sku_id`) REFERENCES `goods_sku` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goods_sku_image`
--

LOCK TABLES `goods_sku_image` WRITE;
/*!40000 ALTER TABLE `goods_sku_image` DISABLE KEYS */;
/*!40000 ALTER TABLE `goods_sku_image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `goods_sku_sale_attr_value`
--

DROP TABLE IF EXISTS `goods_sku_sale_attr_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `goods_sku_sale_attr_value` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sku_id` bigint NOT NULL,
  `saleattrvalue_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `goods_sku_sale_attr_value_sku_id_saleattrvalue_id_80ce7a94_uniq` (`sku_id`,`saleattrvalue_id`),
  KEY `goods_sku_sale_attr__saleattrvalue_id_7e2dfed2_fk_goods_sal` (`saleattrvalue_id`),
  CONSTRAINT `goods_sku_sale_attr__saleattrvalue_id_7e2dfed2_fk_goods_sal` FOREIGN KEY (`saleattrvalue_id`) REFERENCES `goods_sale_attr_value` (`id`),
  CONSTRAINT `goods_sku_sale_attr_value_sku_id_2fc83e9f_fk_goods_sku_id` FOREIGN KEY (`sku_id`) REFERENCES `goods_sku` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goods_sku_sale_attr_value`
--

LOCK TABLES `goods_sku_sale_attr_value` WRITE;
/*!40000 ALTER TABLE `goods_sku_sale_attr_value` DISABLE KEYS */;
INSERT INTO `goods_sku_sale_attr_value` VALUES (2,2,1),(3,3,2),(4,4,3),(5,5,4),(6,6,5),(7,7,6),(8,8,7),(9,9,8),(10,10,9),(11,11,10),(12,12,11),(13,13,12),(14,14,13),(15,15,14);
/*!40000 ALTER TABLE `goods_sku_sale_attr_value` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `goods_sku_stock`
--

DROP TABLE IF EXISTS `goods_sku_stock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `goods_sku_stock` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `storage_in_out` varchar(5) NOT NULL,
  `person_in_charge` varchar(10) NOT NULL,
  `quantity` int NOT NULL,
  `version` int NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `sku_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `goods_sku_stock_sku_id_8e55acbe_fk_goods_sku_id` (`sku_id`),
  CONSTRAINT `goods_sku_stock_sku_id_8e55acbe_fk_goods_sku_id` FOREIGN KEY (`sku_id`) REFERENCES `goods_sku` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goods_sku_stock`
--

LOCK TABLES `goods_sku_stock` WRITE;
/*!40000 ALTER TABLE `goods_sku_stock` DISABLE KEYS */;
INSERT INTO `goods_sku_stock` VALUES (1,'入庫','劉軒佑',100,0,'2023-05-25 08:52:05.851077','2023-05-25 08:52:48.737664',2),(2,'出庫','劉軒佑',81,0,'2023-05-25 08:53:02.887565','2023-05-25 08:53:02.887599',2),(3,'入庫','劉軒佑',100,0,'2023-05-25 08:53:24.560702','2023-05-25 08:53:24.560736',3),(4,'出庫','劉軒佑',100,0,'2023-05-25 08:53:35.601403','2023-05-25 08:53:35.601435',3),(5,'入庫','劉軒佑',50,0,'2023-05-25 08:53:51.430267','2023-05-25 08:53:51.430304',4),(6,'入庫','劉軒佑',100,0,'2023-05-25 08:54:44.778986','2023-05-25 08:54:44.779024',5),(7,'出庫','劉軒佑',20,0,'2023-05-25 08:55:06.639073','2023-05-25 08:55:06.639107',5),(8,'入庫','劉軒佑',100,0,'2023-05-25 08:55:47.098081','2023-05-25 08:55:47.098118',6),(9,'出庫','劉軒佑',50,0,'2023-05-25 08:55:58.913947','2023-05-25 08:55:58.913983',6),(10,'入庫','劉軒佑',50,0,'2023-05-25 08:56:25.534542','2023-05-25 08:56:25.534579',7),(11,'出庫','劉軒佑',40,0,'2023-05-25 08:56:45.114915','2023-05-25 08:56:45.114947',7),(12,'入庫','劉軒佑',500,0,'2023-05-25 08:58:31.797997','2023-05-25 08:58:31.798031',8),(13,'入庫','劉軒佑',500,0,'2023-05-25 08:59:03.202475','2023-05-25 08:59:03.202513',10),(14,'入庫','劉軒佑',500,0,'2023-05-25 08:59:59.103314','2023-05-25 08:59:59.103369',11),(15,'入庫','劉軒佑',1000,0,'2023-05-25 09:00:38.141243','2023-05-25 09:00:38.141350',12),(16,'出庫','劉軒佑',200,0,'2023-05-25 09:01:05.259853','2023-05-25 09:01:05.259887',12),(17,'入庫','劉軒佑',50,0,'2023-05-25 09:01:26.685117','2023-05-25 09:01:26.685154',13),(18,'出庫','劉軒佑',20,0,'2023-05-25 09:01:47.765729','2023-05-25 09:01:47.765764',13),(19,'入庫','劉軒佑',1000,0,'2023-05-25 09:02:04.523694','2023-05-25 09:02:04.528134',14),(20,'入庫','劉軒佑',50,0,'2023-05-25 09:02:17.638076','2023-05-25 09:02:17.638111',15);
/*!40000 ALTER TABLE `goods_sku_stock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `goods_spu`
--

DROP TABLE IF EXISTS `goods_spu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `goods_spu` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `sales` int NOT NULL,
  `comments` int NOT NULL,
  `apply_to` varchar(50) NOT NULL,
  `product_description` longtext NOT NULL,
  `nutrition_facts` longtext NOT NULL,
  `remark` varchar(100) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `brand_id` bigint NOT NULL,
  `catalog_id` bigint NOT NULL,
  `storage_method` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `goods_spu_brand_id_3f522ca9_fk_goods_brand_id` (`brand_id`),
  KEY `goods_spu_catalog_id_fbc03d74_fk_goods_catalog_id` (`catalog_id`),
  CONSTRAINT `goods_spu_brand_id_3f522ca9_fk_goods_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `goods_brand` (`id`),
  CONSTRAINT `goods_spu_catalog_id_fbc03d74_fk_goods_catalog_id` FOREIGN KEY (`catalog_id`) REFERENCES `goods_catalog` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goods_spu`
--

LOCK TABLES `goods_spu` WRITE;
/*!40000 ALTER TABLE `goods_spu` DISABLE KEYS */;
INSERT INTO `goods_spu` VALUES (1,'老犬飼料 長壽配方 低過敏 小顆粒 狗飼料',181,0,'高齡犬/易過敏體質','切爾思 老犬飼料是適合高齡犬之配方，利用易於消化的特殊配方幫助老犬能夠更容易吸收營養。\r\nOmega-6幫助毛色鮮艷\r\n添加硫酸軟骨素、膠原蛋白，有助關節強化，增加高齡犬的行動歷','雞肉粉、碎珍珠大麥、糙米、全穀粒小麥、全穀粒玉米、全穀粒高粱、全穀粒燕麥、雞肉脂肪、脫水甜菜漿、雞肝香料、玉米筋質粉、黃豆油、乳酸、豬肉香料、氯化鉀、碳酸鈣、亞麻仁籽、碘鹽、氯化膽鹼、左旋離胺酸、維生素(維生素E添加劑、抗壞血酸多聚磷酸酯(維生素C來源)、菸鹼酸添加劑、維生素B1、維生素A添加劑、泛酸鈣、核黃素添加劑、生物素、維生素B12添加劑、維生素B6、葉酸、維生素D3添加劑)、礦物質(硫酸亞鐵、氧化鋅、硫酸銅、氧化錳、碘酸鈣、亞硒酸鈉)、牛磺酸、DL-蛋胺酸、燕麥纖維、左旋肉酸素、添加綜合維生素E類以保鮮、天然香料、β-胡蘿蔔素、蘋果、青花菜、胡蘿蔔、蔓越莓、綠豌豆','鑑賞期並非試用期，若消費者需要退貨/退換商品，請保持包裝完整性。','2023-05-24 18:21:11.342887','2023-05-25 19:08:47.766211',1,1,'開封後，請勿放置於高溫潮濕處避免發霉。'),(2,'火雞+雞肉 挑嘴全齡 貓飼料',110,0,'全齡貓/挑食貓','優質火雞肉蛋白強健肌肉。\r\n獨特香料配方專門針對挑食貓。\r\n維生素E助於毛色亮麗。\r\n多種莓果幫助泌尿道保健、幫助膀胱健康。','去骨雞肉、去骨火雞肉、雞肉粉、全蛋、火雞粉、扁豆、豌豆、鷹嘴豆、雞脂肪（以混合生育酚保存）、莢豌豆、亞麻籽、天然雞肉香料、南瓜、西蘭花、奎奴亞藜種子、乾蔓越橘、氯化膽鹼、石榴、覆盆子、羽衣甘藍、鹽、菊苣根萃取物、維生素和礦物質〔維生素E補充物、菸酸（維生素B3來源）、維生素A補充物、硫胺素（維生素B1來源）、D-泛酸鈣（維生素B5來源）、鹽酸吡哆醇（維生素B6來源）、核黃素（維生素B2來源）、β-胡蘿蔔素、維生素D3補充物，葉酸、生物素、維生素B12補充物、鋅蛋白鹽、硫酸亞鐵、氧化鋅、鐵蛋白鹽、硫酸銅、銅蛋白鹽、錳蛋白鹽、氧化錳、碘酸鈣、亞硒酸鈉〕、DL-蛋氨酸、牛磺酸、絲蘭萃取物、菠菜、芹菜種子、薄荷、洋甘菊、薑黃、生薑、迷迭香。','鑑賞期並非試用期，若消費者需要退貨/退換商品，請保持包裝完整性。','2023-05-24 18:37:38.152358','2023-05-25 19:08:47.777373',1,2,'開封後，請勿放置於高溫潮濕處避免發霉。'),(3,'愛犬機能餐罐 100g',0,0,'全齡犬','富含豐富蛋白質，提供愛犬成長時所需的營養。\r\n富含維生素、礦物質及微量元素，補充狗狗缺乏的營養。','*雞肉*\r\n雞肉、鮪魚、米、再製起司、沙丁魚、大豆油、膠凍、維他命(A.B6.B12.D3.E.K)、菸鹼酸、核黃素、葉酸等微量元素。\r\n*羊肉*\r\n鮪魚、雞肉、羊肉、雞肝、牛肉、米、沙丁魚、大豆油、膠凍、維他命(A.B6.B12.D3.E.K)、菸鹼酸、核黃素、葉酸等微量元素。','鑑賞期並非試用期，若消費者需要退貨/退換商品，請保持包裝完整性。','2023-05-24 18:55:52.399617','2023-05-25 19:08:47.787106',2,3,'請放置於乾燥陰涼處，開封後請盡早食用避免錯失賞味期。'),(4,'愛貓機能餐罐 100g',0,0,'全齡貓','富含豐富蛋白質，提供愛貓成長時所需的營養。\r\n富含維生素、礦物質及微量元素，補充愛貓缺乏的營養。','*雞肉*\r\n雞肉、鮪魚、米、再製起司、沙丁魚、大豆油、膠凍、維他命(A.B6.B12.D3.E.K)、菸鹼酸、核黃素、葉酸等微量元素。\r\n*羊肉*\r\n鮪魚、雞肉、羊肉、雞肝、牛肉、米、沙丁魚、大豆油、膠凍、維他命(A.B6.B12.D3.E.K)、菸鹼酸、核黃素、葉酸等微量元素。','鑑賞期並非試用期，若消費者需要退貨/退換商品，請保持包裝完整性。','2023-05-24 18:57:57.344450','2023-05-25 19:08:47.797873',2,4,'請放置於乾燥陰涼處，開封後請盡早食用避免錯失賞味期。'),(5,'狗狗凍乾零食-毛鱗魚60g',220,0,'全齡犬','毛鱗魚富含維生素、礦物質及微量元素\r\n獨家冷凍乾燥技術，保留食物的完整營養價值\r\n純天然食材，不含額外添加物，讓愛犬吃的放心','富含Omega-3、DHA、維生素A.B.E.D','鑑賞期並非試用期，若消費者需要退貨/退換商品，請保持包裝完整性。','2023-05-24 19:05:57.423335','2023-05-25 19:08:47.808603',3,5,'開封後，請勿放置於高溫潮濕處避免發霉。'),(6,'貓咪凍乾零食-鱈魚 60g',0,0,'全齡貓','促進新陳代謝，恢復寵物體力，降低疲勞感\r\n獨家冷凍乾燥技術，保留食物的完整營養價值\r\n純天然食材，不含額外添加物，讓愛貓吃的放心','富含胺基酸、Omega-3、高蛋白質','鑑賞期並非試用期，若消費者需要退貨/退換商品，請保持包裝完整性。','2023-05-24 19:10:56.520480','2023-05-25 19:08:47.822799',3,6,'開封後，請勿放置於高溫潮濕處避免發霉。');
/*!40000 ALTER TABLE `goods_spu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `goods_spu_sale_attr`
--

DROP TABLE IF EXISTS `goods_spu_sale_attr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `goods_spu_sale_attr` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `spu_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `goods_spu_sale_attr_spu_id_df2755da_fk_goods_spu_id` (`spu_id`),
  CONSTRAINT `goods_spu_sale_attr_spu_id_df2755da_fk_goods_spu_id` FOREIGN KEY (`spu_id`) REFERENCES `goods_spu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goods_spu_sale_attr`
--

LOCK TABLES `goods_spu_sale_attr` WRITE;
/*!40000 ALTER TABLE `goods_spu_sale_attr` DISABLE KEYS */;
INSERT INTO `goods_spu_sale_attr` VALUES (1,'切爾思狗飼料/尺寸','2023-05-24 19:47:07.119604','2023-05-25 08:30:41.756681',1),(2,'切爾思貓飼料/尺寸','2023-05-25 08:31:08.772668','2023-05-25 08:31:08.772702',2),(3,'沛瑞思狗罐頭/口味','2023-05-25 08:36:03.391723','2023-05-25 08:36:03.391756',3),(4,'沛瑞思貓罐頭/口味','2023-05-25 08:39:37.075264','2023-05-25 08:39:37.075296',4),(5,'哈里斯狗零食/規格','2023-05-25 08:45:48.678130','2023-05-25 08:45:48.678163',5),(6,'哈里斯貓零食/規格','2023-05-25 08:48:55.254893','2023-05-25 08:48:55.254925',6);
/*!40000 ALTER TABLE `goods_spu_sale_attr` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-09-15 14:07:52
