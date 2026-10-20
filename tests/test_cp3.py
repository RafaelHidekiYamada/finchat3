"""Critérios técnicos do CP3: produção, container e segurança HTTP."""

import sys

import pytest

from scripts import docker_start
from tests.helpers import sucesso


def test_inicializacao_do_container_aplica_migration_seed_e_porta_configurada(monkeypatch):
    commands = []
    execution = []
    monkeypatch.setenv("SEED_DEMO_DATA", "true")
    monkeypatch.setenv("PORT", "10000")
    monkeypatch.setattr(docker_start.subprocess, "run", lambda command, check: commands.append((command, check)))
    monkeypatch.setattr(docker_start.os, "execv", lambda executable, command: execution.append((executable, command)))

    docker_start.main()

    assert commands == [
        ([sys.executable, "-m", "alembic", "upgrade", "head"], True),
        ([sys.executable, "-m", "app.seed"], True),
    ]
    assert execution[0][1][-2:] == ["--port", "10000"]


def test_inicializacao_do_container_rejeita_porta_invalida(monkeypatch):
    monkeypatch.setenv("PORT", "70000")
    monkeypatch.setattr(docker_start.subprocess, "run", lambda command, check: None)

    with pytest.raises(RuntimeError, match="PORT"):
        docker_start.main()


def test_health_cp3_confirma_banco_e_cabecalhos_de_seguranca(client):
    response = client.get("/health")
    health = sucesso(response)
    assert health == {"status": "ok", "database": "ok", "environment": "CP3"}
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"
    assert "camera=()" in response.headers["permissions-policy"]
