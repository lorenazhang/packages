with teradatasql.connect(host='YOUR_HOST', user='YOUR_USER', password='YOUR_PASSWORD') as con:
    with con.cursor() as cur:
        # 1) Staging table with composite PI on (case_nr, run_date)
        cur.execute("""
            CREATE VOLATILE TABLE updated_values (
                case_nr          DECIMAL(28,0),
                run_date         TIMESTAMP,          -- use DATE if your base column is DATE
                product          VARCHAR(200),
                product_category VARCHAR(200)
            )
            PRIMARY INDEX (case_nr, run_date)
            ON COMMIT PRESERVE ROWS;
        """)

        # 2) Bulk insert into staging
        cur.executemany(
            """
            INSERT INTO updated_values (case_nr, run_date, product, product_category)
            VALUES (?, ?, ?, ?)
            """,
            list(df_updates[['case_nr', 'run_date', 'product', 'product_category']]
                 .itertuples(index=False, name=None))
        )

        # 3) Set-based UPDATE joining on both keys
        cur.execute("""
            UPDATE YOUR_SCHEMA.YOUR_TABLE AS t
            FROM updated_values AS u
            SET
                t.product          = u.product,
                t.product_category = u.product_category
            WHERE t.case_nr  = u.case_nr
              AND t.run_date = u.run_date
        """)
        print(f"Rows updated: {cur.rowcount}")
        con.commit()
