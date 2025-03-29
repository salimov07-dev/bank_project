import smtplib
import random
import pyodbc
import pprint
import os
import tabulate
import time
from email.message import EmailMessage
from datetime import time as d_time
from MangeUsers.main import clear_screen

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
    def clear_screen(): # Salimov
        """ Ekranni tozalash funksiyasi """
        os.system("cls" if os.name == "nt" else "clear")

    def send_verification_email(to_email): # Salimov
        """Foydalanuvchiga Gmail orqali tasdiqlash kodini jo‘natadi"""
        verification_code = str(random.randint(100000, 999999))  # 6 xonali kod
        verification_codes[to_email] = verification_code  # Kodni saqlash

        msg = EmailMessage()
        msg['Subject'] = "🔐 Transaction Verification Code"
        msg['To'] = to_email
        msg['From'] = "Bank Project"

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verification Code</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    padding: 20px;
                    text-align: center;
                }}
                .container {{
                    max-width: 400px;
                    background: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    margin: auto;
                }}
                h2 {{
                    color: #333;
                }}
                .code {{
                    font-size: 24px;
                    font-weight: bold;
                    background: #007bff;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                    display: inline-block;
                    margin: 10px 0;
                }}
                p {{
                    color: #555;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>🔐 Your Transaction Verification Code</h2>
                <p>Use the following code to verify your transaction:</p>
                <div class="code">{verification_code}</div>
                <p>This code is valid for a limited time. Do not share it with anyone.</p>
            </div>
        </body>
        </html>
        """

        msg.add_alternative(html_content, subtype="html")

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

    def verify_transaction(to_email, user_code): # Salimov
        """Foydalanuvchi kiritgan kodni tekshiradi"""
        expected_code = verification_codes.get(to_email)

        if expected_code and expected_code == user_code:
            print("✅ Transaction verified successfully!")
            return True
        else:
            print("❌ Incorrect verification code. Transaction canceled.")
            return False

    @staticmethod
    def transfer_to_card(): # Salimov
        """💳 Kartadan kartaga pul o‘tkazmalar"""
        clear_screen()
        print("=" * 50)
        print(" " * 12 + "💳 PUL O‘TKAZMALAR MENYUSI")
        print("=" * 50)

        card_number = input("🔹 Enter your Card Number (without spaces): ").strip()
        user_name = input("🔹 Enter your Name: ").strip()
        user_email = input('🔹 Enter your Email: ')
        to_card = input("🔹 Recipient Card Number: ").strip()

        if not card_number or not user_name or not to_card:
            print("❌ Xato: Barcha maydonlarni to‘ldiring!")
            return

        cursor.execute("SELECT id, is_blocked, balance FROM cards WHERE card_number = ?", (card_number,))
        sender_card = cursor.fetchone()
        
        if sender_card is None:
            print("❌ Xato: Kartangiz bazada topilmadi!")
            return

        sender_id, is_blocked, sender_balance = sender_card

        if is_blocked:
            print("🚫 Kartangiz bloklangan!")
            return

        cursor.execute("SELECT is_blocked FROM cards WHERE card_number = ?", (to_card,))
        recipient_card = cursor.fetchone()

        if recipient_card is None:
            print("❌ Xato: Qabul qiluvchi karta topilmadi!")
            return

        if recipient_card[0] == 1:
            user_choice = input("⚠️ Qabul qiluvchi karta bloklangan").strip().lower() 
            print("❌ Tranzaksiya bekor qilindi.")
            return
        
        while True:
            amount = input("💰 Enter Amount: ").strip()
            if not amount.isdigit() or int(amount) <= 0:
                print("❌ Xato: Yaroqsiz summa, qayta kiriting!")
                continue
            amount = int(amount)
            if amount > sender_balance:
                print("❌ Xato: Balans yetarli emas!")
                return
            break
        ControlTransactions.send_verification_email(user_email)
        user_input_code = input("Enter the verification code sent to your email: ").strip()

        if not ControlTransactions.verify_transaction(user_email, user_input_code):
            print("🚫 Transaction canceled due to incorrect verification code.")
            return
        cursor.execute("SELECT id FROM cards WHERE card_number = ?", (to_card,))
        receiver_card = cursor.fetchone()
        receiver_id = receiver_card[0]

        # Tranzaksiya amalga oshirish
        cursor.execute("UPDATE cards SET balance = balance - ? WHERE card_number = ?", (amount, card_number))
        cursor.execute("UPDATE cards SET balance = balance + ? WHERE id = ?", (amount, receiver_id))

        cursor.execute("EXEC insert_into_transactions ?, ?, ?, ?, ?, ?", 
                    (sender_id, receiver_id, 'transfer', amount, 'success', 0))
        connection.commit()

        print("\n⏳ Tranzaksiya amalga oshirilmoqda...", end="", flush=True)
        time.sleep(2)
        print("\r✅ Tranzaksiya muvaffaqiyatli amalga oshirildi!")
    
    @staticmethod
    def get_transactions(period): # Salimov
        """📊 Kunlik va haftalik tranzaksiyalarni ko‘rish"""
        clear_screen()
        print("=" * 50)
        print(" " * 10 + "📊 TRANZAKSIYA TARIXI")
        print("=" * 50)

        periods = {"day": 1, "week": 7}
        if period not in periods:
            print("❌ Xato: Noto‘g‘ri vaqt oralig‘i! 'day' yoki 'week' kiriting.")
            return

        days = periods[period]
        cursor.execute("SELECT * FROM dbo.get_transactions(?)", (days,))
        transactions = cursor.fetchall()

        if not transactions:
            print(f"📭 {days} kunlik tranzaksiyalar topilmadi.")
            return

        headers = ["ID", "Sender", "Receiver", "Type", "Amount", "Status", "Date"]
        table = tabulate(transactions, headers, tablefmt="fancy_grid", numalign="center")

        print("\n⏳ Ma'lumotlar yuklanmoqda...", end="", flush=True)
        time.sleep(1.5)
        print("\r✅ Tranzaksiyalar ro‘yxati tayyor!\n")
        print(table)

    @staticmethod
    def withdraw_deposit():  # Salimov
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
