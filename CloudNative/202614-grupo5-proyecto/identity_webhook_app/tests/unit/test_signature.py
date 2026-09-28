from signature import build_verify_token, is_signature_valid


def test_build_verify_token_is_deterministic():
    """The same inputs always produce the same signature."""
    a = build_verify_token("secret", "ruv-1", 80)
    b = build_verify_token("secret", "ruv-1", 80)

    assert a == b


def test_is_signature_valid_accepts_the_matching_signature():
    """A verifyToken built from the same inputs is accepted."""
    token = build_verify_token("secret", "ruv-1", 80)

    assert is_signature_valid("secret", "ruv-1", 80, token)


def test_is_signature_valid_rejects_a_tampered_score():
    """Changing any signed field invalidates the signature."""
    token = build_verify_token("secret", "ruv-1", 80)

    assert not is_signature_valid("secret", "ruv-1", 90, token)


def test_is_signature_valid_rejects_the_wrong_secret():
    """A verifyToken signed with a different secret is rejected."""
    token = build_verify_token("other-secret", "ruv-1", 80)

    assert not is_signature_valid("secret", "ruv-1", 80, token)
