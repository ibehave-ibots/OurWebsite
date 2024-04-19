from ssg.page import Page

## Markdown tests


def test_can_extract_markdown():
    text_in = """
    # hello
    """
    text_out = "# hello"
    page = Page(text=text_in)
    assert page.markdown == text_out

    

def test_end_whitespace_is_ignored():
    text_in = """
    

    # hello

    """

    text_out = """# hello"""
    page = Page(text=text_in)
    assert page.markdown == text_out


def test_yaml_and_whitespace_is_ignored():
    text_in = """
    ---

    # hello
    
    """

    text_out = """# hello"""
    page = Page(text=text_in)
    assert page.markdown == text_out


def test_yaml_and_whitespace_is_ignored2():
    text_in = """
    a: 3
    b: 5
    ---

    # hello
    
    """

    text_out = """# hello"""
    page = Page(text=text_in)
    assert page.markdown == text_out


## YAML Tests

def test_yaml_is_extracted():
    text_in = """
    a: 3
    b: 5
    ---
    # hello
    """

    data_out = {'a': 3, 'b': 5}
    page = Page(text=text_in)
    assert page.data == data_out


## YAML + Jinja Tests


def test_jinja_templating_works_on_yaml_when_data_extracted():
    text_in = """
    a: 3
    b: 5
    c: {{ d }}
    ---
    # hello
    """

    data_out = {'a': 3, 'b': 5, 'c': 7}
    page = Page(text=text_in, extra_data={'d': 7})
    assert page.data == data_out

## Markdown + Jinja Tests

