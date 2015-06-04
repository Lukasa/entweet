from __future__ import division
import getpass
import gnupg
import math
import operator
import sys
import requests
from cStringIO import StringIO
from PIL import Image, ImageFont, ImageDraw, ImageChops

font_size = 24
padding = 5
font = ImageFont.truetype('Inconsolata-Regular.ttf', size=font_size)
char_width, char_height = font.getsize('A')
char_height += padding
chars = ''.join([chr(o) for o in range(32, 127)])


def get_char_image(image, col, row):
    return image.crop((
        col * char_width,
        row * char_height,
        (col + 1) * char_width,
        (row + 1) * char_height,
    ))


def generate_image_map(chars):
    image = Image.new('RGB', (10000, 100))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), chars, font=font)
    width, height = font.getsize(chars)
    image = image.crop((0, 0, width, height))
    return {c: get_char_image(image, i, 0) for i, c in enumerate(chars)}
image_map = generate_image_map(chars)

def rmsdiff(diff):
    h = diff.histogram()

    # calculate rms
    return math.sqrt(reduce(operator.add,
        map(lambda h, i: h*((i or 0)**2), h, range(256))
    ) / (float(char_width) * char_height))

def get_image_char(image):
    diffs = {}
    for char, char_image in image_map.items():
        diff = ImageChops.difference(image, char_image)
        if diff.getbbox() is None:
            return char
        diffs[char] = diff

    min_rms = 10**6
    closest_char = ''
    for char, diff in diffs.items():
        rms = rmsdiff(diff)
        if rms < min_rms:
            min_rms = rms
            closest_char = char
    return closest_char

def encode(message):
    image = Image.new('RGB', (10000, 10000))
    draw = ImageDraw.Draw(image)
    height = padding
    max_width = 0
    size = (0, 0)

    for line in message.splitlines():
        # Leave a space for blank lines.
        if not line:
            height += char_height
            continue

        size = font.getsize(line)
        draw.text((padding, height), line, font=font)
        height += char_height
        max_width = max(max_width, size[0] + 10)

    return image.crop((0, 0, max_width, height + 10))


def decode(text_image):
    width, height = text_image.size
    text_image = text_image.crop((padding, padding, width - padding, height - padding))
    width, height = text_image.size
    cols = int(width / char_width)
    rows = int(height / char_height)

    lines = []
    for row in range(rows):
        line = ''
        for col in range(cols):
            image = get_char_image(text_image, col, row)
            line += get_image_char(image)
        lines.append(line.strip())

    return '\n'.join(lines)


def gpgify(message):
    g = gnupg.GPG()
    passphrase = getpass.getpass('Passphrase: ')

    signature = str(g.sign(message, passphrase=passphrase, clearsign=False))
    if not signature:
        raise ValueError("Invalid passphrase!")

    return signature


def ungpgify(message):
    g = gnupg.GPG()
    d = g.decrypt(message)

    if not d:
        raise ValueError("Invalid data!")

    if d.username:
        print "Message from %s" % d.username

    print d.data


def encode_tweet(twitter_session, message):
    message = gpgify(message)
    image = encode(message)
    image.save('/tmp/tweet.png')
    r = twitter_session.post(
        'https://upload.twitter.com/1.1/media/upload.json',
        files={'media': open('/tmp/tweet.png', 'rb')},
    )

    r.raise_for_status()
    media_id = r.json()['media_id_string']
    r = twitter_session.post(
        'https://api.twitter.com/1.1/statuses/update.json',
        data={
            'status': 'Posted from Entweet',
            'media_ids': [media_id],
        },
    )
    r.raise_for_status()
    return r.json()


def decode_tweet(twitter_session, tweet_id):
    url = 'https://api.twitter.com/1.1/statuses/show.json?id={}'.format(tweet_id)
    tweet = twitter_session.get(url).json()
    image_url = tweet['entities']['media'][0]['media_url_https'] + ':large'
    image_bytes = requests.get(image_url).content
    buff = StringIO(image_bytes)
    buff.seek(0)
    image = Image.open(buff)
    message = decode(image)
    print message
    return ungpgify(message)
