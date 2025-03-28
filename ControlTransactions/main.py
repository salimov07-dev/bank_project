import smtplib
import random
import pyodbc
import pprint
from email.message import EmailMessage

connection = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=172.25.59.2,1433;"  # Yoki kompyuter nomi
    "DATABASE=project_1;"
    "UID=project;"  # SQL Server foydalanuvchi nomi
    "PWD=qwerty123;"  # SQL Server paroli
    "TrustServerCertificate=yes;",
    timeout=60
)

cursor = connection.cursor()

verification_codes = {}


class ControlTransactions:

    def send_verification_email(to_email):
        """Foydalanuvchiga Gmail orqali tasdiqlash kodini jo‘natadi"""
        verification_code = str(random.randint(100000, 999999))  # 6 xonali kod
        verification_codes[to_email] = verification_code  # Kodni saqlash

        msg = EmailMessage()
        msg.set_content(f"Your transaction verification code is: {verification_code}")
        msg['Subject'] = "Transaction Verification Code"
        msg['To'] = to_email
        msg['From'] = "salimovmironshoh07@gmail.com"  # O‘zingizning emailingiz

        user = "salimovmironshoh07@gmail.com"
        password = "uobt pylh boce aazz"  # Gmail App Password ishlatish kerak!

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(user, password)
            server.send_message(msg)
            server.quit()
            print(f"✅ Verification code sent to {to_email}")
        except Exception as e:
            print(f"❌ Email sending error: {e}")

    def verify_transaction(to_email, user_code):
        """Foydalanuvchi kiritgan kodni tekshiradi"""
        expected_code = verification_codes.get(to_email)

        if expected_code and expected_code == user_code:
            print("✅ Transaction verified successfully!")
            return True
        else:
            print("❌ Incorrect verification code. Transaction canceled.")
            return False

    @staticmethod
    def transfer_to_card():  # salimov
        """Kartadan kartaga pul o`tkazmalar"""
        card_number = input('Enter your Card number (without space): ').strip()
        user_name = input('Enter your name: ').strip()
        to_card = input('Which card do you want to transfer money to? (card number): ').strip()

        if not card_number or not user_name or not to_card:
            print("Error: All fields are required.")
            return


        cursor.execute("SELECT id, is_blocked, balance FROM cards WHERE card_number = ?", (card_number,))
        sender_card = cursor.fetchone()
        sender_id, is_blocked, sender_balance = sender_card

        cursor.execute("SELECT is_blocked FROM cards WHERE card_number = ?", (to_card,))
        sender_card_1 = cursor.fetchone()
        recipient_card_status = sender_card_1
        if sender_card is None:
            print("Error: Your card number is not found in the database.")
            return

        if is_blocked:
            print('Your card is blocked')
            return
        if recipient_card_status and recipient_card_status[0] == 1:
            user_choice = input("The recipient's card is blocked. Do you want to continue? (yes/no): ").strip().lower()

            if user_choice != 'yes':
                print("Transaction canceled.")
                return
        amount = input('Enter Amount: ').strip()
        if not amount.isdigit() or int(amount) <= 0:
            print("Error: Invalid amount.")
            return
        amount = int(amount)

        if amount > sender_balance:
            print("Error: Insufficient balance.")
            return

        cursor.execute("SELECT id FROM cards WHERE card_number = ?", (to_card,))
        receiver_card = cursor.fetchone()

        if receiver_card is None:
            print("Error: Destination card not found.")
            return

        receiver_id = receiver_card[0]

        cursor.execute("UPDATE cards SET balance = balance - ? WHERE card_number = ?", (amount, card_number))
        cursor.execute("UPDATE cards SET balance = balance + ? WHERE id = ?", (amount, receiver_id))

        cursor.execute("EXEC insert_into_transactions ?, ?, ?, ?, ?, ?",
                       (sender_id, receiver_id, 'transfer', amount, 'success', 0))
        connection.commit()
        print("Transaction completed successfully.")

    @staticmethod
    def get_transactions(period):  # salimov
        """Kunlik, haftalik tranzaksiyalarni ko‘rish"""
        periods = {"day": 1, "week": 7}
        if period not in periods:
            print("Error: Invalid period. Use 'day' or 'week'.")
            return

        days = periods[period]
        cursor.execute("SELECT * FROM dbo.get_transactions(?)", (days,))
        transactions = cursor.fetchall()

        if not transactions:
            print("No transactions found for the selected period.")
            return

        for row in transactions:
            print(row)

    @staticmethod
    def withdraw_deposit():  # salimov
        """Pul yechish va depozit qilish"""
        operation = input("Withdraw or deposit (w/d): ").strip().lower()
        if operation not in ['w', 'd']:
            print("Error: Invalid input. Use 'w' for withdraw and 'd' for deposit.")
            return

        card_number = input('Enter your card number (without space): ').strip()
        user_name = input('Enter your name: ').strip()
        user_email = input('Enter your email: ').strip()

        if not card_number or not user_name:
            print("Error: Card number and name cannot be empty.")
            return

        cursor.execute("SELECT id, balance FROM cards WHERE card_number = ?", (card_number,))
        card_data = cursor.fetchone()

        if card_data is None:
            print("Error: Card not found.")
            return

        card_id, balance = card_data

        amount = input("Enter Amount: ").strip()
        if not amount.isdigit() or int(amount) <= 0:
            print("Error: Invalid amount.")
            return
        amount = int(amount)

        ControlTransactions.send_verification_email(user_email)
        user_input_code = input("Enter the verification code sent to your email: ").strip()

        if not ControlTransactions.verify_transaction(user_email, user_input_code):
            print("🚫 Transaction canceled due to incorrect verification code.")
            return

        if operation == 'd':  # Deposit
            new_balance = balance + amount
            cursor.execute("UPDATE cards SET balance = ? WHERE card_number = ?", (new_balance, card_number))
            cursor.execute("EXEC insert_into_transactions ?, ?, ?, ?, ?, ?",
                           (None, card_id, 'deposit', amount, 'success', 0))
            connection.commit()
            print("Deposit successful.")
        else:  # Withdraw
            if amount > balance:
                print("Error: Not enough balance.")
                cursor.execute("EXEC insert_into_transactions ?, ?, ?, ?, ?, ?",
                               (card_id, None, 'withdrawal', amount, 'failed', 0))
            else:
                new_balance = balance - amount
                cursor.execute("UPDATE cards SET balance = ? WHERE card_number = ?", (new_balance, card_number))
                cursor.execute("EXEC insert_into_transactions ?, ?, ?, ?, ?, ?",
                               (card_id, None, 'withdrawal', amount, 'success', 0))
            connection.commit()
            print("Withdrawal successful.")


connection.commit()
