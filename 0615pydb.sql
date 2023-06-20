-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2023-06-15 04:04:07
-- 伺服器版本： 10.4.28-MariaDB
-- PHP 版本： 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `pydb`
--

-- --------------------------------------------------------

--
-- 資料表結構 `account`
--

CREATE TABLE `account` (
  `acc_nu` varchar(20) NOT NULL,
  `passwd` varchar(20) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  `department` varchar(20) DEFAULT NULL,
  `limits` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `account`
--

INSERT INTO `account` (`acc_nu`, `passwd`, `name`, `department`, `limits`) VALUES
('0', '0', '0', '管理部', 3),
('1', '1', '1', '生產部', 1);

-- --------------------------------------------------------

--
-- 資料表結構 `end_work`
--

CREATE TABLE `end_work` (
  `SID` int(11) NOT NULL,
  `project_name` varchar(120) DEFAULT NULL,
  `work_mode` varchar(80) DEFAULT NULL,
  `start_time` varchar(80) DEFAULT NULL,
  `expected_end_time` varchar(80) DEFAULT NULL,
  `end_time` varchar(80) DEFAULT NULL,
  `percent_complete` int(11) DEFAULT NULL,
  `estimated_working_day` varchar(80) DEFAULT NULL,
  `actual_working_day` varchar(80) DEFAULT NULL,
  `warranty_expiry_date` varchar(80) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `end_work`
--

INSERT INTO `end_work` (`SID`, `project_name`, `work_mode`, `start_time`, `expected_end_time`, `end_time`, `percent_complete`, `estimated_working_day`, `actual_working_day`, `warranty_expiry_date`) VALUES
(0, '[value-2]', '[value-3]', '[value-4]', '[value-5]', '[value-6]', 0, '[value-8]', '[value-9]', '[value-10]');

-- --------------------------------------------------------

--
-- 資料表結構 `option_item`
--

CREATE TABLE `option_item` (
  `id` int(255) NOT NULL,
  `item_id` int(11) NOT NULL,
  `item_value` varchar(80) DEFAULT NULL,
  `is_checked` tinyint(1) DEFAULT NULL,
  `SID` varchar(80) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `option_item`
--

INSERT INTO `option_item` (`id`, `item_id`, `item_value`, `is_checked`, `SID`) VALUES
(26, 17, '9', 1, 'kh01'),
(27, 17, '10', 1, 'kh01'),
(28, 17, '11', 1, 'kh01'),
(29, 17, '12', 1, 'kh01'),
(30, 17, '13', 1, 'kh01'),
(31, 19, '細項一111', 1, 'kh02'),
(35, 17, '14', 1, 'kh01'),
(36, 17, '15', 1, 'kh01'),
(37, 18, '123', 0, 'kh01'),
(38, 18, '321', 1, 'kh01'),
(39, 18, '14', 1, 'kh01'),
(43, 21, '測試', 1, 'kh02'),
(44, 21, '測試R', 1, 'kh02'),
(45, 21, '測試RRR', 0, 'kh02');

-- --------------------------------------------------------

--
-- 資料表結構 `project_option`
--

CREATE TABLE `project_option` (
  `option_id` int(11) NOT NULL,
  `option_value` varchar(80) DEFAULT NULL,
  `SID` varchar(80) DEFAULT NULL,
  `option_percentage` int(11) DEFAULT NULL,
  `option_start_time` varchar(80) DEFAULT NULL,
  `option_end_time` varchar(80) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `project_option`
--

INSERT INTO `project_option` (`option_id`, `option_value`, `SID`, `option_percentage`, `option_start_time`, `option_end_time`) VALUES
(17, '前期規劃', 'kh01', 100, '2023-06-07', ''),
(18, '現場工程', 'kh01', 67, '2023-06-07', ''),
(19, '前期規劃', 'kh02', 100, '2023-06-08', ''),
(20, '貨櫃現場工程', 'kh02', 0, '2023-06-08', ''),
(21, '現場工程', 'kh02', 67, '2023-06-08', ''),
(22, '設備吊裝', 'kh02', 0, '2023-06-08', ''),
(25, '設備吊裝', 'kh01', 0, '2023-06-08', ''),
(26, '貨櫃現場工程', 'kh01', 0, '2023-06-08', ''),
(28, '貨櫃預置工程', 'kh02', 0, '2023-06-12', '2023-06-30');

-- --------------------------------------------------------

--
-- 資料表結構 `work_schedule`
--

CREATE TABLE `work_schedule` (
  `SID` varchar(80) NOT NULL,
  `project_name` varchar(120) DEFAULT NULL,
  `work_mode` varchar(80) DEFAULT NULL,
  `start_time` varchar(80) DEFAULT NULL,
  `expected_end_time` varchar(80) DEFAULT NULL,
  `end_time` varchar(80) DEFAULT NULL,
  `percent_complete` int(11) DEFAULT NULL,
  `estimated_working_day` varchar(80) DEFAULT NULL,
  `actual_working_day` varchar(80) DEFAULT NULL,
  `state` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `work_schedule`
--

INSERT INTO `work_schedule` (`SID`, `project_name`, `work_mode`, `start_time`, `expected_end_time`, `end_time`, `percent_complete`, `estimated_working_day`, `actual_working_day`, `state`) VALUES
('fin', 'fin', '進行中', '2023-06-15', '2023-07-08', '2023-07-08', NULL, '23', '23', 1),
('FIN2', 'FIN2', '進行中', '2023-06-15', '2023-07-07', '2023-07-08', NULL, '22', '23', 1),
('FIN3', 'FIN3', '停工', '2023-06-15', '2023-07-07', '2023-07-07', NULL, '22', '22', 1),
('kh01', '測試專案一', '進行中', '2023-06-06', '2023-06-22', '2023-06-23', 42, '16', '17', 0),
('kh02', '測試專案二', '進行中', '2023-06-08', '2023-07-01', '2023-06-30', 33, '23', '22', 0);

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`acc_nu`);

--
-- 資料表索引 `end_work`
--
ALTER TABLE `end_work`
  ADD PRIMARY KEY (`SID`),
  ADD UNIQUE KEY `SID` (`SID`);

--
-- 資料表索引 `option_item`
--
ALTER TABLE `option_item`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_id` (`item_id`);

--
-- 資料表索引 `project_option`
--
ALTER TABLE `project_option`
  ADD PRIMARY KEY (`option_id`),
  ADD KEY `SID` (`SID`);

--
-- 資料表索引 `work_schedule`
--
ALTER TABLE `work_schedule`
  ADD PRIMARY KEY (`SID`),
  ADD UNIQUE KEY `SID` (`SID`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `option_item`
--
ALTER TABLE `option_item`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `project_option`
--
ALTER TABLE `project_option`
  MODIFY `option_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `option_item`
--
ALTER TABLE `option_item`
  ADD CONSTRAINT `fk_id` FOREIGN KEY (`item_id`) REFERENCES `project_option` (`option_id`) ON DELETE CASCADE;

--
-- 資料表的限制式 `project_option`
--
ALTER TABLE `project_option`
  ADD CONSTRAINT `fk_SID` FOREIGN KEY (`SID`) REFERENCES `work_schedule` (`SID`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;