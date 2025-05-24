from flask import Flask, request, render_template
import requests, json
import gcs_utils
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/weather', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        lat = request.form.get('lat')
        lon = request.form.get('lon')
        start = request.form.get('start')
        end = request.form.get('end')

        if not all([lat, lon, start, end]):
            return "Missing input values", 400

        open_meteo_url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            'latitude': lat,
            'longitude': lon,
            'start_date': start,
            'end_date': end,
            'daily': ['temperature_2m_max', 'temperature_2m_min', 'temperature_2m_mean', 'apparent_temperature_max', 'apparent_temperature_min', 'apparent_temperature_mean']
        }

        try:
            response = requests.get(open_meteo_url, params=params)
            response.raise_for_status()
            data = response.json()

            json_file = f"weather_data_{lat}_{lon}_{start}_to_{end}.json"
            bucket_name = app.config['BUCKET_NAME']
            gcs_utils.upload_json_to_gcs(bucket_name, data, json_file)

            return render_template('success.html', filename=json_file)

        except requests.RequestException as e:
            return f"Error fetching weather data: {e}", 500

    return render_template('index.html')

@app.route('/list-weather-files', methods=['GET'])
def list_weather_data():
    try:
        data = gcs_utils.list_files_in_gcs(app.config['BUCKET_NAME'])
        return render_template('result.html', data)
    except requests.RequestException as e:
        return f"Error fetching list of weather data: {e}", 500
    
@app.route('/-weather-file-content', methods=['GET', 'POST'])
def list_weather_data():
    if request.method == 'POST':
        filename = request.form.get('filename')
        if not filename:
            return "Missing filename", 400
        try:
            data = gcs_utils.get_weather_data_from_gcs(app.config['BUCKET_NAME'], filename)
            return render_template('result.html', data)
        except requests.RequestException as e:
            return f"Error fetching weather data: {e}", 500
    else:
        return render_template('getweather.html')


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
