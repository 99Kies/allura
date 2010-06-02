from os import path, environ

import webob
from tg import config
from paste.deploy import loadapp
from paste.script.appinstall import SetupCommand
from pylons import c, g, session, request

from . import helpers

def setUp(self):
    """Method called by nose before running each test"""
    helpers.setup_basic_test()
    helpers.setup_global_objects()

def test_app_globals():
    g.oid_session()
    g.oid_session()
    g.set_project('test')
    g.set_app('hello')
    assert g.app_static('css/style.css') == '/nf/hello_forge/css/style.css', g.app_static('css/style.css')
    assert g.url('/foo', a='foo bar') == 'http://localhost:80/foo?a=foo+bar', g.url('/foo', a='foo bar')
    assert g.url('/foo') == 'http://localhost:80/foo', g.url('/foo')


def test_markdown():
    'Just a test to get coverage in our markdown extension'
    g.set_project('test')
    g.set_app('hello')
    assert '<a href=' in g.markdown.convert('# Foo!\n[Root]')
    assert '<a href=' not in g.markdown.convert('# Foo!\n[Rooted]')
    assert '<a href=' not in g.markdown.convert('http://sf.net') # Meta ext grabs it
    assert '<a href=' in g.markdown.convert('This is http://sf.net')
    assert '<a href=' not in g.markdown.convert('http://sf.net is this') # Meta ext grabs it
    assert '<a href=' in g.markdown_wiki.convert('This is a WikiPage')
    assert '<br>' in g.markdown.convert('Multi\nLine')
    assert '<br>' not in g.markdown.convert('Multi\n\nLine')
    r = g.markdown.convert('[[projects]]')
    assert '<div class="gravatar sm">' in r
    assert '<br>' not in g.markdown.convert('''# Header

Some text in a regular paragraph

    :::python
    for i in range(10):
        print i
''')

def test_oembed():
    g.set_project('test')
    g.set_app('hello')
    urls = [
        'http://www.youtube.com/watch?v=LGRycUpBLS4',
        'http://www.flickr.com/photos/wizardbt/2584979382/',
        'http://www.viddler.com/explore/cdevroe/videos/424/',
        'http://qik.com/qiknews',
        'http://qik.com/video/49565',
        'http://revision3.com/diggnation/2008-04-17xsanned/',
        'http://www.hulu.com/watch/20807/late-night-with-conan-obrein-wed-may-21-2008',
        # 'http://www.vimeo.com/757219', # vimeo's stuff is broken
        # 'http://www.amazon.com/Essential-SQLAlchemy-Rick-Copeland/dp/0596516142/',
        'http://www.polleverywhere.com/multiple_choice_polls/LTIwNzM1NTczNTE',
        'http://my.opera.com/cstrep/albums/show.dml?id=504322',
        # 'http://www.clearspring.com/widgets/480fbb38b51cb736',
        'http://twitter.com/mai_co_jp/statuses/822499364',
        ]
    for url in urls:
        result = g.markdown.convert('[embed#%s]' % url)
        assert ('cannot be embedded' not in result or 'HTTP Error' in result)
    for url in urls:
        result = g.markdown.convert('[embed#(100%%,400)%s]' % url)
        assert ('cannot be embedded' not in result or 'HTTP Error' in result)
    assert 'cannot be embedded' in g.markdown.convert(
        '[embed#http://www.amazon.com/Essential-SQLAlchemy-Rick-Copeland/dp/0596516142/]')
    assert 'cannot be embedded' in g.markdown.convert(
        '[embed#http://www.clearspring.com/widgets/480fbb38b51cb736]')

