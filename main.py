from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import datetime
from imutils import paths
import cv2
import shutil
import os

currentTime = datetime.datetime.now()
today = currentTime.day
month = currentTime.month


def googleLogin(mail_address, password):
	# Login Page
	driver.get(
		'https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/&ec=GAZAAQ')

	# input Gmail
	driver.find_element_by_id("identifierId").send_keys(mail_address)
	driver.find_element_by_id("identifierNext").click()
	driver.implicitly_wait(10)

	# input Password
	driver.find_element_by_xpath(
		'//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
	driver.implicitly_wait(10)
	driver.find_element_by_id("passwordNext").click()
	driver.implicitly_wait(10)

	# go to google home page
	driver.get('https://google.com/')
	driver.implicitly_wait(100)


def turnOffMicCam():
	# turn off Microphone
	time.sleep(2)
	driver.find_element_by_xpath(
		'//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[4]/div/div/div[1]/div[1]/div/div[4]/div[1]/div/div/div').click()
	driver.implicitly_wait(3000)

	# turn off camera
	time.sleep(1)
	driver.find_element_by_xpath(
		'//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[4]/div/div/div[1]/div[1]/div/div[4]/div[2]/div/div').click()
	driver.implicitly_wait(3000)


def joinNow():
	# Join meet
	time.sleep(5)
	driver.implicitly_wait(2000)
	driver.find_element_by_css_selector(
		'div.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt').click()


def AskToJoin():
	# Ask to Join meet
	time.sleep(5)
	driver.implicitly_wait(2000)
	driver.find_element_by_css_selector(
		'div.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt').click()
	# Ask to join and join now buttons have same xpaths

def takeScreenshot(date,month,hr,id):
	time.sleep(10)
	try:
		screen = driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[2]/div[1]/div[2]/div[1]/div[3]')
	except:
		screen = None
	if screen is not None:
		screen.screenshot(f'lastClassSS/{date}-{month}-{hr}-{id}.png')
		return True
	else:
		return False

def studentCount():
	try:
		number = int(driver.find_element_by_class_name('uGOf1d').text)
		if number>1:
			return number
		else:
			driver.quit()
			return -1
	except:
		return -1

# assign email id and password
mail_address = '19u230@psgtech.ac.in'
with open('password.txt','r') as f:
	password = f.readline()

# create chrome instamce
opt = Options()
opt.add_argument('--disable-blink-features=AutomationControlled')
opt.add_argument('--start-maximized')
opt.add_experimental_option("prefs", {
	"profile.default_content_setting_values.media_stream_mic": 1,
	"profile.default_content_setting_values.media_stream_camera": 1,
	"profile.default_content_setting_values.geolocation": 0,
	"profile.default_content_setting_values.notifications": 1
})
driver = webdriver.Chrome(options=opt)

# login to Google account
googleLogin(mail_address, password)

# go to google meet
driver.get('https://meet.google.com/zba-wdyx-tfs')
turnOffMicCam()
# AskToJoin()
joinNow()
time.sleep(5)

id = 1
while(studentCount()>1):
	captured = takeScreenshot(today,month,currentTime.hour,id)
	id+=1
	if not captured:
		break

driver.quit()
# Sorting Screenshots

def dhash(image,hashsize=8):
	resized = cv2.resize(image, (hashsize + 1, hashsize))
	# compute the (relative) horizontal gradient between adjacent
	# column pixels
	diff = resized[:, 1:] > resized[:, :-1]
	# convert the difference image to a hash
	return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

haystackDir = '/home/rahul/Documents/College/classScreenshots'
needleDir = '/home/rahul/Noah-Willis/python projects/gmeetAutomation/lastClassSS/'
haystackImages = list(paths.list_images(haystackDir))
needleImages = list(paths.list_images(needleDir))


haystack = {}

for h in haystackImages:
	# load the image from disk
	image = cv2.imread(h)
	# if the image is None then we could not load it from disk (so
	# skip it)
	if image is None:
		continue
	# convert the image to grayscale and compute the hash
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	imageHash = dhash(image)
	# update the haystack dictionary
	l = haystack.get(imageHash,'')
	l+=h
	haystack[imageHash] = l

# loop over the needle paths
for n in needleImages:
	# load the image from disk
	image = cv2.imread(n)
	# if the image is None then we could not load it from disk (so
	# skip it)
	if image is None:
		continue
	# convert the image to grayscale and compute the hash
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	imageHash = dhash(image)
	# grab all image paths that match the hash
	matchedImages = haystack.get(imageHash,None)

	if matchedImages is None:
		ll = haystack.get(imageHash,'')
		ll+=n
		haystack[imageHash] = ll
		shutil.move(n,haystackDir)

for n in os.listdir(needleDir):
    os.remove(os.path.join(needleDir, n))

