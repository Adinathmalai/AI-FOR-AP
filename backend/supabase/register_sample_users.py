from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# Create Supabase client
supabase = create_client(url, key)

def register_user(email, password, designation):
    # Step 1: Register the user with Supabase Auth
    auth_response = supabase.auth.sign_up({
        "email": email,
        "password": password
    })

    # Step 2: Add custom info to 'users' table
    supabase.table("users").insert({
        "email": email,
        "designation": designation
    }).execute()

    print(f"✅ Registered user: {email} with designation {designation}")

# ✅ Add your sample users
register_user("alice@example.com", "alice1234", "Manager")
register_user("bob@example.com", "bob1234", "Developer")
register_user("carol@example.com", "carol1234", "Analyst")
