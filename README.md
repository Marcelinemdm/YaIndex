# YaIndex

> Índice completo de recursos otaku!

---

## 📚 Sobre o projeto

**YaIndex** é um índice que reúne diversos recursos relacionados à cultura otaku em um só lugar.
Aqui você encontra sites, ferramentas e comunidades para **assistir, ler, ouvir, jogar e explorar** conteúdos de anime, mangá e muito mais.

O objetivo é facilitar o acesso a tudo que um fã pode precisar.

---

## 🗂️ Categorias

O índice atualmente inclui **214+ recursos organizados em 18 categorias**:

* 📺 Anime Streaming
* 🇨🇳 Donghua
* 📖 Manga
* 📚 Manhwa
* 📘 Novels
* ⬇️ Download
* 📱 Apps
* 🗄️ Banco de Dados
* 🎵 Música
* 📅 Calendário
* 📚 Wiki & Guias
* 🛠️ Ferramentas
* 💬 Fóruns
* 🎨 Arte
* 🧑‍🎤 VTubers
* 🎮 Games / Visual Novels
* 🧠 Quiz
* 🔒 VPN

---

## ➕ Como sugerir um site

Abra uma **Issue** com a label **`add-site`** e inclua um bloco JSON com os dados do site.
O GitHub Actions processa automaticamente, adiciona ao `data.json` e fecha a issue com uma confirmação.

### Formato obrigatório

```json
{
  "name": "Nome do Site",
  "url": "https://exemplo.com",
  "category": "id-da-categoria",
  "tags": [
    "tag1",
    "tag2",
    "tag3"
  ],
  "status": "online"
}
```

### Campos

| Campo | Obrigatório | Descrição |
|-------|-------------|-----------|
| `name` | ✅ | Nome exibido no índice |
| `url` | ✅ | URL completa com `https://` |
| `category` | ✅ | ID da categoria (ver lista abaixo) |
| `tags` | — | Lista de tags para busca (até 3 recomendado) |
| `status` | — | `online` (padrão), `warning` ou `offline` |

### IDs de categorias disponíveis

| ID | Categoria |
|----|-----------|
| `anime-streaming` | Anime Streaming |
| `donghua` | Donghua |
| `manga` | Manga |
| `manhwa` | Manhwa |
| `novels` | Novels |
| `download` | Download |
| `apps` | Apps |
| `banco-de-dados` | Banco de Dados |
| `musica` | Música |
| `calendario` | Calendário |
| `wiki-guias` | Wiki & Guias |
| `ferramentas` | Ferramentas |
| `foruns` | Fóruns |
| `arte` | Arte |
| `vtuber` | VTuber |
| `games-vn` | Games/VN |
| `quiz` | Quiz |
| `vpn` | VPN |

> Não sabe o ID exato? Verifique em [`data.json`](./data.json) — é o campo `"id"` de cada categoria.

### Exemplo de issue

**Título:** `MangaDex`

**Corpo:**
````
```json
{
  "name": "MangaDex",
  "url": "https://mangadex.org",
  "category": "manga",
  "tags": ["manga", "gratuito", "multi-idioma"],
  "status": "online"
}
```
````

---

## 🔄 Auto-update

O índice é atualizado automaticamente via **GitHub Actions** (`.github/workflows/update.yml`):
- Verifica o status de todos os sites diariamente
- Faz commit automático do `data.json` atualizado
- Issues com label `add-site` são processadas imediatamente

---

## 🛠️ Rodando localmente

```bash
git clone https://github.com/Marcelinemdm/YaIndex
cd YaIndex
python update.py   # verifica status de todos os sites
```

## ⭐ Apoie o projeto

Se este projeto foi útil para você, considere dar uma **estrela ⭐ no repositório**.
Isso ajuda outras pessoas a encontrarem o YaIndex!

---

*Feito para a comunidade otaku ❤️*
