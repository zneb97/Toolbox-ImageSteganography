"""A program that encodes and decodes hidden messages in images through LSB steganography"""
from PIL import Image, ImageFont, ImageDraw
import textwrap

def decode_image(file_location="images/encoded_sample.png" , saveLocation = "images/decoded_image.png"):
    """Decodes the hidden message in an image

    file_location: the location of the image file to decode. By default is the provided encoded image in the images folder
    """
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]
    red_channel = red_channel.load()

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()

    for x in range(0, x_size):
        for y in range(0, y_size):
            #Get last value in binary
            bit = int(bin(red_channel[x,y])[-1])
            #Rewrite Image
            if bit == 1:
                pixels[x,y] = (255,255,255)
            else:
                pixels[x,y] = (0,0,0)


    decoded_image.save(saveLocation)

def write_text(text_to_write, image_size):
    """Writes text to an RGB image. Automatically line wraps

    text_to_write: the text to write to the image
    image_size: size of the resulting text image. Is a tuple (x_size, y_size)
    """
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    #Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin,offset), line, font=font)
        offset += 10
    return image_text

def encode_image(text_to_encode, template_image="images/samoyed.jpg"):
    """Encodes a text message into an image

    text_to_encode: the text to encode into the template image
    template_image: the image to use for encoding. An image is provided by default.
    """

    #Start image
    default_image = Image.open(template_image)
    default_image_red = (default_image.split()[0]).load()
    default_image_green = (default_image.split()[1]).load()
    default_image_blue = (default_image.split()[2]).load()
    x_size = default_image.size[0]
    y_size = default_image.size[1]

    #New Image
    secret_text_image = write_text(text_to_encode, default_image.size)
    secret_text_red = secret_text_image.split()[0]
    pixel_red = secret_text_red.load()
    encoded_image = Image.new("RGB", default_image.size)
    encoded_pixels = encoded_image.load()

    #Encode new image
    for x in range(0, x_size):
        for y in range(0,  y_size):
            update_red = bin(default_image_red[x,y])
            if pixel_red[x,y] == 255:
                update_red = int(update_red[0:-1]+'1',2)
            else:
                update_red = int(update_red[0:-1]+'0',2)
            encoded_pixels[x,y] = (update_red,default_image_green[x,y],default_image_blue[x,y])

    encoded_image.save("images/encoded_image.png")


if __name__ == '__main__':
    decode_image()
    encode_image("It's a secret to everybody")
    decode_image("images/encoded_image.png", "images/myDecodedImage.png")
