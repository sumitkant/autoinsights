import textwrap
import streamlit as st
from glob import glob
from pilmoji import Pilmoji
from PIL import Image, ImageDraw, ImageFont

@st.cache_data
def generate_post(heading, subtitle, content, color='#000000', width=2160, aspect_ratio=(1, 1), hashtag='212',
                  textcolor='white', heading_color='31BD93', font='Livvic', wrap=20, body_font_size=20,
                  lab='STUDY LAB'):

    heading_font_path = glob(f"assets/fonts/{font}/bold*")[0]
    body_font_path = glob(f"assets/fonts/{font}/bold*")[0]
    print(heading_font_path, body_font_path)
    logo_font_path = 'assets/fonts/Logo/regular.ttf'
    logo_font_path2 = 'assets/fonts/Logo/nourd_bold.ttf'
    w, h = width, int(width*aspect_ratio[1]/aspect_ratio[0])
    body_font_size = int(w / 30)
    heading_font_size = int(w / 12)
    margin = int(w / 10)
    line_spacing = int(body_font_size*.30)

    # initiate image
    image = Image.new("RGB", (w, h), color)
    draw = ImageDraw.Draw(image)

    # draw subtitle
    subtitle_font_size = int(body_font_size*1.5)
    subtitle_font = ImageFont.truetype(heading_font_path, subtitle_font_size)
    subtitle_lines = textwrap.wrap(subtitle, width=29)
    y = margin
    for line in subtitle_lines:
        with Pilmoji(image) as pilmoji:
            pilmoji.text((margin, y), line, font=subtitle_font, fill=textcolor)
            y += subtitle_font_size + line_spacing

    # draw headings
    heading_font = ImageFont.truetype(heading_font_path, heading_font_size)
    heading_lines = textwrap.wrap(heading, width=20)
    y += int(margin/10)
    for line in heading_lines:
        with Pilmoji(image) as pilmoji:
            pilmoji.text((margin, y), line, font=heading_font, fill=heading_color)
            y += heading_font_size + line_spacing

    # draw content
    body_font = ImageFont.truetype(body_font_path, body_font_size)
    body_lines = textwrap.wrap(content, width=47)
    y += int(margin / 3)
    for line in body_lines:
        with Pilmoji(image) as pilmoji:
            pilmoji.text((margin, y), line, font=body_font, fill=textcolor)
            y += body_font_size + line_spacing

    # draw logo (bottom right)
    logo_font_size = int(body_font_size*0.75)
    logo_font = ImageFont.truetype(logo_font_path, logo_font_size)
    logo_width, logo_height = draw.textsize('Johnny\'s', font=logo_font)
    draw.text((w - margin - logo_width, h - margin*1.35 - logo_font_size), 'Johnny\'s',
              font=logo_font, fill=heading_color)


    print(lab)
    lab = ' '.join([x for x in lab])
    print(lab)
    lab_font = ImageFont.truetype(logo_font_path2, int(logo_font_size/1.5))
    lab_width, lab_height = draw.textsize(lab, font=lab_font)
    draw.text((w - margin - lab_width +20, h - margin * 0.8 - logo_font_size), lab,
              font=lab_font, fill=textcolor)

    # draw hashtag (bottom left)
    hashtag_font_size = int(body_font_size * 0.7)
    hashtag = f'{hashtag}'.upper()
    hashtag_font = ImageFont.truetype(body_font_path, hashtag_font_size)
    draw.text((margin, h - margin - hashtag_font_size), hashtag, font=hashtag_font, fill=heading_color)

    # image.save(f"images/post.png")
    print(f"Post created.")
    return image