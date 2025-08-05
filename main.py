from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from newspaper import Article
import uvicorn

app = FastAPI()

@app.get("/scrape")
def scrape(url: str = Query(..., description="URL da notícia para extrair conteúdo")):
    try:
        article = Article(url)
        article.download()
        article.parse()

        return {
            "url": url,
            "titulo": article.title,
            "texto": article.text
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.get("/")
def home():
    return {"status": "OK", "mensagem": "Scraper API está no ar!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
