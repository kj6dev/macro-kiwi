"""Secret retrieval for macro-kiwi — Proton Pass primary, macOS Keychain fallback."""

import os
import subprocess

ACCOUNT = os.environ.get("KEYCHAIN_ACCOUNT", "")
VAULT = "Developer Secrets"


def get_secret(service: str) -> str:
    """Retrieve a secret, trying Proton Pass first then macOS Keychain.

    Args:
        service: Secret name (e.g., 'openai-api-key-macro-kiwi')

    Returns:
        The secret value, or empty string if not found.
    """
    result = subprocess.run(
        [
            "pass-cli",
            "item",
            "view",
            "--vault-name",
            VAULT,
            "--item-title",
            service,
            "--field",
            "note",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()

    result = subprocess.run(
        ["security", "find-generic-password", "-a", ACCOUNT, "-s", service, "-w"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()
