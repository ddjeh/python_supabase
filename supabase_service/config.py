import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()


# create a class and create client

class SupabaseClient:

    def __init__(self):
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        self.__client = create_client(url, key)

    @property
    def _get_client(self):
        from supabase_service.auth import SupabaseAuth
        from supabase_service.storage import SupabaseStorage
        from supabase_service.database import SupabaseDatabase
        if isinstance(self, (SupabaseAuth, SupabaseStorage, SupabaseDatabase)):
            return self.__client
        else:
            return None
