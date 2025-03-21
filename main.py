import pyodbc
import pprint

connection = pyodbc.connect(
    'DRIVER={SQL Server};'
    'Server=LAPTOP-5B8TNS55;'
    'Database=project_1;'
    'trusted_Connection=yes;',
    timeout=60
)

cursor = connection.cursor()


# Foydalanuvchilarni boshqarish
class ManageUsers:
    @staticmethod
    def get_users():
        return 'select * from users'

    @staticmethod
    def get_active_users():
        return """select * from get_active_users"""

    @staticmethod
    def check_balance(user_id):
        return f'''select id,name,email,status,total_balance from users where id = '{user_id}' '''

    def manage_user_cards(self):
        pass


# Tranzaksiya boshqaruvi

class ControlTransactions:
    # Kartadan kartaga pul o‘tkazmalar
    @staticmethod
    def transfer_to_card():
        pass

    # Kunlik, haftalik tranzaksiyalarni ko‘rish
    @staticmethod
    def get_transactions(var: str):
        day = 1
        week = 7
        if var == 'day':
            return f'''select s1.id,s1.from_card_id,s1.to_card_id,amount,s1.status,s1.created_at,transaction_type from transactions s1
where s1.created_at between DATEADD(DAY,-{day},s1.created_at) and GETDATE()'''
        else:
            return f'''select s1.id,s1.from_card_id,s1.to_card_id,amount,s1.status,s1.created_at,transaction_type from transactions s1
where s1.created_at between DATEADD(DAY,-{week},s1.created_at) and GETDATE()'''

    # Yirik tranzaksiyalarni avtomatik tekshirish
    @staticmethod
    def check_transaction():
        pass

    # Pul yechish va depozit qilish
    @staticmethod
    def withdraw_deposit():
        inp = input('withdraw / deposit (w/d): ').lower().strip()
        # for deposit
        if inp == 'd':
            card_number = input('Enter your card number (without space): ').strip()
            user_name = input('Enter your name: ').strip()

            query = "SELECT s2.id FROM users s1 JOIN cards s2 ON s1.id = s2.user_id WHERE s1.name = ? AND s2.card_number = ?"
            cursor.execute(query, (user_name, card_number))
            result = cursor.fetchone()

            if result:
                id_user = result[0]

                amount = int(input('Enter Amount: '))

                cursor.execute("SELECT balance FROM cards WHERE card_number = ?", (card_number,))
                balance = cursor.fetchone()

                if balance:
                    balance = balance[0]
                else:
                    print("Error: Card not found.")
                    return

                new_balance = balance + amount
                cursor.execute("UPDATE cards SET balance = ? WHERE card_number = ?", (new_balance, card_number))
                connection.commit()
                print("Successfully updated balance.")

                query = """INSERT INTO transactions (from_card_id, to_card_id, amount, status, transaction_type, is_flagged) 
                           VALUES (?, NULL, ?, 'pending', 'withdrawal', 0);"""
                cursor.execute(query, (id_user, amount))
                connection.commit()
                print("Transaction recorded successfully.")
            else:
                print("Error: User or card number not found.")
        # for withdraw
        pass


def print_menu():
    print("\nBank Account Management Menu:")
    print("1. Foydalanuvchilarni boshqarish")
    print("2. Tranzaksiya boshqaruvi")
    print("3. ")
    print("4. ")
    print("5. ")
    print("6. Exit")


def print_menu_ManageUsers():
    print("\nFoydalanuvchilarni boshqarish:")
    print("1. Barcha foydalanuvchilarni ko‘rish")
    print("2. So‘nggi 1 oy ichida faol bo‘lgan foydalanuvchilarni ko‘rish")
    print("3. Har bir foydalanuvchining hisob holatini tekshirish")
    print("4. Foydalanuvchi kartalarining limitini nazorat qilish")
    print("5. Ortga qaytish")


def print_menu_ManageTransactions():
    print("\nTranzaksiya boshqaruvi:")
    print("1. Kartadan kartaga pul o‘tkazmalar")
    print("2. Kunlik, haftalik tranzaksiyalarni ko‘rish")
    print("3. Yirik tranzaksiyalarni avtomatik tekshirish (150 mln so‘mdan oshsa)")
    print("4. Pul yechish va depozit qilish")
    print("5. Ortga qaytish")


while True:
    print_menu()
    command = int(input('Enter command number: '))
    if command == 1:
        while True:
            print_menu_ManageUsers()
            command = int(input('enter command number: ').capitalize())
            if command == 1:
                get_users = cursor.execute(ManageUsers.get_users())
                pprint.pp(get_users.fetchall())
            elif command == 2:
                get_active_users = cursor.execute(ManageUsers.get_active_users())
                pprint.pp(get_active_users.fetchall())
            elif command == 3:
                id = int(input('Enter user id: '))
                get_user_balance = cursor.execute(ManageUsers.check_balance(id))
                pprint.pp(get_user_balance.fetchall())
            elif command == 4:
                pass
                # 1. Foydalanuvchi kartalarining limitini nazorat qilish
            else:
                break
    elif command == 2:
        while True:
            print_menu_ManageTransactions()
            command = int(input('enter command number: ').capitalize())
            if command == 1:
                pass
                # Kartadan kartaga pul o‘tkazmalar
            elif command == 2:
                dw = input('Enter (day / week): ').strip().lower()
                get_columns = cursor.execute('''select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS
                where TABLE_NAME = 'transactions' ''')
                columns = [col[0] for col in get_columns.fetchall()]  # Ustun nomlarini olish
                print(" | ".join(columns))
                get_transactions = cursor.execute(ControlTransactions.get_transactions(dw))
                pprint.pp(get_transactions.fetchall())
            elif command == 3:
                pass
                # Yirik tranzaksiyalarni avtomatik tekshirish (150 mln so‘mdan oshsa)
            elif command == 4:
                ControlTransactions.withdraw_deposit()
                # Pul yechish va depozit qilish
            else:
                break
    else:
        break

connection.commit()

cursor.close()
connection.close()
