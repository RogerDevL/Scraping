import requests #Responsavel por enviar a requisição
from bs4 import BeautifulSoup # Responsavel por tratar a requisição
from flask import Flask, render_template



app = Flask(__name__) 

@app.route("/")
def previsao_tempo():
    url = "https://www.climatempo.com.br/previsao-do-tempo/cidade/558/saopaulo-sp"

    headers = {
    "User-Agent": "Mozilla/5.0 (windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    resposta = requests.get(url, headers=headers)

    if resposta.status_code != 200:
        return "Erro ao buscar dados do Climatempo."

    soup = BeautifulSoup(resposta.text, "html.parser")

     # previsao hoje
    previsao = soup.find_all("h1", class_="-bold -font-18 -dark-blue _margin-r-10")
    previsoes = []
    for bloco in previsao:
        texto = bloco.get_text(strip=True)
        texto = " ".join(texto.split()) 
        print(f"{texto}")
        print("\n")
        previsoes.append(texto)

    # descricao hoje de São Paulo SP
    sp = soup.find_all("p", class_="-gray -line-height-24 _center")
    descricoes = []
    print("São Paulo, tempo:")
    for noticia in sp:
            descricao = noticia.text.strip() if noticia else "Descrição não encontrada"
            p = noticia.get_text(strip=True)
            linhas = [linha.strip() for linha in noticia.stripped_strings]
            texto = " ".join(linhas).replace("  ", " ")
            texto = " ".join(texto.split()) 
            print(texto)
            print("\n")
            descricoes.append(texto)

    # mais detalhes da previsao em São Paulo SP
    tempo_detalhado = soup.find("ul", class_="variables-list")
    detalhes_dia = []
    print("Tempo detalhado:")
    if tempo_detalhado:
        itens = tempo_detalhado.find_all("li")
        for i, item in enumerate(itens, start=1):
            linhas = [linha.strip() for linha in item.stripped_strings]
            texto = " | ".join(linhas)
            texto = " ".join(texto.split())
            print(f"{i}. {texto}")
            detalhes_dia.append(f"{i}. {texto}")

    # mais detalhes do clima(saúde, registros de hoje e proximidades)
    detalhes = soup.find_all("ul", class_="list")
    detalhes_climas =[]
    print("Mais detalhes do clima:")
    for index, ul in enumerate(detalhes, start=1):
        itens = ul.find_all("li")
        for i, item in enumerate(itens, start=1):
            linhas = [linha.strip() for linha in item.stripped_strings]
            texto = item.get_text(strip=True)
            texto = " | ".join(linhas)
            texto = " ".join(texto.split()) 
            print(f"  {i}. {texto}\n")
            detalhes_climas.append(texto)

        
    return render_template(
        "clima.html",
        previsoes=previsoes,
        descricoes=descricoes,
        detalhes_dia=detalhes_dia,
        detalhes_climas=detalhes_climas
    )
    

if __name__ == "__main__":
    app.run(debug=True)



