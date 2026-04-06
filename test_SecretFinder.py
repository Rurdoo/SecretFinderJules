import pytest
import SecretFinder

class MockArgs:
    def __init__(self, ignore="", only=""):
        self.ignore = ignore
        self.only = only

@pytest.fixture(autouse=True)
def setup_args():
    # Setup mock args before each test
    SecretFinder.args = MockArgs()

def test_extractjsurl_absolute_url():
    html_content = '''
    <html>
        <script src="http://example.com/test1.js"></script>
        <script src="https://example.com/test2.js"></script>
        <script src="ftp://example.com/test3.js"></script>
        <script src="ftps://example.com/test4.js"></script>
    </html>
    '''
    base_url = "http://base.com/"
    expected = [
        "http://example.com/test1.js",
        "https://example.com/test2.js",
        "ftp://example.com/test3.js",
        "ftps://example.com/test4.js",
    ]
    result = SecretFinder.extractjsurl(html_content, base_url)
    assert result == expected

def test_extractjsurl_protocol_relative_url():
    html_content = '''
    <html>
        <script src="//example.com/test.js"></script>
    </html>
    '''
    base_url = "http://base.com/"
    expected = ["http://example.com/test.js"]
    result = SecretFinder.extractjsurl(html_content, base_url)
    assert result == expected

def test_extractjsurl_domain_relative_url():
    html_content = '''
    <html>
        <script src="/js/test.js"></script>
    </html>
    '''
    base_url = "http://base.com/path/index.html"
    expected = ["http://base.com/js/test.js"]
    result = SecretFinder.extractjsurl(html_content, base_url)
    assert result == expected

def test_extractjsurl_path_relative_url():
    html_content = '''
    <html>
        <script src="js/test.js"></script>
    </html>
    '''
    base_url = "http://base.com/path/index.html"
    expected = ["http://base.com/path/js/test.js"]
    result = SecretFinder.extractjsurl(html_content, base_url)
    assert result == expected

def test_extractjsurl_no_script_tags():
    html_content = '''
    <html>
        <body>
            <h1>Hello World</h1>
        </body>
    </html>
    '''
    base_url = "http://base.com/"
    expected = []
    result = SecretFinder.extractjsurl(html_content, base_url)
    assert result == expected

def test_extractjsurl_script_tag_no_src():
    html_content = '''
    <html>
        <script>console.log('inline');</script>
    </html>
    '''
    base_url = "http://base.com/"
    expected = []
    result = SecretFinder.extractjsurl(html_content, base_url)
    assert result == expected

def test_extractjsurl_ignore_args():
    html_content = '''
    <html>
        <script src="http://example.com/test1.js"></script>
        <script src="http://example.com/test2.js"></script>
        <script src="http://ignore.com/test3.js"></script>
    </html>
    '''
    base_url = "http://base.com/"
    SecretFinder.args = MockArgs(ignore="ignore.com;test2.js")
    expected = ["http://example.com/test1.js"]
    result = SecretFinder.extractjsurl(html_content, base_url)
    assert result == expected

def test_extractjsurl_only_args():
    html_content = '''
    <html>
        <script src="http://example.com/test1.js"></script>
        <script src="http://example.com/test2.js"></script>
        <script src="http://ignore.com/test3.js"></script>
    </html>
    '''
    base_url = "http://base.com/"
    SecretFinder.args = MockArgs(only="test1.js;test3.js")
    expected = [
        "http://example.com/test1.js",
        "http://ignore.com/test3.js"
    ]
    result = SecretFinder.extractjsurl(html_content, base_url)
    assert result == expected

def test_extractjsurl_deduplication():
    html_content = '''
    <html>
        <script src="http://example.com/test1.js"></script>
        <script src="http://example.com/test1.js"></script>
    </html>
    '''
    base_url = "http://base.com/"
    expected = ["http://example.com/test1.js"]
    result = SecretFinder.extractjsurl(html_content, base_url)
    assert result == expected
