/*
 Navicat Premium Data Transfer

 Source Server         : Connection
 Source Server Type    : MySQL
 Source Server Version : 80017
 Source Host           : localhost:3306
 Source Schema         : BikeSharedSystem

 Target Server Type    : MySQL
 Target Server Version : 80017
 File Encoding         : 65001

 Date: 07/11/2019 15:09:18
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for bike
-- ----------------------------
DROP TABLE IF EXISTS `bike`;
CREATE TABLE `bike` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Condition` varchar(255) NOT NULL,
  `Location_ID` int(11) NOT NULL,
  `City_ID` int(11) NOT NULL,
  `Created_At` datetime DEFAULT NULL,
  `Updated_At` datetime DEFAULT NULL,
  `Type_ID` int(11) NOT NULL,
  `Last_Operator_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of bike
-- ----------------------------
BEGIN;
INSERT INTO `bike` VALUES (1, 'Available', 1, 1, '2019-11-05 20:41:10', '2019-11-05 20:41:10', 1, 1);
INSERT INTO `bike` VALUES (2, 'Available', 2, 1, '2019-11-05 20:41:52', '2019-11-05 20:43:52', 1, 1);
INSERT INTO `bike` VALUES (3, 'Available', 1, 1, '2019-11-05 20:42:05', '2019-11-05 20:53:05', 1, 1);
INSERT INTO `bike` VALUES (4, 'Available', 2, 1, '2019-11-05 20:42:15', '2019-11-05 20:53:26', 1, 1);
INSERT INTO `bike` VALUES (5, 'Available', 3, 2, '2019-11-05 20:42:19', '2019-11-05 20:42:19', 1, 1);
INSERT INTO `bike` VALUES (6, 'Available', 3, 2, '2019-11-05 20:42:22', '2019-11-05 20:42:22', 1, 1);
INSERT INTO `bike` VALUES (7, 'Available', 4, 2, '2019-11-05 20:42:27', '2019-11-05 20:42:27', 1, 1);
INSERT INTO `bike` VALUES (8, 'Available', 4, 2, '2019-11-05 20:42:30', '2019-11-05 20:42:30', 1, 1);
COMMIT;

-- ----------------------------
-- Table structure for city
-- ----------------------------
DROP TABLE IF EXISTS `city`;
CREATE TABLE `city` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `City_Name` varchar(255) NOT NULL,
  `Status` varchar(255) NOT NULL,
  `Created_At` datetime DEFAULT NULL,
  `Updated_At` datetime DEFAULT NULL,
  `Last_Operator_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `City_Name` (`City_Name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of city
-- ----------------------------
BEGIN;
INSERT INTO `city` VALUES (1, 'Glasgow', 'Active', '2019-11-05 20:18:49', '2019-11-05 20:18:49', 1);
INSERT INTO `city` VALUES (2, 'Edinburgh', 'Active', '2019-11-05 20:39:45', '2019-11-05 20:39:45', 1);
COMMIT;

-- ----------------------------
-- Table structure for customer
-- ----------------------------
DROP TABLE IF EXISTS `customer`;
CREATE TABLE `customer` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Amount_Balance` double(10,2) DEFAULT NULL,
  `Phone_Number` varchar(255) DEFAULT NULL,
  `Full_Name` varchar(255) NOT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Username` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Email_Subscription` tinyint(1) DEFAULT NULL,
  `Card_No` int(11) DEFAULT NULL,
  `Expired_Date` varchar(255) DEFAULT NULL,
  `CVV` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Username` (`Username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of customer
-- ----------------------------
BEGIN;
INSERT INTO `customer` VALUES (1, NULL, '0671426335', 'Customer One', 'abc@gmail.com', 'customer1', 'P@ssw0rd', NULL, 123456789, '03/21', 910);
COMMIT;

-- ----------------------------
-- Table structure for location
-- ----------------------------
DROP TABLE IF EXISTS `location`;
CREATE TABLE `location` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Zone_Name` varchar(255) NOT NULL,
  `Slot` int(255) DEFAULT NULL,
  `Status` varchar(255) NOT NULL,
  `Created_At` datetime DEFAULT NULL,
  `Updated_At` datetime DEFAULT NULL,
  `City_ID` int(11) NOT NULL,
  `Last_Operator_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of location
-- ----------------------------
BEGIN;
INSERT INTO `location` VALUES (1, 'Zone A', 20, 'Active', '2019-11-05 20:19:25', '2019-11-05 20:19:25', 1, 1);
INSERT INTO `location` VALUES (2, 'Zone B', 10, 'Active', '2019-11-05 20:40:09', '2019-11-05 20:40:09', 1, 1);
INSERT INTO `location` VALUES (3, 'Zone X', 15, 'Active', '2019-11-05 20:40:25', '2019-11-05 20:40:25', 2, 1);
INSERT INTO `location` VALUES (4, 'Zone Y', 20, 'Active', '2019-11-05 20:40:38', '2019-11-05 20:40:38', 2, 1);
COMMIT;

-- ----------------------------
-- Table structure for operator_manager
-- ----------------------------
DROP TABLE IF EXISTS `operator_manager`;
CREATE TABLE `operator_manager` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Username` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Full_Name` varchar(255) NOT NULL,
  `Role` varchar(255) NOT NULL,
  `Status` varchar(255) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Username` (`Username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of operator_manager
-- ----------------------------
BEGIN;
INSERT INTO `operator_manager` VALUES (1, 'operator1', 'P@ssw0rd', 'Operator 1', 'Operator', 'Active');
INSERT INTO `operator_manager` VALUES (2, 'manager1', 'P@ssw0rd', 'Manager 1', 'Manager', 'Active');
COMMIT;

-- ----------------------------
-- Table structure for transaction
-- ----------------------------
DROP TABLE IF EXISTS `transaction`;
CREATE TABLE `transaction` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Status` varchar(255) NOT NULL,
  `Paid_Amount` double(10,2) DEFAULT NULL,
  `Created_At` datetime DEFAULT NULL,
  `Updated_At` datetime DEFAULT NULL,
  `Customer_ID` int(11) NOT NULL,
  `Bike_ID` int(11) NOT NULL,
  `Remarks` varchar(255) DEFAULT NULL,
  `Origin_ID` int(11) NOT NULL,
  `Destination_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of transaction
-- ----------------------------
BEGIN;
INSERT INTO `transaction` VALUES (1, 'Paid', 2.00, '2019-11-06 19:18:49', '2019-11-06 21:12:23', 1, 1, NULL, 1, 1);
INSERT INTO `transaction` VALUES (2, 'Paid', 3.50, '2019-10-02 10:00:00', '2019-10-02 15:00:00', 1, 1, NULL, 1, 2);
COMMIT;

-- ----------------------------
-- Table structure for type
-- ----------------------------
DROP TABLE IF EXISTS `type`;
CREATE TABLE `type` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Type_Name` varchar(255) NOT NULL,
  `Fixed_Price` double(10,2) DEFAULT NULL,
  `Add_Price` double(10,2) DEFAULT NULL,
  `Day_Price` double(10,2) DEFAULT NULL,
  `Created_At` datetime DEFAULT NULL,
  `Updated_At` datetime DEFAULT NULL,
  `Last_Operator_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Type_Name` (`Type_Name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of type
-- ----------------------------
BEGIN;
INSERT INTO `type` VALUES (1, 'Normal', 1.00, 0.50, 5.00, '2019-11-05 19:29:54', '2019-11-05 20:32:14', 1);
INSERT INTO `type` VALUES (2, 'Special', 3.00, 2.00, 8.00, '2019-11-05 20:31:10', '2019-11-05 20:31:10', 1);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
