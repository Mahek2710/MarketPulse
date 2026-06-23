FEEDS = [
    {
        'name': 'moneycontrol',
        'display_name': 'MoneyControl Markets',
        'url': 'https://www.moneycontrol.com',
        'feed_url': 'https://www.moneycontrol.com/rss/MCtopnews.xml',
        'is_active': True,
    },
    {
        'name': 'economic_times',
        'display_name': 'Economic Times Markets',
        'url': 'https://economictimes.indiatimes.com',
        'feed_url': 'https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms',
        'is_active': True,
    },
    {
        'name': 'livemint',
        'display_name': 'Livemint Markets',
        'url': 'https://www.livemint.com',
        'feed_url': 'https://www.livemint.com/rss/markets',
        'is_active': True,
    },
    {
        'name': 'nse_announcements',
        'display_name': 'NSE Corporate Announcements',
        'url': 'https://www.nseindia.com',
        'feed_url': 'https://www.nseindia.com/api/corporate-announcements?index=equities',
        'is_active': False,  # NSE blocks direct API calls without session — disable for now
    },
]