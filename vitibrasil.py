from enum import Enum
import requests
import csv
import io
from fastapi.responses import JSONResponse


class TipoUva(str, Enum):
    viniferas = "viniferas"
    americanas_e_hibridas =  "americanas-e-hibridas" 
    uvas_de_mesa = "uvas-de-mesa"
    sem_clasificacao = "sem-clasificacao"

class ItemImportacao(str, Enum):
    vinhos_de_mesa = "vinhos-de-mesa"
    espumantes =  "espumantes" 
    uvas_frescas = "uvas-frescas"
    uvas_passas = "uvas-passas"
    suco_de_uva = "suco-de-uva"

class ItemExportacao(str, Enum):
    vinhos_de_mesa = "vinhos-de-mesa"
    espumantes =  "espumantes" 
    uvas_frescas = "uvas-frescas"
    suco_de_uva = "suco-de-uva"


url_download = {
    "producao": "http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv",
    TipoUva.viniferas: "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv",
    TipoUva.americanas_e_hibridas: "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaAmericanas.csv",
    TipoUva.uvas_de_mesa: "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaMesa.csv",
    TipoUva.sem_clasificacao: "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaSemclass.csv",
    "comercio": "http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv",
    ItemImportacao.vinhos_de_mesa: "http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv",
    ItemImportacao.espumantes: "http://vitibrasil.cnpuv.embrapa.br/download/ImpEspumantes.csv",
    ItemImportacao.uvas_frescas: "http://vitibrasil.cnpuv.embrapa.br/download/ImpFrescas.csv",
    ItemImportacao.uvas_passas: "http://vitibrasil.cnpuv.embrapa.br/download/ImpPassas.csv",
    ItemImportacao.suco_de_uva: "http://vitibrasil.cnpuv.embrapa.br/download/ImpSuco.csv",
    ItemExportacao.vinhos_de_mesa : "http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv",
    ItemExportacao.espumantes: "http://vitibrasil.cnpuv.embrapa.br/download/ExpEspumantes.csv",
    ItemExportacao.uvas_frescas : "http://vitibrasil.cnpuv.embrapa.br/download/ExpUva.csv",
    ItemExportacao.suco_de_uva: "http://vitibrasil.cnpuv.embrapa.br/download/ExpSuco.csv"
}


def baixar_arquivo_csv(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        raise Exception(f"Falha ao baixar arquivo. Status code: {response.status_code}")



def converter_csv_para_json(conteudo_csv, delimitador = ";"):
    # converte csv para uma lista de dicionários
    leitor = csv.DictReader(io.StringIO(conteudo_csv), delimiter=delimitador)
    dicionarios = [row for row in leitor]

    # converte para json
    return JSONResponse(content=dicionarios)

def baixar_csv_e_converter_para_json(url, delimitador = ";"):
    conteudo_csv = baixar_arquivo_csv(url)
    return converter_csv_para_json(conteudo_csv, delimitador = delimitador)
     

class VitiBrasil(object):
    
    def baixar_arquivo_producao(self):
        return baixar_csv_e_converter_para_json(url_download["producao"])
    
    def baixar_arquivo_processamento(self, tipo_uva: TipoUva):
        if tipo_uva == TipoUva.viniferas:
            return baixar_csv_e_converter_para_json(url_download[tipo_uva])
        else:
            return baixar_csv_e_converter_para_json(url_download[tipo_uva], delimitador="\t")
    
    def baixar_arquivo_comercio(self):
        return baixar_csv_e_converter_para_json(url_download["comercio"])
    
    def baixar_arquivo_importacao(self, item: ItemImportacao):
        return baixar_csv_e_converter_para_json(url_download[item])
    
    def baixar_arquivo_exportacao(self, item: ItemExportacao):
        return baixar_csv_e_converter_para_json(url_download[item])

