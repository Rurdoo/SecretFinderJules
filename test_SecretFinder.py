import pytest
import os
import argparse
import SecretFinder

@pytest.fixture(autouse=True)
def setup_args():
    # Setup global args object that SecretFinder expects
    SecretFinder.args = argparse.Namespace(
        burp=False,
        ignore="",
        only="",
        headers="",
        cookie="",
        proxy="",
        input="",
        output="",
        regex=None,
        extract=False
    )

def test_getContext():
    matches = [('matched_string', 10, 24)]
    content = "prefix matched_string suffix"
    name = "test_regex"

    result = SecretFinder.getContext(matches, content, name)

    assert len(result) == 1
    assert result[0]['matched'] == 'matched_string'
    assert result[0]['name'] == 'test_regex'
    assert len(result[0]['context']) > 0

def test_parser_file_mode_0():
    content = "var apiKey = 'AIzaSyB-abcdefghijklmnopqrstuvwxyz12345';"
    # mode=0 for cli
    res = SecretFinder.parser_file(content, mode=0)
    assert len(res) >= 1

    google_api_matches = [m for m in res if m['name'] == 'google_api']
    assert len(google_api_matches) == 1
    assert google_api_matches[0]['matched'] == 'AIzaSyB-abcdefghijklmnopqrstuvwxyz12345'

def test_parser_file_mode_1():
    content = "var apiKey = 'AIzaSyB-abcdefghijklmnopqrstuvwxyz12345';"
    # mode=1 for html
    res = SecretFinder.parser_file(content, mode=1)
    assert len(res) >= 1

    google_api_matches = [m for m in res if m['name'] == 'google_api']
    assert len(google_api_matches) == 1
    assert google_api_matches[0]['matched'] == 'AIzaSyB-abcdefghijklmnopqrstuvwxyz12345'
    assert 'context' in google_api_matches[0]

def test_parser_input_url():
    url = "https://example.com/script.js"
    res = SecretFinder.parser_input(url)
    assert res == [url]

def test_parser_input_wildcard(tmp_path):
    js_file = tmp_path / "test.js"
    js_file.write_text("console.log('test');")

    wildcard_path = str(tmp_path / "*.js")
    res = SecretFinder.parser_input(wildcard_path)

    assert len(res) == 1
    assert res[0] == f"file://{js_file.absolute()}"

def test_urlParser():
    url = "https://example.com/path/to/script.js"
    SecretFinder.urlParser(url)
    assert SecretFinder.urlParser.this_root == "https://example.com"
    # urlParser actually prefixes with double slash: parse.scheme + '://' + parse.netloc  + '/' + parse.path
    # which leads to https://example.com//path/to/script.js
    assert SecretFinder.urlParser.this_path == "https://example.com//path/to/script.js"

def test_extractjsurl():
    html_content = '''
    <html>
    <head>
        <script src="https://example.com/abs.js"></script>
        <script src="//example.com/proto.js"></script>
        <script src="/root.js"></script>
        <script src="rel.js"></script>
    </head>
    <body></body>
    </html>
    '''
    base_url = "https://test.com/base/index.html"
    res = SecretFinder.extractjsurl(html_content, base_url)

    assert "https://example.com/abs.js" in res
    assert "http://example.com/proto.js" in res
    assert "https://test.com/root.js" in res
    # given urlParser implementation, this path is generated:
    assert "https://test.com//base/index.htmlrel.js" in res

def test_send_request_file(tmp_path):
    test_file = tmp_path / "test.js"
    test_file.write_text("var secret = '12345';")

    file_url = f"file://{test_file.absolute()}"
    res = SecretFinder.send_request(file_url)

    assert "var secret = '12345';" in res

def test_send_request_http(mocker):
    mock_get = mocker.patch('requests.get')
    mock_response = mocker.Mock()
    mock_response.content = b"var data = 'test';"
    mock_get.return_value = mock_response

    url = "https://example.com/test.js"
    res = SecretFinder.send_request(url)

    assert res == "var data = 'test';"
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert kwargs['url'] == url
    assert 'verify' in kwargs
    assert kwargs['verify'] is False
    assert 'headers' in kwargs
