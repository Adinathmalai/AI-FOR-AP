from .client import supabase

def save_chat_log(log):
    return supabase.table("chat_logs").insert(log).execute()

def get_chat_logs(user_id):
    return supabase.table("chat_logs").select("*").eq("user_id", user_id).execute().data
