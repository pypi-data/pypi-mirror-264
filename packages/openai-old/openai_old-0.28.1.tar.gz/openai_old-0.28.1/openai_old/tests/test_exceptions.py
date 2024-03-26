import pickle

import pytest

import openai_old

EXCEPTION_TEST_CASES = [
    openai_old.InvalidRequestError(
        "message",
        "param",
        code=400,
        http_body={"test": "test1"},
        http_status="fail",
        json_body={"text": "iono some text"},
        headers={"request-id": "asasd"},
    ),
    openai_old.error.AuthenticationError(),
    openai_old.error.PermissionError(),
    openai_old.error.RateLimitError(),
    openai_old.error.ServiceUnavailableError(),
    openai_old.error.SignatureVerificationError("message", "sig_header?"),
    openai_old.error.APIConnectionError("message!", should_retry=True),
    openai_old.error.TryAgain(),
    openai_old.error.Timeout(),
    openai_old.error.APIError(
        message="message",
        code=400,
        http_body={"test": "test1"},
        http_status="fail",
        json_body={"text": "iono some text"},
        headers={"request-id": "asasd"},
    ),
    openai_old.error.OpenAIError(),
]


class TestExceptions:
    @pytest.mark.parametrize("error", EXCEPTION_TEST_CASES)
    def test_exceptions_are_pickleable(self, error) -> None:
        assert error.__repr__() == pickle.loads(pickle.dumps(error)).__repr__()
