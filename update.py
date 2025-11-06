import teradatasql
import pandas as pd

# Connect
with teradatasql.connect(host='your_host', user='your_user', password='your_password') as con:
    with con.cursor() as cur:
        # Create a temporary table
        cur.execute("""
            CREATE VOLATILE TABLE updated_values (
                case_nr DECIMAL(28,0),
                product_category VARCHAR(100)
            ) ON COMMIT PRESERVE ROWS;
        """)
        
        # Insert your updated df into the volatile table
        insert_sql = "INSERT INTO updated_values (case_nr, product_category) VALUES (?, ?)"
        cur.executemany(insert_sql, df[['case_nr', 'product_category']].itertuples(index=False, name=None))
        
        # Run one big UPDATE joining on case_nr
        cur.execute("""
            UPDATE your_schema.your_table AS t
            FROM updated_values AS u
            SET t.product_category = u.product_category
            WHERE t.case_nr = u.case_nr;
        """)
        con.commit()
