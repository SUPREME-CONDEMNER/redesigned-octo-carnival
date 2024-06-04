import asyncio
from pyppeteer import launch

async def set_fingerprint():
    proxy_ip = '38.154.227.167'
    proxy_port = '5868'
    proxy_username = 'irinbkag'
    proxy_password = '59cpz5symen8'

    browser = await launch({
        'headless': False,
        'args': [
            f'--proxy-server=http://{proxy_ip}:{proxy_port}',
            '--user-agent=Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-G935FQ Build/MMB29M) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/53.0.2529.326 Mobile Safari/603.8'
        ]
    })

    page = await browser.newPage()

    # Handle proxy authentication
    await page.authenticate({'username': proxy_username, 'password': proxy_password})

    # Set additional fingerprint attributes
    await page.emulate({
        'viewport': {
            'width': 360,
            'height': 640,
            'deviceScaleFactor': 3,
            'isMobile': True,
            'hasTouch': True,
            'isLandscape': False
        },
        'userAgent': 'Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-G935FQ Build/MMB29M) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/53.0.2529.326 Mobile Safari/603.8',
        'geolocation': {
            'latitude': 37.7749,
            'longitude': -122.4194,
            'accuracy': 100
        },
        'permissions': ['geolocation']
    })

    await page.goto('https://www.google.com')
    # Add additional actions or navigation as needed

    # Close browser when done
    # await browser.close()

asyncio.get_event_loop().run_until_complete(set_fingerprint())
