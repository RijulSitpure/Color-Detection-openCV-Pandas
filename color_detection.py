import cv2
import pandas as pd

# Read image
img_path = r'boat.jpg'
img = cv2.imread(img_path)

# Get image dimensions
height, width, _ = img.shape

# Declaring global variables
clicked = False
r = g = b = x_pos = y_pos = 0

# Reading csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

# Function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# Function to get x, y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

def main():
    global clicked, b, g, r, x_pos, y_pos
    
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', width, height)
    cv2.setMouseCallback('image', draw_function)

    while True:
        if cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) < 1:
            break

        cv2.imshow("image", img)

        if clicked:
            # Dynamically adjust rectangle and font size based on image dimensions
            box_width = int(width * 0.6)
            box_height = int(height * 0.05)
            font_scale = height / 800.0
            thickness = int(height / 200.0)

            # Define rectangle start and end points
            rect_start = (20, 20)
            rect_end = (20 + box_width, 20 + box_height)

            # Draw the rectangle
            cv2.rectangle(img, rect_start, rect_end, (b, g, r), -1)

            # Creating text string to display (Color name and RGB values)
            text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

            # Calculate text size to center it in the rectangle
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
            text_x = rect_start[0] + (box_width - text_size[0]) // 2
            text_y = rect_start[1] + (box_height + text_size[1]) // 2

            # Put the text on the image
            cv2.putText(img, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

            # For very light colors, display text in black color
            if r + g + b >= 600:
                cv2.putText(img, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), thickness, cv2.LINE_AA)

            clicked = False

        # Wait for 20 milliseconds before next iteration
        if cv2.waitKey(20) & 0xFF == 27:
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
