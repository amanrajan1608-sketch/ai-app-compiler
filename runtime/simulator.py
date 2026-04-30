import sqlite3

def simulate_execution(config):
    """
    Proves 'Execution Awareness' by attempting to build the 
    database schema in an in-memory SQLite instance.
    """
    try:
        # Create a temporary database in RAM
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        
        db_schema = config.get('db_schema', {})
        tables = db_schema.get('tables', [])
        
        if not tables:
            return False, "No tables found in DB schema."

        for table in tables:
            name = table.get('name')
            columns = table.get('columns', [])
            
            # Format: CREATE TABLE users (id INTEGER, name TEXT)
            col_defs = []
            for col in columns:
                col_defs.append(f"{col.get('name')} {col.get('type', 'TEXT')}")
            
            query = f"CREATE TABLE {name} ({', '.join(col_defs)})"
            cursor.execute(query)
            
        conn.commit()
        return True, f"Success: Simulated execution of {len(tables)} tables."
    
    except Exception as e:
        return False, f"Execution Failed: {str(e)}"
