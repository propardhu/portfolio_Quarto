import feedparser
import requests
import os
import re
from bs4 import BeautifulSoup
from datetime import datetime

# Replace with your Medium username's RSS feed URL
MEDIUM_RSS_URL = 'https://medium.com/feed/@guttikondaparthasai'
OUTPUT_DIR = 'blog_posts'
IMAGE_DIR = 'images'

# Create directories if they don't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

def slugify(text):
    return re.sub(r'[\W_]+', '-', text.lower())

# def save_image(image_url, filename):
#     try:
#         response = requests.get(image_url)
#         response.raise_for_status()  # Check for HTTP errors
#         with open(os.path.join(IMAGE_DIR, filename), 'wb') as f:
#             f.write(response.content)
#         return f'/images/{filename}'
#     except requests.exceptions.RequestException as e:
#         print(f"Error saving image {image_url}: {e}")
#         return ''

def extract_first_image_src(summary):
    soup = BeautifulSoup(summary, 'html.parser')
    img_tag = soup.find('img')
    if img_tag and 'src' in img_tag.attrs:
        return img_tag['src']
    return ''

def create_markdown_file(post_data):
    title = post_data['title']
    slug = slugify(title)
    date = post_data['date']
    read_time = post_data['read_time']
    categories = post_data['categories']
    link = post_data['link']
    image_filename = f"{slug}.png"
    description = post_data['description']
    # if post_data['image_src']:
    #     save_image(post_data['image_src'], image_filename)

    markdown_content = f"""---
title: "{title}"
date: {date}
reading-time: "{read_time}"
categories: {categories}
image: {post_data['image_src']}
---

[click here to read this in medium]({link})\


{description}
"""

    filepath = os.path.join(OUTPUT_DIR, f'{date}-{slug}.md')
    with open(filepath, 'w') as f:
        f.write(markdown_content)

def fetch_medium_posts(rss_url):
    feed = feedparser.parse(rss_url)
    posts = []
    for entry in feed.entries:
        image_src = extract_first_image_src(entry.summary)
        post_data = {
            'title': entry.title,
            'link': entry.link,
            'date': datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d'),
            'read_time': '5 min read',  # Medium doesn't provide read time in RSS feed
            'categories': entry.tags[0].term,
            'image_src': image_src,
            'description': entry.summary
        }
        posts.append(post_data)
    return posts

def main():
    posts = fetch_medium_posts(MEDIUM_RSS_URL)
    for post in posts:
        create_markdown_file(post)

if __name__ == '__main__':
    main()
