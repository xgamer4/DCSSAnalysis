-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jan 15, 2015 at 07:28 PM
-- Server version: 5.5.40-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `Crawl`
--
CREATE DATABASE IF NOT EXISTS `Crawl` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `Crawl`;

-- --------------------------------------------------------

--
-- Table structure for table `Branch`
--

CREATE TABLE IF NOT EXISTS `Branch` (
  `ID` smallint(3) NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=52 ;

-- --------------------------------------------------------

--
-- Table structure for table `Class`
--

CREATE TABLE IF NOT EXISTS `Class` (
  `ID` mediumint(3) NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=27 ;

-- --------------------------------------------------------

--
-- Table structure for table `Deity`
--

CREATE TABLE IF NOT EXISTS `Deity` (
  `ID` mediumint(3) NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=23 ;

-- --------------------------------------------------------

--
-- Table structure for table `Game`
--

CREATE TABLE IF NOT EXISTS `Game` (
  `ID` int(7) NOT NULL AUTO_INCREMENT,
  `File` varchar(250) NOT NULL,
  `ServerID` smallint(2) NOT NULL,
  `PlayerID` int(5) NOT NULL,
  `VersionID` int(5) NOT NULL,
  `RaceID` smallint(3) NOT NULL,
  `ClassID` smallint(3) NOT NULL,
  `DeityID` smallint(3) NOT NULL,
  `DeityPiety` tinyint(2) NOT NULL,
  `Title` varchar(50) NOT NULL,
  `StartTime` date NOT NULL,
  `EndTime` date NOT NULL,
  `Turns` int(7) NOT NULL,
  `PlayTime` int(5) NOT NULL,
  `DeathBy` varchar(100) NOT NULL,
  `DeathLvl` tinyint(3) NOT NULL,
  `DeathBranch` varchar(50) NOT NULL,
  `DeathNotes` text NOT NULL,
  `Score` int(10) NOT NULL,
  `Won` tinyint(1) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `ServerID` (`ServerID`,`PlayerID`,`VersionID`,`RaceID`,`ClassID`,`DeityID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3977 ;

-- --------------------------------------------------------

--
-- Table structure for table `GameBranches`
--

CREATE TABLE IF NOT EXISTS `GameBranches` (
  `ID` int(7) NOT NULL AUTO_INCREMENT,
  `GameID` int(7) NOT NULL,
  `BranchID` smallint(3) NOT NULL,
  `ExploredFloors` tinyint(2) NOT NULL,
  `TotalFloors` tinyint(2) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `GameID` (`GameID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7146 ;

-- --------------------------------------------------------

--
-- Table structure for table `GameEquipment`
--

CREATE TABLE IF NOT EXISTS `GameEquipment` (
  `ID` int(9) NOT NULL AUTO_INCREMENT,
  `GameID` int(7) NOT NULL,
  `FullName` varchar(250) NOT NULL,
  `Modifier` smallint(4) NOT NULL,
  `Brand` varchar(50) NOT NULL,
  `BaseType` varchar(100) NOT NULL,
  `Effects` varchar(200) NOT NULL,
  `Worn` tinyint(1) NOT NULL,
  `Known` tinyint(1) NOT NULL,
  `Cursed` tinyint(1) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `GameID` (`GameID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=80651 ;

-- --------------------------------------------------------

--
-- Table structure for table `GameResistance`
--

CREATE TABLE IF NOT EXISTS `GameResistance` (
  `GameID` int(7) NOT NULL,
  `rFire` tinyint(2) NOT NULL,
  `rCold` tinyint(2) NOT NULL,
  `rNeg` tinyint(2) NOT NULL,
  `rPois` tinyint(2) NOT NULL,
  `rElec` tinyint(2) NOT NULL,
  `SustAb` tinyint(2) NOT NULL,
  `rMut` tinyint(2) NOT NULL,
  `Gourm` tinyint(2) NOT NULL,
  `MR` tinyint(2) NOT NULL,
  `SeeInvis` tinyint(2) NOT NULL,
  `Clarity` tinyint(2) NOT NULL,
  `rCorr` tinyint(2) NOT NULL,
  `rRot` tinyint(2) NOT NULL,
  `Spirit` tinyint(2) NOT NULL,
  `Warding` tinyint(2) NOT NULL,
  `NoTele` tinyint(2) NOT NULL,
  UNIQUE KEY `GameID` (`GameID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `GameRunes`
--

CREATE TABLE IF NOT EXISTS `GameRunes` (
  `ID` int(7) NOT NULL AUTO_INCREMENT,
  `GameID` int(7) NOT NULL,
  `Rune` varchar(25) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `GameID` (`GameID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=582 ;

-- --------------------------------------------------------

--
-- Table structure for table `GameSkills`
--

CREATE TABLE IF NOT EXISTS `GameSkills` (
  `ID` int(7) NOT NULL AUTO_INCREMENT,
  `GameID` int(7) NOT NULL,
  `Skill` varchar(40) NOT NULL,
  `Level` decimal(4,2) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `GameID` (`GameID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=23848 ;

-- --------------------------------------------------------

--
-- Table structure for table `GameSpells`
--

CREATE TABLE IF NOT EXISTS `GameSpells` (
  `ID` int(7) NOT NULL AUTO_INCREMENT,
  `GameID` int(7) NOT NULL,
  `SpellID` smallint(4) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `GameID` (`GameID`,`SpellID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6138 ;

-- --------------------------------------------------------

--
-- Table structure for table `GameStats`
--

CREATE TABLE IF NOT EXISTS `GameStats` (
  `GameID` int(7) NOT NULL,
  `CurHP` smallint(4) NOT NULL,
  `MaxHP` smallint(4) NOT NULL,
  `CurMP` smallint(4) NOT NULL,
  `MaxMP` smallint(4) NOT NULL,
  `Gold` int(5) NOT NULL,
  `AC` int(4) NOT NULL,
  `EV` int(4) NOT NULL,
  `SH` int(4) NOT NULL,
  `Str` int(4) NOT NULL,
  `Intel` int(4) NOT NULL,
  `Dex` int(4) NOT NULL,
  `XL` int(4) NOT NULL,
  `SpellMem` int(4) NOT NULL,
  `SpellMax` int(4) NOT NULL,
  UNIQUE KEY `GameID_2` (`GameID`),
  KEY `GameID` (`GameID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Player`
--

CREATE TABLE IF NOT EXISTS `Player` (
  `ID` int(5) NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=171 ;

-- --------------------------------------------------------

--
-- Table structure for table `Race`
--

CREATE TABLE IF NOT EXISTS `Race` (
  `ID` mediumint(3) NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=36 ;

-- --------------------------------------------------------

--
-- Table structure for table `Server`
--

CREATE TABLE IF NOT EXISTS `Server` (
  `ID` smallint(2) NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- Table structure for table `Spell`
--

CREATE TABLE IF NOT EXISTS `Spell` (
  `ID` smallint(3) NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=130 ;

-- --------------------------------------------------------

--
-- Table structure for table `Version`
--

CREATE TABLE IF NOT EXISTS `Version` (
  `ID` int(5) NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=21 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
