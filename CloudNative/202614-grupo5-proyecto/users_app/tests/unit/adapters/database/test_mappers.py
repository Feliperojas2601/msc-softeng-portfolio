from adapters.database.mappers import user_entity_to_model, user_model_to_entity
from domain.models.user import UserStatus


def test_user_entity_to_model_maps_every_field(existing_user):
    """Converting a domain User to an ORM model preserves every field."""
    model = user_entity_to_model(existing_user)

    assert model.id == existing_user.id
    assert model.username == existing_user.username
    assert model.email == existing_user.email
    assert model.status == existing_user.status.value
    assert model.created_at == existing_user.created_at


def test_user_model_to_entity_maps_every_field(existing_user):
    """Converting an ORM model back to a domain User round-trips every field."""
    model = user_entity_to_model(existing_user)

    entity = user_model_to_entity(model)

    assert entity == existing_user
    assert entity.status is UserStatus.POR_VERIFICAR
