<h1>Supabase Service Project Overview</h1>

This project provides a Python-based service for interacting with Supabase, a backend-as-a-service platform.  
The service includes functionalities for database operations, file storage, and authentication.  
<h3>Requirements</h3>
To install the required dependencies, run:
<strong>pip install -r requirements.txt</strong>

<h3>Project Structure</h3>
<h4>supabase_service/</h4>
<strong>database.py:</strong> Contains the SupabaseDatabase class for database operations. (better use direct connection
jdbc) <br>
<strong>storage.py:</strong> Contains principal methods for use Supabase storage. <br>
<strong>auth.py:</strong> Contains principal methods for authentication operations and session verification. <br>
<strong>types.py:</strong> Defines the GenericResponse class used for standardized responses. <br>
<strong>requirements.txt:</strong> Lists the dependencies required for the project. <br>
