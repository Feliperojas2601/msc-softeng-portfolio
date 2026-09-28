from adapters.database.mappers import post_entity_to_model, post_model_to_entity


def test_post_entity_to_model_maps_every_field(existing_post):
    model = post_entity_to_model(existing_post)

    assert model.id == existing_post.id
    assert model.route_id == existing_post.routeId
    assert model.user_id == existing_post.userId
    assert model.expire_at == existing_post.expireAt
    assert model.created_at == existing_post.createdAt


def test_post_model_to_entity_maps_every_field(existing_post):
    model = post_entity_to_model(existing_post)
    entity = post_model_to_entity(model)

    assert entity == existing_post
