import os
import subprocess
from django.http import JsonResponse
from django.conf import settings
from datetime import datetime

def save_db_snapshot(transaction_id):
    # Get database configuration from Django settings
    db_name = settings.DATABASES['default']['NAME']
    db_user = settings.DATABASES['default']['USER']
    db_password = settings.DATABASES['default']['PASSWORD']
    db_host = settings.DATABASES['default'].get('HOST', 'localhost')
    db_port = settings.DATABASES['default'].get('PORT', '5432')

    # Set up the backup directory and file name
    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    backup_file = os.path.join(
        backup_dir,
        f"{db_name}_snapshot_{transaction_id}.sql"
    )

    # Prepare the pg_dump command
    pg_dump_command = [
        '/Library/PostgreSQL/16/bin/pg_dump',
        '-h', db_host,
        '-p', db_port,
        '-U', db_user,
        '-Fc',  # Custom format, better for large databases
        '-f', backup_file,
        db_name,
    ]

    try:
        # Set environment variable for password
        os.environ['PGPASSWORD'] = db_password
        subprocess.run(pg_dump_command, check=True)
        return f"{db_name}_snapshot_{transaction_id}.sql"
    except subprocess.CalledProcessError as e:
        raise e
    finally:
        # Clean up the environment variable
        del os.environ['PGPASSWORD']