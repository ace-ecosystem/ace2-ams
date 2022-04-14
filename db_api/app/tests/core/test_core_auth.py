import pytest

from core.auth import hash_password, verify_password


@pytest.mark.parametrize(
    "initial_password,updated_password",
    [
        ("abcd1234", "wxyz6789"),
        ("abcd1234", "abcd1234"),
    ],
)
def test_hash_and_verify_password(initial_password, updated_password):
    # Create the hashes of each password
    initial_hash = hash_password(initial_password)
    updated_hash = hash_password(updated_password)

    # Make sure the two hashes are not the same
    assert initial_hash != updated_hash

    # Make sure both passwords validate against their hash
    assert verify_password(initial_password, initial_hash) is True
    assert verify_password(updated_password, updated_hash) is True
