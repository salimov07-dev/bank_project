import csv
import pyodbc
from datetime import datetime
from typing import Any
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
class ReportGenerator:
    @staticmethod
    def save_report(filename, headers, data):
        """Hisobotni CSV faylga yozish."""
        with open(filename, "w", newline="", encoding="utf-8") as file:
            csv.writer(file).writerows([headers] + data)
        print(f"✅ Hisobot yaratildi: {filename}")

    @staticmethod
    def show_report(headers, data):
        """Konsolga jadval shaklida chiqarish."""
        print("\n" + tabulate(data, headers=headers, tablefmt="grid"))

    @staticmethod
    def generate_report(query, filename, headers):
        """Hisobotni yaratish va chiqarish."""
        results = cursor.execute(query).fetchall()
        ReportGenerator.save_report(filename, headers, results)
        ReportGenerator.show_report(headers, results)

    @staticmethod
    def blocked_users_report():
        """Bloklangan foydalanuvchilar."""
        ReportGenerator.generate_report(
            "SELECT id, name, phone_number, email, last_active_at, total_balance FROM users WHERE status = 'blocked' ORDER BY last_active_at DESC",
            f"Reports/Blocked_Users/blocked_users_{datetime.now().strftime('%Y-%m-%d')}.csv",
            ["ID", "Name", "Phone Number", "Email", "Last Active", "Total Balance"]
        )

    @staticmethod
    def avg_card_usage_report():
        """Kartalarning o‘rtacha foydalanish muddati."""
        ReportGenerator.generate_report(
            "SELECT card_type, AVG(DATEDIFF(DAY, created_at, GETDATE())) AS avg_days_used FROM cards GROUP BY card_type",
            f"Reports/Avg_Cards_Usage/avg_card_usage_{datetime.now().strftime('%Y-%m-%d')}.csv",
            ["Card Type", "Avg Days Used"]
        )

    @staticmethod
    def vip_users_report():
        """VIP foydalanuvchilar."""
        ReportGenerator.generate_report(
            "SELECT u.id, u.name, v.assigned_at, v.reason FROM vip_users v JOIN users u ON v.user_id = u.id",
            f"Reports/VIP_Users/vip_users_{datetime.now().strftime('%Y-%m-%d')}.csv",
            ["ID", "Name", "Assigned At", "Reason"]
        )

    @staticmethod
    def scheduled_payments_report():
        """Rejalashtirilgan to‘lovlar."""
        ReportGenerator.generate_report(
            "SELECT user_id, COUNT(*) AS total_scheduled_payments, SUM(amount) AS total_scheduled_amount FROM scheduled_payments WHERE status = 'pending' GROUP BY user_id ORDER BY total_scheduled_amount DESC",
            f"Reports/Scheduled_Payments/scheduled_payments_{datetime.now().strftime('%Y-%m-%d')}.csv",
            ["User ID", "Total Scheduled Payments", "Total Scheduled Amount"]
        )