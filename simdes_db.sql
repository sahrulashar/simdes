-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: simdes_db
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `aparat_desa`
--

DROP TABLE IF EXISTS `aparat_desa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `aparat_desa` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nama` varchar(100) NOT NULL,
  `jabatan` varchar(100) NOT NULL,
  `foto` varchar(255) DEFAULT NULL,
  `kontak` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aparat_desa`
--

LOCK TABLES `aparat_desa` WRITE;
/*!40000 ALTER TABLE `aparat_desa` DISABLE KEYS */;
INSERT INTO `aparat_desa` VALUES (6,'KASMAWATI','SEKRETARIS DESA','WhatsApp_Image_2025-07-22_at_13.48.30.jpeg','xxxxxxxxx','2025-07-22 10:25:01'),(7,'SUMARNI','KASI KESEJAHTERAAN','WhatsApp_Image_2025-07-22_at_13.48.31_2.jpeg','xxxxxxxxx','2025-07-22 10:25:42'),(8,'ALISMAN','KAUR PERENCANAAN','WhatsApp_Image_2025-07-22_at_13.48.31_3.jpeg','xxxxxxxxx','2025-07-22 10:26:05'),(9,'KAHAR,SE','KAUR KEUANGAN','WhatsApp_Image_2025-07-22_at_13.48.32_3.jpeg','xxxxxxxxx','2025-07-22 10:26:27'),(10,'NURHAYATI,S.SI','KASI PELAYANAN','WhatsApp_Image_2025-07-22_at_13.48.33_1.jpeg','xxxxxxxxx','2025-07-22 10:27:21'),(11,'RISMAWATI','KAUR TATA USAHA DAN UMUM','WhatsApp_Image_2025-07-22_at_13.48.32_2.jpeg','xxxxxxxxx','2025-07-22 10:27:43'),(12,'NURUL ICHSAN,S.KOM','KASI PEMERINTAHAN','WhatsApp_Image_2025-07-22_at_13.48.33.jpeg','xxxxxxxxx','2025-07-22 10:28:44'),(13,'NURHADIN','KEPALA DUSUN GATTARENG','WhatsApp_Image_2025-07-22_at_13.48.31_1.jpeg','xxxxxxxxx','2025-07-22 10:29:08'),(14,'HERIANTO ','KEPALA DUSUN KESSI','WhatsApp_Image_2025-07-22_at_13.48.32_1.jpeg','xxxxxxxxx','2025-07-22 10:29:30'),(15,'IRWANSA,S.IP','KEPALA DESA','kepala_desa.jpeg','xxxxxxxxx','2025-07-28 06:07:11');
/*!40000 ALTER TABLE `aparat_desa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `belum_nikah`
--

DROP TABLE IF EXISTS `belum_nikah`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `belum_nikah` (
  `id` int NOT NULL AUTO_INCREMENT,
  `no_surat` varchar(50) NOT NULL,
  `nik` varchar(20) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `jenis_kelamin` enum('Laki-laki','Perempuan') NOT NULL,
  `tempat_lahir` varchar(50) DEFAULT NULL,
  `tanggal_lahir` date DEFAULT NULL,
  `pekerjaan` varchar(100) DEFAULT NULL,
  `alamat` text,
  `status` enum('pending','approved') DEFAULT 'pending',
  `pembuat_surat` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no_surat` (`no_surat`),
  KEY `fk_belum_nikah_penduduk` (`nik`),
  CONSTRAINT `fk_belum_nikah_penduduk` FOREIGN KEY (`nik`) REFERENCES `penduduk` (`nik`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `belum_nikah`
--

LOCK TABLES `belum_nikah` WRITE;
/*!40000 ALTER TABLE `belum_nikah` DISABLE KEYS */;
INSERT INTO `belum_nikah` VALUES (1,'BN-20250824032531','7302010101011001','Ahmad Saputra','Laki-laki','Soppeng','1995-06-12','Petani','Jl. Merpati No.1','approved','Admin','2025-08-23 19:25:31'),(2,'BN-20250824033124','7302010101011003','Budi Setiawan','Laki-laki','Makassar','1988-09-30','Buruh','Dusun Makmur, RT 01/RW 01, Desa Gattareng Toa, Kec. Marioriwawo, Soppeng, Sulawesi Selatan','approved','User','2025-08-23 19:31:24');
/*!40000 ALTER TABLE `belum_nikah` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `berita`
--

DROP TABLE IF EXISTS `berita`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `berita` (
  `id` int NOT NULL AUTO_INCREMENT,
  `judul` varchar(255) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `konten` text NOT NULL,
  `gambar` varchar(255) DEFAULT NULL,
  `pembuat` varchar(100) DEFAULT 'Admin',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `berita`
--

LOCK TABLES `berita` WRITE;
/*!40000 ALTER TABLE `berita` DISABLE KEYS */;
INSERT INTO `berita` VALUES (1,'Dusun Bunga, 25 Juli 2025 — Warga Dusun Bunga bersama aparat desa melaksanakan kegiatan gotong royong membersihkan saluran irigasi dan jalan lingkungan desa.','dusun-bunga-25-juli-2025-warga-dusun-bunga-bersama-aparat-desa-melaksanakan-kegiatan-gotong-royong-membersihkan-saluran-irigasi-dan-jalan-lingkungan-desa','<p>Kegiatan ini bertujuan untuk menjaga kebersihan lingkungan serta mencegah terjadinya banjir akibat tersumbatnya saluran air. Kegiatan dimulai pukul 07.00 WITA dan diikuti oleh lebih dari 60 warga serta perangkat desa.</p><p>Beberapa aktivitas utama yang dilakukan:</p><ol><li>Pembersihan saluran air sepanjang 300 meter</li><li>Pengangkutan sampah dan gulma dari area pertanian</li><li>Penanaman bibit pohon di sepanjang jalan desa</li></ol><p>Kepala Desa mengucapkan terima kasih atas partisipasi aktif seluruh warga dan berharap semangat gotong royong ini terus dipelihara sebagai bagian dari budaya desa.</p>','Screenshot_2024-03-10-19-43-59-38_6012fa4d4ddec268fc5c7112cbb265e7.jpg','Admin','2025-07-25 03:01:05'),(2,'Pelatihan Digitalisasi Administrasi Desa Berbasis Website','pelatihan-digitalisasi-administrasi-desa-berbasis-website','<p data-start=\"242\" data-end=\"561\">Balai Desa Sumber Makmur, 22 Juli 2025 — Pemerintah Desa Sumber Makmur menggelar pelatihan digitalisasi administrasi desa bagi perangkat dan operator desa. Kegiatan ini bertujuan meningkatkan pemahaman teknologi dalam pengelolaan surat menyurat, data penduduk, serta pengelolaan informasi publik berbasis sistem online.</p><p>\r\n</p><p data-start=\"563\" data-end=\"671\">Pelatihan ini berlangsung selama dua hari dan diikuti oleh seluruh aparat desa, dengan materi yang mencakup:</p><ol><li>Dasar-dasar penggunaan komputer dan internet</li><li>Pengelolaan data kependudukan menggunakan aplikasi desa</li><li>Upload dan publikasi berita melalui sistem informasi desa</li></ol><p data-start=\"838\" data-end=\"995\">Instruktur utama berasal dari Dinas Komunikasi dan Informatika Kabupaten yang telah berpengalaman dalam pengembangan sistem pemerintahan berbasis elektronik.</p><p>\r\n</p><p data-start=\"997\" data-end=\"1138\">Kepala Desa Sumber Makmur berharap kegiatan ini dapat menjadi langkah awal menuju pelayanan publik yang lebih cepat, transparan, dan efisien.</p>','1713359248242819-0.jpg','Admin','2025-07-25 03:12:22'),(3,'Posyandu Balita di Desa Lestari Kembali Aktif Setiap Bulan','posyandu-balita-di-desa-lestari-kembali-aktif-setiap-bulan','<p data-start=\"241\" data-end=\"560\">Desa Lestari, 18 Juli 2025 — Kegiatan Posyandu Balita di Desa Lestari kembali berjalan rutin setiap bulan setelah sempat terhenti selama masa pandemi. Antusiasme ibu-ibu sangat tinggi dalam mengikuti pemeriksaan rutin anak-anak mereka, mulai dari penimbangan, pengukuran tinggi badan, hingga pemberian makanan tambahan.</p><p>\r\n</p><p data-start=\"562\" data-end=\"717\">Petugas kesehatan dari Puskesmas Kecamatan juga turut hadir untuk memberikan penyuluhan tentang gizi seimbang dan pentingnya imunisasi lengkap bagi balita.</p><p data-start=\"562\" data-end=\"717\">Adapun tujuan kegiatan ini adalah:</p><ol><li>Meningkatkan status kesehatan dan gizi anak-anak usia dini</li><li>Memberikan edukasi kepada ibu tentang perawatan anak</li><li>Memantau pertumbuhan dan perkembangan balita secara berkala</li></ol><p>Kepala Desa Lestari mengucapkan terima kasih atas kerja sama para kader dan ibu-ibu yang telah mendukung pelaksanaan kegiatan ini. Ia berharap Posyandu bisa menjadi pilar penting dalam menjaga generasi muda yang sehat dan cerdas.</p>','maxresdefault.jpg','Admin','2025-07-25 03:14:13');
/*!40000 ALTER TABLE `berita` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `galeri`
--

DROP TABLE IF EXISTS `galeri`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `galeri` (
  `id` int NOT NULL AUTO_INCREMENT,
  `judul` varchar(255) NOT NULL,
  `deskripsi` text,
  `gambar` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `galeri`
--

LOCK TABLES `galeri` WRITE;
/*!40000 ALTER TABLE `galeri` DISABLE KEYS */;
INSERT INTO `galeri` VALUES (4,'Permandian Alam Lereng Hijau','Halo','bg-hero.jpg','2025-07-24 10:57:44'),(5,'Lereng Hijau','Lereng Hijau','hq720.jpg','2025-07-24 11:29:02'),(6,'Lereng Hijau','Lereng Hijau','2017-03-19.jpg','2025-07-24 11:29:02'),(7,'Lereng Hijau','Lereng Hijau','bg-hero.jpg','2025-07-24 11:29:02'),(9,'Lereng Hijau','Lereng Hijau','kolam-renang-di-soppeng_20160106_182255.jpg','2025-07-24 11:29:02');
/*!40000 ALTER TABLE `galeri` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gambar_subpotensi`
--

DROP TABLE IF EXISTS `gambar_subpotensi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gambar_subpotensi` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sub_potensi_id` int DEFAULT NULL,
  `file_gambar` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sub_potensi_id` (`sub_potensi_id`),
  CONSTRAINT `gambar_subpotensi_ibfk_1` FOREIGN KEY (`sub_potensi_id`) REFERENCES `sub_potensi` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gambar_subpotensi`
--

LOCK TABLES `gambar_subpotensi` WRITE;
/*!40000 ALTER TABLE `gambar_subpotensi` DISABLE KEYS */;
INSERT INTO `gambar_subpotensi` VALUES (2,3,'bglerenghijau.jpg'),(3,4,'Screenshot_2024-03-10-19-43-59-38_6012fa4d4ddec268fc5c7112cbb265e7.jpg'),(4,5,'Screenshot_2024-03-10-19-43-59-38_6012fa4d4ddec268fc5c7112cbb265e7.jpg');
/*!40000 ALTER TABLE `gambar_subpotensi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hilang`
--

DROP TABLE IF EXISTS `hilang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hilang` (
  `id` int NOT NULL AUTO_INCREMENT,
  `no_surat` varchar(50) NOT NULL,
  `nik` varchar(20) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `jenis_kelamin` enum('Laki-laki','Perempuan') DEFAULT NULL,
  `tempat_lahir` varchar(50) DEFAULT NULL,
  `tanggal_lahir` date DEFAULT NULL,
  `alamat` text,
  `keterangan` text,
  `status` enum('pending','approved') DEFAULT 'pending',
  `pembuat_surat` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no_surat` (`no_surat`),
  KEY `fk_hilang_penduduk` (`nik`),
  CONSTRAINT `fk_hilang_penduduk` FOREIGN KEY (`nik`) REFERENCES `penduduk` (`nik`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hilang`
--

LOCK TABLES `hilang` WRITE;
/*!40000 ALTER TABLE `hilang` DISABLE KEYS */;
INSERT INTO `hilang` VALUES (1,'HIL-20250824034052','7302010101011006','Nur Aisyah','Perempuan','Soppeng','2002-04-10','Jl. Melati No.3','Dompet','approved','Admin','2025-08-23 19:40:52'),(2,'HIL-20250824034520','7302010101011007','Rahmat Hidayat','Laki-laki','Bone','1980-11-18','Dusun Lestari, RT 02/RW 01, Desa Gattareng Toa, Kec. Marioriwawo, Soppeng, Sulawesi Selatan','Ijazah SMK','approved','User','2025-08-23 19:45:20'),(3,'HIL-20250824082704','7302010101011005','Andi Firman','Laki-laki','Soppeng','2000-07-25','Dusun Lestari, RT 02/RW 01, Desa Gattareng Toa, Kec. Marioriwawo, Soppeng, Sulawesi Selatan','Dompet','approved','User','2025-08-24 00:27:04');
/*!40000 ALTER TABLE `hilang` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kartu_keluarga`
--

DROP TABLE IF EXISTS `kartu_keluarga`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kartu_keluarga` (
  `id` int NOT NULL AUTO_INCREMENT,
  `no_kk` varchar(20) NOT NULL,
  `dusun` varchar(100) DEFAULT NULL,
  `rt` varchar(5) DEFAULT NULL,
  `rw` varchar(5) DEFAULT NULL,
  `desa` varchar(100) DEFAULT NULL,
  `kecamatan` varchar(100) DEFAULT NULL,
  `kabupaten` varchar(100) DEFAULT NULL,
  `provinsi` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no_kk` (`no_kk`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kartu_keluarga`
--

LOCK TABLES `kartu_keluarga` WRITE;
/*!40000 ALTER TABLE `kartu_keluarga` DISABLE KEYS */;
INSERT INTO `kartu_keluarga` VALUES (1,'7304041234567890','Gattareng Toa','01','01','Gattareng Toa','Marioriawa','Soppeng ','Sulawesi Selatan'),(2,'7302010100010001','Dusun Makmur','01','01','Gattareng Toa','Marioriwawo','Soppeng','Sulawesi Selatan'),(3,'7302010100010002','Dusun Makmur','01','01','Gattareng Toa','Marioriwawo','Soppeng','Sulawesi Selatan'),(4,'7302010100010003','Dusun Lestari','02','01','Gattareng Toa','Marioriwawo','Soppeng','Sulawesi Selatan'),(5,'7302010100010004','Dusun Lestari','02','01','Gattareng Toa','Marioriwawo','Soppeng','Sulawesi Selatan'),(6,'7302010100010005','Dusun Baru','03','02','Gattareng Toa','Marioriwawo','Soppeng','Sulawesi Selatan'),(7,'7302010100010006','Dusun Baru','03','02','Gattareng Toa','Marioriwawo','Soppeng','Sulawesi Selatan'),(8,'7302010100010007','Dusun Damai','04','02','Gattareng Toa','Marioriwawo','Soppeng','Sulawesi Selatan'),(9,'7302010100010008','Dusun Damai','04','02','Gattareng Toa','Marioriwawo','Soppeng','Sulawesi Selatan'),(10,'7302010100010009','Dusun Sentosa','05','03','Gattareng Toa','Marioriwawo','Soppeng','Sulawesi Selatan'),(11,'7302010100010010','Dusun Sentosa','05','03','Gattareng Toa','Marioriwawo','Soppeng','Sulawesi Selatan');
/*!40000 ALTER TABLE `kartu_keluarga` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kelahiran`
--

DROP TABLE IF EXISTS `kelahiran`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kelahiran` (
  `id` int NOT NULL AUTO_INCREMENT,
  `no_kelahiran` varchar(30) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `tempat_lahir` varchar(100) DEFAULT NULL,
  `tanggal_lahir` date DEFAULT NULL,
  `berat` varchar(10) DEFAULT NULL,
  `jenis_kelamin` enum('L','P') DEFAULT NULL,
  `nama_ayah` varchar(100) DEFAULT NULL,
  `nama_ibu` varchar(100) DEFAULT NULL,
  `alamat` text,
  `pelapor` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no_kelahiran` (`no_kelahiran`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kelahiran`
--

LOCK TABLES `kelahiran` WRITE;
/*!40000 ALTER TABLE `kelahiran` DISABLE KEYS */;
INSERT INTO `kelahiran` VALUES (1,'KLH-20250719-001','Syahrul Ramadhan','Gattareng','2000-06-12','300','L','Syahrul','Siti','Gattareng','Syahril','2025-07-19 13:07:04');
/*!40000 ALTER TABLE `kelahiran` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kematian`
--

DROP TABLE IF EXISTS `kematian`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kematian` (
  `id` int NOT NULL AUTO_INCREMENT,
  `no_kematian` varchar(30) NOT NULL,
  `nik` varchar(20) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `tanggal_lahir` date DEFAULT NULL,
  `tanggal_meninggal` date NOT NULL,
  `tempat_meninggal` varchar(100) DEFAULT NULL,
  `umur` varchar(100) DEFAULT NULL,
  `sebab` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `tempat_makam` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `pelapor` varchar(100) DEFAULT NULL,
  `hubungan_pelapor` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no_kematian` (`no_kematian`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kematian`
--

LOCK TABLES `kematian` WRITE;
/*!40000 ALTER TABLE `kematian` DISABLE KEYS */;
INSERT INTO `kematian` VALUES (1,'KM-20250720-001','7304040505000001','Andi Sitti Aminah','2005-05-05','2025-07-20','Soppeng',NULL,'Usia',NULL,'2025-07-19 19:21:43','Syahrul Ramadhan','Keluarga');
/*!40000 ALTER TABLE `kematian` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kepindahan`
--

DROP TABLE IF EXISTS `kepindahan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kepindahan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `no_pindah` varchar(30) NOT NULL,
  `nik` varchar(20) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `tanggal_pindah` date NOT NULL,
  `keterangan` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kepindahan`
--

LOCK TABLES `kepindahan` WRITE;
/*!40000 ALTER TABLE `kepindahan` DISABLE KEYS */;
INSERT INTO `kepindahan` VALUES (1,'KP-20250720-001','7304040505000001','Andi Sitti Aminah','2025-07-20','Ingin ikut bersama suami','2025-07-20 11:10:56');
/*!40000 ALTER TABLE `kepindahan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `keramaian`
--

DROP TABLE IF EXISTS `keramaian`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `keramaian` (
  `id` int NOT NULL AUTO_INCREMENT,
  `no_surat` varchar(50) NOT NULL,
  `nik` varchar(20) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `umur` int DEFAULT NULL,
  `pekerjaan` varchar(100) DEFAULT NULL,
  `alamat` text,
  `kegiatan` varchar(200) DEFAULT NULL,
  `tanggal_acara` date DEFAULT NULL,
  `tempat` varchar(150) DEFAULT NULL,
  `dusun` varchar(100) DEFAULT NULL,
  `status` enum('pending','approved') DEFAULT 'pending',
  `pembuat_surat` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no_surat` (`no_surat`),
  KEY `fk_keramaian_penduduk` (`nik`),
  CONSTRAINT `fk_keramaian_penduduk` FOREIGN KEY (`nik`) REFERENCES `penduduk` (`nik`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `keramaian`
--

LOCK TABLES `keramaian` WRITE;
/*!40000 ALTER TABLE `keramaian` DISABLE KEYS */;
INSERT INTO `keramaian` VALUES (1,'KRM-20250824041000','7302010101011008','Dewi Sartika',41,'Bidan','Jl. Mawar No.4','Akikah','2025-08-24','di rumah','gattareng','approved','Admin','2025-08-23 20:10:00'),(2,'KRM-20250824041500','7302010101011009','Ilham Pratama',29,'Sopir','Dusun Baru, RT 03/RW 02, Desa Gattareng Toa, Kec. Marioriwawo, Soppeng, Sulawesi Selatan','Resepsi Pernikahan','2025-08-24','Gattareng Toa','Gattareng Toa','approved','User','2025-08-23 20:15:00');
/*!40000 ALTER TABLE `keramaian` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kunjungan`
--

DROP TABLE IF EXISTS `kunjungan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kunjungan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tanggal` date NOT NULL,
  `ip_address` varchar(45) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kunjungan`
--

LOCK TABLES `kunjungan` WRITE;
/*!40000 ALTER TABLE `kunjungan` DISABLE KEYS */;
INSERT INTO `kunjungan` VALUES (1,'2025-07-21','127.0.0.1','2025-07-21 12:28:11'),(2,'2025-07-22','127.0.0.1','2025-07-22 03:11:31'),(3,'2025-07-23','127.0.0.1','2025-07-22 16:01:43'),(4,'2025-07-24','127.0.0.1','2025-07-24 11:58:17'),(5,'2025-07-25','127.0.0.1','2025-07-25 02:37:34'),(6,'2025-07-26','127.0.0.1','2025-07-26 01:53:09'),(7,'2025-07-27','127.0.0.1','2025-07-27 02:53:41'),(8,'2025-07-28','127.0.0.1','2025-07-27 17:15:03'),(9,'2025-07-29','127.0.0.1','2025-07-28 16:36:56'),(10,'2025-07-30','127.0.0.1','2025-07-30 02:56:59'),(11,'2025-08-22','127.0.0.1','2025-08-22 09:39:39'),(12,'2025-08-24','127.0.0.1','2025-08-23 19:07:35'),(13,'2025-08-31','127.0.0.1','2025-08-31 11:57:23');
/*!40000 ALTER TABLE `kunjungan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pendatang`
--

DROP TABLE IF EXISTS `pendatang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pendatang` (
  `id` int NOT NULL AUTO_INCREMENT,
  `no_kedatangan` varchar(30) NOT NULL,
  `nik` varchar(20) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `tanggal_datang` date NOT NULL,
  `asal` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pendatang`
--

LOCK TABLES `pendatang` WRITE;
/*!40000 ALTER TABLE `pendatang` DISABLE KEYS */;
INSERT INTO `pendatang` VALUES (1,'PD-20250720-001','7304040505000001','Andi Sitti Aminah','2025-07-20','Sinjai','2025-07-20 11:20:33');
/*!40000 ALTER TABLE `pendatang` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `penduduk`
--

DROP TABLE IF EXISTS `penduduk`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `penduduk` (
  `id` int NOT NULL AUTO_INCREMENT,
  `no_kk` varchar(20) DEFAULT NULL,
  `nik` varchar(20) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `alamat` varchar(100) DEFAULT NULL,
  `jenis_kelamin` enum('L','P') NOT NULL,
  `tempat_lahir` varchar(100) DEFAULT NULL,
  `tanggal_lahir` date DEFAULT NULL,
  `agama` varchar(50) DEFAULT NULL,
  `pendidikan` varchar(50) DEFAULT NULL,
  `pekerjaan` varchar(100) DEFAULT NULL,
  `status_kawin` varchar(50) DEFAULT NULL,
  `kewarganegaraan` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nik` (`nik`),
  KEY `no_kk` (`no_kk`),
  CONSTRAINT `penduduk_ibfk_1` FOREIGN KEY (`no_kk`) REFERENCES `kartu_keluarga` (`no_kk`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `penduduk`
--

LOCK TABLES `penduduk` WRITE;
/*!40000 ALTER TABLE `penduduk` DISABLE KEYS */;
INSERT INTO `penduduk` VALUES (1,'7304041234567890','7304040505000001','Andi Sitti Aminah','Gattareng Toa','P','Soppeng','2005-05-05','Islam','SMA','Pelajar','Belum Kawin','Indonesia'),(2,'7302010100010001','7302010101011001','Ahmad Saputra','Jl. Merpati No.1','L','Soppeng','1995-06-12','Islam','SMA','Petani','Belum Kawin','WNI'),(3,'7302010100010001','7302010101011002','Siti Aminah','Jl. Merpati No.1','P','Soppeng','1998-01-20','Islam','S1','Ibu Rumah Tangga','Kawin','WNI'),(4,'7302010100010002','7302010101011003','Budi Setiawan','Jl. Anggrek No.2','L','Makassar','1988-09-30','Islam','SMA','Buruh','Kawin','WNI'),(5,'7302010100010002','7302010101011004','Sri Wahyuni','Jl. Anggrek No.2','P','Makassar','1990-02-15','Islam','D3','Guru','Kawin','WNI'),(6,'7302010100010003','7302010101011005','Andi Firman','Jl. Melati No.3','L','Soppeng','2000-07-25','Islam','S1','Mahasiswa','Belum Kawin','WNI'),(7,'7302010100010003','7302010101011006','Nur Aisyah','Jl. Melati No.3','P','Soppeng','2002-04-10','Islam','SMA','Pelajar','Belum Kawin','WNI'),(8,'7302010100010004','7302010101011007','Rahmat Hidayat','Jl. Mawar No.4','L','Bone','1980-11-18','Islam','SMA','Wiraswasta','Kawin','WNI'),(9,'7302010100010004','7302010101011008','Dewi Sartika','Jl. Mawar No.4','P','Bone','1983-12-30','Islam','S1','Bidan','Kawin','WNI'),(10,'7302010100010005','7302010101011009','Ilham Pratama','Jl. Dahlia No.5','L','Soppeng','1996-03-05','Islam','SMA','Sopir','Kawin','WNI'),(11,'7302010100010006','7302010101011010','Lisa Marlina','Jl. Dahlia No.6','P','Soppeng','1994-10-21','Islam','S1','Sekretaris','Kawin','WNI'),(12,'7302010100010007','7302010101011011','Herman Putra','Jl. Cendana No.7','L','Soppeng','1999-08-08','Islam','SMA','Montir','Belum Kawin','WNI'),(13,'7302010100010008','7302010101011012','Wulan Dari','Jl. Cendana No.8','P','Soppeng','2001-12-12','Islam','SMA','Kasir','Belum Kawin','WNI'),(14,'7302010100010009','7302010101011013','M. Ikbal','Jl. Kenanga No.9','L','Soppeng','1985-05-14','Islam','SMA','Nelayan','Kawin','WNI'),(15,'7302010100010009','7302010101011014','Fatmawati','Jl. Kenanga No.9','P','Soppeng','1987-08-19','Islam','SMA','Pedagang','Kawin','WNI'),(16,'7302010100010010','7302010101011015','Rudi Hartono','Jl. Flamboyan No.10','L','Soppeng','1992-02-02','Islam','SMA','Satpam','Kawin','WNI'),(17,'7302010100010010','7302010101011016','Nina Kartika','Jl. Flamboyan No.10','P','Soppeng','1993-06-17','Islam','SMA','Ibu Rumah Tangga','Kawin','WNI'),(18,'7302010100010001','7302010101011017','Putri Aulia','Jl. Merpati No.1','P','Soppeng','2012-09-01','Islam','SD','Pelajar','Belum Kawin','WNI'),(19,'7302010100010002','7302010101011018','Rian Maulana','Jl. Anggrek No.2','L','Makassar','2010-03-03','Islam','SD','Pelajar','Belum Kawin','WNI'),(20,'7302010100010003','7302010101011019','Almira Zahra','Jl. Melati No.3','P','Soppeng','2008-07-14','Islam','SMP','Pelajar','Belum Kawin','WNI'),(21,'7302010100010004','7302010101011020','Zulkifli','Jl. Mawar No.4','L','Bone','1975-01-09','Islam','SMA','Petani','Kawin','WNI');
/*!40000 ALTER TABLE `penduduk` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `potensi_desa`
--

DROP TABLE IF EXISTS `potensi_desa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `potensi_desa` (
  `id` int NOT NULL AUTO_INCREMENT,
  `judul` varchar(255) DEFAULT NULL,
  `tanggal` date DEFAULT NULL,
  `penulis` varchar(100) DEFAULT NULL,
  `dilihat` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `potensi_desa`
--

LOCK TABLES `potensi_desa` WRITE;
/*!40000 ALTER TABLE `potensi_desa` DISABLE KEYS */;
INSERT INTO `potensi_desa` VALUES (3,'Pariwisata','2025-07-23','Administrator',0),(4,'Sawah','2025-07-26','Administrator',0);
/*!40000 ALTER TABLE `potensi_desa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `s_cerai`
--

DROP TABLE IF EXISTS `s_cerai`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `s_cerai` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `no_surat` varchar(80) NOT NULL,
  `nik` varchar(20) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `tempat_lahir` varchar(50) DEFAULT NULL,
  `tanggal_lahir` date DEFAULT NULL,
  `jenis_kelamin` enum('L','P') DEFAULT NULL,
  `pekerjaan` varchar(100) DEFAULT NULL,
  `agama` varchar(50) DEFAULT NULL,
  `alamat` text,
  `nama_pasangan` varchar(100) NOT NULL,
  `tahun_cerai` year NOT NULL,
  `status` enum('pending','approved') DEFAULT 'pending',
  `pembuat_surat` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_no_surat` (`no_surat`),
  KEY `idx_nik` (`nik`),
  CONSTRAINT `fk_scerai_penduduk` FOREIGN KEY (`nik`) REFERENCES `penduduk` (`nik`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `s_cerai`
--

LOCK TABLES `s_cerai` WRITE;
/*!40000 ALTER TABLE `s_cerai` DISABLE KEYS */;
INSERT INTO `s_cerai` VALUES (1,'SCR-20250831202517','7302010101011001','Ahmad Saputra','Soppeng','1995-06-12','L','Petani','Islam','Jl. Merpati No.1','Rsma',2022,'approved','Admin','2025-08-31 12:25:17'),(2,'SCR-20250831203833','7302010101011003','Budi Setiawan','Makassar','1988-09-30','L','Buruh','Islam','Dusun Makmur, RT 01/RW 01, Desa Gattareng Toa, Kec. Marioriwawo, Soppeng, Sulawesi Selatan','Ibu Suriani',2021,'pending','User','2025-08-31 12:38:33');
/*!40000 ALTER TABLE `s_cerai` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `s_izin_potong`
--

DROP TABLE IF EXISTS `s_izin_potong`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `s_izin_potong` (
  `id` int NOT NULL AUTO_INCREMENT,
  `no_surat` varchar(80) NOT NULL,
  `nik` varchar(20) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `tempat_lahir` varchar(50) DEFAULT NULL,
  `tanggal_lahir` date DEFAULT NULL,
  `jenis_kelamin` enum('L','P') DEFAULT NULL,
  `pekerjaan` varchar(100) DEFAULT NULL,
  `alamat` text,
  `jenis_hewan` varchar(50) NOT NULL,
  `jumlah_ekor` int NOT NULL,
  `umur_hewan` int DEFAULT NULL,
  `tanggal_potong` date NOT NULL,
  `acara` varchar(100) NOT NULL,
  `nama_anak` varchar(100) DEFAULT NULL,
  `tempat_acara` varchar(150) DEFAULT NULL,
  `status` enum('pending','approved') DEFAULT 'pending',
  `pembuat_surat` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no_surat` (`no_surat`),
  KEY `idx_nik` (`nik`),
  CONSTRAINT `fk_izin_potong_penduduk` FOREIGN KEY (`nik`) REFERENCES `penduduk` (`nik`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `s_izin_potong`
--

LOCK TABLES `s_izin_potong` WRITE;
/*!40000 ALTER TABLE `s_izin_potong` DISABLE KEYS */;
INSERT INTO `s_izin_potong` VALUES (1,'SIP-20250831205241','7302010101011003','Budi Setiawan','Makassar','1988-09-30','L','Buruh','Jl. Anggrek No.2','Sapi',1,2,'2025-08-31','Akikah','Levi junior','Gattareng','approved','Admin','2025-08-31 12:52:41');
/*!40000 ALTER TABLE `s_izin_potong` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `s_kematian`
--

DROP TABLE IF EXISTS `s_kematian`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `s_kematian` (
  `id` int NOT NULL AUTO_INCREMENT,
  `no_surat` varchar(80) NOT NULL,
  `nik` varchar(20) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `tempat_lahir` varchar(50) DEFAULT NULL,
  `tanggal_lahir` date DEFAULT NULL,
  `jenis_kelamin` enum('L','P') DEFAULT NULL,
  `alamat` text,
  `tanggal_meninggal` date NOT NULL,
  `tempat_meninggal` varchar(150) NOT NULL,
  `status` enum('pending','approved') DEFAULT 'pending',
  `pembuat_surat` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no_surat` (`no_surat`),
  KEY `idx_nik` (`nik`),
  CONSTRAINT `fk_skematian_penduduk` FOREIGN KEY (`nik`) REFERENCES `penduduk` (`nik`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `s_kematian`
--

LOCK TABLES `s_kematian` WRITE;
/*!40000 ALTER TABLE `s_kematian` DISABLE KEYS */;
INSERT INTO `s_kematian` VALUES (1,'SKK-20250831211328','7302010101011004','Sri Wahyuni','Makassar','1990-02-15','P','Jl. Anggrek No.2','2025-08-31','Gattareng`','approved','Admin','2025-08-31 13:13:28');
/*!40000 ALTER TABLE `s_kematian` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `s_kurang_mampu`
--

DROP TABLE IF EXISTS `s_kurang_mampu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `s_kurang_mampu` (
  `id` int NOT NULL AUTO_INCREMENT,
  `no_surat` varchar(80) NOT NULL,
  `nik` varchar(20) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `tempat_lahir` varchar(50) DEFAULT NULL,
  `tanggal_lahir` date DEFAULT NULL,
  `pekerjaan` varchar(100) DEFAULT NULL,
  `alamat` text,
  `status` enum('pending','approved') DEFAULT 'pending',
  `pembuat_surat` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no_surat` (`no_surat`),
  KEY `fk_skm_penduduk` (`nik`),
  CONSTRAINT `fk_skm_penduduk` FOREIGN KEY (`nik`) REFERENCES `penduduk` (`nik`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `s_kurang_mampu`
--

LOCK TABLES `s_kurang_mampu` WRITE;
/*!40000 ALTER TABLE `s_kurang_mampu` DISABLE KEYS */;
INSERT INTO `s_kurang_mampu` VALUES (1,'SKM-20250824042236','7302010101011006','Nur Aisyah','Soppeng','2002-04-10','Pelajar','Jl. Melati No.3','approved','Admin','2025-08-23 20:22:36'),(2,'SKM-20250824042656','7302010101011005','Andi Firman','Soppeng','2000-07-25','Mahasiswa','Dusun Lestari, RT 02/RW 01, Desa Gattareng Toa, Kec. Marioriwawo, Soppeng, Sulawesi Selatan','approved','User','2025-08-23 20:26:56');
/*!40000 ALTER TABLE `s_kurang_mampu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `s_merantau`
--

DROP TABLE IF EXISTS `s_merantau`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `s_merantau` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `no_surat` varchar(80) NOT NULL,
  `nik` varchar(20) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `tempat_lahir` varchar(50) DEFAULT NULL,
  `tanggal_lahir` date DEFAULT NULL,
  `pekerjaan` varchar(100) DEFAULT NULL,
  `alamat` text,
  `nama_pasangan` varchar(100) NOT NULL,
  `tujuan_merantau` varchar(150) NOT NULL,
  `status` enum('pending','approved') DEFAULT 'pending',
  `pembuat_surat` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_s_merantau_no_surat` (`no_surat`),
  KEY `idx_s_merantau_nik` (`nik`),
  CONSTRAINT `fk_smerantau_penduduk` FOREIGN KEY (`nik`) REFERENCES `penduduk` (`nik`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `s_merantau`
--

LOCK TABLES `s_merantau` WRITE;
/*!40000 ALTER TABLE `s_merantau` DISABLE KEYS */;
INSERT INTO `s_merantau` VALUES (1,'SMR-20250831200910','7302010101011001','Ahmad Saputra','Soppeng','1995-06-12','Petani','Jl. Merpati No.1','Ibu Mastang','Samarinda','approved','Admin','2025-08-31 12:09:10'),(2,'SMR-20250831201247','7302010101011003','Budi Setiawan','Makassar','1988-09-30','Buruh','Dusun Makmur, RT 01/RW 01, Desa Gattareng Toa, Kec. Marioriwawo, Soppeng, Sulawesi Selatan','Ibu Suriani','Koreiha','approved','User','2025-08-31 12:12:47');
/*!40000 ALTER TABLE `s_merantau` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `s_penguburan`
--

DROP TABLE IF EXISTS `s_penguburan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `s_penguburan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `no_surat` varchar(80) NOT NULL,
  `nik` varchar(20) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `tempat_lahir` varchar(50) DEFAULT NULL,
  `tanggal_lahir` date DEFAULT NULL,
  `jenis_kelamin` enum('L','P') DEFAULT NULL,
  `alamat` text,
  `hari_meninggal` varchar(20) DEFAULT NULL,
  `jam_meninggal` time DEFAULT NULL,
  `hari_penguburan` varchar(20) DEFAULT NULL,
  `tanggal_penguburan` date DEFAULT NULL,
  `lokasi_penguburan` varchar(150) DEFAULT NULL,
  `jam_penguburan` time DEFAULT NULL,
  `status` enum('pending','approved') DEFAULT 'pending',
  `pembuat_surat` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no_surat` (`no_surat`),
  KEY `fk_spenguburan_penduduk` (`nik`),
  CONSTRAINT `fk_spenguburan_penduduk` FOREIGN KEY (`nik`) REFERENCES `penduduk` (`nik`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `s_penguburan`
--

LOCK TABLES `s_penguburan` WRITE;
/*!40000 ALTER TABLE `s_penguburan` DISABLE KEYS */;
INSERT INTO `s_penguburan` VALUES (1,'SPG-20250831214009','7302010101011003','Budi Setiawan','Makassar','1988-09-30','L','Jl. Anggrek No.2','Senin','21:39:00','selasa','2025-08-31','Jalan Gattareng','13:40:00','approved','Admin','2025-08-31 13:40:09'),(2,'SPG-20250831215112','7302010101011001','Ahmad Saputra','Soppeng','1995-06-12','L','Dusun Makmur, RT 01/RW 01, Desa Gattareng Toa, Kec. Marioriwawo, Soppeng, Sulawesi Selatan','Minggu','21:48:00','Senin','2025-09-01','Gattareng','21:48:00','approved','User','2025-08-31 13:51:12');
/*!40000 ALTER TABLE `s_penguburan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sktm`
--

DROP TABLE IF EXISTS `sktm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sktm` (
  `id` int NOT NULL AUTO_INCREMENT,
  `no_surat` varchar(100) NOT NULL,
  `no_kk` varchar(50) NOT NULL,
  `nik` varchar(20) NOT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `jenis_kelamin` enum('L','P') DEFAULT NULL,
  `tempat_lahir` varchar(100) DEFAULT NULL,
  `tanggal_lahir` date DEFAULT NULL,
  `alamat` text,
  `keperluan` varchar(255) DEFAULT NULL,
  `status` enum('pending','approved') DEFAULT 'pending',
  `pembuat_surat` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sktm`
--

LOCK TABLES `sktm` WRITE;
/*!40000 ALTER TABLE `sktm` DISABLE KEYS */;
INSERT INTO `sktm` VALUES (1,'SKTM-20250729015423','7302010100010001','7302010101011001','Ahmad Saputra','L','Soppeng','1995-06-12','Jl. Merpati No.1','Mengurus KIP Kuliah','approved','Admin','2025-07-28 17:54:23'),(2,'SKTM-20250729023404','7302010100010001','7302010101011001','Ahmad Saputra',NULL,NULL,NULL,'Dusun Makmur, RT 01/RW 01, Desa Gattareng Toa, Kec. Marioriwawo, Soppeng, Sulawesi Selatan','KIP KUliah ','approved','User','2025-07-28 18:34:04'),(3,'SKTM-20250729030408','7302010100010001','7302010101011001','Ahmad Saputra',NULL,NULL,NULL,'Dusun Makmur, RT 01/RW 01, Desa Gattareng Toa, Kec. Marioriwawo, Soppeng, Sulawesi Selatan','KIP KUliah ','approved','User','2025-07-28 19:04:08'),(4,'SKTM-20250729090116','7304041234567890','7304040505000001','Andi Sitti Aminah','P','Soppeng','2005-05-05','Gattareng Toa','KIPP Kuliah','pending','Admin','2025-07-29 01:01:16'),(5,'SKTM-20250730132642','7304041234567890','7304040505000001','Andi Sitti Aminah',NULL,NULL,NULL,'Gattareng Toa, RT 01/RW 01, Desa Gattareng Toa, Kec. Marioriawa, Soppeng , Sulawesi Selatan','Surat Keterangan Jujur','approved','User','2025-07-30 05:26:42');
/*!40000 ALTER TABLE `sktm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sku`
--

DROP TABLE IF EXISTS `sku`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sku` (
  `id` int NOT NULL AUTO_INCREMENT,
  `no_surat` varchar(80) NOT NULL,
  `nik` varchar(20) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `tempat_lahir` varchar(50) DEFAULT NULL,
  `tanggal_lahir` date DEFAULT NULL,
  `pekerjaan` varchar(100) DEFAULT NULL,
  `alamat` text,
  `nama_usaha` varchar(150) DEFAULT NULL,
  `tempat_usaha` varchar(150) DEFAULT NULL,
  `dusun` varchar(100) DEFAULT NULL,
  `status` enum('pending','approved') DEFAULT 'pending',
  `pembuat_surat` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `no_surat` (`no_surat`),
  KEY `fk_sku_penduduk` (`nik`),
  CONSTRAINT `fk_sku_penduduk` FOREIGN KEY (`nik`) REFERENCES `penduduk` (`nik`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sku`
--

LOCK TABLES `sku` WRITE;
/*!40000 ALTER TABLE `sku` DISABLE KEYS */;
INSERT INTO `sku` VALUES (1,'SKU-20250824043353','7302010101011008','Dewi Sartika','Bone','1983-12-30','Bidan','Jl. Mawar No.4','Usaha Warung Coto','Gattareng Toa','Gattareng Toa','approved','Admin','2025-08-23 20:33:53'),(2,'SKU-20250824043611','7304040505000001','Andi Sitti Aminah','Soppeng','2005-05-05','Pelajar','Gattareng Toa, RT 01/RW 01, Desa Gattareng Toa, Kec. Marioriawa, Soppeng , Sulawesi Selatan','Usaha Warung Bakso','Gattareng','Gattareng Toa','approved','User','2025-08-23 20:36:11');
/*!40000 ALTER TABLE `sku` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sub_potensi`
--

DROP TABLE IF EXISTS `sub_potensi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sub_potensi` (
  `id` int NOT NULL AUTO_INCREMENT,
  `potensi_id` int DEFAULT NULL,
  `sub_judul` varchar(255) DEFAULT NULL,
  `deskripsi` text,
  PRIMARY KEY (`id`),
  KEY `potensi_id` (`potensi_id`),
  CONSTRAINT `sub_potensi_ibfk_1` FOREIGN KEY (`potensi_id`) REFERENCES `potensi_desa` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sub_potensi`
--

LOCK TABLES `sub_potensi` WRITE;
/*!40000 ALTER TABLE `sub_potensi` DISABLE KEYS */;
INSERT INTO `sub_potensi` VALUES (3,3,'Wisata Lereng Hijau Bulu Dua','Lereng Hijau Bulu Dua adalah destinasi wisata yang menawarkan pemandangan alam yang memukau dan fasilitas yang lengkap. Pengunjung dapat menikmati kolam renang yang sejuk, air terjun, dan pemandangan pegunungan yang indah. Di sini, pengunjung juga dapat menikmati pemandian yang menyegarkan dan berbagai fasilitas lainnya yang memanjakan mata dan menenangkan.'),(4,4,'Penghasil Beras terbaik','Desa Gattareng Toa adalah desa yang memiliiki sumber penghasil beras yang terbaik di kabupaten soppeng'),(5,4,'Beras Desa Gattareng ','Beras Yang bagus');
/*!40000 ALTER TABLE `sub_potensi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nik` varchar(20) NOT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `no_hp` varchar(15) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `level` enum('admin','operator','warga') DEFAULT 'warga',
  PRIMARY KEY (`id`),
  UNIQUE KEY `nik` (`nik`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'1234567890123456','Admin Desa','admin@desa.id','081234567890','admin123','admin');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'simdes_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-31 21:52:50
