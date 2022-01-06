"""Tests IO scrap functions
"""
import pytest
from ascii_art.io.scrap import create_header
from ascii_art.io.scrap import get_data_from_url


@pytest.mark.parametrize(
    "url, host",
    [
        ("http://test.com", "test.com"),
        ("http://i.am.an.url.com", "i.am.an.url.com"),
    ],
)
def test_create_header(url, host):
    """Test the function create header with correct input"""
    header = create_header(url)
    assert header["Host"] == host


@pytest.mark.parametrize(
    "url",
    [10, 1.2, ["http://error.com"]],
)
def test_create_header_typeerror(url):
    """Test the function create header with incorrect input"""

    with pytest.raises(TypeError):
        create_header(url)


@pytest.mark.parametrize(
    "url",
    ["not_an_url", "http:/test.com", "https//42.fr"],
)
def test_create_header_url_http_error(url):
    """Test the function create header with string but not url"""

    with pytest.raises(ValueError):
        create_header(url)
