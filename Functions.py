def extract_vagadesc(reader):
    vagadesc = reader.get_page(0).extract_text()
    linhas = vagadesc.splitlines()
    return "\n".join(linhas[2:-1])

def extract_cvdesc(reader):
    paginas = []
    for page in reader.pages:
        texto = page.extract_text()
        linhas = texto.splitlines()
        cv = "\n".join(linhas[2:-1])
        paginas.append(cv)
    return paginas

def emb_cv(paginas, model):
    vetores = []
    for texto in paginas:
        emb = model.encode(texto)
        vetores.append(emb)
    return vetores

def similaridade_cvaga(emb_cv, emb_vaga, util):
    vetores = []
    for emb_cv in emb_cv:
        similaridade_cvaga = util.cos_sim(emb_cv, emb_vaga)[0][0].item()
        vetores.append(similaridade_cvaga)
    return vetores