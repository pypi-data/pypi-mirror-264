import htmlmin


def find_article_in_soup(soup):
    """Try to find the main content article location in a soup"""
    # try article
    for article in soup.find_all("article", recursive=True):
        return article, "article"  # return the first found article
    for main in soup.find_all("main", recursive=True):
        return main, "main"  # return the first found main
    return soup, None


def _remove_all_attrs(soup):
    """remove all attributes from soup
    see: https://gist.github.com/revotu/21d52bd20a073546983985ba3bf55deb"""
    for tag in soup.find_all(True):
        tag.attrs = {}
    return soup

def _remove_tags_contents(soup, tags):
    """Remove given tags and contents from soup
    see: https://copyprogramming.com/howto/how-can-i-remove-all-different-script-tags-in-beautifulsoup"""
    for tag in tags:
        for b in soup.find_all(tag):
            b.clear()
            b.decompose()
    return soup


def _minify_html(html: str):
    """Minify html by removing COMMENTS, EMPTY SPACE, and BOOLEAN attribute"""
    min_ = htmlmin.minify(html, remove_comments=True, remove_empty_space=True, remove_all_empty_space=True,
                          reduce_boolean_attributes=True)
    return min_

def get_minified_soup(soup):
    """Get a minified soup"""
    soup = _remove_all_attrs(soup)
    soup = _remove_tags_contents(soup, ["script", "style", "header"])
    return soup
    # return _minify_html(str(soup))