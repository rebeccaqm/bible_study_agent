# Agente de Estudo Bíblico

Um agente de linha de comando que ajuda a estudar a Bíblia livro por livro, capítulo a capítulo — com contexto histórico/teológico, perguntas livres, resumos automáticos, e progresso salvo entre sessões.

Segue a tradição evangélica/protestante reformada, com referência a teólogos como John Piper, D.A. Carson, João Calvino, Jonathan Edwards, Wayne Grudem, entre outros.

## Como rodar

1. Instale as dependências:
- pip install google-genai python-dotenv
2. Configure sua chave da API do Gemini como variável de ambiente `GEMINI_API_KEY` (você pode gerar uma chave em https://aistudio.google.com/apikey)
3. Rode o script:
- python bible_study_agent.py

## Comandos disponíveis

- `vamos estudar [nome do livro]` — escolhe (ou troca para) um livro específico
- `próximo` — avança para o próximo capítulo do livro atual
- `anterior` — volta para o capítulo anterior
- `resumo` — gera um resumo do capítulo atual que está sendo estudado
- `sair` — encerra o programa
- Qualquer outra frase é tratada como uma pergunta livre para o agente

Perguntas livres podem ser feitas a qualquer momento, mesmo sem ter escolhido um livro ainda.

## Limitações conhecidas

- Os comandos de navegação (`vamos estudar`, `próximo`, `anterior`, `resumo`) exigem a sintaxe exata — frases livres como "vamos ler Gênesis" ou "quero voltar um capítulo" não são reconhecidas como comando, e serão tratadas como pergunta comum para o Gemini, sem alterar o progresso salvo.
- O progresso de capítulo é isolado por livro, mas o histórico de conversa é compartilhado entre todos os livros.

## Possíveis melhorias futuras

- Usar a própria IA para interpretar a intenção da pessoa em frases livres (ex: reconhecer "vamos pro capítulo 4" como comando de navegação)
- Tratamento de erros de conexão/indisponibilidade da API, sem derrubar o programa
- Exportar anotações/progresso para um arquivo de leitura mais amigável
