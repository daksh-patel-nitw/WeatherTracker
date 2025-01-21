<h1>WeatherGuard: Encrypted Access and Weather Data Fetching Tool</h1>

<h2>Setup Instructions</h2>

<h3>1. Install Dependencies</h3>
    <ul>
        <li>Navigate to the <strong>Code</strong> folder.</li>
        <li>Run the following command to install the required dependencies:
            <pre><code>pip install -r requirements.txt</code></pre>
        </li>
        <li><em>(Make sure Python is installed on your system)</em></li>
    </ul>

<h3>2. Set Up OpenWeatherMap API Key</h3>
    <ul>
        <li>Open <strong>weather.py</strong> and add your API key in the first line between the quotes (<code>''</code>), which you can obtain from <a href="https://openweathermap.org/">openweathermap.org</a>.</li>
    </ul>

<h3>3. Set Up MySQL Database</h3>
    <ul>
        <li>Log in to your MySQL database:
            <pre><code>mysql -u root -p</code></pre>
            Enter the password when prompted.
        </li>
        <li>Create a new database:
            <pre><code>CREATE DATABASE python_app_cli;</code></pre>
        </li>
        <li>Create a new user and grant privileges, Replace the <b>&lt;foldername&gt;</b> to "Folder Name" in which you have downloaded the code:
            <pre><code>

CREATE USER 'weather_cli'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON <folder_name> TO 'weather_cli'@'localhost';
FLUSH PRIVILEGES;
</code></pre>

</li>
</ul>

<h3>4. Run the Application</h3>
    <ul>
        <li>In the <strong>Code Folder</strong>, open a terminal (cmd) and run:
            <pre><code>python main.py</code></pre>
        </li>
    </ul>

<h2> Application Flow</h2>
    <ol>
        <li><strong>Login/Signup:</strong>
            <ul>
                <li>Enter <strong>userID</strong> and <strong>password</strong> to log in.</li>
                <li>If you don't have an account, select <strong>2</strong> to sign up (name, password, unique userID, mobile, and security_phrase required).</li>
            </ul>
        </li>
        <li><strong>Password Reset:</strong>
            <ul>
                <li>If you've forgotten your password, select <strong>3</strong> to reset it using your <strong>userID</strong> and <strong>security phrase</strong>.</li>
            </ul>
        </li>
        <li><strong>User Interface After Login:</strong><br>
            After logging in, you’ll see the number of API calls left (out of 20) at the top.
            <ul>
                <li><strong>View Profile:</strong> Displays your name, mobile number, and user ID.</li>
                <li><strong>Fetch Weather Data:</strong> Enter the city, state, and country to retrieve the weather data. This will be saved to the <strong>WEATHER_LOGS</strong> database.</li>
                <li><strong>View Logs:</strong> Shows previously viewed weather logs with timestamps.</li>
                <li><strong>Delete Logs:</strong> Allows you to delete specific logs using the row ID.</li>
                <li><strong>Log Out:</strong> Logs out and returns you to the login/signup section.</li>
            </ul>
        </li>
    </ol>

<h2> Validations</h2>
    <ul>
        <li><strong>Unique User IDs:</strong> User IDs must be unique. If a userID already exists, you will be prompted to choose a new one.</li>
        <li><strong>Password Validation:</strong>
            <ul>
                <li>Password must be at least 8 characters long.</li>
                <li>Must contain at least one lowercase letter, one uppercase letter, one digit, and one special symbol.</li>
            </ul>
        </li>
        <li><strong>Mobile Number:</strong> Must be 10 digits long (Indian mobile number format).</li>
        <li><strong>Security Phrase:</strong> Used to reset your password. Both password and security phrase are hashed using SHA-256 before being stored.</li>
    </ul>

<h2> API Call Limitation</h2>
    <ul>
        <li>Users can make a maximum of 20 API calls in a 24-hour period. Once the API call limit reaches 0, you will not be able to make further requests until the next 24-hour cycle.</li>
    </ul>

<h2>Database Schema</h2>

<h3>1. USERS Table</h3>
    <table border="1">
        <tr>
            <th>Attribute</th>
            <th>Type</th>
            <th>Description</th>
        </tr>
        <tr>
            <td>u_ID</td>
            <td>Varchar</td>
            <td>Stores the unique user ID of the user.</td>
        </tr>
        <tr>
            <td>name</td>
            <td>Varchar</td>
            <td>Stores the user's name.</td>
        </tr>
        <tr>
            <td>password</td>
            <td>Char</td>
            <td>Stores the hashed password (SHA-256).</td>
        </tr>
        <tr>
            <td>mobile</td>
            <td>Varchar</td>
            <td>Stores the user's mobile number.</td>
        </tr>
        <tr>
            <td>security_phrase</td>
            <td>Char</td>
            <td>Stores the hashed security phrase (SHA-256).</td>
        </tr>
    </table>

<h3>2. API_USAGE Table</h3>
    <table border="1">
        <tr>
            <th>Attribute</th>
            <th>Type</th>
            <th>Description</th>
        </tr>
        <tr>
            <td>id</td>
            <td>Int</td>
            <td>Primary key to uniquely identify each record.</td>
        </tr>
        <tr>
            <td>user_id</td>
            <td>Varchar</td>
            <td>Foreign key to the <strong>USERS</strong> table, linking each record to a specific user.</td>
        </tr>
        <tr>
            <td>last_update</td>
            <td>Timestamp</td>
            <td>Stores the timestamp when the API call count resets (every 24 hours).</td>
        </tr>
        <tr>
            <td>request_count</td>
            <td>Int</td>
            <td>Keeps track of the user's remaining API call count (maximum of 20 per 24 hours).</td>
        </tr>
    </table>

<h3>3. WEATHER_LOGS Table</h3>
    <table border="1">
        <tr>
            <th>Attribute</th>
            <th>Type</th>
            <th>Description</th>
        </tr>
        <tr>
            <td>id</td>
            <td>Int</td>
            <td>Primary key, used to uniquely identify weather log records.</td>
        </tr>
        <tr>
            <td>timestamp</td>
            <td>Datetime</td>
            <td>Timestamp when the API call was made.</td>
        </tr>
        <tr>
            <td>location</td>
            <td>Varchar</td>
            <td>The city/state/country searched for weather information.</td>
        </tr>
        <tr>
            <td>temperature</td>
            <td>Varchar</td>
            <td>Temperature in Celsius for the specified location.</td>
        </tr>
        <tr>
            <td>humidity</td>
            <td>Varchar</td>
            <td>Humidity level for the specified location.</td>
        </tr>
        <tr>
            <td>weather_conditions</td>
            <td>Varchar</td>
            <td>Weather conditions (e.g., cloudy, rainy, sunny) for the specified location.</td>
        </tr>
        <tr>
            <td>wind_speed</td>
            <td>Varchar</td>
            <td>Wind speed for the specified location.</td>
        </tr>
        <tr>
            <td>u_ID</td>
            <td>Varchar</td>
            <td>Foreign key to the <strong>USERS</strong> table, indicating which user made the request.</td>
        </tr>
    </table>
