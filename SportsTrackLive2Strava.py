import ConfigParser
import os
import cookielib
import urllib2
import MultipartPostHandler
import urllib
import re
import zipfile

def LoginStrava(url) :
	cookie_jar = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar), MultipartPostHandler.MultipartPostHandler)

	# acquire cookie
	home = opener.open(url)
	text = home.read()

	# Get authenticity_token
	try:

#"authenticity_token" type="hidden" value="

# input name="authenticity_token"
		token = re.search('"authenticity_token" type="hidden" value="(.+?)"', text).group(1)
	except AttributeError:
		# AAA, ZZZ not found in the original string
		token = '' # apply your error handling
	
	print token

	# Login
	loginData = urllib.urlencode({
		'utf8' : '&#x2713;',
		'authenticity_token' : token,
		'plan' : '',
		'email' : 'username', 
		'password' : 'password'})
	try:
		response = opener.open("https://www.strava.com/session", loginData);
	except urllib2.HTTPError, e:
		if e.code == 401:
			print 'not authorized'
		elif e.code == 404:
			print 'not found'
		elif e.code == 503:
			print 'service unavailable'
		else:
			print 'unknown error: '
	else:
		print 'Successfully logged in'

#	print response.read()

	# Get upload file page
	try:
		response = opener.open("http://www.strava.com/upload/select");
	except urllib2.HTTPError, e:
		if e.code == 401:
			print 'not authorized'
		elif e.code == 404:
			print 'not found'
		elif e.code == 503:
			print 'service unavailable'
		else:
			print 'unknown error: '
	else:
		print 'Successfully got upload page'

	print token
	print response.read()
	
	uploadData = urllib.urlencode({
		'_method' : 'post',
		'authenticity_token' : token,
		'files[]' : open('/home/nicky/SportsTrackLive2Strava/1.gpx', "rb")})
	
	params = { "_method" : "post", "authenticity_token" : token,
             "files[]" : open("/home/nicky/SportsTrackLive2Strava/1.gpx", "rb") }

	try:
		response = opener.open("http://www.strava.com/upload/files", params);
	except urllib2.HTTPError, e:
		if e.code == 401:
			print 'not authorized'
		elif e.code == 404:
			print 'not found'
		elif e.code == 503:
			print 'service unavailable'
		else:
			print e.code
			print 'unknown error: '
	else:
		print 'Successfully uploaded file'
	print response.read()
	

def Login(url) :
	cookie_jar = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
	
	# acquire cookie
	home = opener.open(url)

	# Login
	loginData = urllib.urlencode({
		'userCredentialsForm.userCredentials.email' : 'username', 
		'userCredentialsForm.userCredentials.password' : 'password'})
	try:
		response = opener.open(url, loginData);
	except urllib2.HTTPError, e:
		if e.code == 401:
			print 'not authorized'
		elif e.code == 404:
			print 'not found'
		elif e.code == 503:
			print 'service unavailable'
		else:
			print 'unknown error: '
	else:
		print 'Successfully logged in'


		
	
	text = response.read()
	userId = -1;
	try:
		found = re.search('track\/gpx\?userid=(.+?)">', text).group(1)
	except AttributeError:
		# AAA, ZZZ not found in the original string
		found = '' # apply your error handling
	
	
	print found
	userId = found
	text = 'http://www.sportstracklive.com/track/gpx?userid=19981">'

	try:
		found = re.search('track\/gpx\?userid=(.+?)">', text).group(1)
	except AttributeError:
		# AAA, ZZZ not found in the original string
		found = '' # apply your error handling

	print found
	
	zipUrl = "http://www.sportstracklive.com/track/gpx?userid=" + userId	
	file = opener.open(zipUrl)
	print "downloading zip file with gpx data"
	
	# Open our local file for writing
	with open(os.path.basename("Sportstracklive.zip"), "wb") as local_file:
		local_file.write(file.read())
	

#todo

#try:
# urllib2.urlopen(url)
# except urllib2.HTTPError, e:
#    print e.code
#except urllib2.URLError, e:
#    print e.args
	
	print "-------"	
	
def DownloadZipFile() :
	print "downloaded zipfile"
	
def ExtractZipFile(filename, targetdir) :
	try:
		with zipfile.ZipFile(filename) as f :
			f.extractall(targetdir)
			print "extracted zipfile"
	except IOError:
	   print 'No file available'

def ReadGpxFile() :
	print "read gpxfile"
	
def ProcessGpxFile() :
	print "processed gpxfile"
	
def main() :
	config = ConfigParser.ConfigParser()
	config.readfp(open('settings.ini'))
	
	# login to sportstracker and get zip file.
	Login(config.get('SportsTrackLive', 'BaseUrl') + config.get('SportsTrackLive', 'LoginUri'))
	
	# login to strava and upload file.
	#LoginStrava(config.get('Strava', 'BaseUrl') + config.get('Strava', 'LoginUri'))
	

	DownloadZipFile()
	ExtractZipFile('Sportstracklive.zip', 'gpx')
	ReadGpxFile()
	ProcessGpxFile()
	
if __name__ == "__main__":
    main()
