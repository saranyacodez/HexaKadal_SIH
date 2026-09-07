import pandas as pd
import sqlite3

def setup_worldbank_db():
    excel_path = "worldbank_pink_sheet.xlsx (1).xlsx"
    try:
        xls = pd.ExcelFile(excel_path)
        df_monthly = pd.read_excel(xls, sheet_name="Monthly Prices", skiprows=3)
        df_monthly.columns = [str(c).strip() for c in df_monthly.columns]
        df_monthly.rename(columns={df_monthly.columns[0]: 'Period'}, inplace=True)
        df_monthly = df_monthly[df_monthly['Period'].astype(str).str.match(r'^\d{4}M\d{2}$', na=False)]
        
        conn = sqlite3.connect("hexakadal.db")
        df_monthly.to_sql("worldbank_commodities", conn, if_exists="replace", index=False)
        conn.commit()
        conn.close()
        print("World Bank Pink Sheet successfully loaded into hexakadal.db!")
    except Exception as e:
        print(f"Error setting up database: {e}")

if __name__ == "__main__":
    setup_worldbank_db()