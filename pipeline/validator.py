def validate_consistency(config):
    # Safety Shield: If config is a list, take the first item. If not a dict, fail gracefully.
    if isinstance(config, list) and len(config) > 0:
        config = config[0]
        
    if not isinstance(config, dict):
        return {"is_valid": False, "errors": ["AI output was not a valid configuration object."]}
    
    errors = []
    
    # Use .get() safely with defaults
    db_schema = config.get('db_schema', {})
    if not isinstance(db_schema, dict): db_schema = {}
    
    db_tables = [t.get('name') for t in db_schema.get('tables', []) if isinstance(t, dict)]
    
    api_schema = config.get('api_schema', {})
    if not isinstance(api_schema, dict): api_schema = {}
    
    api_endpoints = api_schema.get('endpoints', [])

    # Validation Logic
    for api in api_endpoints:
        if isinstance(api, dict):
            target = api.get('target_table')
            if target and target not in db_tables:
                errors.append(f"API refers to missing table '{target}'")
            
    return {"is_valid": len(errors) == 0, "errors": errors}
