# coding=utf-8
token = '347749840:AAEVH6XhXttYr2mT-Y9Fh0-pE4M9Y3zJdX4'
WEBHOOK_HOST = '46.172.8.144'
WEBHOOK_PORT = 8443
WEBHOOK_LISTEN = '0.0.0.0'
WEBHOOK_SSL_CERT = './webhook_cert.pem'
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % token

VK_API_URL = 'https://api.vk.com/method/'
VK_WALL_GET = 'wall.get'
VK_WALL_SEARCH = 'wall.search'
VK_TOKEN = 'f12bbf76f12bbf76f12bbf76cdf1707db8ff12bf12bbf76a8230421da55513957bb0895'
