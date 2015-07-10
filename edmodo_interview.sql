-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 10, 2015 at 02:05 AM
-- Server version: 5.5.43
-- PHP Version: 5.4.36-1+deb.sury.org~precise+2

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `edmodo_interview`
--

-- --------------------------------------------------------

--
-- Table structure for table `homeworks`
--

CREATE TABLE IF NOT EXISTS `homeworks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `title` varchar(255) NOT NULL,
  `question` text NOT NULL,
  `due_date` date NOT NULL,
  `teacher_id` int(11) NOT NULL,
  `submissions` int(5) NOT NULL DEFAULT '0',
  `students` int(5) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `teacher_id` (`teacher_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `homeworks`
--

INSERT INTO `homeworks` (`id`, `created_at`, `updated_at`, `title`, `question`, `due_date`, `teacher_id`, `submissions`, `students`) VALUES
(1, '2015-07-07 00:00:00', '2015-07-08 06:24:31', 'Infinity Stone 101', 'What is Tessaract?', '2015-07-13', 3, 3, 1),
(2, '2015-07-07 00:00:00', '2015-07-08 06:25:26', 'History of Shield', 'Write a little about the history of shield', '2015-07-06', 3, 0, 2),
(3, '2015-07-07 00:00:00', '2015-07-08 06:26:09', 'Project PEGASUS', 'What is Pegasus', '2015-07-23', 3, 1, 5);

-- --------------------------------------------------------

--
-- Table structure for table `homework_students`
--

CREATE TABLE IF NOT EXISTS `homework_students` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `homework_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `homework_id` (`homework_id`),
  KEY `student_id` (`student_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=9 ;

--
-- Dumping data for table `homework_students`
--

INSERT INTO `homework_students` (`id`, `created_at`, `updated_at`, `homework_id`, `student_id`) VALUES
(1, '0000-00-00 00:00:00', '2015-07-08 07:33:28', 1, 4),
(2, '0000-00-00 00:00:00', '2015-07-09 04:03:29', 2, 4),
(3, '0000-00-00 00:00:00', '2015-07-10 03:30:55', 1, 7),
(4, '2015-07-08 00:00:00', '2015-07-10 03:41:51', 3, 4),
(5, '2015-07-08 00:00:00', '2015-07-10 03:41:51', 3, 5),
(6, '2015-07-08 00:00:00', '2015-07-10 03:42:23', 3, 6),
(7, '2015-07-08 00:00:00', '2015-07-10 03:42:23', 3, 7),
(8, '2015-07-08 00:00:00', '2015-07-10 03:43:11', 3, 8);

-- --------------------------------------------------------

--
-- Table structure for table `homework_submissions`
--

CREATE TABLE IF NOT EXISTS `homework_submissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `student_id` int(11) NOT NULL,
  `homework_id` int(11) NOT NULL,
  `submission` text NOT NULL,
  `seen` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `homework_id` (`homework_id`),
  KEY `student_id` (`student_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `homework_submissions`
--

INSERT INTO `homework_submissions` (`id`, `created_at`, `updated_at`, `student_id`, `homework_id`, `submission`, `seen`) VALUES
(1, '0000-00-00 00:00:00', '2015-07-08 07:30:39', 4, 1, 'This is my first answer', 0),
(2, '0000-00-00 00:00:00', '2015-07-08 07:41:29', 4, 1, 'This is my second submission', 0),
(3, '0000-00-00 00:00:00', '2015-07-09 07:35:15', 4, 1, 'This is my third answer', 0),
(4, '0000-00-00 00:00:00', '2015-07-10 05:52:05', 5, 3, 'Hulk first answer!', 0);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `role` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=9 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `email`, `username`, `name`, `created_at`, `updated_at`, `role`, `password`) VALUES
(3, 'teacher@demo.com', 'nick_fury', 'Nick Fury', '2015-07-07 00:00:00', '2015-07-10 03:34:43', 'teacher', 'demo'),
(4, 'student1@demo.com', 'tony_stark', 'Tony Stark', '2015-07-08 00:00:00', '2015-07-10 03:34:51', 'student', 'demo'),
(5, 'student2@demo.com', 'bruce_banner', 'Bruce Banner', '2015-07-08 00:00:00', '2015-07-10 03:34:58', 'student', 'demo'),
(6, 'student3@demo.com', 'hawk_eye', 'Hawk eye', '2015-07-08 00:00:00', '2015-07-10 03:35:15', 'student', 'demo'),
(7, 'student5@demo.com', 'nathasha_romanov', 'Nathasha Romanov', '2015-07-08 00:00:00', '2015-07-10 03:35:43', 'student', 'demo'),
(8, 'student4@demo.com', 'steve_rogers', 'Steve Rogers', '0000-00-00 00:00:00', '2015-07-10 03:35:54', 'student', 'demo');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
