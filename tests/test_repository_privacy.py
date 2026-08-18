import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).parents[1]
TEXT_SUFFIXES = {".json", ".md", ".py", ".toml", ".txt", ".yaml", ".yml"}
PRIVATE_TOKEN_DIGESTS = {
    "0c6cd881b28efaa78660cf1476794f940df8d68eec515333421dc64f11fff538",
    "191c07159a1d039c0ccb06793ff7b89919cbc222fe732920e0d0ebeba0c5139e",
    "9fd34c43e2644502eabac3731869a7a387bfa96941914b5a7541422a77d191a9",
}


def test_public_repository_contains_no_private_identity_tokens():
    offenders = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        if any(part in {".pytest_cache", "__pycache__"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8").lower()
        token_digests = {
            hashlib.sha256(token.encode("utf-8")).hexdigest()
            for token in re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", text)
        }
        if token_digests & PRIVATE_TOKEN_DIGESTS:
            offenders.append(str(path.relative_to(ROOT)))

    assert offenders == [], f"private identity token found in: {offenders}"
