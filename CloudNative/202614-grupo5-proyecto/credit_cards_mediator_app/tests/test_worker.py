import pytest

import worker as module
from handler import InternalApiError, ProviderResponseError, Settings


def settings():
    return Settings(
        "https://native.test",
        "native-secret",
        "https://cards.test",
        "cards-secret",
        "https://users.test",
        "http://notifications-app-service",
    )


def test_run_forever_polls_until_stop_check_true(monkeypatch):
    calls = []
    monkeypatch.setattr(module, "run_once", lambda s: calls.append(s))
    sleeps = []
    iterations = iter([False, False, True])

    module.run_forever(
        settings(),
        sleep_fn=sleeps.append,
        stop_check=lambda: next(iterations),
    )

    assert len(calls) == 2
    assert sleeps == [module.POLL_INTERVAL_SECONDS, module.POLL_INTERVAL_SECONDS]


def test_run_forever_stops_immediately_when_already_requested(monkeypatch):
    calls = []
    monkeypatch.setattr(module, "run_once", lambda s: calls.append(s))
    sleeps = []

    module.run_forever(settings(), sleep_fn=sleeps.append, stop_check=lambda: True)

    assert calls == []
    assert sleeps == []


def test_shutdown_signal_handler_sets_flag():
    shutdown = module._Shutdown()
    assert shutdown.requested is False
    shutdown.request(signum=15, frame=None)
    assert shutdown.requested is True


def test_run_forever_uses_settings_from_env_when_not_given(monkeypatch):
    from_env_calls = []
    monkeypatch.setattr(
        module.Settings,
        "from_env",
        classmethod(lambda cls: from_env_calls.append(1) or settings()),
    )
    monkeypatch.setattr(module, "run_once", lambda s: None)

    module.run_forever(sleep_fn=lambda _: None, stop_check=lambda: True)

    assert from_env_calls == [1]


@pytest.mark.parametrize(
    "error", [InternalApiError("HTTP 503"), ProviderResponseError("timeout")]
)
def test_worker_survives_claim_failure_and_retries(monkeypatch, error):
    calls = []
    sleeps = []
    iterations = iter([False, False, True])

    def run_once(configuration):
        calls.append(configuration)
        if len(calls) == 1:
            raise error
        return 1, 0

    monkeypatch.setattr(module, "run_once", run_once)
    module.run_forever(
        settings(), sleep_fn=sleeps.append, stop_check=lambda: next(iterations)
    )
    assert len(calls) == 2
    assert sleeps == [module.POLL_INTERVAL_SECONDS] * 2
