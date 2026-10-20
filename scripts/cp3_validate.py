"""Executa cenários HTTP reais do CP3 contra o frontend/proxy em execução."""

from __future__ import annotations

import json
import os
from datetime import date, datetime
from decimal import Decimal

import httpx


BASE_URL = os.getenv("CP3_BASE_URL", "http://127.0.0.1:5173/api/v1").rstrip("/")
DEMO_PASSWORD = "FinChatDemo!2026"


def envelope(response: httpx.Response, expected: int = 200):
    if response.status_code != expected:
        raise AssertionError(f"{response.request.method} {response.request.url}: {response.status_code} {response.text}")
    body = response.json()
    if "data" not in body:
        raise AssertionError(f"Envelope de sucesso inválido: {body}")
    return body["data"]


def login(client: httpx.Client, email: str) -> dict[str, str]:
    data = envelope(client.post(f"{BASE_URL}/auth/login", json={"email": email, "password": DEMO_PASSWORD}))
    return {"Authorization": f"Bearer {data['access_token']}"}


def main() -> None:
    results: list[dict[str, str]] = []
    created_transaction_id: int | None = None
    validate_ai = os.getenv("CP3_VALIDATE_AI", "false").strip().lower() in {"1", "true", "yes", "on"}
    with httpx.Client(timeout=360.0 if validate_ai else 30.0) as client:
        cpf_headers = login(client, "cpf@finchat.demo")
        cnpj_headers = login(client, "empresa@finchat.demo")
        try:
            health = envelope(client.get(f"{BASE_URL}/health"))
            assert health == {"status": "ok", "database": "ok", "environment": "CP3"}
            results.append({"id": "CT-01", "status": "APROVADO", "resultado": "Frontend Nginx encaminhou a chamada e a API/banco responderam CP3/ok."})

            today = date.today().isoformat()
            categories = envelope(client.get(f"{BASE_URL}/categories", headers=cpf_headers))
            expense_category = next(item for item in categories if item["type"] == "EXPENSE")
            before = envelope(client.get(f"{BASE_URL}/dashboard/overview", headers=cpf_headers, params={"start_date": today[:8] + "01", "end_date": today}))
            description = f"Validação CP3 {datetime.now().strftime('%Y%m%d%H%M%S')}"
            created = envelope(client.post(f"{BASE_URL}/transactions", headers=cpf_headers, json={
                "description": description,
                "amount": "12.34",
                "date": today,
                "type": "EXPENSE",
                "category_id": expense_category["id"],
                "origin": "CASH",
            }), 201)
            created_transaction_id = created["id"]
            listed = envelope(client.get(f"{BASE_URL}/transactions", headers=cpf_headers, params={"start_date": today, "end_date": today}))
            assert any(item["id"] == created_transaction_id for item in listed)
            after = envelope(client.get(f"{BASE_URL}/dashboard/overview", headers=cpf_headers, params={"start_date": today[:8] + "01", "end_date": today}))
            assert Decimal(after["total_expenses"]) == Decimal(before["total_expenses"]) + Decimal("12.34")
            results.append({"id": "CT-02", "status": "APROVADO", "resultado": "Transação criada, persistida, consultada e refletida no dashboard consolidado."})

            invalid = client.post(f"{BASE_URL}/transactions", headers=cpf_headers, json={
                "description": "Valor inválido CP3",
                "amount": "0.00",
                "date": today,
                "type": "EXPENSE",
                "category_id": expense_category["id"],
            })
            assert invalid.status_code == 422
            assert invalid.json()["error"]["code"] == "VALIDATION_ERROR"
            results.append({"id": "CT-03", "status": "APROVADO", "resultado": "Valor monetário inválido recusado com 422 e erro padronizado."})

            forbidden = client.get(f"{BASE_URL}/partners", headers=cpf_headers)
            assert forbidden.status_code == 403
            assert forbidden.json()["error"]["code"] == "FORBIDDEN"
            results.append({"id": "CT-04", "status": "APROVADO", "resultado": "Perfil CPF bloqueado na área empresarial com 403."})

            partners = envelope(client.get(f"{BASE_URL}/partners", headers=cnpj_headers))
            contracts = envelope(client.get(f"{BASE_URL}/contracts", headers=cnpj_headers))
            assert partners and contracts
            results.append({"id": "CT-05", "status": "APROVADO", "resultado": f"Perfil CNPJ recuperou {len(partners)} parceiros e {len(contracts)} contratos."})

            profile = envelope(client.get(f"{BASE_URL}/auth/me", headers=cpf_headers))
            assert profile["document_type"] == "CPF"
            results.append({"id": "CT-06", "status": "APROVADO", "resultado": "Login JWT e recuperação do perfil funcionaram através do proxy do frontend."})

            if validate_ai:
                analysis = envelope(client.post(f"{BASE_URL}/ai/financial-analysis", headers=cpf_headers, json={
                    "start_date": today[:8] + "01",
                    "end_date": today,
                }))
                assert analysis["analysis_source"] == "ollama"
                assert analysis["fallback_used"] is False
                assert analysis["financial_summary"] and analysis["recommendations"]
                results.append({"id": "CT-07", "status": "APROVADO", "resultado": "Ollama real respondeu com schema válido, analysis_source=ollama e fallback_used=false."})
        finally:
            if created_transaction_id is not None:
                cleanup = client.delete(f"{BASE_URL}/transactions/{created_transaction_id}", headers=cpf_headers)
                if cleanup.status_code != 200:
                    raise AssertionError(f"Falha ao remover dado temporário: {cleanup.status_code} {cleanup.text}")

    print(json.dumps({"executed_at": datetime.now().astimezone().isoformat(), "base_url": BASE_URL, "scenarios": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
