from pathlib import Path


ROOT = Path(__file__).parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "test.yml"


def test_ci_runs_the_standalone_release_barrier_on_supported_python():
    assert WORKFLOW.is_file()
    text = WORKFLOW.read_text(encoding="utf-8")
    for required in (
        "push:",
        "pull_request:",
        'python-version: ["3.11", "3.12"]',
        "actions/checkout@v7",
        "actions/setup-python@v6",
        "python -m pytest tests -q",
        "python -m compileall -q src skill/altar/scripts",
        "python -m build --wheel",
    ):
        assert required in text
    for forbidden in ("publish", "pypi", "contents: write", "id-token: write"):
        assert forbidden not in text.lower()
