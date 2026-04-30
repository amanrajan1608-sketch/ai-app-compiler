def validate_consistency(config):
    """
    Checks for cross-layer consistency as required by the PDF.
    - API fields must match DB schema
    - UI fields must map to API
    """
    def validate_consistency(config):
    # Safety Check: Ensure config is a dictionary
    if not isinstance(config, dict):
        return {
            "is_valid": False, 
            "errors": [f"Expected dictionary but got {type(config).__name__}"]
        }
    errors = []
    
    # 1. Extract names for comparison
    db_tables = [t.get('name') for t in config.get('db_schema', {}).get('tables', [])]
    api_endpoints = config.get('api_schema', {}).get('endpoints', [])
    ui_pages = config.get('ui_schema', {}).get('pages', [])

    # 2. Check if API refers to non-existent DB tables
    for api in api_endpoints:
        target = api.get('target_table')
        if target and target not in db_tables:
            errors.append(f"Inconsistency: API '{api.get('path')}' refers to missing table '{target}'")

    # 3. Check if UI pages have matching API routes
    api_paths = [a.get('path') for a in api_endpoints]
    for page in ui_pages:
        for component in page.get('components', []):
            if component.get('type') == 'form' or component.get('type') == 'button':
                action_path = component.get('api_endpoint')
                if action_path and action_path not in api_paths:
                    errors.append(f"Inconsistency: UI Component in '{page.get('title')}' calls missing API '{action_path}'")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }
