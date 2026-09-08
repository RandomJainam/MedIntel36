import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

from config import (
    RAW_DATA_DIR,
    DATABASE_URI
)


def create_database():

    print("=" * 70)
    print("🏥 MedIntel360 Database Loader")
    print("=" * 70)

    engine = create_engine(DATABASE_URI)

    metadata = []

    csv_files = sorted(RAW_DATA_DIR.glob("*.csv"))

    if not csv_files:
        print(f"\n❌ No CSV files found in:\n{RAW_DATA_DIR}")
        return

    total_tables = 0

    for csv in csv_files:

        table_name = csv.stem.lower()

        print(f"\n📂 Loading : {table_name}")

        try:

            df = pd.read_csv(csv)

            rows = len(df)

            cols = len(df.columns)

            duplicates = int(df.duplicated().sum())

            missing = int(df.isnull().sum().sum())

            memory = round(
                df.memory_usage(deep=True).sum() / 1024 / 1024,
                2
            )

            df.to_sql(
                table_name,
                engine,
                if_exists="replace",
                index=False
            )

            metadata.append({

                "table_name": table_name,
                "rows": rows,
                "columns": cols,
                "duplicates": duplicates,
                "missing_values": missing,
                "memory_mb": memory

            })

            total_tables += 1

            print(f"   ✅ Rows       : {rows}")
            print(f"   ✅ Columns    : {cols}")
            print(f"   ✅ Duplicates : {duplicates}")
            print(f"   ✅ Missing    : {missing}")
            print(f"   ✅ Memory     : {memory} MB")

        except Exception as e:

            print(f"❌ Error loading {table_name}")

            print(e)

    metadata_df = pd.DataFrame(metadata)

    metadata_df.to_sql(

        "metadata_catalog",

        engine,

        if_exists="replace",

        index=False

    )

    print("\n")

    print("=" * 70)

    print("📊 Database Summary")

    print("=" * 70)

    print(metadata_df)

    print("\n")

    print(f"✅ Total Tables Loaded : {total_tables}")

    print(f"✅ Database Created Successfully")

    print("=" * 70)


def verify_database():

    engine = create_engine(DATABASE_URI)

    print("\n")

    print("=" * 70)

    print("📁 Tables inside SQLite")

    print("=" * 70)

    with engine.connect() as conn:

        tables = conn.execute(text(
            "SELECT name FROM sqlite_master WHERE type='table';"
        ))

        for table in tables:

            print("•", table[0])


if __name__ == "__main__":

    create_database()

    verify_database()