import textwrap
from pilmoji import Pilmoji
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
pals1 = ['#eb3b5a', '#fa8231', '#f7b731', '#20bf6b', '#0fb9b1', '#eb3b5a', '#fa8231', '#f7b731', '#20bf6b', '#0fb9b1']
pals2 = ['#2d98da', '#3867d6', '#8854d0', '#a5b1c2', '#4b6584', '#2d98da', '#3867d6', '#8854d0', '#a5b1c2', '#4b6584']

@st.cache_data
def generate_card(heading, content, color='#000000', width=2160, aspect_ratio=(1, 1), num='212', textcolor='white'):
    heading_font_path = "assets/BOLD.OTF"
    body_font_path = "assets/REGULAR.OTF"
    logo_font_path = 'assets/logo_font.ttf'
    w, h = width, int(width*aspect_ratio[1]/aspect_ratio[0])
    heading_font_size = int(w / 12)
    body_font_size = int(w / 25)
    margin = int(w / 10)
    line_spacing = int(body_font_size*.20)

    # initiate image
    image = Image.new("RGB", (w, h), color)
    draw = ImageDraw.Draw(image)

    # draw headings
    heading_font = ImageFont.truetype(heading_font_path, heading_font_size)
    heading_lines = textwrap.wrap(heading, width=20)
    y = margin
    for line in heading_lines:
        with Pilmoji(image) as pilmoji:
            pilmoji.text((margin, y), line, font=heading_font, fill='#31BD93')
            y += heading_font_size + line_spacing

    # draw content
    body_font = ImageFont.truetype(body_font_path, body_font_size)
    body_lines = textwrap.wrap(content, width=44)
    y += int(margin / 2)
    for line in body_lines:
        with Pilmoji(image) as pilmoji:
            pilmoji.text((margin, y), line, font=body_font, fill=textcolor)
            y += body_font_size + line_spacing

    # draw page number
    page_number = f'{num}'
    page_number_width, page_number_height = draw.textsize(page_number, font=body_font)
    draw.text((w - margin - page_number_width, h - margin - body_font_size), page_number,
              font=body_font, fill=textcolor)

    # logo font
    logo_font = ImageFont.truetype(logo_font_path, int(body_font_size*0.75))
    draw.text((margin, h - margin*1.25 - body_font_size), 'Johnny\'s', font=logo_font, fill="#31BD93")

    # Save the image
    # with Pilmoji(image) as pilmoji:/
    #     pilmoji.text((10, 10), my_string.strip(), (0, 0, 0), font)

    image.save(f"images/card_{num}.png")

    print(f"Image {num} created.")


@st.cache_data
def generate_post(heading, subtitle, content, color='#000000', width=2160, aspect_ratio=(1, 1), hashtag='212', textcolor='white'):
    heading_font_path = "assets/BOLD.OTF"
    body_font_path = "assets/REGULAR.OTF"
    logo_font_path = 'assets/logo_font.ttf'
    w, h = width, int(width*aspect_ratio[1]/aspect_ratio[0])
    heading_font_size = int(w / 12)
    body_font_size = int(w / 25)
    margin = int(w / 10)
    line_spacing = int(body_font_size*.20)

    # initiate image
    image = Image.new("RGB", (w, h), color)
    draw = ImageDraw.Draw(image)

    # draw subtitle
    subtitle_font_size = int(heading_font_size/2)
    subtitle_font = ImageFont.truetype(heading_font_path, subtitle_font_size)
    subtitle_lines = textwrap.wrap(subtitle, width=40)
    y = margin
    for line in subtitle_lines:
        with Pilmoji(image) as pilmoji:
            pilmoji.text((margin, y), line, font=subtitle_font, fill=textcolor)
            y += subtitle_font_size + line_spacing

    # draw headings
    heading_font = ImageFont.truetype(heading_font_path, heading_font_size)
    heading_lines = textwrap.wrap(heading, width=20)
    y += int(margin/4)
    for line in heading_lines:
        with Pilmoji(image) as pilmoji:
            pilmoji.text((margin, y), line, font=heading_font, fill='#31BD93')
            y += heading_font_size + line_spacing

    # draw content
    body_font = ImageFont.truetype(body_font_path, body_font_size)
    body_lines = textwrap.wrap(content, width=44)
    y += int(margin / 3)
    for line in body_lines:
        with Pilmoji(image) as pilmoji:
            pilmoji.text((margin, y), line, font=body_font, fill=textcolor)
            y += body_font_size + line_spacing

    # draw hashtag
    page_number = f'{hashtag}'
    page_number_width, page_number_height = draw.textsize(page_number, font=body_font)
    draw.text((w - margin - page_number_width, h - margin - body_font_size), page_number,
              font=body_font, fill=textcolor)

    # logo font
    logo_font = ImageFont.truetype(logo_font_path, int(body_font_size*0.75))
    draw.text((margin, h - margin*1.25 - body_font_size), 'Johnny\'s', font=logo_font, fill="#31BD93")

    # Save the image
    # with Pilmoji(image) as pilmoji:/
    #     pilmoji.text((10, 10), my_string.strip(), (0, 0, 0), font)

    image.save(f"images/post.png")

    print(f"Post created.")



@st.cache_data
def generate_info_cards(json_list, pal1=pals2):
    heading_font_path = "assets/BOLD.OTF"  # Replace with the actual path to your font file
    body_font_path = "assets/REGULAR.OTF"
    w, h = 1500, 1500
    heading_font_size = int(w/10)
    body_font_size = int(w/20)
    hashtag_font_size = int(w/30)
    margin = int(w/10)
    line_spacing = int(w/300)


    for i, json_obj in enumerate(json_list):
        heading = json_obj.get("heading", "")
        insights = json_obj.get("insight", "")
        hashtag = json_obj.get("topic", "")
        hashtag = '#'+str(hashtag).lower()

        # Create a blank image with a white background
        image_width = w
        image_height = h
        image = Image.new("RGB", (image_width, image_height), pal1[i])
        draw = ImageDraw.Draw(image)

        # Load the font
        heading_font = ImageFont.truetype(heading_font_path, heading_font_size)
        body_font = ImageFont.truetype(body_font_path, body_font_size)
        hashtag_font = ImageFont.truetype(heading_font_path, hashtag_font_size)

        # Wrap the heading and insights text
        heading_lines = textwrap.wrap(heading, width=16)
        insights_lines = textwrap.wrap(insights, width=35)

        # Calculate the height required for the text
        # heading_height = len(heading_lines) * (heading_font_size + line_spacing)
        # insights_height = len(insights_lines) * (body_font_size + line_spacing)

        # Draw the heading
        y = margin
        for line in heading_lines:
            draw.text((margin, y), line, font=heading_font, fill="white")
            y += heading_font_size + line_spacing

        # Draw the insights
        y += int(margin/2)
        for line in insights_lines:
            draw.text((margin, y), line, font=body_font, fill="white")
            y += body_font_size + line_spacing

        # draw hashtag
        draw.text((margin, image_height - margin - hashtag_font_size), hashtag, font=hashtag_font, fill="white")

        # draw page number
        page_number = str(i+1)
        page_number_width, page_number_height = draw.textsize(page_number, font=hashtag_font)
        draw.text((image_width - margin - page_number_width, image_height - margin - hashtag_font_size), page_number,
                  font=hashtag_font, fill="white")

        # Save the image
        image.save(f"images/card_{i}.png")

        print(f"Image {i} created.")

@st.cache_data
def generate_title_cards(titles, subtitle, topic, text_top_right="@bluestoneai", logo='assets/final_white.png', factor=10, mgn=2.5, bg_color='black',headingwrap=7):
    for i, heading in enumerate(titles):
        heading_font_path = "assets/BOLD.OTF"  # Replace with the actual path to your font file
        w, h = 1500, 1500
        heading_font_size = int(w / 10)
        body_font_size = int(heading_font_size / 2)
        margin = int(w / 10)
        line_spacing = int(w / 300)
        heading_font = ImageFont.truetype(heading_font_path, heading_font_size)
        body_font = ImageFont.truetype(heading_font_path, body_font_size)
        image = Image.new("RGB", (w, h), bg_color)
        draw = ImageDraw.Draw(image)

        logo = Image.open(logo)
        # logo = Image.open('assets/logo_white.png')
        logo_width, logo_height = logo.size
        logo = logo.resize((int(logo_width/factor), int(logo_height/factor)))
        image.paste(logo, (margin, margin))

        # top right label

        text_top_right_font = ImageFont.truetype('assets/BOLD.OTF', int(w/25))
        text_top_right_width, text_top_right_height = draw.textsize(text_top_right, font=text_top_right_font)
        draw.text((w - margin - text_top_right_width, margin), text_top_right, font=text_top_right_font, fill="white")

        # bottom right arrow
        # arrow = Image.open('assets/rightarrow.png')
        # arrow_w, arrow_h = arrow.size
        # arrow_w, arrow_h = int(arrow_w/10), int(arrow_h / 10)
        # arrow = arrow.resize((arrow_w, arrow_h))
        # image.paste(arrow, (w - margin - arrow_w, h-margin-arrow_h))

        # draw hashtag
        draw.text((margin, h - margin - int(w/25)), '#'+str(topic).lower(), font=text_top_right_font, fill="white")

        # right arrows
        page_number_width, page_number_height = draw.textsize('>>>', font=text_top_right_font)
        draw.text((w - margin - page_number_width, h - margin - int(w/25)), '>>>',
                  font=text_top_right_font, fill="white")

        # Draw the heading
        y = margin*mgn
        heading_lines = textwrap.wrap(heading, width=int(heading_font_size/headingwrap))

        for line in heading_lines:
            draw.text((margin, y), line, font=heading_font, fill="white")
            y += heading_font_size + line_spacing


        # Draw the insights
        insights_lines = textwrap.wrap(subtitle, width=25)
        y += int(margin / 5)
        for line in insights_lines:
            draw.text((margin, y), line, font=body_font, fill="white")
            y += body_font_size + line_spacing

        # Save the image
        image.save(f"images/heading_{i}.png")

        print(f"Title Image {i} created.")