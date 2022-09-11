from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import socket, time





def matrixSend(img, buzzer=False, brightness=15):
    matrix = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # rofl = [0] * 33
    # for x in range(0, 32):
    #     column = 0
    #     for y in range(0, 8):
    #         column = column | (img.getpixel((x, y))[0] > 128) << y
    #     rofl[x] = column
    # rofl[32] = 255 if buzzer is True else 0 # whooooa, pythonic as fuck
    # wtf = bytearray(rofl)
    
    rofl = [0] * 34
    for device in range(0, 4):
        for y in range(0, 8):
            row = 0
            for x in range(0, 8):
                print ((device * 8) + x, y)
                row = row | (img.getpixel(((device * 8) + x, y))[0] > 128) << (7 - x)
            rofl[(device * 8) + y] = row
    
    rofl[32] = 255 if buzzer is True else 0 # whooooa, pythonic as fuck
    rofl[33] = brightness
    wtf = bytearray(rofl)
    print (wtf)
    
    

    matrix.sendto(wtf, ("10.0.0.213", 1234))
    # matrix.sendto(wtf, ("10.0.0.209", 1234))


def matrixDrawFromString(text, size=9, gap_width=-1.2, buzzer=False):
    font = ImageFont.truetype("slkscr.ttf",size)
    img=Image.new("RGBA", (32,8),(0,0,0))

    draw = ImageDraw.Draw(img)
    
    # total_text_width = draw.textlength(text, font=font)
    # width_difference = 32 - total_text_width
    # gap_width = int(width_difference / (len(text) - 1))
    xpos = 0
    for letter in text:
        draw.text((xpos,-1), letter, font=font)
        letter_width = draw.textlength(letter, font=font)
        xpos += letter_width + gap_width
    
    
    # draw.text((0, -1), str, font=font)
    
    matrixSend(img, buzzer)
    

def matrixAlert(count=3):
    for i in range(0, count):
        img=Image.new("RGBA", (32,8),(0,0,0))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(0, 0), (7, 7)], fill="white")
        draw.rectangle([(16, 0), (23, 7)], fill="white")
        matrixSend(img, buzzer=True)
        
        time.sleep(0.4)
        
        img=Image.new("RGBA", (32,8),(0,0,0))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(8, 0), (15, 7)], fill="white")
        draw.rectangle([(24, 0), (31, 8)], fill="white")
        matrixSend(img, buzzer=False)
        
        time.sleep(0.4)

    
if __name__ == "__main__":
    matrixAlert()
    matrixDrawFromString("n600ll", 9)
    time.sleep(4)
    matrixDrawFromString("")