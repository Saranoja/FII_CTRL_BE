from xml.etree import ElementTree
from typing import List, Union
import re
import xml

whitespace_re = re.compile(r'\s+')
ns = {
    'atom': 'http://www.w3.org/2005/Atom',
    'arxiv': 'http://arxiv.org/schemas/atom'
}


def parse_response(xml_string: str) -> Union[List[dict], bool]:
    try:
        root = ElementTree.fromstring(xml_string)
    except xml.etree.ElementTree.ParseError:
        return False

    # Store 'math' and 'cs' categories in cs_entries
    filtered_entries = []
    entries = root.findall('atom:entry', ns)
    for entry in entries:
        for category in entry.findall('atom:category', ns):
            if category.attrib['term'].startswith('cs') or category.attrib['term'].startswith('math'):
                filtered_entries.append(entry)
                continue

    responses: List[dict] = []
    for entry in filtered_entries:
        title = entry.find('atom:title', ns).text
        title = whitespace_re.sub(' ', title).strip()
        summary = entry.find('atom:summary', ns).text
        summary = whitespace_re.sub(' ', summary).strip()
        authors = [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)]
        authors = list(map(lambda author: whitespace_re.sub(' ', author).strip(), authors))
        link = entry.find("atom:link[@title='pdf']", ns).attrib['href']

        response = {
            'title': title,
            'summary': summary,
            'authors': authors,
            'link': link
        }
        if response not in responses:
            responses.append(response)

    return responses
