USE movie_ticketing;


CREATE TABLE `users` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,    
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE TABLE `movies` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL DEFAULT '',
  `genre` varchar(255) NOT NULL DEFAULT '',
  `release_date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE TABLE `bookings` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `movie_id` int NOT NULL,
  `num_tickets` int NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
  FOREIGN KEY (`movie_id`) REFERENCES `movies`(`id`)
) ENGINE=InnoDB;

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
-- view bookings
CREATE VIEW view_bookings AS
    SELECT bookings.*, movies.title AS movie_title
    FROM bookings
    JOIN movies ON bookings.movie_id = movies.id;

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