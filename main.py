import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from newspaper import Article
from urllib.parse import unquote

app = FastAPI()

@app.get("/scrape")
def scrape(url: str):
    try:
        decoded_url = unquote(url)
        article = Article(decoded_url, language='pt')
        article.download()
        article.parse()

        return {
            "url": decoded_url,
            "titulo": article.title,
            "texto": article.text
        }
    except Exception as e:
        return JSONResponse(content={"erro": str(e)}, status_code=500)

@app.get("/")
def home():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Railway define PORT
    uvicorn.run(app, host="0.0.0.0", port=port)
