import os
import aioodbc
import asyncio
from functools import wraps
from fastapi import HTTPException

DB_SERVER = os.getenv('DB_SERVER')
DB_USER_NAME = os.getenv('DB_USER_NAME')
DB_USER_PW = os.getenv('DB_USER_PW')
DB_DATABASE = os.getenv('DB_DATABASE')


# Create a connection pool
dsn=f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={DB_SERVER};PORT=1433;DATABASE={DB_DATABASE};UID={DB_USER_NAME};PWD={DB_USER_PW};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
pool = None


async def create_pool():
    """Create a pool to execute later queries under.
    """
    global pool
    pool = await aioodbc.create_pool(dsn=dsn, pool_recycle=25*60)


async def close_pool():
    """Close out the pool before shutting down.
    """
    global pool
    pool.close()
    await pool.wait_closed()


def retry_sql_query(retries=3, delay=1):
    """Retry sql query in case of bad connections. TODO: Implement more specific error catching and verify decorator fully async.

    Args:
        retries (int, optional): Number of retry attempts. Defaults to 3.
        delay (int, optional): How many seconds to wait before retry. Defaults to 1.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for _ in range(retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    print(f'Retry on error {e}')
                    if _ == retries - 1:
                        raise e
                await asyncio.sleep(delay)
        return wrapper
    return decorator


@retry_sql_query()
async def run_query(sql_query_statement: str, params: list = None, query_context: str = None, extra_tabs: int = 0, exec_many: bool = False) -> list[dict]:
    """Run a query against database pool. TODO: Change all prints to logging.

    Args:
        sql_query_statement (str): Query statement (ex: SELECT * FROM schema.table WHERE id = ?).
        params (optional, list): list of params to pipe into the query.
        query_context (optional, str): String representing context of the query, for displaying/logging/debug.
        extra_tabs (optional, int): Number of extra tabs to insert. Defaults to 0.
        exec_many (optional, bool): Whether to exec many or single. Defaults to false (exec single).

    Raises:
        HTTPException: Exception if the query failed.

    Returns:
        list[dict]: List of rows returned in column_name:column_value dict format.
    """
    if query_context is not None:
        print('\n' + '\t'*extra_tabs + '+'*10 + f' Running Select Query {query_context} ' + '+'*10)
    else:
        print('\n' + '\t'*extra_tabs + '+'*10 + ' Running Select Query ' + '+'*10)

    try:
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                print('\t'*extra_tabs  + 'Executing Query...')
                print('\t'*extra_tabs  + sql_query_statement)
                if params is not None:
                    if exec_many:
                        batch_size = 1000
                        for i in range(0, len(params), batch_size):
                            batch_params = params[i:i + batch_size]
                            await cursor.executemany(sql_query_statement, batch_params)
                    else:
                        print('\t'*extra_tabs + f"Query Params: {','.join([str(param) for param in params])}.")
                        await cursor.execute(sql_query_statement, params)
                else:
                    await cursor.execute(sql_query_statement)
                if cursor.description:
                    column_names = [column[0] for column in cursor.description]
                    rows = await cursor.fetchall()
                    result = [dict(zip(column_names, row)) for row in rows]
                    print('\t'*extra_tabs  + '-'*10 + ' Select Query Completed ' + '-'*10)
                    return result
                else:
                    print('\t'*extra_tabs  + '-'*10 + ' Select Query Completed ' + '-'*10)
                    return True
    except Exception as e:
        print('\t'*extra_tabs  + f"Error occurred during database query: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during the database query.")


@retry_sql_query()
async def execute_store_procedure(stored_procedure_name: str, params: dict, extra_tabs: int = 0) -> list[dict]:
    """Execute Parameterized Stored Proc. TODO: Change all prints to logging.

    Args:
        stored_procedure_name (str): Stored procedure name.
        params (dict): Params in the param_name:param_value dict format.
        extra_tabs (optional, int): Number of extra tabs to insert. Defaults to 0.

    Raises:
        HTTPException: Exception if proc failed.

    Returns:
        list[dict]: List of rows returned in column_name:column_value dict format.
    """
    print('\n' + '\t'*extra_tabs + '+'*10 + f' Running Stored Proc {stored_procedure_name} ' + '+'*10)
    try:
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                sql_query_statement = f"EXEC {stored_procedure_name} " + ", ".join([f"@{name} = ?" for name in params])
                print('\t'*extra_tabs + sql_query_statement)
                print('\t'*extra_tabs)
                print(*params.values())
                await cursor.execute(sql_query_statement, *params.values())
                if cursor.description:
                    column_names = [column[0] for column in cursor.description]
                    rows = await cursor.fetchall()
                    result = [dict(zip(column_names, row)) for row in rows]
                    print('\t'*extra_tabs  + '-'*10 + ' Stored Proc Completed ' + '-'*10)
                    return result
                else:
                    print('\t'*extra_tabs  + '-'*10 + ' Stored Proc Completed ' + '-'*10)
                    return True
    except Exception as e:
        print('\t'*extra_tabs + f"Error occurred during database query: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during the database query.")
