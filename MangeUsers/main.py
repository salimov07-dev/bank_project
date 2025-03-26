class ManageUsers:
    @staticmethod  # done
    def get_users():
        return 'select * from users'

    @staticmethod  # done
    def get_active_users():
        return """select * from get_active_users"""

    @staticmethod
    def check_balance(user_id_1):  # done
        return f'''select * from dbo.GetUserByID({user_id_1}) '''

    def manage_user_cards(self):  # in progress
        pass
