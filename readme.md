
# Downloader de legendas

Uma aplicação feita para verificar e baixar legendas faltantes dos seus animes.

A aplicação pega as legendas faltantes do bazarr, procura como nome da serie, temporada e episodio no site animetosho (indexer de anime para prowlarr), caso ele ache uma legenda que contem por ou pt no link, ele baixa e dps anexa ao episodio atravez da api do bazarr.
## Variáveis de Ambiente

Para rodar esse projeto, você vai precisar adicionar as seguintes variáveis de ambiente no seu .env

`BAZARR_URL` - link de acesso para a api do bazarr

`BAZARR_API_KEY` - chave de acesso a api

`NOTIFICATION_URL` - link do ntfy para notificações de erro no programa


## Referência

 - [Bazarr](https://www.bazarr.media/)
 - [Animetosho](https://animetosho.org/)
