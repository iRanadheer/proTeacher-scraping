import sqlite3

import warnings
warnings.filterwarnings('ignore')

con = sqlite3.connect('/home/ranu/data_to_go/proTeacher/data.sqlite')

cursor = con.cursor()

try:
    cursor.execute('DROP TABLE training')
    print('Table is deleted')
except Exception as e:
    print('Table does not exists')


def add_data_to_db(df, table_name='forums',if_exists='append',wipe_data='no',cursor=cursor):

    cursor.execute('CREATE TABLE IF NOT EXISTS forums (uid integer PRIMARY KEY, user_link text, username text, joined_date text, no_of_posts text, membership_type text, post_title text, posted_date text, post_text text, user_details text, post_url text);')

    if wipe_data =='yes':
        cursor.execute(f'DELETE FROM {table_name}')
        print(f'{table_name} is deleted')
        
    try:
        df.to_sql(table_name,con=con,if_exists=if_exists,index=False)
        print(f'Successfully added {df.shape[0]} rows into the db')
        con.commit()
    except Exception as e:
        print(f'duplicate ids found or {e}')
    
    
        