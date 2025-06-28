from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def login_user(email, password, designation):
    response = supabase.auth.sign_in_with_password({"email": email, "password": password})
    if response.user:
        profile = supabase.table("users").select("*").eq("email", email).execute()
        if profile.data and profile.data[0]["designation"] == designation:
            return profile.data[0]
    return None

    return False

