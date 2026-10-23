from connection import *      


async def create_user(username, full_name, telegram_id):
    try:
        conn = await connection_db()
        await conn.execute("""
        insert into users(username, full_name, telegram_id) Values
        ($1, $2, $3) 
                     """, username, full_name,str(telegram_id))
    except Exception as Error:
        print(f"Create user Error: {Error}")
    finally:
        await conn.close()
        
        

async def get_user_by_id(telegram_id):
    try:
        conn = await connection_db()
        user = await conn.fetchrow("""
        select * from users where telegram_id = $1
                     """, str(telegram_id))
        return user
    except Exception as Error:
        print(f"Get user by id Error: {Error}")
    finally:
        await conn.close()
        


        
        
async def get_balance(telegram_id):
    try:
        conn = await connection_db()
        balance = await conn.fetchrow("""
        select balance from users where telegram_id = $1
                     """, str(telegram_id))
        return balance
    except Exception as Error:
        print(f"Get user by id Error: {Error}")
    finally:
        await conn.close()
        
        
        

    
                
async def get_history(telegram_id):
    try:
        conn = await connection_db()
        tranz = await conn.fetchrow("""
        select * from tranzactions where telegram_id = $1
                     """, str(telegram_id))
        return tranz
    except Exception as Error:
        print(f"Get tranz Error: {Error}")
    finally:
        await conn.close()
        


async def create_tranzaction(amount, type,title,telegram_id):
    try:
        conn = await connection_db()
        if type == "deposit":
            await conn.execute("""
            UPDATE users
            set balance = balance + $1
            WHERE telegram_id = $2
            """, amount, str(telegram_id))
        elif type == "withdraw":
            await conn.execute("""
            UPDATE users
            set balance = balance - $1
            WHERE telegram_id = $2
            """, amount, str(telegram_id))
        await conn.execute("""
        insert into tranzactions(amount, title,type,telegram_id) Values
        ($1, $2, $3, $4) 
                     """, amount, title,type, str(telegram_id))
        return True 
    except Exception as Error:
        print(f"Create tranzaction Error: {Error}")
        return False 
    finally:
        await conn.close()
        
        
        
        


async def create_tranzaction_goal(goal_id, amount, type,title,telegram_id):
    try:
        conn = await connection_db()
        if type == "goal":
            await conn.execute("""
            UPDATE goals
            set amount = amount + $1
            WHERE telegram_id = $2 and goal_id = $3
            """, amount, str(telegram_id), goal_id)
        elif type == "credit":
            await conn.execute("""
            UPDATE goals
            set amount = amount - $1
            WHERE telegram_id = $2 and goal_id = $3
            """, amount, str(telegram_id), goal_id)
        await conn.execute("""
        insert into tranzactions(amount, title,type,telegram_id) Values
        ($1, $2, $3, $4) 
                     """, amount, title,type, str(telegram_id))
        return True 
    except Exception as Error:
        print(f"Create tranzaction Error: {Error}")
        return False 
    finally:
        await conn.close()        

        
        
async def create_goal(amount, type,title,telegram_id):
    try:
        conn = await connection_db()
        await conn.execute("""
        insert into goals(amount, title,type,telegram_id) Values
        ($1, $2, $3, $4) 
                     """, amount, title,type, str(telegram_id))
        return True 
    except Exception as Error:
        print(f"Create goal rror: {Error}")
        return False 
    finally:
        await conn.close()
        
        
        
        
async def get_goal(telegram_id):
    try:
        conn = await connection_db()
        goal = await conn.fetch("""
        select * from goal where telegram_id = $1
                     """, str(telegram_id))
        return goal
    except Exception as Error:
        print(f"Get goal Error: {Error}")
    finally:
        await conn.close()
        
        
        
async def get_tranz(telegram_id, type):
    try:
        conn = await connection_db()
        goal = await conn.fetch("""
        select * from  tranzactions where telegram_id = $1 and type = $2
                     """, str(telegram_id), type)
        return goal
    except Exception as Error:
        print(f"Get tranzactions Error: {Error}")
    finally:
        await conn.close()
        
        
        
        
async def get_goal_type(telegram_id, type):
    try:
        conn = await connection_db()
        goal = await conn.fetch("""
        select * from goal where telegram_id = $1 and type = $2
                     """, str(telegram_id), type)
        return goal
    except Exception as Error:
        print(f"Get goal Error: {Error}")
    finally:
        await conn.close()