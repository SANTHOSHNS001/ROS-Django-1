/*!40101 SET NAMES utf8 */;
/*!40014 SET FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET SQL_NOTES=0 */;
DROP TABLE IF EXISTS auth_group;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS auth_group_permissions;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS auth_permission;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS django_admin_log;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_ros_app_customuser_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_ros_app_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `ros_app_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS django_content_type;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS django_migrations;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS django_session;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS ros_app_custompermissions;
CREATE TABLE `ros_app_custompermissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS ros_app_customroles;
CREATE TABLE `ros_app_customroles` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS ros_app_customroles_permission;
CREATE TABLE `ros_app_customroles_permission` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `customroles_id` bigint(20) NOT NULL,
  `custompermissions_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ros_app_customroles_perm_customroles_id_customper_a8b7f2b1_uniq` (`customroles_id`,`custompermissions_id`),
  KEY `ros_app_customroles__custompermissions_id_ae949c4c_fk_ros_app_c` (`custompermissions_id`),
  CONSTRAINT `ros_app_customroles__custompermissions_id_ae949c4c_fk_ros_app_c` FOREIGN KEY (`custompermissions_id`) REFERENCES `ros_app_custompermissions` (`id`),
  CONSTRAINT `ros_app_customroles__customroles_id_afc78383_fk_ros_app_c` FOREIGN KEY (`customroles_id`) REFERENCES `ros_app_customroles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS ros_app_customuser;
CREATE TABLE `ros_app_customuser` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(254) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `password` varchar(128) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `picture` varchar(100) DEFAULT NULL,
  `role_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `ros_app_customuser_role_id_e21ce8b6_fk_ros_app_customroles_id` (`role_id`),
  CONSTRAINT `ros_app_customuser_role_id_e21ce8b6_fk_ros_app_customroles_id` FOREIGN KEY (`role_id`) REFERENCES `ros_app_customroles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS ros_app_customuser_groups;
CREATE TABLE `ros_app_customuser_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ros_app_customuser_groups_customuser_id_group_id_706c5ebf_uniq` (`customuser_id`,`group_id`),
  KEY `ros_app_customuser_groups_group_id_0b97a130_fk_auth_group_id` (`group_id`),
  CONSTRAINT `ros_app_customuser_g_customuser_id_4e8761c3_fk_ros_app_c` FOREIGN KEY (`customuser_id`) REFERENCES `ros_app_customuser` (`id`),
  CONSTRAINT `ros_app_customuser_groups_group_id_0b97a130_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS ros_app_customuser_user_permissions;
CREATE TABLE `ros_app_customuser_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ros_app_customuser_user__customuser_id_permission_c2fff6e3_uniq` (`customuser_id`,`permission_id`),
  KEY `ros_app_customuser_u_permission_id_508008d9_fk_auth_perm` (`permission_id`),
  CONSTRAINT `ros_app_customuser_u_customuser_id_b0923b0e_fk_ros_app_c` FOREIGN KEY (`customuser_id`) REFERENCES `ros_app_customuser` (`id`),
  CONSTRAINT `ros_app_customuser_u_permission_id_508008d9_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS ros_app_projects;
CREATE TABLE `ros_app_projects` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `project_name` varchar(100) NOT NULL,
  `description` longtext DEFAULT NULL,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `client_name` varchar(100) NOT NULL,
  `cpm_name` longtext NOT NULL,
  `cpm_email` varchar(254) NOT NULL,
  `cpm_phone` varchar(20) NOT NULL,
  `cdm_name` varchar(255) NOT NULL,
  `cdm_email` varchar(254) NOT NULL,
  `cdm_phone` varchar(20) NOT NULL,
  `document_manager_id` bigint(20) DEFAULT NULL,
  `project_manager_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_name` (`project_name`),
  UNIQUE KEY `client_name` (`client_name`),
  KEY `ros_app_projects_document_manager_id_7dc22a8d_fk_ros_app_c` (`document_manager_id`),
  KEY `ros_app_projects_project_manager_id_0a31f211_fk_ros_app_c` (`project_manager_id`),
  CONSTRAINT `ros_app_projects_document_manager_id_7dc22a8d_fk_ros_app_c` FOREIGN KEY (`document_manager_id`) REFERENCES `ros_app_customuser` (`id`),
  CONSTRAINT `ros_app_projects_project_manager_id_0a31f211_fk_ros_app_c` FOREIGN KEY (`project_manager_id`) REFERENCES `ros_app_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



INSERT INTO auth_permission(id,name,content_type_id,codename) VALUES('1','\'Can add log entry\'','1','\'add_logentry\''),('2','\'Can change log entry\'','1','\'change_logentry\''),('3','\'Can delete log entry\'','1','\'delete_logentry\''),('4','\'Can view log entry\'','1','\'view_logentry\''),('5','\'Can add permission\'','2','\'add_permission\''),('6','\'Can change permission\'','2','\'change_permission\''),('7','\'Can delete permission\'','2','\'delete_permission\''),('8','\'Can view permission\'','2','\'view_permission\''),('9','\'Can add group\'','3','\'add_group\''),('10','\'Can change group\'','3','\'change_group\''),('11','\'Can delete group\'','3','\'delete_group\''),('12','\'Can view group\'','3','\'view_group\''),('13','\'Can add content type\'','4','\'add_contenttype\''),('14','\'Can change content type\'','4','\'change_contenttype\''),('15','\'Can delete content type\'','4','\'delete_contenttype\''),('16','\'Can view content type\'','4','\'view_contenttype\''),('17','\'Can add session\'','5','\'add_session\''),('18','\'Can change session\'','5','\'change_session\''),('19','\'Can delete session\'','5','\'delete_session\''),('20','\'Can view session\'','5','\'view_session\''),('21','\'Can add custom permissions\'','6','\'add_custompermissions\''),('22','\'Can change custom permissions\'','6','\'change_custompermissions\''),('23','\'Can delete custom permissions\'','6','\'delete_custompermissions\''),('24','\'Can view custom permissions\'','6','\'view_custompermissions\''),('25','\'Can add custom roles\'','7','\'add_customroles\''),('26','\'Can change custom roles\'','7','\'change_customroles\''),('27','\'Can delete custom roles\'','7','\'delete_customroles\''),('28','\'Can view custom roles\'','7','\'view_customroles\''),('29','\'Can add user\'','8','\'add_customuser\''),('30','\'Can change user\'','8','\'change_customuser\''),('31','\'Can delete user\'','8','\'delete_customuser\''),('32','\'Can view user\'','8','\'view_customuser\''),('33','\'Can add projects\'','9','\'add_projects\''),('34','\'Can change projects\'','9','\'change_projects\''),('35','\'Can delete projects\'','9','\'delete_projects\''),('36','\'Can view projects\'','9','\'view_projects\'');


INSERT INTO django_content_type(id,app_label,model) VALUES('1','\'admin\'','\'logentry\''),('3','\'auth\'','\'group\''),('2','\'auth\'','\'permission\''),('4','\'contenttypes\'','\'contenttype\''),('6','\'ros_app\'','\'custompermissions\''),('7','\'ros_app\'','\'customroles\''),('8','\'ros_app\'','\'customuser\''),('9','\'ros_app\'','\'projects\''),('5','\'sessions\'','\'session\'');

INSERT INTO django_migrations(id,app,name,applied) VALUES('1','\'contenttypes\'','\'0001_initial\'','\'2023-10-05 08:50:44.740297\''),('2','\'contenttypes\'','\'0002_remove_content_type_name\'','\'2023-10-05 08:50:44.768751\''),('3','\'auth\'','\'0001_initial\'','\'2023-10-05 08:50:44.908912\''),('4','\'auth\'','\'0002_alter_permission_name_max_length\'','\'2023-10-05 08:50:44.954790\''),('5','\'auth\'','\'0003_alter_user_email_max_length\'','\'2023-10-05 08:50:44.965760\''),('6','\'auth\'','\'0004_alter_user_username_opts\'','\'2023-10-05 08:50:44.976735\''),('7','\'auth\'','\'0005_alter_user_last_login_null\'','\'2023-10-05 08:50:44.990223\''),('8','\'auth\'','\'0006_require_contenttypes_0002\'','\'2023-10-05 08:50:44.994206\''),('9','\'auth\'','\'0007_alter_validators_add_error_messages\'','\'2023-10-05 08:50:45.003182\''),('10','\'auth\'','\'0008_alter_user_username_max_length\'','\'2023-10-05 08:50:45.012164\''),('11','\'auth\'','\'0009_alter_user_last_name_max_length\'','\'2023-10-05 08:50:45.022131\''),('12','\'auth\'','\'0010_alter_group_name_max_length\'','\'2023-10-05 08:50:45.035096\''),('13','\'auth\'','\'0011_update_proxy_permissions\'','\'2023-10-05 08:50:45.045070\''),('14','\'auth\'','\'0012_alter_user_first_name_max_length\'','\'2023-10-05 08:50:45.053050\''),('15','\'ros_app\'','\'0001_initial\'','\'2023-10-05 08:50:45.243852\''),('16','\'admin\'','\'0001_initial\'','\'2023-10-05 08:50:45.303576\''),('17','\'admin\'','\'0002_logentry_remove_auto_add\'','\'2023-10-05 08:50:45.313616\''),('18','\'admin\'','\'0003_logentry_add_action_flag_choices\'','\'2023-10-05 08:50:45.324416\''),('19','\'ros_app\'','\'0002_customuser_role\'','\'2023-10-05 08:50:45.361187\''),('20','\'sessions\'','\'0001_initial\'','\'2023-10-05 08:50:45.384135\''),('21','\'ros_app\'','\'0003_rename_username_customroles_name\'','\'2023-10-05 08:53:47.423470\''),('22','\'ros_app\'','\'0004_alter_customuser_options_alter_customuser_email_and_more\'','\'2023-10-05 09:06:03.452820\''),('23','\'ros_app\'','\'0005_alter_customuser_picture\'','\'2023-10-05 09:41:06.059127\''),('24','\'ros_app\'','\'0006_customuser_created_at\'','\'2023-10-05 10:21:44.759707\''),('25','\'ros_app\'','\'0003_remove_customuser_picture_remove_customuser_role\'','\'2023-10-05 12:55:50.703840\''),('26','\'ros_app\'','\'0004_customuser_picture_customuser_role\'','\'2023-10-05 12:55:50.755603\''),('27','\'ros_app\'','\'0005_alter_customroles_permission\'','\'2023-10-06 05:01:43.125193\''),('28','\'ros_app\'','\'0006_alter_customroles_permission\'','\'2023-10-06 06:00:55.429534\''),('29','\'ros_app\'','\'0007_projects\'','\'2023-10-06 10:06:21.633879\''),('30','\'ros_app\'','\'0008_alter_customuser_managers\'','\'2023-10-07 05:08:17.621160\'');

INSERT INTO django_session(session_key,session_data,expire_date) VALUES('\'2vl0hgis3opfm29qhv0nh4d54kuvmlp7\'','X\'2e654a785669376b4f776a415142665f464e59725774304f4a52453146626133747452784244746d6b51767737695a51437571655a4e325f6d63583056767a6171666b6a737a4467375f624b41385548544c7572635043354c643544573354635f34556933656831786546364f35313965734a57747451514f49476d4a49714277655a2d5a43305736707879466752436a56745a714c5757696e49564d52706873754f733567414c322d514a7a765461743a31716f4f69453a44446f48546963616d507351756c4a346c52726f335a67765648624a51307939513444575a4e4732754559\'','\'2023-10-19 13:48:22.120807\''),('\'5rgz8mmnh8hdofwusigslanxkwkijvrf\'','X\'2e654a785669376b4f776a415142665f464e59725774304f4a52453146626133747452784244746d6b51767737695a51437571655a4e325f6d63583056767a6171666b6a737a4467375f624b41385548544c7572635043354c643544573354635f34556933656831786546364f35313965734a57747451514f49476d4a49714277655a2d5a43305736707879466752436a56745a714c5757696e49564d52706873754f733567414c322d514a7a765461743a31716f4c70673a65315f6d71466650685671305f346d546a5977653379646843686d4b38656d6a7769333762324e54726b49\'','\'2023-10-19 10:43:52.553311\''),('\'9r4owp437jc0cqr7bxk99a893w98sw0h\'','X\'2e654a78566937734f7769415568742d4632545345397079436f346d7a6b7a50356755506161477344646a4b2d757a58706f4f743365536d5039546e347455727859314a487865727779774c69546561764b495f7173537a4e546d707a3366794d5353376c504747386e5f627962783951682d306c345568574c4c686e596b5a756e645a426f6d5058697455706b556d647a656a49574154694347665968524354375a464236763042674851337a773a3171703131503a546861696f4b5f736f532d6146375270573669306966644e48754b49497a6f5963526c4a4a7758434a6730\'','\'2023-10-21 06:42:43.042037\''),('\'c324lw7238yislzju2g3oqqgcb8ma6bz\'','X\'2e654a785669376b4f776a415142665f464e59725774304f4a52453146626133747452784244746d6b51767737695a51437571655a4e325f6d63583056767a6171666b6a737a4467375f624b41385548544c7572635043354c643544573354635f34556933656831786546364f35313965734a57747451514f49476d4a49714277655a2d5a43305736707879466752436a56745a714c5757696e49564d52706873754f733567414c322d514a7a765461743a31716f4f676d3a4c342d726c56324f635951532d6e486a6f666e72485a6c6245765a425765353276395a6a2d56506e6e674d\'','\'2023-10-19 13:46:52.451985\''),('\'myg72h6v7560hyp9gqzjmwci5m6fkswd\'','X\'2e654a785669376b4f776a415142665f464e59725774304f4a52453146626133747452784244746d6b51767737695a51437571655a4e325f6d63583056767a6171666b6a737a4467375f624b41385548544c7572635043354c643544573354635f34556933656831786546364f35313965734a57747451514f49476d4a49714277655a2d5a43305736707879466752436a56745a714c5757696e49564d52706873754f733567414c322d514a7a765461743a31716f4f62703a71397471443748655454316a6e6b314e414c626f41732d6751774932615274706842314f6a6a6858423477\'','\'2023-10-19 13:41:45.414231\''),('\'tjkdkvbr9l5dmkn059cgg6bmx9d7dcvx\'','X\'2e654a785669376b4f776a415142665f464e59725774304f4a52453146626133747452784244746d6b51767737695a51437571655a4e325f6d63583056767a6171666b6a737a4467375f624b41385548544c7572635043354c643544573354635f34556933656831786546364f35313965734a57747451514f49476d4a49714277655a2d5a43305736707879466752436a56745a714c5757696e49564d52706873754f733567414c322d514a7a765461743a31716f4f68593a664a6a4a6865554b397355654a55797566503032365475364a30384e7a7170334a454664716d5175483163\'','\'2023-10-19 13:47:40.513362\''),('\'veuohuci00xhlz06nrl8p9zq5z268c45\'','X\'2e654a785669376b4f776a415142665f464e59725774304f4a52453146626133747452784244746d6b51767737695a51437571655a4e325f6d63583056767a6171666b6a737a4467375f624b41385548544c7572635043354c643544573354635f34556933656831786546364f35313965734a57747451514f49476d4a49714277655a2d5a43305736707879466752436a56745a714c5757696e49564d52706873754f733567414c322d514a7a765461743a31716f63446f3a4b7856453658466c77444b31662d36584571704f6e7449545950506e34326e4f7466484d4348414570696f\'','\'2023-10-20 04:13:52.725911\''),('\'ygl56h5dw20moa5orgeoj9uzn6rv97kg\'','X\'2e654a785669376b4f776a415142665f464e59725774304f4a52453146626133747452784244746d6b51767737695a51437571655a4e325f6d63583056767a6171666b6a737a4467375f624b41385548544c7572635043354c643544573354635f34556933656831786546364f35313965734a57747451514f49476d4a49714277655a2d5a43305736707879466752436a56745a714c5757696e49564d52706873754f733567414c322d514a7a765461743a31716f4e68633a6c3049706e6b5a6e4d4f54736d426f50384b744c62515667767631642d6a7541536a506a4f705a65673845\'','\'2023-10-19 12:43:40.169232\'');

INSERT INTO ros_app_custompermissions(id,name,description,created_at) VALUES('1','\'Permissions\'','NULL','\'2023-10-05 08:52:31.513809\''),('2','\'Users\'','NULL','\'2023-10-05 08:52:37.679807\''),('3','\'Documents\'','NULL','\'2023-10-06 09:12:58.013761\''),('4','\'Roles\'','NULL','\'2023-10-06 09:13:17.361890\''),('5','\'Projects\'','NULL','\'2023-10-07 07:06:38.041332\'');

INSERT INTO ros_app_customroles(id,name,description,created_at) VALUES('1','\'Admin\'','NULL','\'2023-10-05 08:53:50.960306\''),('2','\'Super Admin\'','NULL','\'2023-10-05 08:54:04.115174\''),('3','\'Project Manager\'','NULL','\'2023-10-06 09:56:21.620526\''),('4','\'Document Manager\'','NULL','\'2023-10-06 09:56:42.737189\''),('7','\'Manager\'','NULL','\'2023-10-07 07:07:08.270750\'');

INSERT INTO ros_app_customroles_permission(id,customroles_id,custompermissions_id) VALUES('1','1','1'),('4','1','2'),('7','2','1'),('10','2','2'),('13','3','2'),('16','3','3'),('19','4','3'),('21','7','2'),('24','7','3'),('27','7','5');

INSERT INTO ros_app_customuser(id,last_login,is_superuser,username,is_staff,is_active,date_joined,email,first_name,last_name,password,created_at,picture,role_id) VALUES('1','\'2023-10-07 05:08:40.365599\'','1','\'admin1\'','1','1','\'2023-10-05 08:51:22.678646\'','\'admin1@ros.com\'','\'\'','\'\'','\'pbkdf2_sha256$600000$JPKPHIfUyufrwrquLFkG6Y$sX996GexKrDzDGqEx+4KMrChKaZIMF3l98H/yM3TpnY=\'','\'2023-10-05 10:21:44.738763\'','NULL','NULL'),('2','\'2023-10-05 12:57:41.125521\'','0','\'Suganesh\'','0','1','\'2023-10-05 09:42:06.695388\'','\'sugan739@gmail.com\'','\'Suganesh\'','\'R\'','\'pbkdf2_sha256$600000$DXcjIVU2VDQAs7RMylskAy$PZ6FKvp/ZMTpVMuoJknu2OOpb/DebnbZiCcxX1CGDho=\'','\'2023-10-05 10:21:44.738763\'','NULL','NULL'),('3','NULL','0','\'User1\'','0','1','\'2023-10-05 13:42:49.963131\'','\'user1@ros.com\'','\'User\'','\'1\'','\'pbkdf2_sha256$600000$z02i6BgzDwreUe621taTWk$bx8zFOP7mp1g4LckMOuf+4CWtvfY5OvNqUsVNTSKlD4=\'','\'2023-10-05 13:42:50.597942\'','\'\'','1'),('4','\'2023-10-07 04:16:30.694832\'','0','\'Jhon123\'','0','1','\'2023-10-06 09:57:49.058159\'','\'jhon@ros.com\'','\'Jhon\'','\'Doe\'','\'pbkdf2_sha256$600000$zbawsAPRmwlOtW8LkE0PzU$JNzc1nMn02RDLOIm0a7X4eE7d4im+4usNPdJPNq3kSk=\'','\'2023-10-06 09:57:49.734439\'','\'\'','3'),('5','NULL','0','\'Janedoe\'','0','1','\'2023-10-06 09:58:36.769238\'','\'jane@ros.com\'','\'Jane\'','\'Doe\'','\'pbkdf2_sha256$600000$bQn1HpzI1rlHVAQhuvOe5A$4SGdrfNxNXSVGsehemntcjPVXd8OrI1fKfA6Q94Xo1c=\'','\'2023-10-06 09:58:37.414393\'','\'\'','4'),('6','\'2023-10-07 06:42:43.039641\'','1','\'admin2\'','1','1','\'2023-10-07 05:57:48.795135\'','\'admin2@ros.com\'','\'\'','\'\'','\'pbkdf2_sha256$600000$WpLmslNNqmVSTeNO2gUv62$3kiZjZXS5yZVCA3p9kpr8kd5qGHrMYk1gjdle1gToAQ=\'','\'2023-10-07 05:57:49.570484\'','\'\'','2');


INSERT INTO ros_app_projects(id,project_name,description,start_date,end_date,client_name,cpm_name,cpm_email,cpm_phone,cdm_name,cdm_email,cdm_phone,document_manager_id,project_manager_id) VALUES('1','\'Project2\'','X\'646f63746f7220636f6e73756c74616e7420617070207769746820746578742022446f63746f7222\'','\'2023-10-13 00:00:00.000000\'','\'2023-10-24 00:00:00.000000\'','\'Client1\'','X\'504d32\'','\'pm2@ros.com\'','\'1234567890\'','\'DM2\'','\'dm2@ros.com\'','\'1234569870\'','5','4'),('2','\'Project3\'','X\'646f63746f7220636f6e73756c74616e7420617070207769746820746578742022446f63746f7222\'','\'2023-10-06 00:00:00.000000\'','\'2023-10-31 00:00:00.000000\'','\'Client2\'','X\'504d33\'','\'pm3@ros.com\'','\'1234567890\'','\'DM3\'','\'dm3@ros.com\'','\'1234569870\'','5','4');