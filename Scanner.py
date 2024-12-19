import sys
import numpy as np
import cv2
import math

def calculate_dimensions(approx):
    # Convert to a simpler format for easier processing
    points = approx.reshape(4, 2)

    # Sort the points based on their sum and difference
    points_sum = points.sum(axis=1)  # Sum of x + y
    points_diff = np.diff(points, axis=1)  # Difference of x - y

    top_left = points[np.argmin(points_sum)]
    bottom_right = points[np.argmax(points_sum)]
    top_right = points[np.argmin(points_diff)]
    bottom_left = points[np.argmax(points_diff)]

    # Calculate the width
    width_top = math.sqrt((top_right[0] - top_left[0]) ** 2 + (top_right[1] - top_left[1]) ** 2)
    width_bottom = math.sqrt((bottom_right[0] - bottom_left[0]) ** 2 + (bottom_right[1] - bottom_left[1]) ** 2)
    width = max(int(width_top), int(width_bottom))  # Take the maximum width

    # Calculate the height
    height_left = math.sqrt((bottom_left[0] - top_left[0]) ** 2 + (bottom_left[1] - top_left[1]) ** 2)
    height_right = math.sqrt((bottom_right[0] - top_right[0]) ** 2 + (bottom_right[1] - top_right[1]) ** 2)
    height = max(int(height_left), int(height_right))  # Take the maximum height

    input_pts = np.float32([top_left, bottom_left, bottom_right, top_right])
    return width, height, input_pts

def scan(imgInput, imgPath):
    img=cv2.imread(imgInput)
    assert img is not None, "file could not be read, check with os.path.exists()"
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, imageThresh = cv2.threshold(gray,thresh=127,maxval=255,type=cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(imageThresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour (assuming it's the page)
    largest_contour = max(contours, key=cv2.contourArea)

    # Approximate the contour to a polygon with four points
    epsilon = 0.02 * cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, epsilon, True)

    # Ensure the result is a quadrilateral
    if len(approx) == 4:
        # Draw the approximated polygon on the image
        cv2.polylines(img, [approx], isClosed=True, color=(0, 255, 255), thickness=3)

        # Mark the four corner points
        for point in approx:
            x, y = point[0]  # Each point is a 2D coordinate
            cv2.circle(img, (x, y), radius=10, color=(0, 0, 255), thickness=-1)  # Red dots

    maxWidth, maxHeight, input_pts= calculate_dimensions(approx)

    output_pts = np.float32([[0, 0],
                             [0, maxHeight - 1],
                             [maxWidth - 1, maxHeight - 1],
                             [maxWidth - 1, 0]])

    M = cv2.getPerspectiveTransform(input_pts, output_pts)

    out = cv2.warpPerspective(img, M, (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)

    # Save the result to the specified path
    cv2.imwrite(imgPath, out)
    # # Display the result
    cv2.imshow('Scanned Image', out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("less or more paramters")
        sys.exit()
    scan(sys.argv[1],sys.argv[2])


