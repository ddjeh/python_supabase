# Example use of the class

# Example select all from supabase api database
from supabase_service.database import SupabaseDatabase

foo_records = SupabaseDatabase().select_all(table_name='foo')

for foo in foo_records:
    print(foo)

# Example use supabase storage
from supabase_service.storage import SupabaseStorage

supabase_storage = SupabaseStorage()
# create bucket
foo_bucket_response = supabase_storage.create_bucket(bucket_id='foo_bucket_id', bucket_name='foo_bucket')

if foo_bucket_response.status != 201:
    exit()

foo_bucket = foo_bucket_response.data

#list all files

foo_files = supabase_storage.list_files(bucket_id=foo_bucket['id'])

for file in foo_files:
    print(file)

# Example use supabase auth
from supabase_service.auth import SupabaseAuth

supabase_auth = SupabaseAuth()

# create user
foo_user_response = supabase_auth.sign_up(email='foo@example.it', password='password')

if foo_user_response.status != 201:
    exit()

foo_user = foo_user_response.data

#login user
foo_login_response = supabase_auth.sign_in(email='foo@example', password='password')

if foo_login_response.status != 200:
    exit()

foo_login = foo_login_response.data