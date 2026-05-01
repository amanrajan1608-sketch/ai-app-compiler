def validate_consistency(config):
    if not isinstance(config, dict):
        return {"is_valid": False, "errors": ["Not a dict"]}
    
    errors = []
    db_tables = [t.get('name') for t in config.get('db_schema', {}).get('tables', [])]
    api_endpoints = config.get('api_schema', {}).get('endpoints', [])

    for api in api_endpoints:
        target = api.get('target_table')
        if target and target not in db_tables:
            errors.append(f"API refers to missing table '{target}'")
            
    return {"is_valid": len(errors) == 0, "errors": errors}
