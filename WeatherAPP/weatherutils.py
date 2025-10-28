import sqlite3
import requests
import datetime,json
db_name='weather_data.db'

def init_db():
   
    conn=sqlite3.connect(db_name)
    c=conn.cursor()
    c.execute('''
                    CREATE TABLE IF NOT EXISTS weather(
              
                                    city TEXT PRIMARY KEY,
                                    data TEXT,
                                    timestamp DATETIME)
                            ''')
    conn.commit()
    conn.close()
 
def fetch_weatherutils(city):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Check cache first
    c.execute("SELECT data, timestamp FROM weather WHERE city = ?", (city,))
    row = c.fetchone()
    if row:
        data, timestamp = row
        age = (datetime.datetime.now() - datetime.datetime.fromisoformat(timestamp)).seconds
        if age < 3600:  # 1 hour freshness
            conn.close()
            return data, True  # Cached

    # Fetch from API
    api_key = "f8abb352fd936982b241c33f132c653e"
    url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    #url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"


    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises HTTPError for 4xx/5xx
        data = response.json()       # Convert JSON text to dict
    except requests.exceptions.HTTPError as e:
        conn.close()
        return {"error": f"HTTP error: {e}"}, False
    except requests.exceptions.RequestException as e:
        conn.close()
        return {"error": f"Request failed: {e}"}, False

    # Cache the result
    c.execute("REPLACE INTO weather (city, data, timestamp) VALUES (?, ?, ?)",
              (city, json.dumps(data), datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

    return data, False
