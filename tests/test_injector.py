"""Injector tests — the low-level send is mocked (no real keystrokes sent)."""

from unittest.mock import patch

from src.injector import TextInjector


def test_empty_text_sends_nothing():
    with patch.object(TextInjector, "_send_char") as send:
        TextInjector().inject("")
        send.assert_not_called()


def test_each_character_is_sent_once():
    text = "Grüße"
    with patch.object(TextInjector, "_send_char") as send:
        TextInjector().inject(text)
        assert [c.args[0] for c in send.call_args_list] == list(text)
