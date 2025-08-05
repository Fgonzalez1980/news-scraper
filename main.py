from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import newspaper
from newspaper import Article
from newspaper.article import ArticleException
import uvicorn

app = FastAPI()

@app.get("/scrape")
def scrape(url: str = Query(..., description="URL da notícia")):
    try:
        article = Article(url, language='pt')
        article.download()
        article.parse()
        article.nlp()

        # Se o texto for muito curto, assume que é restrito
        if len(article.text.strip()) < 200:
            return JSONResponse(content={
                "title": article.title,
                "text": "(Conteúdo restrito a assinantes)",
                "summary": None
            })

        return JSONResponse(content={
            "title": article.title,
            "text": article.text,
            "summary": article.summary
        })
    except ArticleException as e:
        return JSONResponse(content={
            "title": None,
            "text": None,
            "summary": None,
            "error": str(e)
        }, status_code=400)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
