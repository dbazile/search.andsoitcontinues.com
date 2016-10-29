import logging
import time

import aiohttp_cors
from aiohttp.web import Application, Request, json_response

from asic_search import blog, portfolio, github


_timer = None  # type: Timer


def init(app: Application):
    global _timer
    _timer = Timer()

    log = logging.getLogger(__name__)
    github.pull()

    log.info('Configure CORS')
    cors = aiohttp_cors.setup(app, defaults={
        '*': {
            'max_age': 86400,
        },
    })

    log.info('Attaching routes')
    cors.add(app.router.add_get('/', health_check))
    cors.add(app.router.add_get('/blog', search_blog))
    cors.add(app.router.add_get('/combined', search_combined))
    cors.add(app.router.add_get('/portfolio', search_portfolio))
    cors.add(app.router.add_get('/touch', touch))

    log.info('Ready for requests')


def teardown(server_: Application):
    log = logging.getLogger(__name__)
    log.info('Tearing down')


#
# Routes
#

async def health_check(request: Request):
    return json_response({
        'uptime': _timer.duration,
        'commit': github.get_commit(),
    })


async def search_blog(request: Request):
    timer = Timer()
    github.pull_if_needed()
    return json_response({
        'results': blog.search(*_extract_query(request)),
        'duration': timer.duration,
        'commit': github.get_commit(),
    })


async def search_combined(request: Request):
    timer = Timer()
    github.pull_if_needed()
    query, tags_only = _extract_query(request)
    return json_response({
        'results': blog.search(query, tags_only) +
                   portfolio.search(query, tags_only),
        'duration': timer.duration,
        'commit': github.get_commit(),
    })


async def search_portfolio(request: Request):
    timer = Timer()
    github.pull_if_needed()
    return json_response({
        'results': portfolio.search(*_extract_query(request)),
        'duration': timer.duration,
        'commit': github.get_commit(),
    })


async def touch(request: Request):
    timer = Timer()
    log = logging.getLogger(__name__)
    log.info('Forcing git pull now')
    github.pull()
    return json_response({
        'duration': timer.duration,
        'commit': github.get_commit(),
    })


#
# Helpers
#

def _extract_query(request: Request):
    query = request.GET.get('query', '').strip().lower()
    tags_only = False
    if query.startswith('tagged:'):
        tags_only = True
        query = query[7:]
    return query, tags_only


class Timer:

    def __init__(self):
        self.start = time.time()

    @property
    def duration(self):
        return round(time.time() - self.start, 3)


#
# Bootstrapping
#

server = Application()
server.on_startup.append(init)
server.on_shutdown.append(teardown)
