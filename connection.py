import asyncpg
from dotenv import load_dotenv 
import os

load_dotenv()

pass_db = os.getenv("PASSWORD_DB")


async def connection_db():
    try:
        conn = await asyncpg.connect(
            user="postgres",
            database="finance_db",
            password=pass_db,
            host="localhost",
            port=5432
        )
        return conn
    except Exception as Error:
        print(f"Connection error: {Error}")
    
    
async def create_table_db():
    try:
        conn = await connection_db()
        await conn.execute("""
        create table if not exists users(
            user_id serial primary key,
            username varchar(200),
            full_name varchar(200),
            telegram_id varchar(300),
            balance int,
            is_active boolean default true,
            created_at timestamp default now()
        );
        create table if not exists tranzactions(
            tranz_id serial primary key,
            title varchar(200),
            type varchar(200),
            amount int,
            telegram_id varchar(200),
            is_active boolean default true,
            created_at timestamp default now()
        );
          
        create table if not exists goals(
            goal_id serial primary key,
            title varchar(200),
            amount int,
            type varchar(200),
            telegram_id varchar(300),
            is_active boolean default true,
            created_at timestamp default now()
        )
    
                     """)
        print("Table created!")
    except Exception as Error:
        print(f"create table error: {Error}")
    finally:
        await conn.close()
    
    