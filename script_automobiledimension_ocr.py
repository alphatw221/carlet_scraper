import db


import requests
from PIL import Image
import pytesseract
from pytesseract import Output

def read_image_from_url(url):


    img = Image.open(requests.get(url, stream=True, verify=False).raw)


    return img



def main():


    page_number = 1
    page_size = 10
    
    threshold = 200

    with db.automobiledimension.Session() as session:
        cars= session.query(db.automobiledimension.car.Car).filter_by(length=None).limit(page_size).offset((page_number - 1) * page_size).all()


        for car in cars:
            print(car.image_src)

            img = read_image_from_url(car.image_src)

            img = img.convert("L")
            img = img.point( lambda p: 255 if p > threshold else 0 )
            # img = img.convert('1')
            img.show()
            data = pytesseract.image_to_data(img,output_type=Output.DICT,lang='eng', config='--psm 12 -c tessedit_char_whitelist="0123456789mm()"')
            print(data)


            # break

if __name__ == "__main__":
    main()