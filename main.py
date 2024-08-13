import vitibrasil as vb
from fastapi import FastAPI, Path, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from typing import Optional
from jose import JWTError, jwt

app = FastAPI()

# Config JWT
CHAVE_JWT = "92msdh23hsdfjkjj6d"
ALGORITMO = "HS256"

# Usuário de teste apenas para validar a autenticação da seção e atender ao requisito trabalho
# No próximo passo, o usuário e senha (com hash) devem ser persistidos em banco de dados 
usuario_ativo = {"username" : "fiap", "password" : "techchallenge"}

# Instância de OAuth2PasswordBearer - rota de autenticacao
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def autenticar_usuario(username: str, password: str):
    if username == usuario_ativo["username"] and password == usuario_ativo["password"]:
        return username
    return False
    
def criar_token_de_acesso(data: dict):
    to_encode = data.copy()
    token = jwt.encode(to_encode, CHAVE_JWT, algorithm=ALGORITMO)
    return token

async def obter_usuario_atual(token: str = Depends(oauth2_scheme)):
    credenciais_excecao = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, CHAVE_JWT, algorithms=[ALGORITMO])
        username: str = payload.get("sub")
        if username is None:
            raise credenciais_excecao
    except JWTError:
        raise credenciais_excecao
    
    if username != usuario_ativo["username"]:
            raise credenciais_excecao
    return username

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = autenticar_usuario(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = criar_token_de_acesso(data={"sub": user})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
async def home():
    return JSONResponse(content="Desafio Tech FIAP - 2MLET - Grupo 20")

@app.get("/vitivinicultura/producao", description="Produção de vinhos, sucos e derivados do Rio Grande do Sul")
async def obter_producao(current_user: str = Depends(obter_usuario_atual)):
    vitivinicultura = vb.VitiBrasil()
    return vitivinicultura.baixar_arquivo_producao()

@app.get("/vitivinicultura/processamento/{tipo_uva}", description="Quantidade de uvas processadas no Rio Grande do Sul")
async def obter_processamento(tipo_uva: vb.TipoUva = Path(..., description="Tipo de uva"), current_user: str = Depends(obter_usuario_atual)):
    vitivinicultura = vb.VitiBrasil()
    return vitivinicultura.baixar_arquivo_processamento(tipo_uva)

@app.get("/vitivinicultura/comercio", description="Comercialização de vinhos e derivados no Rio Grande do Sul")
async def obter_comercio(current_user: str = Depends(obter_usuario_atual)):
    vitivinicultura = vb.VitiBrasil()
    return vitivinicultura.baixar_arquivo_comercio()

@app.get("/vitivinicultura/importacao/{item_importacao}", description="Comercialização de vinhos e derivados no Rio Grande do Sul")
async def obter_importacao(item_importacao: vb.ItemImportacao = Path(..., description="Item de importação"), current_user: str = Depends(obter_usuario_atual)):
    vitivinicultura = vb.VitiBrasil()
    return vitivinicultura.baixar_arquivo_importacao(item_importacao)

@app.get("/vitivinicultura/exportacao/{item_exportacao}", description="Exportação de derivados de uva")
async def obter_exportacao(item_exportacao: vb.ItemExportacao = Path(..., description="Item de exportação"), current_user: str = Depends(obter_usuario_atual)):
    vitivinicultura = vb.VitiBrasil()
    return vitivinicultura.baixar_arquivo_exportacao(item_exportacao)
