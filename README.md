# Automação Multi-Agente (n8n + Gemini + Redis/Supabase) & Contratos Digitais (Python + ZapSign API)

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![n8n](https://img.shields.io/badge/n8n-Workflow%20Automation-EA4B71?style=flat&logo=n8n&logoColor=white)
![ZapSign](https://img.shields.io/badge/REST%20API-ZapSign%20Digital%20Sign-1d4ed8?style=flat)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

> **Segurança & Anonimização:** Todos os workflows JSON (`workflows/`) e o módulo Python (`src/`) foram integralmente sanitizados: tokens de API, IDs de instância WhatsApp, chaves de banco, URLs privadas e dados de clientes reais foram substituídos por placeholders (`YOUR_...`) e dados fictícios (`João Silva Demo`).

## Arquitetura do Projeto

1. **Orquestração n8n Multimodal + Debounce (`workflows/super_agente_multimodal_debounce.json` — 35 nós):** Recebe webhook de atendimento, agrupa mensagens rápidas em janela de *debounce* no **Redis**, analisa áudios/imagens/vídeos via **Google Gemini**, consulta/cria lead no **Supabase**, responde via **LangChain AI Agent** com memória persistente em **PostgreSQL**.
2. **Cadência CRM + WhatsApp (`workflows/workflow_crm_whatsapp_cadenciado.json` — 13 nós):** Agendamento com validação de horário comercial, checagem de número válido, *delay* aleatório anti-bloqueio e atualização de status no Supabase.
3. **Motor Documental Python + ZapSign (`src/gerador_contrato_zapsign.py`):** Gera contratos/procurações em PDF automaticamente e integra via REST API para retorno instantâneo do link de assinatura digital (suporta execução local segura `--dry-run`).

---

## Como Executar a Demonstração Python (`--dry-run`)

```bash
pip install -r requirements.txt
python src/gerador_contrato_zapsign.py
```

---

**Autor:** [Jonathan Campos Cusandei](https://www.linkedin.com/in/jonathancusandei/) · [Portfólio Executivo](https://jonathancusandei-glitch.github.io/portfolio-jonathan/)
