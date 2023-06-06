-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2023-06-06 09:48:36
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
('王八蛋', '0', 'admin', '資材部', 1);

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
  `actual_working_day` varchar(80) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `work_schedule`
--

INSERT INTO `work_schedule` (`SID`, `project_name`, `work_mode`, `start_time`, `expected_end_time`, `end_time`, `percent_complete`, `estimated_working_day`, `actual_working_day`) VALUES
('kh01', '測試專案一', '進行中', '2023-06-06', '2023-06-22', '2023-06-23', NULL, '16', '17');

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
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `project_option`
--
ALTER TABLE `project_option`
  MODIFY `option_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

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
