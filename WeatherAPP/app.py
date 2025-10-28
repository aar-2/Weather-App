from flask import Flask,request,jsonify
from weatherutils import init_db, fetch_weatherutils
app=Flask(__name__)
init_db()

@app.route('/weather',methods=['GET'])
def get_weather():
    city=request.args.get('city')
    if not city:
       
        return jsonify({'error':'City parameter is required'}),400
    data,cached=fetch_weatherutils(city)
    #weather_data=fetch_weatherutils(city)
    import json
    try:
        data_json = json.loads(data)
    except Exception:
        data_json = {"raw_data": data}

    return jsonify({
        "city": city,
        "data": data_json,
        "cached": cached})
if __name__ == "__main__":
    app.run(debug=True)

