/*
 Navicat Premium Data Transfer

 Source Server         : root
 Source Server Type    : MySQL
 Source Server Version : 80041 (8.0.41)
 Source Host           : 127.0.0.1:3306
 Source Schema         : croom

 Target Server Type    : MySQL
 Target Server Version : 80041 (8.0.41)
 File Encoding         : 65001

 Date: 15/08/2025 15:14:22
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for chat_history
-- ----------------------------
DROP TABLE IF EXISTS `chat_history`;
CREATE TABLE `chat_history`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NULL DEFAULT NULL COMMENT '该聊天记录所属用户id',
  `message` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '消息内容',
  `create_at` datetime NULL DEFAULT NULL,
  `room_id` int NULL DEFAULT NULL COMMENT '该聊天记录所属房间id',
  `role` tinyint NULL DEFAULT 2 COMMENT '该聊天记录来自的用户所属角色，1为管理员2为用户',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 619 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '聊天历史数据存放表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for room
-- ----------------------------
DROP TABLE IF EXISTS `room`;
CREATE TABLE `room`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '房间名字',
  `create_at` datetime NULL DEFAULT NULL COMMENT '房间创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin COMMENT = '房间的数据存放表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `account` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '用户的账号',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '用户的密码',
  `token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '弃用',
  `create_at` datetime NULL DEFAULT NULL COMMENT '用户创建日期',
  `is_admin` tinyint(1) NULL DEFAULT 0 COMMENT '是否管理员，1是0不是',
  `username` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '用户的名称',
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '用户的头像url',
  `status` tinyint NOT NULL DEFAULT 1 COMMENT '用户状态，1正常2禁用',
  `is_delete` tinyint NOT NULL DEFAULT 2 COMMENT '用户删除状态，1删除2正常',
  `avatar_update_time` datetime NULL DEFAULT NULL COMMENT '弃用',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`account` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin COMMENT = '用户的信息存放表' ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
