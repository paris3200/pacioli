"""Tests for shell completions."""

import os
from pathlib import Path


def test_bash_completion_file_exists():
    """Bash completion file exists."""
    completion_file = Path("completions/pacioli-complete.bash")
    assert completion_file.exists(), "Bash completion file should exist"


def test_zsh_completion_file_exists():
    """Zsh completion file exists."""
    completion_file = Path("completions/pacioli-complete.zsh")
    assert completion_file.exists(), "Zsh completion file should exist"


def test_bash_completion_has_content():
    """Bash completion file has content."""
    completion_file = Path("completions/pacioli-complete.bash")
    content = completion_file.read_text()
    assert len(content) > 0, "Bash completion file should not be empty"
    assert "_pacioli_completion" in content, "Should contain completion function"
    assert "complete" in content, "Should contain bash complete directive"


def test_zsh_completion_has_content():
    """Zsh completion file has content."""
    completion_file = Path("completions/pacioli-complete.zsh")
    content = completion_file.read_text()
    assert len(content) > 0, "Zsh completion file should not be empty"
    assert "#compdef pacioli" in content, "Should contain zsh compdef directive"
    assert "_pacioli_completion" in content, "Should contain completion function"


def test_bash_completion_syntax():
    """Bash completion file has valid syntax."""
    completion_file = Path("completions/pacioli-complete.bash")
    # Run bash syntax check
    exit_code = os.system(f"bash -n {completion_file}")
    assert exit_code == 0, "Bash completion file should have valid bash syntax"


def test_zsh_completion_syntax():
    """Zsh completion file has valid syntax."""
    completion_file = Path("completions/pacioli-complete.zsh")
    # Run zsh syntax check (if zsh is available)
    if os.system("which zsh > /dev/null 2>&1") == 0:
        exit_code = os.system(f"zsh -n {completion_file}")
        assert exit_code == 0, "Zsh completion file should have valid zsh syntax"
