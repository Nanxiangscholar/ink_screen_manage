#!/usr/bin/env python3

import sys
print(f"Python version: {sys.version}")

try:
    from app import create_app
    print("Successfully imported create_app")
    
    app = create_app()
    print("Successfully created app")
    
    print("App configuration:")
    print(f"SECRET_KEY: {app.config.get('SECRET_KEY')}")
    print(f"SQLALCHEMY_DATABASE_URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    print(f"SQLALCHEMY_BINDS: {app.config.get('SQLALCHEMY_BINDS')}")
    
    print("\nApp routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule}")
        
    print("\nTest completed successfully!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
