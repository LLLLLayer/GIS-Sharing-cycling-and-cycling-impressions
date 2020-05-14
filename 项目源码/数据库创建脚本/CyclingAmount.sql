/*
 Navicat Premium Data Transfer

 Source Server         : gis
 Source Server Type    : MySQL
 Source Server Version : 50718
 Source Host           : cdb-1leyn7gu.bj.tencentcdb.com:10051
 Source Schema         : SharingBikeDataBase

 Target Server Type    : MySQL
 Target Server Version : 50718
 File Encoding         : 65001

 Date: 04/01/2020 22:35:33
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for CyclingAmount
-- ----------------------------
DROP TABLE IF EXISTS `CyclingAmount`;
CREATE TABLE `CyclingAmount`  (
  `curDay` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `curHour0` int(255) NULL DEFAULT NULL,
  `curHour1` int(255) NULL DEFAULT NULL,
  `curHour2` int(255) NULL DEFAULT NULL,
  `curHour3` int(255) NULL DEFAULT NULL,
  `curHour4` int(255) NULL DEFAULT NULL,
  `curHour5` int(255) NULL DEFAULT NULL,
  `curHour6` int(255) NULL DEFAULT NULL,
  `curHour7` int(255) NULL DEFAULT NULL,
  `curHour8` int(255) NULL DEFAULT NULL,
  `curHour9` int(255) NULL DEFAULT NULL,
  `curHour10` int(255) NULL DEFAULT NULL,
  `curHour11` int(255) NULL DEFAULT NULL,
  `curHour12` int(255) NULL DEFAULT NULL,
  `curHour13` int(255) NULL DEFAULT NULL,
  `curHour14` int(255) NULL DEFAULT NULL,
  `curHour15` int(255) NULL DEFAULT NULL,
  `curHour16` int(255) NULL DEFAULT NULL,
  `curHour17` int(255) NULL DEFAULT NULL,
  `curHour18` int(255) NULL DEFAULT NULL,
  `curHour19` int(255) NULL DEFAULT NULL,
  `curHour20` int(255) NULL DEFAULT NULL,
  `curHour21` int(255) NULL DEFAULT NULL,
  `curHour23` int(255) NULL DEFAULT NULL,
  `curHour22` int(255) NULL DEFAULT NULL,
  PRIMARY KEY (`curDay`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of CyclingAmount
-- ----------------------------
INSERT INTO `CyclingAmount` VALUES ('2018-02-05 ', 2734, 1547, 1259, 1009, 853, 773, 958, 1793, 2802, 2019, 1990, 3700, 13779, 11879, 33335, 38492, 33603, 34308, 35567, 27908, 19978, 19473, 20311, 17114);

SET FOREIGN_KEY_CHECKS = 1;
