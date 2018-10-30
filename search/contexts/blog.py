import os.path
import re

import markdown
import yaml

from search.github import REPO_PATH


BASE_URL = 'https://bazile.org'
PATTERN_MARKDOWN = re.compile("""^---\n(?P<meta>.*)\n---\n\n?(?P<content>.*)$""",
                              re.MULTILINE | re.DOTALL)


def search(query: str, tags_only: bool):
    results = []
    for entry in os.scandir(os.path.join(REPO_PATH, 'data/markdown')):
        if not entry.is_file():
            continue

        post = _deserialize_post(entry)

        result = _to_result(post, entry.name)

        # Search tags
        if query in result['tags']:
            results.append(result)
            continue
        if tags_only:
            continue

        # Search everywhere else
        search_space = ' '.join([post['body'], post['abstract'], post['subject']]).lower()
        if query in search_space:
            results.append(result)

    return sorted(results, key=lambda d: d['blog:date'], reverse=True)


def _deserialize_post(entry):
    with open(entry.path) as fp:
        matches = PATTERN_MARKDOWN.search(fp.read())
    if not matches:
        raise ValueError('missing metadata')

    raw_meta, raw_body = matches.groups()

    parser = markdown.Markdown(
        extensions=[
            'markdown.extensions.smarty',
        ],
        extension_configs={
            'markdown.extensions.smarty': {
                'substitutions': {
                    'left-single-quote': '‘',
                    'right-single-quote': '’',
                    'left-double-quote': '“',
                    'right-double-quote': '”',
                },
            },
        },
    )

    post = {k.lower(): v for k, v in yaml.load(raw_meta).items()}
    post['abstract'] = parser.convert(post.get('abstract', ''))
    post['body'] = parser.convert(raw_body)
    post.setdefault('type', 'text')

    return post


def _to_plaintext(html: str):
    return re.sub(r'<[^>]+>', '', html)


def _to_result(post: dict, filename: str) -> dict:
    result = {
        'type':        'blog',
        'subject':     post['subject'],
        'description': _to_plaintext(post['abstract']),
        'tags':        post['tags'],
        'uri':         _to_uri(post['date'], filename),
        'blog:date':   post['date'],
        'blog:type':   post['type'],
    }

    if result['blog:type'] in ('link', 'image'):
        result['blog:url'] = re.sub(r'^(\.\.|/)', BASE_URL, post['url'])

    return result


def _to_uri(date, filename):
    return '{}/writing/{}/{}.html'.format(
        BASE_URL,
        date.year,
        re.sub(r'\W+', '_', re.sub('\.md$', '', filename)),
    )
