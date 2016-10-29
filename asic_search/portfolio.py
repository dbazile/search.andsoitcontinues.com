import os.path
import re
import xml.etree.ElementTree as et

from asic_search.github import REPO_PATH

BASE_URL = 'http://andsoitcontinues.com'
DTD_PREAMBLE = """\
<!DOCTYPE portfolio-item [
<!ENTITY quot    "&#34;">
<!ENTITY amp     "&#38;#38;">
<!ENTITY lt      "&#38;#60;">
<!ENTITY gt      "&#62;">
<!ENTITY apos    "&#39;">
<!ENTITY ndash   "&#8211;">
<!ENTITY mdash   "&#8212;">
<!ENTITY lsquo   "&#8216;">
<!ENTITY rsquo   "&#8217;">
<!ENTITY ldquo   "&#8220;">
<!ENTITY rdquo   "&#8221;">
]>
"""


def search(query: str, tags_only: bool):
    results = []
    for entry in os.scandir(os.path.join(REPO_PATH, 'data/xml')):
        tree = et.fromstring(_prepare_xml(entry.path))

        result = {
            'type': 'portfolio',
            'description': re.sub(r'\s+', ' ', tree.findtext('summary')).strip(),
            'subject': tree.findtext('name'),
            'tags': [node.text.lower() for node in tree.findall('tag')],
            'uri': _to_uri(tree.findtext('name')),
            'portfolio:circa': int(tree.findtext('circa')),
            'portfolio:type': tree.get('type'),
        }

        if result['portfolio:type'] == 'photoshop':
            result['portfolio:thumbnail'] = _to_thumbnail_uri(tree.find('artifact').get('thumbnail'))
        else:
            result['portfolio:thumbnail'] = _to_thumbnail_uri(tree.findtext('brand'))
            result['portfolio:technologies'] = tree.findtext('technologies')

        if query in result['tags']:
            results.append(result)
            continue

        if tags_only:
            continue
        elif query in result['subject'].lower():
            results.append(result)
        elif query in result['description'].lower():
            results.append(result)
    return sorted(results, key=lambda d: d['portfolio:circa'], reverse=True)


def _to_thumbnail_uri(relative_uri: str):
    return '{}/{}'.format(
        BASE_URL,
        re.sub(r'^\.\.', '', relative_uri),
    )


def _to_uri(subject: str):
    return '{}/portfolio/index.html#{}'.format(
        BASE_URL,
        re.sub(r'\W', '-', subject.lower()),
    )


def _prepare_xml(filepath):
    with open(filepath) as fp:
        return DTD_PREAMBLE + fp.read()
