# -*- coding: utf-8 -*-
import os

# def test_bar_fixture(testdir):
#     """Make sure that pytest accepts our fixture."""
#
#     # create a temporary pytest test module
#     testdir.makepyfile("""
#         def test_sth(bar):
#             assert bar == "europython2015"
#     """)
#
#     # run pytest with the following cmd args
#     result = testdir.runpytest(
#         '--foo=europython2015',
#         '-v'
#     )
#
#     # fnmatch_lines does an assertion internally
#     result.stdout.fnmatch_lines([
#         '*::test_sth PASSED',
#     ])
#
#     # make sure that that we get a '0' exit code for the testsuite
#     assert result.ret == 0


def test_slick_url(testdir):
    testdir.makepyfile("""
             def test_url(url):
                 assert url == "http://google.com"
         """)
    result = testdir.runpytest('--slick-url=http://google.com', '-v')
    result.stdout.fnmatch_lines(['*::test_url PASSED'])


def test_help_message(testdir):
    result = testdir.runpytest(
        '--help',
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(['slickqa:', '*--slick-url=SLICK_URL*'])


def test_plugin_can_connect(testdir):
    """Test the plugin to make sure it can connect to the server given some configuration

    :component: DocStringMetaData
    :author: Chris Saxey
    :steps:
        1. Create a file with a test
        2. Run pytest with config info as options
    :expectedResults:
        1. No exception raised
        2. Make sure the test passed
    """
    url = os.environ.get('SLICK_URL')
    testdir.makepyfile("""
    def test_slick(slick):
        '''Test the plugin to make sure it can connect to the server given some configuration

        :component: BatCave
        :author: Batman
        :steps:
            1. Get the url from the slick plugin
            2. Check the url matches
        :expectedResults:
            1. No exception raised
            2. Url matches
        '''
        assert slick.url == "{}"
        """.format(url))
    result = testdir.runpytest('--slick-url={}'.format(url),
                               '--slick-project-name=Python Client',
                               '--slick-release=1.0',
                               '--slick-testplan=Unit',
                               '--slick-build=2',
                               '-v')
    result.stdout.fnmatch_lines(['*::test_slick PASSED'])
