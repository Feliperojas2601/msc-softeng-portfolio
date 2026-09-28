def test_offer_has_expected_fields(existing_offer):
    """An offer exposes every field described by the information view entity."""
    assert existing_offer.id
    assert existing_offer.postId == "9c858901-8a57-4791-81fe-4c455b099bc9"
    assert existing_offer.userId == "b3816c65-4f6a-4a6f-8e8f-2e6a9b6f7a11"
    assert existing_offer.description == "Paquete pequeño con libros"
    assert existing_offer.size == "SMALL"
    assert existing_offer.fragile is False
    assert existing_offer.offer == 25.5
    assert existing_offer.createdAt is not None
