import secrets
import os


if not os.path.exists('.env'):
    
    secret_key = secrets.token_urlsafe(16)

    
    with open('.env', 'w') as f:
        f.write(f'SECRET_KEY={secret_key}')
else:
    print('.env file already exists, skipping secret key generation')