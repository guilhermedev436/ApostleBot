ApostleBot
============

Bot Discord em Python para gerenciamento de liturgias e moderação automática.

**Principais funcionalidades**
- `liturgia` (/liturgia): busca e exibe a liturgia diária ou de uma data específica.
- Envio automático diário da liturgia para um canal configurado.
- Automod: remove mensagens em *threads* de canal específico contendo palavras/expressões proibidas e registra advertências em um canal de logs.
- Comando `/info` para informações sobre o bot.

**Arquivos principais**
- [main.py](main.py) — código-fonte do bot e configuração principal.
- [requirements.txt](requirements.txt) — dependências do projeto.
- [LICENSE](LICENSE) — licença do projeto.

**Instalação**
1. Crie e ative um ambiente virtual (recomendado):

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

2. Instale dependências:

```bash
pip install -r requirements.txt
```

3. Crie um arquivo `.env` na raiz com a variável `DISCORD_TOKEN`:

```
DISCORD_TOKEN=seu_token_aqui
```

**Configuração**
- No `main.py` existem constantes que devem ser ajustadas para o seu servidor:
  - `DEBATE_CHANNEL_ID` — ID do fórum/canal de debate onde o automod deve atuar.
  - `LOG_CHANNEL_ID` — ID do canal onde serão registrados avisos/infrações.
  - `MOD_ROLE_ID` e `ADMIN_ROLE_ID` — IDs de cargos que serão mencionados quando houver infrações.
- A lista de `PALAVRAS_PROIBIDAS` também está em `main.py` e pode ser atualizada conforme necessidade.

**Como executar**

```bash
python main.py
```

O bot usa intents de mensagem e precisa do token com permissões adequadas para ler e deletar mensagens, além de gerenciar mensagens em threads.

**Comandos principais**
- `/liturgia [DD-MM-YYYY]` — mostra a liturgia do dia ou da data informada.
- `/info` — informações sobre o bot e suas funcionalidades.

**Automod**
- O automod monitora apenas mensagens dentro de *threads* cujo `parent_id` corresponde a `DEBATE_CHANNEL_ID`.
- Ao detectar uma expressão proibida, o bot deleta a mensagem, envia um aviso temporário ao usuário e registra a ocorrência no canal de logs com um embed contendo dados do usuário, canal e a palavra/expressão detectada.

**Observação sobre auxílio de IA**
Partes deste projeto foram desenvolvidas com auxílio de IAs (por exemplo, refinamento de regex para moderação, sugestões de mensagens e estrutura de embeds e boa parte da api da liturgia). O código final foi revisado e adaptado manualmente pelo autor.

**Contribuição**
- Pull requests são bem-vindos. Antes de enviar mudanças, abra uma issue descrevendo a alteração planejada.

**Licença**
- Veja o arquivo [LICENSE](LICENSE) para detalhes.
