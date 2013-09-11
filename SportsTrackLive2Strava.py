import ConfigParser
import os
import cookielib
import urllib2
import MultipartPostHandler
import urllib
import re
import zipfile
import glob

def ImportToStrava(url, username, password, baseDir, files) :
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
	
	# print 'found token:' + token

	# Login
	loginData = urllib.urlencode({
		'utf8' : '&#x2713;',
		'authenticity_token' : token,
		'plan' : '',
		'email' : username, 
		'password' : password})
	try:
		response = opener.open("https://www.strava.com/session", loginData);
	except urllib2.HTTPError, e:
		print 'unknown error: '
		return
	else:
		print 'Successfully logged in'

	# Get upload file page
	try:
		response = opener.open("http://www.strava.com/upload/select");
	except urllib2.HTTPError, e:
		print 'unknown error: '
		return
	else:
		print 'Successfully got upload page'
	
	# Import files
	for file in files :
		params = { "_method" : "post", "authenticity_token" : token,
				 "files[]" : open(baseDir + file, "rb") }
		try:
			response = opener.open("http://www.strava.com/upload/files", params);
		except urllib2.HTTPError, e:
			print 'unknown error: ' + baseDir + file
		else:
			print 'Successfully uploaded file -->' + baseDir + file
	
	print 'imported all files'
			
def ImportFromSportstracker(url, username, password) :
	cookie_jar = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
	
	# acquire cookie
	home = opener.open(url)

	# Login
	loginData = urllib.urlencode({
		'userCredentialsForm.userCredentials.email' : username, 
		'userCredentialsForm.userCredentials.password' : password})
	try:
		response = opener.open(url, loginData);
	except urllib2.HTTPError, e:
		print 'unknown error: '
		return	
	else:
		print 'Successfully logged in'

	text = response.read()
	try:
		userId = re.search('track\/gpx\?userid=(.+?)">', text).group(1)
	except AttributeError:
		print 'could not find user id'
		return False

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
	
	print '2 - Get credentials for Sportstracklive'
	usernameTracker = raw_input('Enter username Sportstracker: ')
	passwordTracker = raw_input('Enter password Sportstracker: ')
	
	print '3 - Login at sportstrackerlive and download file'
	# login to sportstracker and get zip file.
	ImportFromSportstracker(config.get('SportsTrackLive', 'BaseUrl') + config.get('SportsTrackLive', 'LoginUri'), usernameTracker, passwordTracker)
		
	print '4 - Extract zip file'
	ExtractZipFile('Sportstracklive.zip', 'gpx')
	
	print '5 - Get credentials for Strava'
	usernameStrava = raw_input('Enter username Strava: ')
	passwordStrava = raw_input('Enter password Strava: ')	
	
	print '6 - Login at sportstrackerlive and upload files'
	# login to strava and upload file.
	ImportToStrava(
		config.get('Strava', 'BaseUrl') + config.get('Strava', 'LoginUri'),
		usernameStrava,
		passwordStrava,
		'./gpx/',
		os.listdir('./gpx/'))
	
	print '---------------------------------'
	print 'End Sportstracklive 2 Strava'
	print 'Now, you\'re an athlete!'
	print 'Enjoy cycling and/or running, and cheers, N.'
	print 'twitter: @nickyjaspers'
	print '---------------------------------\r\n'	
	
if __name__ == "__main__":
    main()
