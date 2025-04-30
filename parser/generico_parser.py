
def parse_generico(xml_tree):
    root = xml_tree.getroot()
    materias = []
    for materia in root.findall('.//materia'):
        mat = {}
        for elem in materia.iterchildren():
            if elem.tag and elem.text:
                mat[elem.tag] = elem.text.strip()
        materias.append(mat)
    return materias
