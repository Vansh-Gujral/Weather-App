from django.shortcuts import render
import requests
import datetime
API_KEY_1 = "49553570ad536febff0f85b9ea44ecb7"  
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY_2 = "AIzaSyChTqfNnKASdIRAstpSDmkqyUMJ3a10Ybw"  
SEARCH_ENGINE_ID = "e05119406b4504790"  
def get_weather(city):
    """Helper function to fetch weather data for a city"""
    params = {
        "q": city,
        "appid": API_KEY_1,
        "units": "metric"
    }
    data = requests.get(BASE_URL, params=params).json()

    if data.get("cod") == 200:
        query = city + " 1920x1080"
        city_url = (
            f"https://www.googleapis.com/customsearch/v1"
            f"?q={query}&cx={SEARCH_ENGINE_ID}&searchType=image&num=1"
            f"&start=1&key={API_KEY_2}&imgSize=xlarge"
        )
        data_img = requests.get(city_url).json()
        search_items = data_img.get("items")
        if search_items and len(search_items) > 0:
            image_url = search_items[0]["link"]
        else:
            image_url = "https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg?auto=compress&cs=tinysrgb&w=1600"
        return {
            "temp": data["main"]["temp"],
            "desc": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
            "city": city,
            "date": datetime.date.today(),
            "image_url": image_url
        }
    else:
        return {
            "error": data.get("message", "City not found"),
            "exception_occured": True
        }
def home(request):
    city = "Kashipur" 
    if request.method == "POST" and "city" in request.POST:
        city = request.POST["city"]
    weather_data = get_weather(city)
    return render(request, "index.html", weather_data)
