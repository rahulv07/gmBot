from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import datetime
from imutils import paths
import cv2
import shutil
import os

accountLoginURL = 'https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/&ec=GAZAAQ'
gHomeURL = 'https://google.com/'

mail_address = '19u230@psgtech.ac.in'
with open('password.txt','r') as f:
	lines = f.readlines()
	password = lines[0]
	parentDir = lines[1]

currentTime = datetime.datetime.now()
today = currentTime.day
month = currentTime.month
year = currentTime.year

def classURL(option):
	if option==1:
		classDir = f'Industrial_Instrumentation/{today}-{month}-{year}'
		return 'https://meet.google.com/fkq-tcqk-gte',classDir # Industrial instrumentation 1
	if option==2:
		classDir = f'Control_Systems_2/{today}-{month}-{year}'
		return 'https://meet.google.com/qgn-myxw-duo',classDir # Control Systems 2
	if option==3:
		classDir = f'MP_MC/{today}-{month}-{year}'
		return 'https://meet.google.com/vcj-qsmb-iev',classDir # MP/MC 
	if option==4:
		classDir = f'DSP/{today}-{month}-{year}'
		return 'https://meet.google.com/cmy-vpzo-tfu' ,classDir # DSP
	if option==5:
		classDir = f'OS/{today}-{month}-{year}'
		return 'https://meet.google.com/izk-qqox-eas',classDir # OS
	if option==6:
		classDir = f'Computer_Networks/{today}-{month}-{year}'
		return 'https://meet.google.com/kvg-vupm-ipt',classDir  # Computer Networks
	if option==7:
		classDir = f'MP_MC_DSP_Lab/{today}-{month}-{year}'
		return 'https://meet.google.com/jxz-tvgf-aci',classDir  # MP/MC and DSP lab
	if option==8:
		classDir = f'CS Lab/{today}-{month}-{year}'
		return 'https://meet.google.com/imi-ybdp-abb' ,classDir # Control Systems lab
	if option==9:
		classDir = f'Testing/{today}-{month}-{year}'
		return 'https://meet.google.com/rek-qgeq-nbh',classDir

def createDirectory(parentDir,classDir):
	path = os.path.join(parentDir,classDir)
	try:
		os.makedirs(path,exist_ok=True)
		return path
	except OSError as error:
		print(error)
		return path

def googleLogin(mail_address, password):
	
	driver.get(accountLoginURL)

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
	driver.get(gHomeURL)
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


def joinMeet():
	time.sleep(5)
	driver.implicitly_wait(2000)
	driver.find_element_by_css_selector(
		'div.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt').click()


def takeScreenshot(date,month,hr,id):
	try:
		#screen = driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[2]/div[1]/div[3]/div[1]/div[3]')
		screen = driver.find_element_by_tag_name('video')
	#If there is no 'presenting' web element
	except:
		screen = None

	if screen is not None:
		screen.screenshot(f'lastClassSS/{date}-{month}-{hr}-{id}.png')
		print(f'\nScreenshot taken {date}-{month}-{id}')
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

choiceValid = False
while ~choiceValid:
	print('\nChoices:\nIndustrial Instrumentation - 1\nControl Systems 2 - 2\nMP & MC - 3\nDSP - 4\nOS - 5\nComputer Networks - 6\nMpMc & DSP lab - 7\nControl Systems Lab - 8')
	choice = int(input('\nEnter your choice: '))
	if choice>=1 and choice<=9:
		choiceValid = True
		break

[meetURL,classDir] = classURL(choice)

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

googleLogin(mail_address, password)

driver.get(meetURL)
turnOffMicCam()
joinMeet()
time.sleep(5)

id = 1
while(studentCount()>10):
	time.sleep(30)
	if studentCount()<=10:
		break
	time.sleep(30)
	if studentCount()<=10:
		break
	captured = takeScreenshot(today,month,currentTime.hour,id)
	if captured:
		id+=1	
	time.sleep(30)
	if studentCount()<=10:
		break
	time.sleep(30)
	if studentCount()<=10:
		break

print('\nMeeting has ended!')
driver.quit()

print('\nProcessing Images!')

print('Organizing')
haystackDir = createDirectory(parentDir,classDir)
needleDir = 'lastClassSS/'
haystackImages = list(paths.list_images(haystackDir))
needleImages = list(paths.list_images(needleDir))
haystack = {}

#Hashing function that converts images to hashes
def dhash(image,hashsize=8):
	#Resize image to 9x8 pixels
	resized = cv2.resize(image, (hashsize + 1, hashsize))
	#compute the difference between the adjacent pixels
	diff = resized[:, 1:] > resized[:, :-1]
	#Return the hash value of the image
	return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

#Computing the hash values of images in the main directory
for h in haystackImages:
	image = cv2.imread(h)
	if image is None:
		continue
	#converting image to grayscale
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#Computing the hash value of the image
	imageHash = dhash(image)
	l = haystack.get(imageHash,'')
	l+=h
	haystack[imageHash] = l

#Computing the hash value of the taken screenshots
for n in needleImages:
	image = cv2.imread(n)
	if image is None:
		continue
	#converting image to grayscale
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#Computing the hash value
	imageHash = dhash(image)
	matchedImages = haystack.get(imageHash,None)

	#If the image is not present in the main directory(unique image), move the image to the main directory
	if matchedImages is None:
		ll = haystack.get(imageHash,'')
		ll+=n
		haystack[imageHash] = ll
		shutil.move(n,haystackDir)

#Delete all the remaining screenshots (not a unique image)
for n in os.listdir(needleDir):
    os.remove(os.path.join(needleDir, n))

print('\nSaving Images done!\n')