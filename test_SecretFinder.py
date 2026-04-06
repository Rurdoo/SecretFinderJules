import pytest
from SecretFinder import cli_output

def test_cli_output_single_match(capsys):
    matched = [{'name': 'google_api', 'matched': 'AIzaSyAXXXXXXX'}]
    cli_output(matched)
    captured = capsys.readouterr()
    assert captured.out == "google_api\t->\tAIzaSyAXXXXXXX\n"
    assert captured.err == ""

def test_cli_output_multiple_matches(capsys):
    matched = [
        {'name': 'google_api', 'matched': 'AIzaSyAXXXXXXX'},
        {'name': 'slack_token', 'matched': 'xoxb-XXXXXXX'}
    ]
    cli_output(matched)
    captured = capsys.readouterr()
    expected = "google_api\t->\tAIzaSyAXXXXXXX\nslack_token\t->\txoxb-XXXXXXX\n"
    assert captured.out == expected
    assert captured.err == ""

def test_cli_output_non_ascii(capsys):
    matched = [{'name': 'test_name', 'matched': 'match_with_emoji😊_and_text'}]
    cli_output(matched)
    captured = capsys.readouterr()
    assert captured.out == "test_name\t->\tmatch_with_emoji_and_text\n"
    assert captured.err == ""

def test_cli_output_empty(capsys):
    matched = []
    cli_output(matched)
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
