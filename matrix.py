from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import socket, time





def matrixSend(img, buzzer=False, brightness=15, ips=["10.0.0.213", "10.0.0.251"]):
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
                row = row | (img.getpixel(((device * 8) + x, y))[0] > 128) << (7 - x)
            rofl[(device * 8) + y] = row
    
    rofl[32] = 255 if buzzer is True else 0 # whooooa, pythonic as fuck
    rofl[33] = brightness
    wtf = bytearray(rofl)
    
    for ip in ips:
        try:
            matrix.sendto(wtf, (ip, 1234))
        except:
            pass


def matrixDrawFromString(text, size=9, gap_width=-1.2, buzzer=False):
    font = ImageFont.truetype("slkscr.ttf",size)
    
    # width_difference = 32 - total_text_width
    # gap_width = int(width_difference / (len(text) - 1))
    
    img=Image.new("RGBA", (32,8),(0,0,0))
    draw = ImageDraw.Draw(img)
    total_text_width = draw.textlength(text, font=font)
    
    
    for i in range(0, int(total_text_width + 32)):
        img=Image.new("RGBA", (32,8),(0,0,0))
        draw = ImageDraw.Draw(img)
        xpos = 0
        for letter in text:
            draw.text((32 + xpos - i, -1), letter, font=font)
            letter_width = draw.textlength(letter, font=font)
            xpos += letter_width + gap_width
        
        
        # draw.text((0, -1), str, font=font)
        
        matrixSend(img, buzzer)
        time.sleep(0.03)
    

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
        
def loadAndSendMatrix(path, ips):
    img = Image.open(path).convert("RGB")
    # pixels = img.load()
    matrixSend(img, buzzer=False, ips=ips)

    
if __name__ == "__main__":
    # matrixAlert()
    # matrixDrawFromString("latest followers:  nicksmadscience, nujj_kmelbone", 9)
    # matrixDrawFromString("new follower: rockem_sockem", 9)
    # time.sleep(4)
    # matrixDrawFromString("")
    while True:
        for i in range(0, 3):
            loadAndSendMatrix("pto6.png", ["10.0.0.251"])
            time.sleep(0.8)
            
            loadAndSendMatrix("pto-blank.png", ["10.0.0.251"])
            time.sleep(0.2)
            
        for i in range(0, 3):
            loadAndSendMatrix("pto4.png", ["10.0.0.251"])
            time.sleep(0.5)
            
            loadAndSendMatrix("pto5.png", ["10.0.0.251"])
            time.sleep(0.5)
           
        loadAndSendMatrix("pto1.png", ["10.0.0.251"])
        time.sleep(1.2)
        
        loadAndSendMatrix("pto2.png", ["10.0.0.251"])
        time.sleep(1.2)
        
        loadAndSendMatrix("pto3.png", ["10.0.0.251"])
        time.sleep(1.2)
        
        for i in range(0, 5):
            loadAndSendMatrix("pto4.png", ["10.0.0.251"])
            time.sleep(0.5)
            
            loadAndSendMatrix("pto5.png", ["10.0.0.251"])
            time.sleep(0.5)