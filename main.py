import pprint

import pyodbc

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
            elif command == 4:  # in progress # salimov
                pass
                # Foydalanuvchi kartalarining limitini nazorat qilish
            else:
                break
    elif command == 2:
        while True:
            Menus.print_menu_ManageTransactions()
            command = int(input(f'{txt}'))
            if command == 1:  # salimov
                Ct.ControlTransactions.transfer_to_card()
            elif command == 2:  # salimov
                transaction_period = input('Enter (day / week): ').strip().lower()
                result = Ct.ControlTransactions.get_transactions(transaction_period)
            elif command == 3:
                pass
                # Yirik tranzaksiyalarni avtomatik tekshirish (150 mln so‘mdan oshsa)
            elif command == 4:  # salimov
                Ct.ControlTransactions.withdraw_deposit()
                # Pul yechish va depozit qilish
            else:
                break
    elif command == 3:
        while True:
            Menus.print_menu_other_functions()
            command = int(input(f'{txt}'))
            if command == 3:  # salimov
                user_id_2 = input('Enter user id:')
                query_2 = ''' exec get_user_transactions @user_id = ? '''
                get_users_1 = cursor.execute(query_2, (user_id_2,))

                pprint.pp('''user_id | card_number | from_card_id | to_card_id | transaction_type''')
                pprint.pp(get_users_1.fetchall(), width=70, compact=True)
            elif command == 4:
                OtherFunc.OtherFunctions.balance()
    else:
        break

connection.commit()

cursor.close()
connection.close()
