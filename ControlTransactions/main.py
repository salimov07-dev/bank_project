import pyodbc
import pprint

connection = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=172.25.59.2,1433"  # Yoki kompyuter nomi
    "DATABASE=project_1;"
    "UID=project;"  # SQL Server foydalanuvchi nomi
    "PWD=qwerty123;"  # SQL Server paroli
    "TrustServerCertificate=yes;",  # Sertifikat xatolarini oldini oladi
    timeout=60
)

cursor = connection.cursor()


class ControlTransactions:
    # Kartadan kartaga pul o‘tkazmalar
    @staticmethod
    def transfer_to_card():  # salimov
        card_number = input('Enter your Card number (without space): ').strip()
        user_name = input('Enter your name: ').strip()
        to_card = input('Which card do you want to transfer money to? (card number): ').strip()

        if not card_number or not user_name:
            print("Error: Card number and name cannot be empty.")
            return

        query = "SELECT * FROM dbo.getusercard(?,?)"
        cursor.execute(query, (user_name, card_number))
        result = cursor.fetchone()

        if not result:
            print("Error: User or card number not found.")
            return

        is_blocked = '''SELECT is_blocked FROM cards WHERE id = (SELECT id FROM dbo.getusercard(?, ?))'''
        cursor.execute(is_blocked, (user_name, card_number))
        result_1 = cursor.fetchone()

        if result_1 and result_1[0] == 1:
            print('Your card is blocked')
        else:
            id_user = result[0]
            amount = int(input('Enter Amount: '))

            cursor.execute("SELECT balance FROM cards WHERE card_number = ?", (card_number,))
            balance_result = cursor.fetchone()

            if balance_result is None:
                print("Error: Your card number is not found in the database.")
                return

            balance = balance_result[0]

            if amount > balance:
                print("Error: Insufficient balance.")
                return

            cursor.execute("SELECT id FROM cards WHERE card_number = ?", (to_card,))
            to_card_result = cursor.fetchone()

            to_card_id = to_card_result[0]
            if to_card_result is None:
                transaction_type = 'transfer'
                print("Error: Destination card not found.")
                status = 'Failed'
                is_flagged = 0
                query = """ EXEC insert_into_transactions ?, ?, ?, ?, ?, ? """
                cursor.execute(query, (id_user, to_card_id, transaction_type, amount, status, is_flagged))
                return
            transaction_type = 'transfer'

            minus_query = ''' UPDATE cards SET balance = balance - ? WHERE card_number = ? '''
            plus_query = ''' UPDATE cards SET balance = balance + ? WHERE id = ? '''

            cursor.execute(minus_query, (amount, card_number))
            cursor.execute(plus_query, (amount, to_card_id))
            status = 'success'
            is_flagged = 0
            query = """ EXEC insert_into_transactions ?, ?, ?, ?, ?, ?"""
            cursor.execute(query, (id_user, to_card_id, transaction_type, amount, status, is_flagged))
            connection.commit()

            print("Transaction completed successfully.")

    # Kunlik, haftalik tranzaksiyalarni ko‘rish
    @staticmethod
    def get_transactions(var):  # salimov
        day = 1
        week = 7

        msg = 'Bir hafta ichida hech qanday tranzaktsiyalar topilmadi❗'
        query_1 = ''' select * from dbo.get_transactions(?) '''
        query_2 = ''' select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS
                                            where TABLE_NAME = 'transactions' and COLUMN_NAME != 'is_flagged'  '''
        get_columns_1 = cursor.execute(query_2)

        columns_1 = [col[0] for col in get_columns_1.fetchall()]
        columns_1 = " | ".join(columns_1)

        if var == 'day':
            user_query = cursor.execute(query_1, (day,))
        elif var == 'week':
            user_query = cursor.execute(query_1, (week,))
        else:
            return "❌ Invalid input! Please enter 'day' or 'week'."

        rows = user_query.fetchall()
        if not rows:
            return msg
        else:
            print(columns_1)
            pprint.pp(rows)

    # Yirik tranzaksiyalarni avtomatik tekshirish
    @staticmethod
    def check_transaction():
        pass

    # Pul yechish va depozit qilish
    @staticmethod
    def withdraw_deposit():  # salimov
        inp = input('withdraw / deposit (w/d): ').lower().strip()
        card_number = input('Enter your card number (without space): ').strip()
        user_name = input('Enter your name: ').strip()

        if not card_number or not user_name:
            print("Error: Card number and name cannot be empty.")
            return

        query = "SELECT * FROM dbo.getusercard(?,?)"
        cursor.execute(query, (user_name, card_number))
        result_2 = cursor.fetchone()

        if not result_2:
            print("Error: User or card number not found.")
            return

        id_user = result_2[0]
        amount = int(input('Enter Amount: '))

        cursor.execute("SELECT balance FROM cards WHERE card_number = ?", (card_number,))
        balance_result = cursor.fetchone()

        if not balance_result:
            print("Error: Card not found.")
            return

        balance = balance_result[0]

        if inp == 'd':  # Deposit
            to_card = id_user
            id_user = None
            new_balance = balance + amount
            status = 'success'
            transaction_type = 'deposit'
            is_flagged = 0
            cursor.execute("UPDATE cards SET balance = ? WHERE card_number = ?", (new_balance, card_number))
            query = """EXEC insert_into_transactions ?, ?, ?, ?, ?, ?"""
            cursor.execute(query, (id_user, to_card, transaction_type.strip(), amount, status, is_flagged))
            connection.commit()
            print("Transaction recorded successfully.")
        elif inp == 'w':  # Withdraw
            transaction_type = 'withdrawal'
            new_balance = balance - amount
            to_card = None
            status = 'success'
            is_flagged = 0
            if amount > balance:
                print("Error: Not enough balance.")
                status = 'failed'
                query = """EXEC insert_into_transactions ?, ?, ?, ?,?,?"""
                cursor.execute(query, (id_user, to_card, transaction_type, amount, status, is_flagged))
                connection.commit()
            else:
                cursor.execute("UPDATE cards SET balance = ? WHERE card_number = ?", (new_balance, card_number))
                query = """EXEC insert_into_transactions ?, ?, ?, ?, ?, ?"""
                cursor.execute(query, (id_user, to_card, transaction_type, amount, status, is_flagged))
                connection.commit()
                print("Transaction recorded successfully.")
        else:
            print("Error: Invalid input.")
            return


connection.commit()

cursor.close()
connection.close()
