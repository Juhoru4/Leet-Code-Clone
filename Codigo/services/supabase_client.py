from supabase import create_client
import os

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

# Cliente para operaciones públicas (signup, signin desde backend)
client = None
admin_client = None

def get_client():
    global client
    if client is None:
        client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    return client

def get_admin_client():
    global admin_client
    if admin_client is None:
        admin_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    return admin_client
