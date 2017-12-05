from pprint import pprint
import urllib2, urllib, json
import hashlib

# init conf
verbose= False
db_cities="cities.db"
src_cities="cities.txt"
cs_cities="cities.cs"
new_checksum=""

# get city id on yahoo webservice
baseurl = "https://query.yahooapis.com/v1/public/yql?"
yql_query = "select * from geo.places(1) where text=\"%s, BR\""

def getWoeid(name):
	yquery = yql_query % name
	yql_url = baseurl + urllib.urlencode({'q':yquery}) + "&format=json"
	result = urllib2.urlopen(yql_url).read()
	data = json.loads(result)
	#pprint(data)
	return(data['query']['results']['place'])

def md5sum(filename, blocksize=65536):
	hash = hashlib.md5()
	with open(filename, "rb") as f:
		for block in iter(lambda: f.read(blocksize), b""):
			hash.update(block)
	return hash.hexdigest()


def check_update():
	global new_checksum
	current_checksum=open(cs_cities).read()
	new_checksum=md5sum(src_cities)

	if verbose:
		pprint("Current checksum %s" % current_checksum)
		pprint("New checksum %s" % new_checksum)

	if current_checksum != new_checksum:
		return True
	else:
		return False

def update_cs():
	global new_checksum
	f = open(cs_cities, "w")
	f.write(new_checksum)
	f.close()
	if verbose:
		pprint("checksum updated!")

def update_db():
	cities=open(src_cities).readlines()
	content = ""
	for city in cities:
		cn = city.strip("\n")
		try:
			res =  getWoeid(cn)
			content = "%s{\"name\":\"%s\", \"id\":\"%s\",\"lat\":\"%s\",\"lon\":\"%s\"}\n" % ( content , res['name'] , res['woeid'], res['centroid']['latitude'] , res['centroid']['longitude']  )
		except:
			print "Ooops! Error getting %s woeid\n" % cn
			break

	if verbose:
		pprint("db content:\n %s" % content)

	f = open(db_cities, "w")
	f.write(content)
	f.close()

def main():
   if check_update():
	   update_db()
	   update_cs()

if __name__ == "__main__":
   main()
