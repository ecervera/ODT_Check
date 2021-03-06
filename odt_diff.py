from odt_parse import str_decode

def style_id(name, par_st):
    if name[0]=='P' or name[0]=='p':
        parent = [st['parent'] for st in par_st if st['name']==name]
        sid = 'formato directo sobre ' + parent[0]
    else:
        sid = name
    return sid

def find_style_by_name(stlist, name):
    dname = str_decode(name)
    st = [st for st in stlist if st['name'] == dname]
    if st:
          return st[0]
    else:
          return None

def find_heading_by_text(hlist, text):
    return [h for h in hlist if text in h['text']]  

def find_par_by_text(plist, text):
    return [p for p in plist if text in p['text']]

def odt_compare(ref, doc):
    s = ''

    s += '<h1>Comprobación de <tt>libro_predefinidos</tt></h1>'
    if doc.emptyHeadings == 1:
        s+= '<p>El documento tiene %d título vacío, debes eliminarlo.</p>' % doc.emptyHeadings
    elif doc.emptyHeadings > 1:
        s+= '<p>El documento tiene %d títulos vacíos, debes eliminarlos.</p>' % doc.emptyHeadings
    if doc.emptyPars == 1:
        s+= '<p>El documento tiene %d párrafo vacío, debes eliminarlo.</p>' % doc.emptyPars
    elif doc.emptyPars > 1:
        s+= '<p>El documento tiene %d párrafos vacíos, debes eliminarlos.</p>' % doc.emptyPars
    else:
        s+= '<p>El documento no tiene párrafos vacíos, ¡muy bien!</p>'

    s += '<hr>'
    
    try:
        num_doc_H = len(doc.H)
    except AttributeError:
        num_doc_H = 0
    try:
        num_ref_H = len(ref.H)
    except AttributeError:
        num_ref_H = 0

    if num_doc_H != num_ref_H:
        s+= '<p>El documento tiene %d títulos en lugar de %d. Corrígelo para poder comprobar los estilos de título.</p>' % (num_doc_H, num_ref_H)
    else:
        s += '<p>El número de títulos es correcto.</p>'
        s += '<h2>Estilos de títulos</h2>'
        try:
            diffs = 0
            for i in range(len(ref.H)):
                ref_id = style_id(ref.H[i]['style'], ref.style['paragraph'])
                doc_id = style_id(doc.H[i]['style'], doc.style['paragraph'])
                if ref_id != doc_id:
                    s += '<p>El título "%s..." tiene estilo <tt>%s</tt> en lugar de <tt>%s</tt>.</p>' % (doc.H[i]['text'][:15], doc_id, ref_id)
                    diffs += 1
            if diffs == 0:
                s += '<p>Todos los títulos tienen el estilo correcto.</p>'
        except IndexError:
            pass

    s += '<hr>'

    if len(doc.P)!=len(ref.P):
        s+= '<p>El documento tiene %d párrafos en lugar de %d. Corrígelo para poder comprobar los estilos de párrafo.</p>' % (len(doc.P), len(ref.P))
    else:
        s += '<p>El número de párrafos es correcto.</p>'
        s += '<h2>Estilos de párrafos</h2>'
        try:
            diffs = 0
            for i in range(len(ref.P)):
                ref_id = style_id(ref.P[i]['style'], ref.style['paragraph'])
                doc_id = style_id(doc.P[i]['style'], doc.style['paragraph'])
                if ref_id != doc_id:
                    s += '<p>El párrafo "%s..." tiene estilo <tt>%s</tt> en lugar de <tt>%s</tt>.</p>' % (doc.P[i]['text'][:30], doc_id, ref_id)
                    diffs += 1
            if diffs == 0:
                s += '<p>Todos los párrafos tienen el estilo correcto.</p>'
        except IndexError:
            pass
    
    return s
