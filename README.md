# qr-code_multiplexer

The BW encoder takes in binary string and converts it into a straight line of 1 pixel height and the lenght of the string in width. Black represents 1 and white 0
The RGBW encoder does the same except the colors that are changed, using the following rules:
- "00" -> White
- "01" -> Red
- "10" -> Green
- "11" -> Blue

The program has 4 functions:
- encoderbw() which is the black and white encoder
- decoderbw() which is the black and white decoder
- encoderrgbw() which is the Red, Green, Blue and White encoder
- decoderrgbw() which is the Red, Green, Blue and White decoder

the encoders input a binary string without spaces and the decoders input a image path

For now it only makes a straight line, but when I will make it into an actual qr-code like shape, it will be twice as efficient with the RGBW version, and 3x efficient with the future RGBWCYMK: Red, Green, Blue, White, Cyan, Yellow, Magenta, Black.

