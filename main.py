#Using Python 3.12.2

from PIL import Image
import textwrap

color_code = {"00": (255, 255, 255),
              "01": (255, 0, 0),
              "10": (0, 255, 0),
              "11": (0, 0, 255)}

color_code_inverted = {s: c for c, s in color_code.items()}

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

forbidden_zones = []

forbidden_zone1 = [(x,y) for y in range(10) for x in range(10)]
forbidden_zone2 = [(x,y) for y in range(10) for x in range(14, 23)]
forbidden_zone3 = [(x,y) for y in range(14, 23) for x in range(10)]
forbidden_zone4 = [(7,y) for y in range(10, 14)]
forbidden_zone5 = [(x,7) for x in range(10, 14)]

forbidden_zones.extend(forbidden_zone1)
forbidden_zones.extend(forbidden_zone2)
forbidden_zones.extend(forbidden_zone3)
forbidden_zones.extend(forbidden_zone4)
forbidden_zones.extend(forbidden_zone5)

def encoderbw(data: str):
    data_lenght = len(data)

    if data_lenght  % 8 != 0:
        raise Exception()


    image_size = (data_lenght , 1)
    image = Image.new("RGB", size=image_size)

    for x, bit in enumerate(data):
        if bit == "0":
            image.putpixel((x, 0), white)
        elif bit == "1":
            image.putpixel((x, 0), black)
        else:
            pass

    image.save("image.png")

def decoderbw(image_path: str):
    image = Image.open(image_path)

    data = ""

    for x in range(image.width):
        pixel = image.getpixel((x, 0))
        if pixel == white:
            data += "0"
        else:
            data += "1"
    print(data)

def encoderrgbw(data: str):
    data_lenght = len(data)

    if data_lenght  % 8 != 0:
        raise Exception()


    image_size = (int(data_lenght/2) , 1)
    image = Image.new("RGB", size=image_size)

    

    for x in range(0, len(data), 2):
        sequence = f"{data[x]}{data[x+1]}"
        image.putpixel((int(x/2), 0), color_code[sequence])

    image.save("image.png")

def decoderrgbw(image_path: str):
    image = Image.open(image_path)

    data = ""

    for x in range(image.width):
        sequence = image.getpixel((int(x), 0))
        data += color_code_inverted[sequence]
    
    print(data)

def qr1_square(image, x, y):
    for i in range(7):
        x_offset = x+i
        y_offset = y+i
        image.putpixel((x_offset, y), black)
        image.putpixel((x_offset, y+6), black)
        image.putpixel((x,  y_offset), black)
        image.putpixel((x+6,  y_offset), black)
    
    for i in range(3):
        for j in range(3):
            image.putpixel((x+i+2, y+j+2), black)

    return image

def qr1_reserved(image):

    for i in range(1, 9):
        image.putpixel((i, 9), red)
        image.putpixel((9, i), red)
        image.putpixel((i+13, 9), red)
        image.putpixel((9, i+13), red)
    image.putpixel((9, 9), red)
    
    for i in range(5):
        if i%2 == 0:
            color = black
        else:
            color = white

        image.putpixel((i+9, 7), color)
        image.putpixel((7, i+9), color)
    
    image.putpixel((9, 14), black)
    
    return image

def qr1_data_upw(image, x, y):
    ...

def qr1_encoding_mode(image):
    image.putpixel((20, 20), black)
    return image

def qr1_ecl(image, ecl): # Error correction level function

    if ecl == "L":
        color1, color2, color3, color4 = black, black, black, black
    elif ecl == "M":
        color1, color2, color3, color4 = black, white, black, white
    elif ecl == "Q":
        color1, color2, color3, color4 = white, black, black, white
    elif ecl == "H":
        color1, color2, color3, color4 = white, white, white, white
    else:
        raise Exception(ValueError)
    
    image.putpixel((1,9), color1)
    image.putpixel((2,9), color2)
    image.putpixel((9,20), color3)
    image.putpixel((9,21), color4)

    return image

def qr1_mask_pattern(image, mask_pattern):

    if mask_pattern == 1:
        ...
    elif mask_pattern == 2:
        ...
    elif mask_pattern == 3:
        ...
    elif mask_pattern == 4:
        image.putpixel((3, 9), black)
        image.putpixel((4, 9), white)
        image.putpixel((5, 9), white)
        image.putpixel((9, 17), black)
        image.putpixel((9, 18), white)
        image.putpixel((9, 19), white)

    elif mask_pattern == 5:
        ...
    elif mask_pattern == 6:
        ...
    elif mask_pattern == 7:
        ...
    elif mask_pattern == 8:
        ...
    else:
        raise Exception(ValueError)
    
    return image

def qr1_fec(image): # Format Error Correction function

    image.putpixel((6, 9), black)
    image.putpixel((8, 9), white)
    [image.putpixel((9, y), black) for y in range(1, 10)]
    image.putpixel((9, 3), white)
    image.putpixel((9, 4), white)
    image.putpixel((9, 15), white)
    image.putpixel((9, 16), black)
    [image.putpixel((x, 9), black) for x in range(14, 22)]
    image.putpixel((19, 9), white)
    image.putpixel((18, 9), white)

    return image

def qr1_write_data(image, data):
    x, y = 21, 15
    
    bytes = textwrap.wrap(data, 8)

    for j in range(len(bytes)):
        image, x, y = draw_section(image, bytes[j], x, y, j)
        
    return image

ups = [0, 1, 2, 7, 8, 13, 14, 15, 16, 23, 25]
downs = [4, 5, 10, 11, 18, 19, 20, 21, 22, 24, 26]
tols = [3, 9, 17]
tods = [6, 12]

def bit_color(bit):
    if bit == "1":
        return black
    else:
        return white

def draw_section(image, byte, x, y, j):
    print(byte)
    j += 2
    print(j)
    match j:
        case w if w in ups: # SECTION 1
            print("SECTION 1")
            print(x,y)
            n = 0
            for i, bit in enumerate(byte):
                color = bit_color(bit)

                if i % 2 == 0:
                    x_offset = x
                else:
                    x_offset = x-1
                
                if i % 2 == 0:
                    n += 1
                    
                    y_offset = y - (n-1)

                print(x_offset, y_offset)
                if (x_offset, y_offset) in forbidden_zones:
                    raise Exception(IndexError)
                
                


                image.putpixel((x_offset, y_offset), color)

            if j == 15:
                y_offset -= 1
            x = x_offset
            x += 1
            y = y_offset
            y -= 1
            print(x, y)

        case w if w in tols: # SECTION 2
            print("SECTION 2")
            ys = [y, y, y-1, y-1, y-1, y-1, y, y]
            xs = [x, x-1, x, x-1, x-2, x-3, x-2, x-3]
            for i, bit in enumerate(byte):

                color = bit_color(bit)

                
                x_offset = xs[i]
                y_offset = ys[i]
                    
                if (x_offset, y_offset) in forbidden_zones:
                    raise Exception(IndexError)
                print(x_offset, y_offset)
                image.putpixel((x_offset, y_offset), color)
                # image.show()
            y += 1
            x -= 3
            print(x, y)
        case w if w in tods: # SECTION 3
            print("SECTION 3")
            ys = [y, y, y+1, y+1, y+1, y+1, y, y]
            xs = [x+1, x, x+1, x, x-1, x-2, x-1, x-2]
            for i, bit in enumerate(byte):

                color = bit_color(bit)

                
                x_offset = xs[i]
                y_offset = ys[i]
                    
                if (x_offset, y_offset) in forbidden_zones:
                    raise Exception(IndexError)
                print(x_offset, y_offset)
                image.putpixel((x_offset, y_offset), color)
                # image.show()
            x_offset = x
            x -= 1
            y_offset = y
            y -= 1
            print(x, y)
        case w if w in downs: # SECTION 4
            print("SECTION 4")
            n = 0
            for i, bit in enumerate(byte):

                color = bit_color(bit)

                if i % 2 == 0:
                    x_offset = x+1
                else:
                    x_offset = x
                
                if i % 2 == 0:
                    n += 1
                    y_offset = y + n-1
                    
                if (x_offset, y_offset) in forbidden_zones:
                    raise Exception(IndexError)
                print(x_offset, y_offset)
                image.putpixel((x_offset, y_offset), color)
                # image.show()
            x = x_offset
            y = y_offset
            y += 1
            print(x, y)

    return image, x, y


def qr1(data):
    image = Image.new("RGB", size=(23,23), color=(255, 255, 255))

    image = qr1_square(image, 1, 1) # Top left
    image = qr1_square(image, 15, 1) # Top right
    image = qr1_square(image, 1, 15) # Bottom left
    image = qr1_reserved(image)

    image = qr1_encoding_mode(image)

    image = qr1_ecl(image, "L")

    image = qr1_mask_pattern(image, 4)

    image = qr1_fec(image)

    image = qr1_write_data(image, data)

    # for i in forbidden_zones:
    #     image.putpixel(i, red)
    
    # image.putpixel((20, 11), (0,255,0))

    image.show()
    image.save("qr.png")

#encoderrgbw("010010000110010101101100011011000110111100100000011101110110111101110010011011000110010000100001")

qr1("0111011101110111011101110010111001110111011010010110101101101001011100000110010101100100011010010110000100101110011011110111001001100111")