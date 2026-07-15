import os
from google import genai
from google.genai import types
import json

# Puxar a variável de ambiente do sistema para que ela armazene a api key da LLM
API_KEY = os.getenv("GEMINI_API_KEY", "")

# Configurando a API
pessoa = genai.Client(api_key="API_KEY")

print("--- ESTUDO BÍBLICO ---")
print("Vou te ajudar a compreender o texto.\n")
print("Digite 'sair' se quiser terminar o estudo.")


def carregar_historico():
    try:
        with open("historico.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        return dados
    except FileNotFoundError:
        return {"livro_atual": None, "historico": [], "livros": {}}

def salvar_historico(dados):
    with open("historico.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo)


dados = carregar_historico()
historico = dados["historico"]

while True:
    pergunta = input("Qual sua dúvida? ")

    if dados["livro_atual"] is not None:
        progresso = dados["livros"][dados["livro_atual"]]
    else:
        progresso = None

    if pergunta.lower().startswith("vamos estudar"):
        partes = pergunta.split()
        nome_livro = " ".join(partes[2:])
        if nome_livro not in dados["livros"]:
            dados["livros"][nome_livro] = {"capitulo_atual": 1}
        dados["livro_atual"] = nome_livro
        salvar_historico(dados)
        print(f"Agora estamos estudando {nome_livro}")
        continue
    if pergunta.lower() == "sair":
        print("Deus abençoe!")
        break
    if pergunta.lower() == "próximo":
        if progresso is None:
            print("Escolha um livro primeiro (ex: vamos estudar João)")
            continue
        progresso["capitulo_atual"] += 1
        salvar_historico(dados)
        print(f"Avançamos para o capítulo {progresso['capitulo_atual']}")
        continue
    if pergunta.lower() == "anterior":
        if progresso is None:
            print("Escolha um livro primeiro (ex: vamos estudar João)")
            continue
        if progresso["capitulo_atual"] > 1:
            progresso["capitulo_atual"] -= 1
            print(f"Voltamos para o capítulo {progresso['capitulo_atual']}")
        else:
            print("Você já está no capítulo 1, não dá para voltar mais.")
        salvar_historico(dados)
        continue
    if pergunta.lower() == "resumo":
        if progresso is None:
            print("Escolha um livro primeiro (ex: vamos estudar João)")
            continue
        pergunta = f"Me dê um resumo claro e didático sobre o capítulo {progresso['capitulo_atual']} que estamos estudando."

    if progresso is None:
        pass
    else:
        pergunta = f"[Contexto: estudando {dados['livro_atual']}, capítulo {progresso['capitulo_atual']}] {pergunta}"

    historico.append({"role": "user", "parts": [{"text": pergunta}]})

    resposta = pessoa.models.generate_content (
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="""Você é um assistente de estudos bíblicos. Você segue a linha reformada,
            a qual tem como teólogos John Piper, D.A Carson, João Calvino, Jonathan Edwards, Augustus Nicodemus,
            Franklin Ferreira, Wayne Grudem e semelhantes. Você foi programado para ajudar quem está estudando a bíblia.
            A pessoa escolhe o livro, você mostrará quem é o autor, a data, a estrutura, o tema central e contexto histórico.
            A pessoa avança capítulo a capítulo, você dá um resumo/contexto de cada capítulo antes ou depois da pessoa ler.
            A pessoa faz perguntas livres a qualquer momento, você responde com base em ferramentas de estudo (comentários, referências cruzadas).
            Você guardará o progresso (em que capítulo a pessoa parou, quais perguntas ela já fez, principais insights dela).
            Você, de vez em quando, sugere conexões (ex: liga um versículo de Deuteronômio com um do Novo Testamento), no momento apropriado."""
        ),
        contents=historico
    )

    historico.append({"role": "model", "parts": [{"text": resposta.text}]})
    salvar_historico(dados)

    print(f"\n{resposta.text}\n")