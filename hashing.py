from imutils import paths
import time
import sys
import cv2
import os
import shutil

def dhash(image,hashsize=8):
    # resize the input image, adding a single column (width) so we
	# can compute the horizontal gradient
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