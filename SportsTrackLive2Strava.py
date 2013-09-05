import ConfigParser
import os
import cookielib
import urllib2
import MultipartPostHandler
import urllib
import re
import zipfile

def LoginAtStrava(url) :
	cookie_jar = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar), MultipartPostHandler.MultipartPostHandler)

	# acquire cookie
	home = opener.open(url)
	text = home.read()

	# Get authenticity_token
	try:
		token = re.search('"authenticity_token" type="hidden" value="(.+?)"', text).group(1)
	except AttributeError:
		print 'Cannot find token'
		return
	
	print 'found token:' + token

	# Login
	loginData = urllib.urlencode({
		'utf8' : '&#x2713;',
		'authenticity_token' : token,
		'plan' : '',
		'email' : 'user', 
		'password' : 'pass'})
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
	

def LoginAtSportstracker(url) :
	cookie_jar = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
	
	# acquire cookie
	home = opener.open(url)

	# Login
	loginData = urllib.urlencode({
		'userCredentialsForm.userCredentials.email' : 'user', 
		'userCredentialsForm.userCredentials.password' : 'pass'})
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
	try:
		userId = re.search('track\/gpx\?userid=(.+?)">', text).group(1)
	except AttributeError:
		print 'could not find user id'
		return False

	print userId

	DownloadZipFile(opener, "http://www.sportstracklive.com/track/gpx?userid=" + userId)
	
	return True
	
def DownloadZipFile(urlOpener, url) :
	file = urlOpener.open(url)
	print "downloading zip file with gpx data..."
	
	# Open our local file for writing
	with open(os.path.basename("Sportstracklive.zip"), "wb") as local_file:
		local_file.write(file.read())
	
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
	print '---------------------------------'
	print 'Starting Sportstracklive 2 Strava'
	print '---------------------------------\r\n'
	print '1 - Reading program settings'
	# read settings
	try:
		config = ConfigParser.ConfigParser()
		config.readfp(open('settings.ini'))
	except:
		print 'Could not read settings file, exiting'
		return -1
	
	print '2 - Login at sportstrackerlive and download file'
	# login to sportstracker and get zip file.
	LoginAtSportstracker(config.get('SportsTrackLive', 'BaseUrl') + config.get('SportsTrackLive', 'LoginUri'))
		
	print '3 - Extract zip file'
	ExtractZipFile('Sportstracklive.zip', 'gpx')
	
	print '4 - Login at sportstrackerlive and upload files'
	# login to strava and upload file.
	#LoginAtStrava(config.get('Strava', 'BaseUrl') + config.get('Strava', 'LoginUri'))
	

	
	
	#ReadGpxFile()
	#ProcessGpxFile()
	print '---------------------------------'
	print 'End Sportstracklive 2 Strava'
	print 'Now, you\'re an athlete!'
	print 'Enjoy cycling running, and cheers, N.'
	print '---------------------------------\r\n'	
	
if __name__ == "__main__":
    main()
