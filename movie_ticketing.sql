

CREATE TABLE `users` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;


CREATE TABLE movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    genre VARCHAR(255) NOT NULL,
    release_date DATE NOT NULL,
    capacity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT NOT NULL,
    booker_name VARCHAR(255) NOT NULL,
    num_tickets INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (movie_id) REFERENCES movies (id) ON DELETE CASCADE
);

DELIMITER //

CREATE TRIGGER after_booking_trigger
AFTER INSERT ON bookings FOR EACH ROW
BEGIN
    DECLARE current_capacity INT;

    -- Fetch the current capacity of the movie
    SELECT capacity INTO current_capacity FROM movies WHERE id = NEW.movie_id;

    -- Update the movie capacity after the booking
    IF current_capacity IS NOT NULL AND current_capacity >= NEW.num_tickets THEN
        UPDATE movies SET capacity = current_capacity - NEW.num_tickets WHERE id = NEW.movie_id;
    END IF;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE create_user(
    IN p_name VARCHAR(255),
    IN p_email VARCHAR(255),
    IN p_password VARCHAR(255)
)
BEGIN
    INSERT INTO users (name, email, password)
    VALUES (p_name, p_email, p_password);

    SELECT * FROM users WHERE id = LAST_INSERT_ID();
END //

DELIMITER ;

-- get users
DELIMITER //

CREATE PROCEDURE get_all_users()
BEGIN
    SELECT * FROM users;
END //

DELIMITER ;

-- get user by id
DELIMITER //

CREATE PROCEDURE get_user_by_id(
    IN p_id INT
)
BEGIN
    SELECT * FROM users WHERE id = p_id;
END //

DELIMITER ;

-- update user
DELIMITER //

CREATE PROCEDURE update_user(
    IN p_id INT,
    IN p_name VARCHAR(255),
    IN p_email VARCHAR(255),
    IN p_password VARCHAR(255)
)
BEGIN
    UPDATE users
    SET name = p_name, email = p_email, password = p_password
    WHERE id = p_id;

    SELECT * FROM users WHERE id = p_id;
END //

DELIMITER ;

-- delete user
DELIMITER //

CREATE PROCEDURE delete_user(
    IN p_id INT
)
BEGIN
    DELETE FROM users WHERE id = p_id;

    SELECT id FROM users WHERE id = p_id;
END //

DELIMITER ;

CREATE VIEW view_bookings AS
    SELECT 
        b.booking_id,
        b.movie_id,
        b.booker_name,
        b.num_tickets,
        b.total_price,
        b.booking_date,
        m.title AS movie_title
    FROM bookings b
    JOIN movies m ON b.movie_id = m.id;

        DELIMITER //

CREATE VIEW movies_with_capacity AS
    SELECT
        m.id,
        m.title,
        m.genre,
        m.release_date,
        m.capacity - COALESCE(SUM(b.num_tickets), 0) AS available_capacity
    FROM
        movies m
    LEFT JOIN
        bookings b ON m.id = b.movie_id
    GROUP BY
        m.id;