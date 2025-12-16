import pytest
from unittest.mock import MagicMock, patch
from app.services.planejamento.ai_service import AIService

@pytest.fixture
def mock_genai():
    with patch("app.services.planejamento.ai_service.genai") as mock:
        # Mock the GenerativeModel class and its instance
        mock_model_instance = MagicMock()
        mock.GenerativeModel.return_value = mock_model_instance
        
        # Mock generate_content return value
        mock_response = MagicMock()
        mock_response.text = "Mocked AI Response"
        mock_model_instance.generate_content.return_value = mock_response
        
        yield mock

def test_ai_service_init(mock_genai):
    # Should init without error if API key is present (mocked orenv)
    with patch.dict("os.environ", {"GEMINI_API_KEY": "fake_key"}):
        service = AIService()
        assert service.model is not None

def test_generate_dfd_object(mock_genai):
    with patch.dict("os.environ", {"GEMINI_API_KEY": "fake_key"}):
        service = AIService()
        res = service.generate_dfd_object("Rascunho")
        assert res == "Mocked AI Response"
        # Check if generate_content was called
        service.model.generate_content.assert_called_once()

def test_generate_dfd_justification(mock_genai):
    with patch.dict("os.environ", {"GEMINI_API_KEY": "fake_key"}):
        service = AIService()
        res = service.generate_dfd_justification("Obj", "Ras")
        assert res == "Mocked AI Response"

def test_generate_risks(mock_genai):
    with patch.dict("os.environ", {"GEMINI_API_KEY": "fake_key"}):
        service = AIService()
        res = service.generate_risks("Obj")
        assert res == "Mocked AI Response"

def test_ai_service_missing_key():
    with patch.dict("os.environ", {}, clear=True):
        with pytest.raises(ValueError, match="GEMINI_API_KEY"):
            AIService()
