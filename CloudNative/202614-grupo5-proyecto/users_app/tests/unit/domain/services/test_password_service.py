from domain.services.password_service import (
    generate_salt,
    hash_password,
    verify_password,
)


def test_generate_salt_returns_a_non_empty_random_hex_string():
    """Two generated salts should be different and hex-encoded."""
    first_salt = generate_salt()
    second_salt = generate_salt()

    assert first_salt != second_salt
    assert bytes.fromhex(first_salt)


def test_hash_password_is_deterministic_for_the_same_salt():
    """Hashing the same password with the same salt yields the same digest."""
    salt = generate_salt()

    assert hash_password("my-password", salt) == hash_password("my-password", salt)


def test_hash_password_differs_for_different_salts():
    """The same password hashed with different salts must yield different digests."""
    assert hash_password("my-password", "aaaa") != hash_password("my-password", "bbbb")


def test_verify_password_returns_true_for_matching_password():
    """verify_password succeeds when the plain password matches the stored hash."""
    salt = generate_salt()
    hashed = hash_password("my-password", salt)

    assert verify_password("my-password", salt, hashed) is True


def test_verify_password_returns_false_for_non_matching_password():
    """verify_password fails when the plain password does not match the stored hash."""
    salt = generate_salt()
    hashed = hash_password("my-password", salt)

    assert verify_password("wrong-password", salt, hashed) is False
