
def parse_article(xml_tree):
    root = xml_tree.getroot()
    materias = []
    for article in root.findall('.//article'):
        materias.append({
            'orgao': article.attrib.get('artCategory', ''),
            'data': article.attrib.get('pubDate', ''),
            'titulo': article.attrib.get('name', ''),
            'conteudo': article.findtext('.//Texto') or article.findtext('.//body')
        })
    return materias
