from pprint import pprint
import urllib2, urllib, json, ast, datetime

# init config
db_cities="cities.db"
db_weather="weather.db"
today = datetime.date.today()

# get weather from yahoo webservice
baseurl = "https://query.yahooapis.com/v1/public/yql?"
yql_query = "select * from weather.forecast where woeid=%s"

def getWeather(woeid):
	yquery = yql_query % woeid
	yql_url = baseurl + urllib.urlencode({'q':yquery}) + "&format=json"
	result = urllib2.urlopen(yql_url).read()
	data = json.loads(result)
	return(data['query']['results']['channel'])

def saveResult(content):
   f = open(db_weather, "w")
   f.write(content)
   f.close()

def main():
	cities=open(db_cities).readlines()
	content = ""
	for city in cities:
		x = {}
		cn = city.strip("\n")
		dline = ast.literal_eval(cn)
		try:
			res =  getWeather(dline["id"])

			# conversion fahrenheit to Celsius
			#T(oC) = (T(oF) - 32) x 5/9
			ttemp = ((int(res['item']['condition']['temp']) -32) *5/9)
			thigh = ((int(res['item']['forecast'][1]['high']) - 32) * 5/9)
			tlow = ((int(res['item']['forecast'][1]['low']) - 32) * 5/9)

			content = "%s{\"city\":\"%s\", \"id\":\"%s\",\"lat\":\"%s\",\"lon\":\"%s\", \"date\":\"%s\", \"temp\":\"%s\",\"high\":\"%s\",\"low\":\"%s\",\"text\":\"%s\",\"wind\":\"%s\",\"humi\",\"%s\"}\n" % ( content , res['location']['city'], dline["id"], res['item']['lat'], res['item']['long'], today,  ttemp, thigh, tlow,res['item']['forecast'][1]['text'], res['wind']['speed'] ,res['atmosphere']['humidity'] )
			saveResult(content)
		except:
			print "Ooops! Error getting %s weather\n" % dline['name']
			break

if __name__ == "__main__":
	main()
