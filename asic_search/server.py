import logging
import time

from flask import Flask, request, jsonify
from flask_cors import CORS

from asic_search import blog, portfolio, github


_time_started = time.time()

server = Flask(__name__)
CORS(server, origins='*', max_age=86400)

github.pull()


#
# Routes
#

@server.route('/')
def health_check():
    return jsonify({
        'uptime': _get_duration(_time_started),
        'commit': github.get_commit(),
    })


@server.route('/combined')
def search_all():
    start = time.time()
    github.pull_if_needed()
    query, tags_only = _get_criteria()
    blog_results = blog.search(query, tags_only)
    portfolio_results = portfolio.search(query, tags_only)
    return jsonify({
        'results': [*blog_results, *portfolio_results],
        'duration': _get_duration(start),
        'commit': github.get_commit(),
    })


@server.route('/blog')
def search_blog():
    start = time.time()
    github.pull_if_needed()
    return jsonify({
        'results': blog.search(*_get_criteria()),
        'duration': _get_duration(start),
        'commit': github.get_commit(),
    })


@server.route('/portfolio')
def search_portfolio():
    start = time.time()
    github.pull_if_needed()
    return jsonify({
        'results': portfolio.search(*_get_criteria()),
        'duration': _get_duration(start),
        'commit': github.get_commit(),
    })


@server.route('/touch')
def touch():
    start = time.time()
    logging.getLogger(__name__).info('Forcing git pull now')
    github.pull()
    return jsonify({
        'duration': _get_duration(start),
        'commit': github.get_commit(),
    })


#
# Helpers
#

def _get_duration(start_time: float):
    return round(time.time() - start_time, 3)


def _get_criteria():
    query = request.args.get('query', '').strip().lower()
    tags_only = False
    if query.startswith('tagged:'):
        tags_only = True
        query = query[7:]
    return query, tags_only
