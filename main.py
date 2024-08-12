import vitibrasil as vb
from fastapi import FastAPI, Path
from fastapi.responses import JSONResponse


app = FastAPI()

@app.get("/")
def home():
    return JSONResponse(content="Tech challenge FIAP - 2MLET - Grupo 20")

@app.get("/vitivinicultura/producao", description="Produção de vinhos, sucos e derivados do Rio Grande do Sul")
def obter_produtcao():
    vitivinicultura = vb.VitiBrasil()
    return vitivinicultura.baixar_arquivo_producao()
    
@app.get("/vitivinicultura/processamento/{tipo_uva}", description="Quantidade de uvas processadas no Rio Grande do Sul")
def obter_processamento(tipo_uva: vb.TipoUva = Path(..., description="Tipo de uva")):
    vitivinicultura = vb.VitiBrasil()
    return vitivinicultura.baixar_arquivo_processamento(tipo_uva)

@app.get("/vitivinicultura/comercio", description="Comercialização de vinhos e derivados no Rio Grande do Sul")
def obter_comercio():
    vitivinicultura = vb.VitiBrasil()
    return vitivinicultura.baixar_arquivo_comercio()

@app.get("/vitivinicultura/importacao/{item_importacao}", description="Comercialização de vinhos e derivados no Rio Grande do Sul")
def obter_importacao(item_importacao: vb.ItemImportacao = Path(..., description="Item de importação")):
    vitivinicultura = vb.VitiBrasil()
    return vitivinicultura.baixar_arquivo_importacao(item_importacao)

@app.get("/vitivinicultura/exportacao/{item_exportacao}", description="Exportação de derivados de uva")
def obter_exportacao(item_exportacao: vb.ItemExportacao = Path(..., description="Item de exportação")):
    vitivinicultura = vb.VitiBrasil()
    return vitivinicultura.baixar_arquivo_exportacao(item_exportacao)
