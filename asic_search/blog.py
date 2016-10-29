import os.path
import re

import markdown

from asic_search.github import REPO_PATH

BASE_URL = 'http://andsoitcontinues.com'


def search(query: str, tags_only: bool):
    results = []
    parser = markdown.Markdown(extensions=['markdown.extensions.meta'])
    for entry in os.scandir(os.path.join(REPO_PATH, 'data/markdown')):
        if not entry.is_file():
            continue

        parser.reset()
        with open(entry.path) as f:
            body = parser.convert(f.read())
            meta = dict((k, v.pop()) for k, v in parser.Meta.items())
            abstract = parser.convert(meta.get('abstract', body))
            plaintext_abstract = _to_plaintext(abstract)
            plaintext_body = _to_plaintext(body)

        result = {
            'type': 'blog',
            'subject': meta['subject'],
            'description': plaintext_abstract,
            'tags': [s.strip() for s in meta['tags'].lower().split(',')],
            'uri': _to_uri(entry.name),
            'blog:date': meta['date'],
            'blog:type': meta.get('type', 'text'),
        }

        if result['blog:type'] in ('link', 'image'):
            result['blog:url'] = re.sub(r'^\.\.', BASE_URL, meta['url'])

        if query in result['tags']:
            results.append(result)
            continue

        if tags_only:
            continue
        elif query in plaintext_body.lower():
            results.append(result)
        elif query in result['subject'].lower():
            results.append(result)

    return sorted(results, key=lambda d: d['blog:date'], reverse=True)


def _to_plaintext(html: str):
    return re.sub(r'<[^>]+>', '', html)


def _to_uri(s):
    return '{}/writing/{}.html'.format(
        BASE_URL,
        re.sub(r'\W+', '_', re.sub('\.md$', '', s)),
    )
