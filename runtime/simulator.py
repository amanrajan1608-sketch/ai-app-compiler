import sqlite3

def simulate_execution(config):
    if not isinstance(config, dict): return False, "Invalid config"
    try:
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        tables = config.get('db_schema', {}).get('tables', [])
        for table in tables:
            name = table.get('name')
            cols = [f"{c.get('name')} {c.get('type', 'TEXT')}" for c in table.get('columns', [])]
            cursor.execute(f"CREATE TABLE {name} ({', '.join(cols)})")
        return True, "Execution Success"
    except Exception as e:
        return False, str(e)
