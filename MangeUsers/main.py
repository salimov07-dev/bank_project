import os
import pyodbc
from tabulate import tabulate

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

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

class ManageUsers: 
    @staticmethod  # done # Salimov
    def get_users():
        clear_screen()    

        cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'users'")
        columns = [col[0] for col in cursor.fetchall()]

        clear_screen() 

        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        print("=" * 60)
        print(" " * 20 + "👥 Foydalanuvchilar Ro‘yxati")
        print("=" * 60)
     
        if users:
            print(tabulate(users, headers=columns, tablefmt="grid"))
        else:
            print("📌 Hech qanday foydalanuvchi topilmadi.")

        print("=" * 60)
 
    @staticmethod  # done # Salimov
    def display_active_users():
        clear_screen()
 
        cursor.execute("SELECT * FROM get_active_users")  
        active_users = cursor.fetchall()
        clear_screen()
        print("=" * 60)
        print(" " * 20 + "✅ Faol Foydalanuvchilar")
        print("=" * 60)

        if not active_users:
            print("📌 Faol foydalanuvchilar yo‘q ❗")
        else: 
            cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'users'")
            columns = [col[0] for col in cursor.fetchall()]
            
            print(tabulate(active_users, headers=columns, tablefmt="fancy_grid")) 
        print("=" * 60)

    @staticmethod
    def display_user_balance(user_id):  # done # Salimov
        cursor.execute(f"SELECT * FROM dbo.GetUserByID({user_id})")
        user_data = cursor.fetchone()

        print("=" * 60)
        print(" " * 20 + "💰 Foydalanuvchi Balansi")
        print("=" * 60)

        if not user_data:
            print(f"❌ Bunday foydalanuvchi topilmadi! (ID: {user_id})")
        else:
            columns = ["id", "name", "email", "status", "total_balance"] 
            print(tabulate([user_data], headers=columns, tablefmt="fancy_grid"))

        print("=" * 60)

connection.commit()