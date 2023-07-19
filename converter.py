import argparse
import io
import os

import gc
import pytesseract
from PIL import Image
from wand.image import Image as wi


def get_text_from_image(pdf_path: str):
    pdf = wi(filename=pdf_path, resolution=300)
    pdf_img = pdf.convert('jpeg')
    img_blobs = []
    extracted_text = []
    try:
        for img in pdf_img.sequence:
            page = wi(image=img)
            img_blobs.append(page.make_blob('jpeg'))
            for i in range(0, 5):
                [gc.collect() for i in range(0, 10)]

            for img_blob in img_blobs:
                im = Image.open(io.BytesIO(img_blob))
                text = pytesseract.image_to_string(im, lang='eng')
                text = text.replace(r'\n', ' ')
                extracted_text.append(text)
                for i in range(0, 5):
                    [gc.collect() for i in range(0, 10)]

            [gc.collect() for i in range(0, 10)]
            return (''.join([i.replace('\n', ' ').replace('\n\n', ' ') for i in extracted_text]))
    finally:
        [gc.collect() for _ in range(0, 10)]


parser = argparse.ArgumentParser(description='Convert PDF file to Text file')
parser.add_argument(
    '-i',
    action='store',
    default='input.pdf',
    help='PDF file to convert',
)
parser.add_argument(
    '-o',
    action='store',
    default='output.txt',
    help='Text output filename',
)
args = parser.parse_args()


if __name__ == '__main__':
    input_file = args.i
    output_file = args.o

    if not os.path.isfile(input_file):
        print(f'{input_file} does not exist')
        exit(0)

    text = get_text_from_image(input_file)
    print(text)
