-- script that creates a trigger that resets the attribute valid_email
-- only when the email has been changed.

DELIMITER //

CREATE TRIGGER update_valid_email_on_change
BEFORE UPDATE
ON users
FOR EACH ROW
BEGIN
    -- update the valid_email value if the email had changed
    IF OLD.email != NEW.email THEN
        -- Reset the email field
        SET NEW.valid_email = 1 - OLD.valid_email;
    END IF;
END;
//

DELIMITER ;
