import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from newspaper import Article, Config
from urllib.parse import unquote
import requests

app = FastAPI()

# Configuração do newspaper3k
config = Config()
config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36'
config.request_timeout = 15  # segundos

@app.get("/scrape")
def scrape(url: str):
    try:
        decoded_url = unquote(url)

        # Primeiro, testa se o site responde sem bloqueio
        head_resp = requests.head(decoded_url, headers={"User-Agent": config.browser_user_agent}, timeout=10)
        if head_resp.status_code == 403:
            return {
                "url": decoded_url,
                "titulo": "",
                "texto": "(Conteúdo não acessível - bloqueado pelo site)"
            }

        # Faz o scraping do artigo
        article = Article(decoded_url, language='pt', config=config)
        article.download()
        article.parse()

        return {
            "url": decoded_url,
            "titulo": article.title,
            "texto": article.text
        }
    except Exception as e:
        # Em caso de erro, retorna aviso mas não quebra o fluxo
        return {
            "url": url,
            "titulo": "",
            "texto": f"(Erro ao processar - {str(e)})"
        }

@app.get("/")
def home():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Railway define PORT
    print(f"Iniciando servidor na porta {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
