from PIL import Image

import scipy

import scipy.misc

import scipy.cluster

insertPix = []
def removeBackground(clust):
	insertPix = []
	NUM_CLUSTERS = clust #Define Number of Clusters to be removed
	print 'reading image' 
	im = Image.open('Test Images/testimage.png') #Open Image Before Pixel Removal
	w, h = im.size #Get Image Width and Height
	tpix = w*h #Total Pixels
	ar = scipy.misc.fromimage(im) #Return as Numpy Array
	shape = ar.shape #Get Array Shape
	ar = ar.reshape(scipy.product(shape[:2]), shape[2]) #Get Product of Array Values

	print 'finding clusters'
	codes, dist = scipy.cluster.vq.kmeans(ar.astype(float), NUM_CLUSTERS) #Get Color Codes of Clusters
	print 'cluster centres:\n', codes

	vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
	counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

	index_max = scipy.argmax(counts)                    # find most frequent
	peak = codes[index_max] #Get Largest Cluster
	j = im
	l = Image.new("RGB", (w,h),"White")
	#j.show() Show Image Before Removal
	j = j.convert("RGBA") #Convert to RGBA Format
	d = 0 #Height Counter
	tpix = w*h #Total Pixels
	c=0 #Width Counter
	p = 0 #Total Pixel Change Counter
	print("Removing Background")
	def almostEquals(a,b,thres=110):
	    return all(abs(a[i]-b[i])<thres for i in range(len(a))) #Check How Close a Pixel Resembles a Specific Color in Image
	if clust == 2: 
		for x in range(0, tpix): 
			if c==w:
				d=d+1
				c=0
			e,f,g,i = j.getpixel((c,d)) #Set Values of RGBA For Current Pixel
			if almostEquals((e,f,g), (codes[0][0], codes[0][1], codes[0][2])) or almostEquals((e,f,g), (codes[1][0], codes[1][1], codes[1][2])): #Check if Almost Equals Two Cluster Colors
				c=c+1
			else:
				l.putpixel((c,d),(0,0,0,0))
				insertPix.append([c,d])
				c=c+1
				p=p+1
	if clust==1:
		for x in range(0, tpix): 
			if c==w:
				d=d+1
				c=0
			e,f,g,i = j.getpixel((c,d)) #Pixel Values
			if almostEquals((e,f,g), (peak[0], peak[1], peak[2])): 
				c=c+1
			else:
				l.putpixel((c,d),(0,0,0,0))
				insertPix.append([c,d])
				c=c+1
				p=p+1
	if clust==2 and p<(tpix/10) and p<(tpix/1.5): #If Not Enough Pixels Are Placed (Image only 2 colors), Rerun but only remove largest cluster
		return removeBackground(1)
	else:
		return insertPix