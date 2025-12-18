-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.5.62 - MySQL Community Server (GPL)
-- Server OS:                    Win64
-- HeidiSQL Version:             9.1.0.4867
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping database structure for blue_cinemas
CREATE DATABASE IF NOT EXISTS blue_cinemas /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `blue_cinemas`;


-- Dumping structure for table blue_cinemas.bookings
CREATE TABLE IF NOT EXISTS `bookings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `show_id` int(11) DEFAULT NULL,
  `username` varchar(100) DEFAULT NULL,
  `movie_title` varchar(100) DEFAULT NULL,
  `show_date` date DEFAULT NULL,
  `show_time` varchar(20) DEFAULT NULL,
  `seats` varchar(100) DEFAULT NULL,
  `ntickets` int(11) DEFAULT NULL,
  `booking_date` datetime DEFAULT NULL,
  `total_price` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `show_id` (`show_id`),
  CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`show_id`) REFERENCES `shows` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

-- Dumping data for table blue_cinemas.bookings: ~6 rows (approximately)
/*!40000 ALTER TABLE `bookings` DISABLE KEYS */;
INSERT INTO `bookings` (`show_id`, `username`, `movie_title`, `show_date`, `show_time`, `seats`, `ntickets`, `booking_date`, `total_price`) VALUES
	(177, 'sherry', 'DUDE', '2025-11-26', '17:00:00', 'D4,D5', 2, '2025-11-10 19:47:45', 438),
	(173, 'dubha', 'ELEVEN', '2025-11-26', '10:30:00', 'B5,C3,E4,E5', 4, '2025-11-11 12:47:49', 860),
	(191, 'sigma', 'COOLIE', '2025-11-29', '10:00:00', 'C4,C6', 2, '2025-11-11 12:58:21', 700),
	(191, 'sherry', 'COOLIE', '2025-11-29', '10:00:00', 'E3,E5', 2, '2025-11-11 13:22:07', 700),
	(176, 'sherry', 'DUDE', '2025-11-26', '12:00:00', 'A1,A2', 2, '2025-11-11 21:08:52', 438),
	(194, 'sherry', 'MADHARAASI', '2025-11-29', '11:00:00', 'E2,E4', 2, '2025-11-15 20:07:52', 480);
/*!40000 ALTER TABLE `bookings` ENABLE KEYS */;


-- Dumping structure for table blue_cinemas.movies
CREATE TABLE IF NOT EXISTS `movies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) DEFAULT NULL,
  `language` varchar(50) DEFAULT NULL,
  `genre` varchar(100) DEFAULT NULL,
  `duration_minutes` int(11) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `rating` varchar(10) DEFAULT NULL,
  `description` text,
  `poster_filename` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=latin1;

-- Dumping data for table blue_cinemas.movies: ~29 rows (approximately)
/*!40000 ALTER TABLE `movies` DISABLE KEYS */;
INSERT INTO `movies` (`title`, `language`, `genre`, `duration_minutes`, `price`, `rating`, `description`, `poster_filename`) VALUES
	('DIESEL', 'Tamil', 'Action, Drama, Thriller', 144, 200, 'UA', 'Vasu, a smuggler who takes over his father\'s illegal fuel trade in North Chennai. His rise to power turns into a fight for survival as betrayal and corruption consume his world.', 'diesel.jpg'),
	('DRAGON', 'Tamil', 'Comedy, Drama', 154, 260, 'UA', 'A college dropout obtains a high-paying job through deception, but when his secret is threatened, he must face the consequences and repair his life', 'dragon.jpg'),
	('ELEVEN', 'Tamil', 'Crime, Mystery, Thriller', 136, 215, 'UA', 'A seasoned cop investigates a series of murders targeting twins, uncovering a dark pattern and a chilling past. The deeper he goes, the more his own beliefs and skills are tested.', 'eleven.jpg'),
	('DUDE', 'Tamil', 'Romantic, Comedy, Action Drama', 139, 219, 'UA', 'Agan, a carefree event organizer, is pushed into adulthood by a staged rescue event that forces him to face his past and love for Kuralarasi. As the truth emerges, his journey transforms from a party-lover to a man seeking redemption and genuine connection.', 'dude.jpg'),
	('BISON', 'Tamil', 'Biography, Drama, Sports', 168, 190, 'UA', 'A young man from a marginalized caste in rural Tamil Nadu defies violent factional politics and caste-based oppression to pursue his dream of playing kabaddi and representing India. His path is fraught with trauma, family loss and sacrifice, but he stands strong to turn his ambition into a symbol of resistance.', 'bison.jpg'),
	('SHAKTHI THIRUMAGAN', 'Tamil', 'Action, Drama, Political Thriller', 157, 200, 'UA', 'A street-smart strategist rises from the shadows, challenging a corrupt power structure to become the voice of the oppressed. His fight turns into a full-scale war for justice, exposing the truth behind political systems.', 'shakthi thirumagan.jpg'),
	('IDLI KADAI', 'Tamil', 'Drama', 147, 300, 'U', 'A humble idli-vendor from rural Tamil Nadu faces unexpected challenges when rural life collides with ambition and tradition. His journey becomes a test of values, community and family as he strives to keep his legacy alive.', 'idli kadai.jpg'),
	('THALAIVAN THALAIVI', 'Tamil', 'Romantic, Comedy-Drama', 140, 250, 'UA', 'Aagasaveeran and Perarasi are newly married with love in their hearts, but everyday conflicts, family pressures and personal pride turn their joyous union into a complicated journey of understanding and forgiveness.', 'thalaivan thalaivi.jpg'),
	('COOLIE', 'Tamil', 'Action, Thriller, Drama', 169, 350, 'A', 'A former gold smuggler turned hostel-owner delves into a dangerous underworld of trafficking and corruption when his friend\'s mysterious death pulls him back into crime. His quest for truth leads him to confront syndicates, hidden betrayals and his own past.', 'coolie.jpg'),
	('MADHARAASI', 'Tamil', 'Psychological Action Thriller', 168, 240, 'A', 'A man haunted by trauma and psychological disorder is recruited to infiltrate a powerful arms smuggling syndicate, leading to a violent confrontation with his own mind and the criminal underworld. As his mission escalates, he must reconcile his inner turmoil with his drive for justice and the cost of his actions.', 'madharaasi.jpg'),
	('LONDON CALLING', 'English', 'Action, Comedy', 114, 210, 'R', 'A mediocre hitman botches a job, flees to Los Angeles, and enters a deal to teach his crime boss\'s awkward son the ropes. What begins as a routine mission turns into a wild ride of gunfights, car chases, and surprising mentorship.', 'london calling.jpg'),
	('THE PLAGUE', 'English', 'Mystery, Thriller, Drama', 95, 260, 'R', 'A socially anxious 12-year-old boy enters an elite all-boys water-polo camp where a cruel tradition labels one student as "the plague." As the ritual escalates, the line between game and real threat blurs, forcing him to face vicious bullying and survival.', 'the plague.jpg'),
	('HAMLET', 'English', 'Drama', 113, 230, 'R', 'A modern Prince Hamlet returns to London after his father\'s sudden death and uncovers a web of betrayal involving his uncle Claudius and the city\'s elite. Struggling with grief and identity, he moves from upscale society into the underground to seek revenge and truth.', 'hamlet.jpg'),
	('THE LOST BUS', 'English', 'Drama, Thriller, Survival', 130, 230, 'PG-13', 'A school-bus driver and a teacher must guide 22 children to safety during California\'s deadly 2018 Camp Fire. As the inferno rages around them, their survival depends on courage, trust, and swift decision-making.', 'the lost bus.jpg'),
	('STEVE', 'English', 'Drama', 92, 190, 'R', 'A dedicated headteacher at a struggling reform school attempts to keep his institution open while battling his own inner demons. Meanwhile, a troubled student fights to shape a future amid a system that has already written him off.', 'steve.jpg'),
	('THE LIFE OF CHUCK', 'English', 'Drama, Fantasy, Science Fiction', 111, 300, 'R', 'Chuck Krantz experiences key moments in his life—from his death coinciding with the end of the universe back to his childhood—uncovering love, loss and cosmic connections as his story plays out in reverse.', 'the life of chuck.jpg'),
	('ELIO', 'English', 'Animation, Science Fiction, Adventure', 99, 200, 'PG', 'An 11-year-old boy named Elio, obsessed with aliens, is accidentally chosen as Earth\'s ambassador to a vast alien alliance. As he navigates intergalactic chaos and his own identity, he discovers what belonging truly means.', 'elio.jpg'),
	('BLUE MOON', 'English', 'Biographical Comedy-Drama', 210, 245, 'R', 'Songwriter Lorenz Hart finds himself on the night of the opening of Oklahoma! grappling with fame, insecurity and lost connection with his former partner. As he enters a world of drinking and emotional collapse, he must face the cost of success and the meaning of legacy.', 'blue moon.jpg'),
	('ONE MORE SHOT', 'English', 'Comedy, Drama, Fantasy', 91, 322, 'PG-13', 'On New Year\'s Eve 1999, Minnie finds a bottle of time-traveling tequila that sends her back to the start of the night with each shot, giving her countless chances to fix her past and win back her old flame. But as the loop continues, she realises that changing the night means changing herself.', 'one more shot.jpg'),
	('HIT THE THIRD CASE', 'Telugu', 'Action Thriller', 157, 234, 'A', 'A top-cop reassigned to a homicide unit uncovers shocking truths about serial killers and his own past.', 'hit the third case.jpg'),
	('GAME CHANGER', 'Telugu', 'Political Action Thriller', 165, 215, 'UA', 'An upright IAS officer battles corruption and fights for fair elections, challenging entrenched power structures.', 'game changer.jpg'),
	('KINGDOM', 'Telugu', 'Spy Action Thriller', 160, 199, 'UA', 'A troubled police constable on an undercover mission confronts his past and a dangerous enemy while navigating a treacherous criminal world.', 'kingdom.jpg'),
	('THANDEL', 'Telugu', 'Romantic Action Thriller', 152, 242, 'UA', 'A fisherman captured by enemy forces fights to survive and seek justice for his community and his love.', 'thandel.jpg'),
	('THEY CALL HIM OG', 'Telugu', 'Action Crime Drama', 154, 238, 'A', 'A feared gangster returns after a decade to reclaim his empire and settle a personal vendetta, triggering a brutal power struggle.', 'they call him og.jpg'),
	('KUBERAA', 'Telugu', 'Social Thriller', 181, 180, 'UA', 'Set in the gritty underbelly of Mumbai, Deva, a beggar from Tirupati, is drawn into a dark conspiracy when a hidden oil field is discovered; as he navigates the world of power and greed, he must decide how far he\'ll go to survive and rise', 'kuberaa.jpg'),
	('MIRAI', 'Telugu', 'Fantasy Action Adventure', 169, 300, 'UA', 'In a fantasy-action adventure set during and after the Kalinga war, a young warrior known as the "Black Sword" must find the nine secret books and stop a looming eclipse that threatens to destroy his world.', 'mirai.jpg'),
	('COURT:NOBODY VS STATE', 'Telugu', 'Drama Thriller', 149, 255, 'UA', 'A young man from a humble background becomes entangled in a false POCSO accusation by a powerful family\'s patriarch; a junior lawyer takes on the case and battles the legal system to help him seek justice.', 'court.jpg'),
	('GHAATI', 'Telugu', 'Action Crime Drama', 156, 230, 'A', 'In rural Uttar Andhra, a woman, driven by circumstances and assault, rises to become a feared figure in the ganja smuggling underworld; as she fights to protect her community, she confronts brutal violence and betrayal.', 'ghaati.jpg'),
	('JATADHARA', 'Telugu', 'Action-Adventure Fantasy Thriller', 135, 199, 'A', 'Amidst ancient mythology, a supernatural thrill ride unfolds when a man breaks a sacred vault\'s curse and unleashes demonic forces; he must face divine wrath, dark rituals, and his own demons to save the world from the power of greed.', 'jatadhara.jpg');
/*!40000 ALTER TABLE `movies` ENABLE KEYS */;


-- Dumping structure for table blue_cinemas.shows
CREATE TABLE IF NOT EXISTS `shows` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_id` int(11) DEFAULT NULL,
  `show_date` date DEFAULT NULL,
  `show_time` time DEFAULT NULL,
  `seats_total` int(11) DEFAULT '100',
  `seats_booked` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `movie_id` (`movie_id`),
  CONSTRAINT `shows_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=197 DEFAULT CHARSET=latin1;

-- Dumping data for table blue_cinemas.shows: ~30 rows (approximately)
/*!40000 ALTER TABLE `shows` DISABLE KEYS */;
INSERT INTO `shows` (`id`, `movie_id`, `show_date`, `show_time`, `seats_total`, `seats_booked`) VALUES
	(167, 1, '2025-11-10', '10:00:00', 100, 0),
	(168, 1, '2025-11-25', '14:30:00', 100, 0),
	(169, 1, '2025-11-25', '19:00:00', 100, 0),
	(170, 2, '2025-11-25', '11:00:00', 100, 0),
	(171, 2, '2025-11-25', '16:00:00', 100, 0),
	(172, 2, '2025-11-25', '20:30:00', 100, 0),
	(173, 3, '2025-11-26', '10:30:00', 100, 4),
	(174, 3, '2025-11-26', '15:00:00', 100, 0),
	(175, 3, '2025-11-26', '19:30:00', 100, 0),
	(176, 4, '2025-11-26', '12:00:00', 100, 2),
	(177, 4, '2025-11-26', '17:00:00', 100, 2),
	(178, 4, '2025-11-26', '21:00:00', 100, 0),
	(179, 5, '2025-11-27', '09:30:00', 100, 0),
	(180, 5, '2025-11-27', '13:30:00', 100, 0),
	(181, 5, '2025-11-27', '18:00:00', 100, 0),
	(182, 6, '2025-11-27', '11:30:00', 100, 0),
	(183, 6, '2025-11-27', '16:30:00', 100, 0),
	(184, 6, '2025-11-27', '21:00:00', 100, 0),
	(185, 7, '2025-11-28', '10:00:00', 100, 0),
	(186, 7, '2025-11-28', '14:00:00', 100, 0),
	(187, 7, '2025-11-28', '18:30:00', 100, 0),
	(188, 8, '2025-11-28', '12:30:00', 100, 0),
	(189, 8, '2025-11-28', '17:30:00', 100, 0),
	(190, 8, '2025-11-28', '22:00:00', 100, 0),
	(191, 9, '2025-11-29', '10:00:00', 100, 4),
	(192, 9, '2025-11-29', '15:00:00', 100, 0),
	(193, 9, '2025-11-29', '20:00:00', 100, 0),
	(194, 10, '2025-11-29', '11:00:00', 100, 2),
	(195, 10, '2025-11-29', '16:00:00', 100, 0),
	(196, 10, '2025-11-29', '21:00:00', 100, 0);
/*!40000 ALTER TABLE `shows` ENABLE KEYS */;


-- Dumping structure for table blue_cinemas.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `is_admin` int(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table blue_cinemas.users: ~10 rows (approximately)
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (`id`, `username`, `password`, `email`, `is_admin`) VALUES
	(1, 'admin', 'admin123', 'bluecinemas@gmail.com', 1),
	(2, 'sherry', 'sherry', 'noneofyobusiness@gmail.com', 0),
	(3, 'ray', 'rayzephyr', 'ray@gmail.com', 0),
	(4, 'samantha', 'sammie', 'sam@gmail.com', 0),
	(5, 'theo', 'theo2025', 'theo@gmail.com', 0),
	(6, 'AP', 'Idk@123', '7bakshayapriya@gmail.com', 0),
	(7, 'shasha', '123', 'vkhb', 0),
	(8, 'prams', '2018', '123@pssenior.com', 0),
	(9, 'dubha', '1345', 'dubha@dubakur.com', 0),
	(10, 'sigma', 'sigma1', 'baboon@gmail.com', 0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
