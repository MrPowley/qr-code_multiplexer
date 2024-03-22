#Using Python 3.12.2

from PIL import Image

color_code = {"00": (255, 255, 255),
              "01": (255, 0, 0),
              "10": (0, 255, 0),
              "11": (0, 0, 255)}

color_code_inverted = {s: c for c, s in color_code.items()}

def encoderbw(data: str):
    data_lenght = len(data)

    if data_lenght  % 8 != 0:
        raise Exception()


    image_size = (data_lenght , 1)
    image = Image.new("RGB", size=image_size)

    for x, bit in enumerate(data):
        if bit == "0":
            image.putpixel((x, 0), (255, 255, 255))
        elif bit == "1":
            image.putpixel((x, 0), (0, 0, 0))
        else:
            pass

    image.save("image.png")

def decoderbw(image_path: str):
    image = Image.open(image_path)

    data = ""

    for x in range(image.width):
        pixel = image.getpixel((x, 0))
        if pixel == (255, 255, 255):
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

