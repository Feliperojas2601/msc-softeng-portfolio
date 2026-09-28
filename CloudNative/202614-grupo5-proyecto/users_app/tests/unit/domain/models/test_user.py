from domain.models.user import UserStatus


def test_user_has_expected_fields(existing_user):
    """A User exposes every field described by the information view entity."""
    assert existing_user.id
    assert existing_user.username == "johndoe"
    assert existing_user.email == "johndoe@example.com"
    assert existing_user.status == UserStatus.POR_VERIFICAR


def test_user_status_has_three_valid_values():
    """UserStatus only defines the three values allowed by the API spec."""
    assert {status.value for status in UserStatus} == {
        "POR_VERIFICAR",
        "NO_VERIFICADO",
        "VERIFICADO",
    }
