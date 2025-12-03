from ..controllers import ingredientcontroller as controller
import pytest
from fastapi import HTTPException, status
from unittest.mock import Mock


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_ingredient_success(db_session):
    class MockRequest:
        def __init__(self):
            self.name = "Flour"
            self.unit = "kg"
            self.current_stock = 100.0
            self.min_stock = 10.0

    request = MockRequest()

    mock_query = Mock()
    mock_filter = Mock()
    mock_filter.first.return_value = None

    db_session.query.return_value = mock_query
    mock_query.filter.return_value = mock_filter

    mock_ingredient = Mock()
    mock_ingredient.id = 1
    mock_ingredient.name = "Flour"
    mock_ingredient.unit = "kg"
    mock_ingredient.current_stock = 100.0
    mock_ingredient.min_stock = 10.0
    from ..models import ingredients
    original_ingredient = ingredients.Ingredient

    mock_ingredient_class = Mock()
    mock_ingredient_instance = Mock()
    mock_ingredient_instance.id = 1
    mock_ingredient_instance.name = "Flour"
    mock_ingredient_instance.unit = "kg"
    mock_ingredient_instance.current_stock = 100.0
    mock_ingredient_instance.min_stock = 10.0
    mock_ingredient_class.return_value = mock_ingredient_instance
    ingredients.Ingredient = mock_ingredient_class

    try:
        db_session.add = Mock()
        db_session.commit = Mock()

        def refresh_mock(obj):
            obj.id = 1

        db_session.refresh = Mock(side_effect=refresh_mock)

        created_ingredient = controller.create(db_session, request)

        assert created_ingredient is not None
        assert created_ingredient.id == 1
        assert created_ingredient.name == "Flour"
        assert created_ingredient.unit == "kg"
        assert created_ingredient.current_stock == 100.0
        assert created_ingredient.min_stock == 10.0

        db_session.add.assert_called_once()
        db_session.commit.assert_called_once()
        db_session.refresh.assert_called_once()

    finally:
        ingredients.Ingredient = original_ingredient