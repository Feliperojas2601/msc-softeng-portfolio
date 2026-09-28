def test_post_has_expected_fields(existing_post):
    """A post exposes every field described by the information view entity."""
    assert existing_post.id
    assert existing_post.routeId == "a1b2c3d4-1111-4000-8000-000000000001"
    assert existing_post.userId == "b2c3d4e5-2222-4000-8000-000000000002"
