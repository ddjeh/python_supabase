<h1>Supabase Service Project Overview</h1>

This project provides a Python-based service for interacting with Supabase, a backend-as-a-service platform.  
The service includes functionalities for database operations, file storage, and authentication.  
<h3>Requirements</h3>
To install the required dependencies, run:
<strong>pip install -r requirements.txt</strong>

<h3>Project Structure</h3>
<h4>supabase_service/</h4>
database.py: Contains the SupabaseDatabase class for database operations. (better use direct connection jdbc)
storage.py: Contains principal methods for use Supabase storage.
auth.py: Contains principal methods for authentication operations and session verification.
types.py: Defines the GenericResponse class used for standardized responses.
requirements.txt: Lists the dependencies required for the project.

his project is licensed under the MIT License. See the LICENSE file for more details