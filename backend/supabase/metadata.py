from .client import supabase

def save_metadata(metadata):
    return supabase.table("metadata").insert(metadata).execute()

def get_metadata(file_id):
    return supabase.table("metadata").select("*").eq("file_id", file_id).execute().data
