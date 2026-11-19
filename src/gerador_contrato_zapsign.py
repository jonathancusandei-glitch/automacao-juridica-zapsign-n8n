# -*- coding: utf-8 -*-
"""Gerador Modular de Documentos PDF (FPDF) Integrado à API REST ZapSign — Template Jurídico Demo."""

import argparse
import base64
import json
import os
import urllib.request
from fpdf import FPDF

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)


def gerar_contrato_pdf(nome_cliente: str, cpf_mask: str = "000.000.000-00", escritorio: str = "Advocacia Modelo (Demo) - OAB/UF 000.000") -> str:
    safe_slug = nome_cliente.lower().replace(" ", "_")
    pdf_path = os.path.join(OUT_DIR, f"contrato_demo_{safe_slug}.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(190, 10, "CONTRATO DE PRESTACAO DE SERVICOS JURIDICOS (DEMO)", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(4)

    pdf.set_font("Helvetica", size=11)
    blocos = [
        f"CONTRATANTE: {nome_cliente}, portador(a) do CPF {cpf_mask}, residente no Brasil.",
        f"CONTRATADO: {escritorio}.",
        "OBJETO: Modelo demonstrativo de formalizacao automatizada apos triagem de Agente de IA.",
        "HONORARIOS: Condicao contratual padrao parametrizada em template modular.",
        "Documento ficticio gerado automaticamente para demonstracao de arquitetura Python + ZapSign API.",
    ]
    for linha in blocos:
        pdf.multi_cell(190, 7, linha)
        pdf.ln(2)

    pdf.output(pdf_path)
    return pdf_path


def enviar_para_zapsign(pdf_path: str, nome_cliente: str, api_token: str | None, dry_run: bool = True) -> dict:
    with open(pdf_path, "rb") as f:
        pdf_b64 = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "name": f"Contrato Demo - {nome_cliente}",
        "base64_pdf": pdf_b64 if not dry_run else f"<BASE64_PDF_{len(pdf_b64)}_BYTES>",
        "signers": [
            {"name": nome_cliente, "auth_mode": "assinatura_tela"},
            {"name": "Advogado Responsavel (Demo)", "auth_mode": "assinatura_tela"},
        ],
    }

    if dry_run or not api_token or api_token.startswith("YOUR_"):
        return {
            "mode": "dry-run",
            "sign_url": "https://app.zapsign.com.br/verificar/demo-token-ficticio",
            "payload_preview": payload,
        }

    url = f"https://api.zapsign.com.br/api/v1/docs/?api_token={api_token}"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        res_data = json.loads(resp.read().decode("utf-8"))
        signers = res_data.get("signers", [])
        return {
            "mode": "live",
            "sign_url": signers[0].get("sign_url") if signers else None,
            "response": res_data,
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cliente", default="Joao Silva Demo")
    parser.add_argument("--live", action="store_true", help="Envia PDF real usando ZAPSIGN_API_TOKEN.")
    args = parser.parse_args()

    pdf_file = gerar_contrato_pdf(args.cliente)
    token = os.getenv("ZAPSIGN_API_TOKEN", "")
    res = enviar_para_zapsign(pdf_file, args.cliente, token, dry_run=not args.live)
    print(f"PDF Demo gerado em: {pdf_file}")
    print(f"Modo: {res['mode']} | Link Assinatura: {res['sign_url']}")


if __name__ == "__main__":
    main()
