import datetime
import pprint
import pyodbc
import pandas
import csv
import tabulate
from datetime import *

import MangeUsers as Mu
import ControlTransactions as Ct
from MangeUsers.main import clear_screen
import Menus as Menus
import OtherFunctions as OtherFunc
import Monitoring as Moni 

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

txt = "\nTanlovni kiriting (1-6): "

while True:
    Menus.print_menu()
    command = int(input(f'{txt}')) 
    if command == 1: # Done
        while True:
            Menus.menu_manage_users()
            command = int(input(f'{txt}'))
            if command == 1:  # Salimov
                Mu.ManageUsers.get_users() 
            elif command == 2:  # Salimov
                Mu.ManageUsers.display_active_users() 
            elif command == 3:  # Salimov
                try:
                    user_id = int(input("🔹 Foydalanuvchi ID ni kiriting: "))
                    Mu.ManageUsers.display_user_balance(user_id)
                except ValueError:
                    print("⚠️ Xato: Raqam kiriting!")
            else:
                break
    elif command == 2: # Done
        while True:
            Menus.print_menu_ManageTransactions()
            command = int(input(f'{txt}'))
            if command == 1:  # Salimov
                # Kartadan kartaga pul o‘tkazmalar
                Ct.ControlTransactions.transfer_to_card()
            elif command == 2:  # Salimov
                # Kunlik, haftalik tranzaksiyalarni ko‘rish
                period = input("Tranzaksiya davrini kiriting (day/week): ").strip().lower()
                Mu.get_transactions(period)
            elif command == 3:  # Salimov
                # Pul yechish va depozit qilish
                Ct.ControlTransactions.withdraw_deposit()
            else:
                break
    elif command == 3: # Done
        while True:
            Menus.print_menu_other_functions()
            command = int(input(f'{txt}'))
            if command == 1:  # Salimov
                transaction_period = input("Enter day period (daily | weekly | monthly): ")
                OtherFunc.OtherFunctions.report_generation(transaction_period)
            elif command == 2: # Salimov
                def register_user(): 
                    print("\n" + "=" * 60)
                    print("  📝 Yangi foydalanuvchini ro‘yxatdan o‘tkazish")
                    print("=" * 60)

                    try:
                        new_user_name = input("👤 Ismingizni kiriting: ").title().strip()
                        new_user_phone = input("📞 Telefon raqamingizni kiriting (+ bilan yoki bo‘sh joysiz): ").replace("+", "").replace(" ", "")
                         
                        if not new_user_phone.isdigit():
                            print("\n❌ Xatolik: Telefon raqami faqat raqamlardan iborat bo‘lishi kerak!")
                            return
                        
                        new_user_phone = int(new_user_phone)

                        new_user_email = input("📧 Email manzilingizni kiriting: ").strip()

                        print("\n" + "-" * 40)
                        print("💳 Kartangiz tafsilotlari")
                        print("-" * 40)
                        new_user_card_type = input("💳 Kartangiz turini kiriting (debit / credit / savings): ").strip().lower()

                        valid_card_types = ["debit", "credit", "savings"]
                        if new_user_card_type not in valid_card_types:
                            print("\n❌ Xatolik: Kartaning turi 'debit', 'credit' yoki 'savings' bo‘lishi kerak!")
                            return

                        query_1 = ''' EXEC insert_proc_users ?, ?, ?, ? '''
                        cursor.execute(query_1, (new_user_name, new_user_phone, new_user_email, new_user_card_type))
                        connection.commit()

                        print("\n✅ Ro‘yxatdan o‘tish muvaffaqiyatli yakunlandi!")
                        print("=" * 60)
                    
                    except Exception as e:
                        print("\n❌ Xatolik yuz berdi!")
                        print(f"🔴 Tafsilotlar: {e}")
                        print("=" * 60)
            elif command == 3:  # Salimov
                OtherFunc.OtherFunctions.view_transactions
            elif command == 4:  # Salimov
                clear_screen()
                print("=" * 70)
                print("        💰 HAMMA FOYDALANUVCHILARNING O‘RTACHA BALANSI")
                print("=" * 70)

                query_3 = ''' SELECT AVG(balance) FROM cards '''
                res_1 = cursor.execute(query_3)
                avg_balance = res_1.fetchone()[0]

                print(f"\n📊 O‘rtacha balans: {avg_balance:,.2f} so‘m")
                print("=" * 70)

                print("\n🏆 Eng ko‘p tranzaksiya qilgan foydalanuvchilar:")
                query_4 = OtherFunc.OtherFunctions.analysis_balance()
                res = cursor.execute(query_4)
                top_users = res.fetchall()

                headers = ["Name", "Phone Number", "Status", "Total Balance", "Blocked"]

                if top_users:
                    print(tabulate(top_users, headers=headers, tablefmt="fancy_grid"))
                else:
                    print("\n⚠️ Eng ko‘p tranzaksiya qilgan foydalanuvchilar topilmadi!")

                print("=" * 70)
            else:
                break
    elif command == 4: # Done
         while True:
            Menus.forth_menu() 
            command = int(input(f'{txt}'))
            if command == 1: # Salimov
                Moni.ReportGenerator.blocked_users_report()
            elif command == 2: # Nozima
                Moni.ReportGenerator.avg_card_usage_report() 
            elif command == 3: # Nozima
                 Moni.ReportGenerator.vip_users_report()
            elif command == 5: # Nozima
                 Moni.ReportGenerator.scheduled_payments_report() 
            else:
                break
    else:
        break

connection.commit()

cursor.close()
connection.close()
