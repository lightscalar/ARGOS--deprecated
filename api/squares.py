import numpy as np
import cv2
import os

def create_rotated_pics(row, col, size, num_rotations):
    
    img = cv2.imread('shadow.jpg',0)

    images = []
    
    rows,cols = img.shape

    shift_right = col < size/2
    shift_left = col > cols - size/2
    shift_down = row < size/2
    shift_up = row > rows - size/2
    
#    os.makedirs('New_images')

    if shift_right + shift_left + shift_down + shift_up > 0:
        if shift_right is True:
            col = size/2
        if shift_left is True:
            col = cols - size/2
        if shift_down is True:
            row = size/2
        if shift_up is True:
            row = rows - size/2
        col_low = int(col-size/2)
        col_high = int(col+size/2)
        row_low = int(row-size/2)
        row_high = int(row+size/2)
        square = img[row_low:row_high, col_low:col_high]
        images.append(square)
#        cv2.imwrite('New_images/image.jpg',square)

    elif col < size*np.sqrt(2)/2 or col > cols - size*np.sqrt(2)/2 or row < size*np.sqrt(2)/2 or row > rows - size*np.sqrt(2)/2:
        col_low = int(col-size/2)
        col_high = int(col+size/2)
        row_low = int(row-size/2)
        row_high = int(row+size/2)
        square = img[row_low:row_high, col_low:col_high]
        images.append(square)
#        cv2.imwrite('New_images/image.jpg',square)

    else:
        for i in range(num_rotations):
            col_low = int(col-size/2)
            col_high = int(col+size/2)
            row_low = int(row-size/2)
            row_high = int(row+size/2)
            r = int(360/num_rotations)
            rotated_original = cv2.getRotationMatrix2D((col,row),r*i,1)
            rotated = cv2.warpAffine(img,rotated_original,(cols,rows))
            square = rotated[row_low:row_high, col_low:col_high]
            images.append(square)
#            cv2.imwrite('New_images/image'+'{0:0=3d}'.format(i)+'.jpg',square)

    return images

if __name__ == '__main__':
    create_rotated_pics(1200,0,200,4)

