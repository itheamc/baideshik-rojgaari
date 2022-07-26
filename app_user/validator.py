import re


class Validators:

    # Method to validate if a string is a valid email
    @staticmethod
    def validate_email(email):
        if len(email) > 7:
            if re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email) is not None:
                return True
        return False

    # Method to validate password
    @staticmethod
    def validate_password(password):
        if len(password) > 7:
            return True
        return False

    # Method to validate if the phone number is valid
    @staticmethod
    def validate_phone(phone):
        if len(phone) == 10:
            if re.match("^[0-9]+$", phone) is not None:
                return True
        return False

    @staticmethod
    def validate_otp(otp):
        if type(otp) == int:
            return len(str(otp)) == 6
        return re.match("^[0-9]+$", otp) is not None and len(otp) == 6
