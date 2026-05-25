CREATE DATABASE  IF NOT EXISTS `techrepair` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `techrepair`;
-- dump do banco techrepair com dados
--
-- servidor local

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
-- tabela clientes
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `telefone` varchar(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- dados da tabela clientes
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (1,'Guilherme Soares','16993536709','nao informado'),(2,'Guilherme Soares','16993536708','Cleitorado123@gmail.com'),(3,'Henrique Linhares','16993536704','henriquel@gmail.com'),(4,'Adriano Alvares','16993536705','ola'),(5,'Adriano Souza','16993536706','AdrianoSouza@gmail.com');
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- tabela dispositivos
--

DROP TABLE IF EXISTS `dispositovos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispositovos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `modelo` varchar(100) NOT NULL,
  `marca` varchar(100) NOT NULL,
  `id_clientes` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_dispositovos_clientes_idx` (`id_clientes`),
  CONSTRAINT `fk_dispositovos_clientes` FOREIGN KEY (`id_clientes`) REFERENCES `clientes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- dados da tabela dispositivos
--

LOCK TABLES `dispositovos` WRITE;
/*!40000 ALTER TABLE `dispositovos` DISABLE KEYS */;
INSERT INTO `dispositovos` VALUES (1,'Poco x13','Não informada',1),(2,'poco x13','Não informada',2),(4,'Moto G84','Não informada',3),(5,'Iphone 25','Não informada',4),(6,'Iphone 30','Não informada',5);
/*!40000 ALTER TABLE `dispositovos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- tabela ordens de servico
--

DROP TABLE IF EXISTS `ordens_servico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordens_servico` (
  `id` int NOT NULL AUTO_INCREMENT,
  `descricao_problema` varchar(250) NOT NULL,
  `data_abertura` date NOT NULL,
  `status` enum('Aguardando','Em Manutenção','Pronto') NOT NULL,
  `id_tecnicos` int NOT NULL,
  `id_dispositivos` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_ordens_servico_tecnicos1_idx` (`id_tecnicos`),
  KEY `fk_ordens_servico_dispositovos1_idx` (`id_dispositivos`),
  CONSTRAINT `fk_ordens_servico_dispositovos1` FOREIGN KEY (`id_dispositivos`) REFERENCES `dispositovos` (`id`),
  CONSTRAINT `fk_ordens_servico_tecnicos1` FOREIGN KEY (`id_tecnicos`) REFERENCES `tecnicos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- dados da tabela ordens de servico
--

LOCK TABLES `ordens_servico` WRITE;
/*!40000 ALTER TABLE `ordens_servico` DISABLE KEYS */;
INSERT INTO `ordens_servico` VALUES (2,'Tela trincada ao deixar o telefone cair','2026-05-25','Aguardando',1,2),(4,'O aparelho não carrega','2026-05-25','Aguardando',1,4),(5,'Bateria descarregando muito rapido','2026-05-25','Aguardando',1,5),(6,'Celular travando','2026-05-25','Aguardando',1,6);
/*!40000 ALTER TABLE `ordens_servico` ENABLE KEYS */;
UNLOCK TABLES;

--
-- tabela tecnicos
--

DROP TABLE IF EXISTS `tecnicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tecnicos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `especialidade` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- dados da tabela tecnicos
--

LOCK TABLES `tecnicos` WRITE;
/*!40000 ALTER TABLE `tecnicos` DISABLE KEYS */;
INSERT INTO `tecnicos` VALUES (1,'Roberto','Telas');
/*!40000 ALTER TABLE `tecnicos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- fim do dump
--


/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- dump finalizado
