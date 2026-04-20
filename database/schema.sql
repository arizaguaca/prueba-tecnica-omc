-- Schema for Lead Management API
-- Database: prueba_tecnica

CREATE TABLE IF NOT EXISTS leads (
    id VARCHAR(36) NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    telefono VARCHAR(50),
    fuente ENUM('instagram', 'facebook', 'landing_page', 'referido', 'otro') DEFAULT 'otro',
    producto_interes VARCHAR(255),
    presupuesto FLOAT DEFAULT 0.0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    PRIMARY KEY (id),
    UNIQUE leads_email (email),
    INDEX idx_leads_fuente (fuente),
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
