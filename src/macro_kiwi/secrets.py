"""Secret retrieval for macro-kiwi via pass (password-store)."""

import subprocess


def get_secret(service: str) -> str:
    """Retrieve a secret from password-store.

    Args:
        service: Secret name (e.g., 'openai-api-key-macro-kiwi')

    Returns:
        The secret value, or empty string if not found.
    """
    result = subprocess.run(
        ["pass", "show", service],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    return ""
