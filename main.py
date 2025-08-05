import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from newspaper import Article
from urllib.parse import unquote

app = FastAPI()

@app.get("/scrape")
def scrape(url: str):
    decoded_url = unquote(url)
    try:
        article = Article(decoded_url, language='pt')
        article.download()
        article.parse()

        texto = article.text.strip()
        if not texto:
            texto = "(Conteúdo não acessível ou restrito)"

        # Sempre inclui o link no final
        texto += f"\n\nLink: {decoded_url}"

        return {
            "url": decoded_url,
            "titulo": article.title.strip() if article.title else "",
            "texto": texto
        }
    except Exception as e:
        # Em caso de erro, mantém o link no final
        return {
            "url": decoded_url,
            "titulo": "",
            "texto": f"(Erro ao processar: {str(e)})\n\nLink: {decoded_url}"
        }

@app.get("/")
def home():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Railway define PORT
    uvicorn.run(app, host="0.0.0.0", port=port)
