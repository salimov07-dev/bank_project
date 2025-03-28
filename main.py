import datetime
import pprint
import pyodbc
import pandas
from datetime import *
import csv

import MangeUsers as Mu
import ControlTransactions as Ct
import Menus as Menus
import OtherFunctions as OtherFunc

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

txt = 'Enter command number: '

while True:
    Menus.print_menu()
    command = int(input(f'{txt}'))
    if command == 1:
        while True:
            Menus.print_menu_ManageUsers()
            command = int(input(f'{txt}'))
            if command == 1:  # salimov
                get_columns = cursor.execute('''select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS
                                               where TABLE_NAME = 'users' ''')
                columns = [col[0] for col in get_columns.fetchall()]
                print(" | ".join(columns))
                get_users = cursor.execute(Mu.ManageUsers.get_users())
                pprint.pp(get_users.fetchall(), width=150)
            elif command == 2:  # salimov
                get_active_users = cursor.execute(Mu.ManageUsers.get_active_users())
                res = get_active_users.fetchall()
                if not res:
                    print('Foal foydalanuvchilar yo`q ❗')
                else:
                    pprint.pp(res)
            elif command == 3:  # salimov
                user_id = int(input('Enter user_id: '))
                get_user_balance = cursor.execute(Mu.ManageUsers.check_balance(user_id))
                res = get_user_balance.fetchone()
                if not res:
                    print('Bunday foydalanuvchi yo`q ❗')
                else:
                    pprint.pp(res)
            else:
                break
    elif command == 2:
        while True:
            Menus.print_menu_ManageTransactions()
            command = int(input(f'{txt}'))
            if command == 1:  # salimov
                # Kartadan kartaga pul o‘tkazmalar
                Ct.ControlTransactions.transfer_to_card()
            elif command == 2:  # salimov
                # Kunlik, haftalik tranzaksiyalarni ko‘rish
                transaction_period = input('Enter (day / week): ').strip().lower()
                result = Ct.ControlTransactions.get_transactions(transaction_period)
            elif command == 3:  # salimov
                # Pul yechish va depozit qilish
                Ct.ControlTransactions.withdraw_deposit()
            else:
                break
    elif command == 3:
        while True:
            Menus.print_menu_other_functions()
            command = int(input(f'{txt}'))
            if command == 1:  # salimov
                transaction_period = input("Enter day period (daily | weekly | monthly): ")
                OtherFunc.OtherFunctions.report_generation(transaction_period)
            elif command == 2:
                new_user_name = input('Enter Your Name: ').title().strip()
                new_user_phone = int(input('Enter your Phone Number: ').replace('+', '').replace(' ', ''))
                new_user_email = input('Enter your email: ')
                print('-- Card details --')
                new_user_card_type = input('Enter Your card type (debit / credit / savings) ')
                query_1 = ''' exec insert_proc_users ?, ?, ?, ? '''
                cursor.execute(query_1, (new_user_name, new_user_phone, new_user_email, new_user_card_type))
                print('Completed successfully ✅')
                print()
                connection.commit()
            elif command == 3:  # salimov
                user_id_2 = input('Enter user id:')
                query_2 = ''' exec get_user_transactions @user_id = ? '''
                get_users_1 = cursor.execute(query_2, (user_id_2,))

                pprint.pp('''user_id | card_number | from_card_id | to_card_id | transaction_type''')
                pprint.pp(get_users_1.fetchall(), width=70, compact=True)
            elif command == 4:  # salimov
                query_3 = ''' select avg(balance) from cards '''
                res_1 = cursor.execute(query_3)
                print('Hamma userlarning o‘rtacha balansi:')
                pprint.pp(res_1.fetchone()[0], width=100)

                print()
                print('''Eng ko‘p tranzaksiya qilgan foydalanuvchi(lar) ''')
                print('''Name | Phone Number | Status | Total_balance | blocked''')
                res = cursor.execute(OtherFunc.OtherFunctions.analysis_balance())
                pprint.pp(res.fetchall(), width=100)
                print()
            else:
                break
    elif command == 4:
        query = '''
        SELECT id, name, phone_number, email, last_active_at, total_balance
        FROM users 
        WHERE status = 'blocked'
        ORDER BY last_active_at DESC;
        '''
        cursor.execute(query)
        results = cursor.fetchall()

        filename = f"Reports\\blocked_users\\blocked_users_report_{datetime.now().strftime('%Y-%m-%d')}.csv"

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow(["ID", "Name", "Phone Number", "Email", "Last Active", "Total Balance"])

            for row in results:
                writer.writerow(row)

        print(f"✅ Bloklangan foydalanuvchilar ro‘yxati saqlandi: {filename}")
    else:
        break

connection.commit()

cursor.close()
connection.close()
