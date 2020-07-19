import html2text
import re
from gensim.summarization import summarize


def convert_Html_to_text_and_make_sumarization(description):

    text_maker = html2text.HTML2Text()

    text_maker.ignore_links = True
    text_maker.ignore_images = True
    html = description
    text = text_maker.handle(html)
    text = re.sub('[!@#$%*]', '', text).strip()

    text = summarize(text)

    return text


def change_image_size(image, name):
    if name[:3] == "TRT":
        return image.replace('/w32', '/w960')
    else:
        return image
