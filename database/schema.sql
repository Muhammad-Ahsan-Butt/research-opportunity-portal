-- Database Schema for University Research Opportunity Portal
-- FAST-NUCES Peshawar - Computer Networks Assignment #1

CREATE DATABASE IF NOT EXISTS research_portal;
USE research_portal;

DROP TABLE IF EXISTS opportunities;

CREATE TABLE opportunities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    research_area VARCHAR(150) NOT NULL,
    faculty_name VARCHAR(150) NOT NULL,
    department VARCHAR(100) NOT NULL,
    required_skills TEXT NOT NULL,
    positions_available INT NOT NULL,
    deadline DATE NOT NULL,
    status ENUM('Open', 'Closed') NOT NULL DEFAULT 'Open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Sample Initial Data (3 Opportunities as required by testing demonstration)
INSERT INTO opportunities (
    title, description, research_area, faculty_name, department, required_skills, positions_available, deadline, status
) VALUES 
(
    'Deep Learning for Medical Image Segmentation',
    'Developing convolutional and transformer architectures for early tumor detection in MRI scans. Involves model training and evaluation on public clinical datasets.',
    'Artificial Intelligence & Healthcare',
    'Dr. Tariq Khan',
    'Computer Science',
    'Python, PyTorch, OpenCV, Data Preprocessing',
    2,
    '2026-11-30',
    'Open'
),
(
    'Secure SDN Routing Protocols for IoT Networks',
    'Analyzing flow table vulnerabilities in Software-Defined Networking (SDN) controllers and designing lightweight authentication for IoT nodes.',
    'Computer Networks & Cybersecurity',
    'Dr. Ayesha Malik',
    'Software Engineering',
    'Python, Mininet, Ryu Controller, Wireshark, Linux',
    3,
    '2026-12-15',
    'Open'
),
(
    'Edge AI Optimization for Autonomous Drones',
    'Investigating model quantization and pruning techniques to run real-time object detection models on low-power edge hardware.',
    'Embedded Systems & Computer Vision',
    'Prof. Bilal Ahmed',
    'Electrical & Computer Engineering',
    'C++, Python, ONNX, TensorRT, ROS',
    1,
    '2026-11-20',
    'Closed'
);
