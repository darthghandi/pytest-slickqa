# -*- coding: utf-8 -*-

import pytest
import os


def pytest_addoption(parser):
    group = parser.getgroup('slickqa')
    env = os.environ
    group.addoption("--slick-url", action="store", default=env.get('SLICK_URL'),
                    metavar="SLICK_URL", dest="slick_url",
                    help="the base url of the slick web app [SLICK_URL]")
    group.addoption("--slick-project-name", action="store", default=env.get('SLICK_PROJECT_NAME'),
                    metavar="SLICK_PROJECT_NAME", dest="slick_project_name",
                    help="the name of the project in slick to use [SLICK_PROJECT_NAME]")
    group.addoption("--slick-release", action="store", default=env.get('SLICK_RELEASE'),
                    metavar="SLICK_RELEASE", dest="slick_release",
                    help="the release under which to file the results in slick [SLICK_RELEASE]")
    group.addoption("--slick-build", action="store", default=env.get('SLICK_BUILD'),
                    metavar="SLICK_BUILD", dest="slick_build",
                    help="the build under which to file the results in slick [SLICK_BUILD]")
    group.addoption("--slick-build-from-function", action="store", default=env.get('SLICK_BUILD_FROM_FUNCTION'),
                    metavar="SLICK_BUILD_FROM_FUNCTION", dest="slick_build_from_function",
                    help="get the slick build from a function.  The parameter should be the module and function name "
                         "to call [SLICK_BUILD_FROM_FUNCTION].")
    group.addoption("--slick-testplan", action="store", default=env.get('SLICK_TESTPLAN'),
                    metavar="SLICK_TESTPLAN", dest="slick_testplan",
                    help="the testplan to link the testrun to in slick [SLICK_TESTPLAN]")
    group.addoption("--slick-testrun-name", action="store", default=env.get('SLICK_TESTRUN_NAME'),
                    metavar="SLICK_TESTRUN_NAME", dest="slick_testrun_name",
                    help="the name of the testrun to create in slick [SLICK_TESTRUN_NAME]")
    group.addoption("--slick-environment-name", action="store", default=env.get('SLICK_ENVIRONMENT_NAME'),
                    metavar="SLICK_ENVIRONMENT_NAME", dest="slick_environment_name",
                    help="the name of the environment in slick to use in the testrun [SLICK_ENVIRONMENT_NAME]")
    group.addoption("--slick-testrun-group", action="store", default=env.get('SLICK_TESTRUN_GROUP'),
                    metavar="SLICK_TESTRUN_GROUP", dest="slick_testrun_group",
                    help="the name of the testrun group in slick to add this testrun to (optional) ["
                         "SLICK_ENVIRONMENT_NAME]")


def pytest_collection_modifyitems(session, config, items):
    for i in items:
        print(i)
    pass


@pytest.fixture
def url(request):
    if hasattr(request.config, 'slick_url'):
        return request.config.slick_url
