-- script pra criar o banco de dados do projeto

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- criando o banco techrepair


CREATE SCHEMA IF NOT EXISTS `techrepair` DEFAULT CHARACTER SET utf8 ;
USE `techrepair` ;

-- tabela de clientes
CREATE TABLE IF NOT EXISTS `techrepair`.`clientes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  `telefone` VARCHAR(11) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- tabela de dispositivos (celulares)
CREATE TABLE IF NOT EXISTS `techrepair`.`dispositovos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `modelo` VARCHAR(100) NOT NULL,
  `marca` VARCHAR(100) NOT NULL,
  `id_clientes` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_dispositovos_clientes_idx` (`id_clientes` ASC) VISIBLE,
  CONSTRAINT `fk_dispositovos_clientes`
    FOREIGN KEY (`id_clientes`)
    REFERENCES `techrepair`.`clientes` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- tabela de tecnicos
CREATE TABLE IF NOT EXISTS `techrepair`.`tecnicos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  `especialidade` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- tabela de ordens de servico
CREATE TABLE IF NOT EXISTS `techrepair`.`ordens_servico` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `descricao_problema` VARCHAR(250) NOT NULL,
  `data_abertura` DATE NOT NULL,
  `status` ENUM('Aguardando', 'Em Manutenção', 'Pronto') NOT NULL,
  `id_tecnicos` INT NOT NULL,
  `id_dispositivos` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_ordens_servico_tecnicos1_idx` (`id_tecnicos` ASC) VISIBLE,
  INDEX `fk_ordens_servico_dispositovos1_idx` (`id_dispositivos` ASC) VISIBLE,
  CONSTRAINT `fk_ordens_servico_tecnicos1`
    FOREIGN KEY (`id_tecnicos`)
    REFERENCES `techrepair`.`tecnicos` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ordens_servico_dispositovos1`
    FOREIGN KEY (`id_dispositivos`)
    REFERENCES `techrepair`.`dispositovos` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
