import pandas as pd
import pyodbc
from sqlalchemy import create_engine

# ✅ Use SQLAlchemy for a better connection
engine = create_engine(
    "mssql+pyodbc://project:qwerty123@172.25.59.2:1433/project_1?driver=ODBC+Driver+17+for+SQL+Server"
)


class OtherFunctions:
    @staticmethod
    def report_generation(report_type: str):  # salimov
        query = """
        select 
            CAST(created_at as DATE) as report_date,
            COUNT(id) as total_transactions,
            SUM(case when is_flagged = 1 then 1 else 0 end) as flagged_transactions,
            SUM(amount) as total_amount
        from transactions
        where created_at >= DATEADD(DAY, -{}, GETDATE()) 
        group by CAST(created_at as DATE)
        order by report_date DESC;
        """

        period_days = {"daily": 1, "weekly": 7, "monthly": 30}

        if report_type.lower() in period_days:
            try:
                with engine.connect() as conn:
                    df = pd.read_sql(query.format(period_days[report_type.lower()]), conn)
                    csv_filename = f"Reports/Transaction_reports/{report_type.lower()}_transactions_report.csv"
                    df.to_csv(csv_filename, index=False, encoding='utf-8')
                    print(f"✅ Data saved as {csv_filename}")
            except Exception as e:
                print(f"❌ Error generating report: {e}")
        else:
            print("❌ Invalid report type. Choose 'daily', 'weekly', or 'monthly'.")

    @staticmethod
    def analysis_balance():  # salimov
        return ''' select * from Transaction_cnt() '''

    @staticmethod
    def view_transactions():
        pass
        # main.py
    @staticmethod
    def register_user():
       pass