import matplotlib.pyplot as plt
import numpy as np
import cv2

class ImageConverter(object):
    # Crop whitespace around image.
    def crop_image(self, img, tol=255):
        # img is image data
        # tol  is tolerance
        mask = img<tol
        return img[np.ix_(mask.any(1),mask.any(0))]
    
    def square_image(self, img):
        # Get Shape
        imgSize = img.shape[0:3]
        maxSize = max(imgSize)
        minSize = min(imgSize)
        
        # Get difference in sides
        diff = maxSize - minSize
        
        # If not square
        if diff > 0:
            # Determine smaller axis
            axis = imgSize.index(minSize)
            # Left/Right
            if axis == 1:
                img = cv2.copyMakeBorder(img, 0, 0, int(diff/2), int(diff/2), cv2.BORDER_CONSTANT, value=[255, 255, 255])
            else:
                img = cv2.copyMakeBorder(img, int(diff/2), int(diff/2), 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        return img
            
    
    def convert(self, filename, destination):
        # Read image
        origImg = cv2.imread(filename, 0)
        
        # Convert to binary image with auto threshold.
        (thresh, binImg) = cv2.threshold(origImg, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
        # Crop edges
        smImg = self.crop_image(binImg)
        
        # Make Image Square.
        smImg = self.square_image(smImg)
        
        # Downsample image to 50x50
        smImg = cv2.resize(smImg, (50, 50))
        
        # Reconvert to binary image with auto threshold.
        (thresh, smImg) = cv2.threshold(smImg, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
        # Enlarge with no interpolation.
        lrgImg = []
        for row in smImg:
            newRow = []
            for x in range(len(row)):
                newRow.append(row[x])
                newRow.extend([255, 255, 255])
            lrgImg.append(newRow[:200])
            for i in range(3):
                lrgImg.append([255 for x in range(200)])
        
        # Convert colour to binary matrix
        matrix = []
        for row in lrgImg:
            matrix.append("".join(["0" if (x > 0) else "1" for x in row]))
            
        # Get new filename.
        filename = filename.split('/')[-1]
        filename = filename.split('.')[0]
        
        # Write binary matrix to file.
        path = destination + filename + ".txt"
        with open(path, 'wt') as f:
            for line in matrix:
                f.write(line + "\n")
        print("Saved as %s" % path)
        
        return path
            