import pytest

from rapids_dependency_file_generator.cli import generate_matrix, validate_args


def test_generate_matrix():
    matrix = generate_matrix("cuda=11.5;arch=x86_64")
    assert matrix == {"cuda": ["11.5"], "arch": ["x86_64"]}

    matrix = generate_matrix(None)
    assert matrix == {}


def test_validate_args():
    # Missing output
    with pytest.raises(Exception):
        validate_args(["--matrix", "cuda=11.5;arch=x86_64", "--file_key", "all"])

    # Missing matrix
    with pytest.raises(Exception):
        validate_args(["--output", "conda", "--file_key", "all"])

    # Missing file_key
    with pytest.raises(Exception):
        validate_args(["--output", "conda", "--matrix", "cuda=11.5;arch=x86_64"])

    # Prepending channels with an output type that is not conda
    with pytest.raises(Exception):
        validate_args(
            [
                "--output",
                "requirements",
                "--matrix",
                "cuda=11.5;arch=x86_64",
                "--file_key",
                "all",
                "--prepend-channels",
                "my_channel;my_other_channel",
            ]
        )

    # Valid
    validate_args(
        [
            "--output",
            "conda",
            "--matrix",
            "cuda=11.5;arch=x86_64",
            "--file_key",
            "all",
        ]
    )

    # Valid
    validate_args(
        [
            "--output",
            "pyproject",
            "--matrix",
            "cuda=11.5;arch=x86_64",
            "--file_key",
            "all",
        ]
    )

    # Valid, with prepended channels
    validate_args(
        [
            "--prepend-channels",
            "my_channel;my_other_channel",
        ]
    )

    # Valid, with output/matrix/file_key and prepended channels
    validate_args(
        [
            "--output",
            "conda",
            "--matrix",
            "cuda=11.5;arch=x86_64",
            "--file_key",
            "all",
            "--prepend-channels",
            "my_channel;my_other_channel",
        ]
    )
