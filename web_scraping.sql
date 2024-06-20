CREATE DATABASE IF NOT EXISTS web_scraping;

USE web_scraping;

CREATE TABLE IF NOT EXISTS website_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255),
    social_media_links JSON,
    tech_stack JSON,
    meta_title VARCHAR(255),
    meta_description TEXT,
    payment_gateways JSON,
    website_language VARCHAR(50),
    category VARCHAR(50)
);

-- Drop the view if it exists before creating it to avoid conflicts
DROP VIEW IF EXISTS basic_info;

-- Create a view to display basic website info
CREATE VIEW basic_info AS
SELECT id, url, meta_title, meta_description, website_language, category
FROM website_info;

-- Drop the procedure if it exists before creating it to avoid conflicts
DROP PROCEDURE IF EXISTS AddWebsiteInfo;

-- Create a stored procedure to add a new website info
DELIMITER //

CREATE PROCEDURE AddWebsiteInfo (
    IN url VARCHAR(255),
    IN social_media_links JSON,
    IN tech_stack JSON,
    IN meta_title VARCHAR(255),
    IN meta_description TEXT,
    IN payment_gateways JSON,
    IN website_language VARCHAR(50),
    IN category VARCHAR(50)
)
BEGIN
    INSERT INTO website_info (url, social_media_links, tech_stack, meta_title, meta_description, payment_gateways, website_language, category)
    VALUES (url, social_media_links, tech_stack, meta_title, meta_description, payment_gateways, website_language, category);
END //

DELIMITER ;


-- Drop the function if it exists before creating it to avoid conflicts
DROP FUNCTION IF EXISTS GetWebsiteInfoByUrl;

-- Create a function to retrieve website info by URL
DELIMITER //

CREATE FUNCTION GetWebsiteInfoByUrl(target_url VARCHAR(255))
RETURNS JSON
READS SQL DATA
BEGIN
    DECLARE result JSON;
    SET result = (
        SELECT JSON_OBJECT(
            'id', id,
            'url', url,
            'social_media_links', social_media_links,
            'tech_stack', tech_stack,
            'meta_title', meta_title,
            'meta_description', meta_description,
            'payment_gateways', payment_gateways,
            'website_language', website_language,
            'category', category
        )
        FROM website_info
        WHERE url = target_url
    );
    RETURN result;
END //

DELIMITER ;

SELECT * FROM website_info;