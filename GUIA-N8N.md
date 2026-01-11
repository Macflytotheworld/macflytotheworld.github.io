# 🔗 Guia de Integração MacFly + n8n

Este guia explica como conectar o MacFly ao n8n para automatizar o fluxo de publicação no TikTok.

---

## 📋 Pré-requisitos

1. **n8n instalado** (self-hosted ou n8n.cloud)
2. **App TikTok registada** no [TikTok Developer Portal](https://developers.tiktok.com/)
3. **Credenciais TikTok:**
   - Client Key
   - Client Secret
   - Redirect URI (ex: `https://teu-dominio.com/callback.html`)

---

## 🚀 Configuração Passo a Passo

### 1. Importar o Workflow no n8n

1. Abre o n8n
2. Vai a **Workflows** → **Import from File**
3. Seleciona o ficheiro `n8n-workflow-template.json`
4. O workflow será importado com todos os nós configurados

### 2. Configurar Variáveis no n8n

No n8n, vai a **Settings** → **Variables** e cria:

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `TIKTOK_CLIENT_KEY` | Client Key da tua app TikTok | `abc123xyz` |
| `TIKTOK_CLIENT_SECRET` | Client Secret da tua app TikTok | `secret456` |
| `TIKTOK_REDIRECT_URI` | URL de callback | `https://macfly.vercel.app/callback.html` |

### 3. Ativar o Workflow

1. Abre o workflow importado
2. Clica em **Active** (canto superior direito)
3. Copia a **URL do Webhook** (clica no nó "Webhook - Receive Auth Code")
   - Exemplo: `https://teu-n8n.app.n8n.cloud/webhook/macfly-tiktok`

### 4. Configurar o Callback do MacFly

**Opção A: Configurar na página**
1. Abre `callback.html` no browser
2. Cola a URL do webhook n8n no campo
3. Clica "Guardar URL"

**Opção B: Configurar no código**
1. Abre `callback.html`
2. Encontra a linha `const N8N_WEBHOOK_URL = '';`
3. Substitui por:
```javascript
const N8N_WEBHOOK_URL = 'https://teu-n8n.app.n8n.cloud/webhook/macfly-tiktok';
const AUTO_SEND_TO_N8N = true; // Enviar automaticamente
```

---

## 🔄 Como Funciona o Fluxo

```
┌─────────────────┐
│  Utilizador     │
│  clica "Login   │
│  com TikTok"    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  TikTok OAuth   │
│  (autorização)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  callback.html  │◄── Recebe o código de autorização
│  (MacFly)       │
└────────┬────────┘
         │
         ▼ POST automático
┌─────────────────┐
│  n8n Webhook    │◄── Recebe: { authorization_code, state, timestamp }
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  n8n troca o    │
│  código por     │──► POST para api.tiktok.com/oauth/token
│  access_token   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Guarda tokens  │
│  e open_id      │
└─────────────────┘
```

---

## 📡 Endpoints TikTok (Referência)

### Trocar código por token
```
POST https://open.tiktokapis.com/v2/oauth/token/
Content-Type: application/x-www-form-urlencoded

client_key=XXX
client_secret=XXX
code=AUTH_CODE_AQUI
grant_type=authorization_code
redirect_uri=https://teu-dominio.com/callback.html
```

### Resposta esperada
```json
{
  "access_token": "act.xxx",
  "expires_in": 86400,
  "open_id": "xxx",
  "refresh_token": "rft.xxx",
  "refresh_expires_in": 31536000,
  "scope": "user.info.basic,video.upload",
  "token_type": "Bearer"
}
```

### Refresh token (quando expira)
```
POST https://open.tiktokapis.com/v2/oauth/token/
Content-Type: application/x-www-form-urlencoded

client_key=XXX
client_secret=XXX
grant_type=refresh_token
refresh_token=REFRESH_TOKEN_AQUI
```

---

## 🎬 Publicar Vídeo no TikTok (via n8n)

Depois de teres o `access_token`, podes criar outro workflow para publicar vídeos:

### Passo 1: Iniciar upload
```
POST https://open.tiktokapis.com/v2/post/publish/inbox/video/init/
Authorization: Bearer ACCESS_TOKEN
Content-Type: application/json

{
  "source_info": {
    "source": "PULL_FROM_URL",
    "video_url": "https://url-do-video.mp4"
  }
}
```

### Passo 2: Publicar
```
POST https://open.tiktokapis.com/v2/post/publish/video/init/
Authorization: Bearer ACCESS_TOKEN
Content-Type: application/json

{
  "post_info": {
    "title": "Título do vídeo #hashtag",
    "privacy_level": "PUBLIC_TO_EVERYONE",
    "disable_duet": false,
    "disable_comment": false,
    "disable_stitch": false
  },
  "source_info": {
    "source": "PULL_FROM_URL",
    "video_url": "https://url-do-video.mp4"
  }
}
```

---

## ❓ Troubleshooting

### "Erro ao enviar para n8n"
- Verifica se o workflow está **ativo**
- Verifica se a URL do webhook está correta
- Testa o webhook com `curl`:
```bash
curl -X POST https://teu-n8n.com/webhook/macfly-tiktok \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
```

### "invalid_grant" ao trocar código
- O código expira em **10 minutos** - tenta novamente
- Verifica se o `redirect_uri` é exatamente igual ao configurado no TikTok

### "access_denied"
- O utilizador rejeitou as permissões
- Verifica os scopes pedidos na app TikTok

---

## 🔐 Segurança

- **Nunca** exponhas o `client_secret` no frontend
- Usa variáveis de ambiente no n8n
- Considera usar HTTPS em produção
- O `state` parameter previne ataques CSRF

---

## 📞 Suporte

- Email: macflytotheworld@gmail.com
- [TikTok API Docs](https://developers.tiktok.com/doc/overview/)
- [n8n Docs](https://docs.n8n.io/)
