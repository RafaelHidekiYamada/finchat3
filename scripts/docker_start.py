"""Aplica migrations, seed opcional e inicia a API como processo principal."""

import os
import subprocess
import sys


def main():
    subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], check=True)
    if os.getenv("SEED_DEMO_DATA", "false").strip().lower() in {"1", "true", "yes", "on"}:
        subprocess.run([sys.executable, "-m", "app.seed"], check=True)
    port = os.getenv("PORT", "8000").strip()
    if not port.isdigit() or not 1 <= int(port) <= 65535:
        raise RuntimeError("PORT deve ser um número entre 1 e 65535.")
    # Substitui o processo para que Uvicorn receba os sinais de encerramento.
    os.execv(sys.executable, [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", port])


if __name__ == "__main__":
    main()
