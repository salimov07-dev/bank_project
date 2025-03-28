import pandas as pd
import pyodbc
import os
import tabulate
from sqlalchemy import create_engine

from MangeUsers.main import clear_screen

# ✅ Use SQLAlchemy for a better connection
engine = create_engine(
    "mssql+pyodbc://project:qwerty123@172.25.59.2:1433/project_1?driver=ODBC+Driver+17+for+SQL+Server"
)


class OtherFunctions:
    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")

    def report_generation(report_type: str):  # Salimov
        """📊 Tranzaksiya hisoboti yaratish"""
        
        query = """
        SELECT 
            CAST(created_at AS DATE) AS report_date,
            COUNT(id) AS total_transactions,
            SUM(CASE WHEN is_flagged = 1 THEN 1 ELSE 0 END) AS flagged_transactions,
            SUM(amount) AS total_amount
        FROM transactions
        WHERE created_at >= DATEADD(DAY, -{}, GETDATE()) 
        GROUP BY CAST(created_at AS DATE)
        ORDER BY report_date DESC;
        """

        period_days = {"daily": 1, "weekly": 7, "monthly": 30}

        if report_type.lower() in period_days:
            print("\n" + "=" * 60)
            print(f"  📊 {report_type.capitalize()} tranzaksiya hisoboti generatsiya qilinmoqda...")
            print("=" * 60)

            try:
                with engine.connect() as conn:
                    df = pd.read_sql(query.format(period_days[report_type.lower()]), conn)
                    csv_filename = f"Reports/Transaction_reports/{report_type.lower()}_transactions_report.csv"
                    df.to_csv(csv_filename, index=False, encoding='utf-8')

                    print("\n✅ Hisobot muvaffaqiyatli yaratildi!")
                    print(f"📂 Fayl saqlandi: {csv_filename}")
                    print("=" * 60)
            except Exception as e:
                print("\n❌ Xatolik yuz berdi!")
                print(f"🔴 Tafsilotlar: {e}")
                print("=" * 60)
        else:
            print("\n❌ Noto‘g‘ri hisobot turi!")
            print("📌 Iltimos, 'daily', 'weekly' yoki 'monthly' tanlang.")
            print("=" * 60)
    @staticmethod
    def analysis_balance():  # Salimov
        return ''' select * from Transaction_cnt() '''

    @staticmethod
    def view_transactions(): # Salimov
        clear_screen()
        print("=" * 60)
        print("        🔍 FOYDALANUVCHI TRANZAKSIYALARINI KO'RISH")
        print("=" * 60)

        user_id_2 = input("🔹 Foydalanuvchi ID sini kiriting: ").strip()
        query_2 = ''' exec get_user_transactions @user_id = ? '''
        engine.execute(query_2, (user_id_2,))
        transactions = engine.fetchall()

        # Sarlavha chiqarish
        headers = ["User ID", "Card Number", "From Card ID", "To Card ID", "Transaction Type"]

        if transactions:
            print("\n📊 Tranzaksiya ma'lumotlari:")
            print(tabulate(transactions, headers=headers, tablefmt="fancy_grid"))
        else:
            print("\n⚠️ Hech qanday tranzaksiya topilmadi!")

        print("=" * 60)  
    def register_user():
        pass
        # main.py