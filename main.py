import os
import uvicorn
import logging
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from newspaper import Article
from urllib.parse import unquote

# Configuração de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("news-scraper")

app = FastAPI(title="News Scraper API", version="1.0")

@app.get("/")
def home():
    return {"status": "ok", "message": "News Scraper API online"}

@app.get("/scrape")
def scrape(url: str = Query(..., description="URL da notícia a ser extraída")):
    try:
        logger.info(f"Recebida requisição para URL: {url}")

        decoded_url = unquote(url)
        logger.info(f"URL decodificada: {decoded_url}")

        article = Article(decoded_url, language='pt')

        logger.info("Baixando conteúdo...")
        article.download()
        logger.info("Download concluído. Iniciando parsing...")
        article.parse()
        logger.info("Parsing concluído com sucesso.")

        return {
            "url": decoded_url,
            "titulo": article.title,
            "texto": article.text
        }

    except Exception as e:
        logger.error(f"Erro ao processar URL: {url} - Erro: {str(e)}", exc_info=True)
        return JSONResponse(content={"erro": str(e)}, status_code=500)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Railway define a variável PORT
    logger.info(f"Iniciando servidor na porta {port}...")
    uvicorn.run("main:app", host="0.0.0.0", port=port)
