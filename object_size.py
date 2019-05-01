import numpy as np
import cv2
import json
import urllib.request
import cloudinary
import cloudinary.uploader
import cloudinary.api

def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)
 
def colour(image, contour):
	mask = np.zeros(image.shape[:2], dtype="uint8")
	cv2.drawContours(mask, [contour], -1, 255, -1)
	mask = cv2.erode(mask, None, iterations=2)
	mean = cv2.mean(image, mask=mask)[:3]
	return mean

def imageProcessing(imageURL, scarID):
    # load the image, convert it to grayscale, and blur it slightly
	resp = urllib.request.urlopen(imageURL)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)

	# img = io.imread(imageURL)
	# image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	blurred = cv2.pyrMeanShiftFiltering(image, 21,35)
	#blurred = cv2.GaussianBlur(image, (7,7), 0)
	gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

	# perform edge detection, then perform a dilation + erosion to
	# close gaps in between object edges
	edged = cv2.Canny(gray, 2,20)
	#edged = cv2.dilate(edged, None, iterations=1)
	#edged = cv2.erode(edged, None, iterations=1)
	#edged = cv2.morphologyEx(edged, cv2.MORPH_GRADIENT, None)

	# find contours in the edge map
	cnts = cv2.findContours(edged, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	cnts = cnts[0]
	pixelsPerMetric = None

	# loop over the contours individually
	for c in cnts:
		# if the contour is not sufficiently large, ignore it
		if cv2.contourArea(c) < 1000:
			continue

		# compute the rotated bounding box of the contour
		orig = image.copy()
		box = cv2.minAreaRect(c)
		box = cv2.boxPoints(box)
		box = np.array(box, dtype="int")


		cv2.drawContours(orig, [box.astype("int")], -1, (255, 255, 255), 2)

		# loop over the original points and draw them
		for (x, y) in box:
			cv2.circle(orig, (int(x), int(y)), 5, (255, 255, 255), -1)

		# unpack the ordered bounding box, then compute the midpoint
		# between the top-left and top-right coordinates, followed by
		# the midpoint between bottom-left and bottom-right coordinates
		(tl, tr, br, bl) = box
		(tltrX, tltrY) = midpoint(tl, tr)
		(blbrX, blbrY) = midpoint(bl, br)

		# compute the midpoint between the top-left and top-right points,
		# followed by the midpoint between the top-righ and bottom-right
		(tlblX, tlblY) = midpoint(tl, bl)
		(trbrX, trbrY) = midpoint(tr, br)

		# draw the midpoints on the image
		cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 255, 255), -1)
		cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 255, 255), -1)
		cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 255, 255), -1)
		cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 255, 255), -1)

		# draw lines between the midpoints
		cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
			(255, 255, 255), 2)
		cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
			(255, 255, 255), 2)

		# compute the Euclidean distance between the midpoints

		dA = np.linalg.norm(np.array((tltrX, tltrY))-np.array((blbrX, blbrY)))
		dB = np.linalg.norm(np.array((tlblX, tlblY))-np.array((trbrX, trbrY)))
		# dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
		# dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

		# if the pixels per metric has not been initialized, then
		# compute it as the ratio of pixels to supplied metric
		# (in this case, inches)
		if pixelsPerMetric is None:
			pixelsPerMetric = dB / 40.0 #<- £1 is 23.03mm in diameter

		# compute the size of the object
		dimA = dA / pixelsPerMetric
		dimB = dB / pixelsPerMetric

		# draw the object sizes on the image
		cv2.putText(orig, "{:.1f}mm".format(dimA),
			(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
			0.65, (0, 0, 255), 2)
		cv2.putText(orig, "{:.1f}mm".format(dimB),
			(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
			0.65, (0, 0, 255), 2)
		
		contourArea = cv2.contourArea(c) / pixelsPerMetric
		cv2.putText(orig, "{:.1f}mm^2".format(contourArea),
			(int(tltrX - 50), int(tltrY - 50)), cv2.FONT_HERSHEY_SIMPLEX,
			0.65, (0, 0, 255), 2)
		averageColour = colour(orig, c) #backwards
		scarColour = tuple(reversed(averageColour))
		#draw contours
		cv2.drawContours(orig, c, -1, (0,0,255), 2)

		#save modified image in temp folder
		path = "./tmp/" + str(scarID) + ".jpg"
		cv2.imwrite(path, orig)

		#post request to cloudinary
		response  = cloudinary.uploader.unsigned_upload(path, "woundscars", cloud_name = 'nikolamus')	
		newImageURL = response['url']

		return newImageURL, scarID, dimA, dimB, contourArea, scarColour


# example_imageURL = "https://res.cloudinary.com/nikolamus/image/upload/v1556297408/wounds-scars/tfk1zzbb26d63avaj1ib.png"
# example_url = "https://www.google.com/"
# example_scarID = 1
# imageProcessing(example_imageURL,example_scarID)

