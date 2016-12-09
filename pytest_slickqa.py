# -*- coding: utf-8 -*-

import pytest
import os
from datetime import datetime
from slickqa import *


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


def pytest_configure(config):
    if hasattr(config.option, 'slick_url'):
        s = SlickQAPyTestPlugin(config.option)
        try:
            s.connect()
            # Don't register if we cannot successfully connect
            config.pluginmanager.register(s, '_slickqa')
        except:
            pass


class SlickQAPyTestPlugin(object):
    def __init__(self, config):
        self.url = config.slick_url
        self.project_name = config.slick_project_name
        self.release = config.slick_release
        self.build = config.slick_build
        self.test_plan = config.slick_testplan
        self.test_run_name = config.slick_testrun_name
        self.env_name = config.slick_environment_name
        self.test_run_group_name = config.slick_testrun_group
        self.slick = None
        self.connected = False
        self.results = {}

    def connect(self):
        try:
            self.slick = SlickQA(self.url, self.project_name, self.release, self.build, self.test_plan,
                                 self.test_run_name, self.env_name, self.test_run_group_name)
            self.connected = True
        except SlickCommunicationError as se:
            print(se)

    # TODO: refactor this method
    @pytest.hookimpl(trylast=True)
    def pytest_collection_modifyitems(self, items):
        if self.connected:
            for item in items:
                # TODO: subclass and make a method to get doc string
                test_data = DocStringMetaData(item._obj)
                slick_test_case = Testcase()
                slick_test_case.name = test_data.name
                for attribute in ['automationConfiguration', 'automationKey', 'author', 'purpose', 'requirements',
                                  'tags']:
                    if attribute is not None and hasattr(test_data, attribute) and \
                            getattr(test_data, attribute) is not None:
                        value = getattr(test_data, attribute)
                        setattr(slick_test_case, attribute, value)
                slick_test_case.project = self.slick.project.create_reference()
                if not hasattr(test_data, 'automationId'):
                    slick_test_case.automationId = item.nodeid
                if not hasattr(test_data, 'automationTool'):
                    slick_test_case.automationTool = 'pytest'
                if not hasattr(test_data, 'automationKey'):
                    slick_test_case.automationKey = item.fspath.strpath
                if hasattr(test_data, 'component'):
                    component = self.slick.get_component(test_data.component)
                    if component is None:
                        component = self.slick.create_component(test_data.component)
                    slick_test_case.component = component.create_reference()
                if hasattr(test_data, 'steps'):
                    slick_test_case.steps = []
                    for step in test_data.steps:
                        slickstep = Step()
                        slickstep.name = step
                        if hasattr(test_data, 'expectedResults') and len(test_data.expectedResults) > len(
                                slick_test_case.steps):
                            expected_result = test_data.expectedResults[len(slick_test_case.steps)]
                            slickstep.expectedResult = expected_result
                result = self.slick.file_result(slick_test_case.name, ResultStatus.NOT_TESTED, reason="not yet run",
                                                runlength=0, testdata=slick_test_case, runstatus=RunStatus.TO_BE_RUN)
                self.results[item.nodeid] = result

    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_setup(self, item):
        test_name = item.nodeid
        if self.connected and test_name in self.results:
            result = self.results[test_name]
            result.runstatus = RunStatus.RUNNING
            result.started = datetime.now()
            result.reason = ""
            if hasattr(result, 'config') and not hasattr(result.config, 'configId'):
                del result.config
            if hasattr(result, 'component') and not hasattr(result.component, 'id'):
                del result.component
            result.update()

    def pytest_runtest_logreport(self, report):
        if report.when != "call" and report.passed:
            return
        test_name = report.nodeid
        if self.connected and test_name in self.results:
            result = self.results[test_name]
            result.finished = datetime.now()
            result.runlength = int((result.finished - result.started).total_seconds() * 1000)
            result.runstatus = RunStatus.FINISHED
            result.status = ResultStatus.FAIL
            reason = ''
            if report.passed:
                result.status = ResultStatus.PASS
            elif report.skipped:
                result.status = ResultStatus.SKIPPED
            else:
                reason = report.longreprtext
            result.reason = reason
            if hasattr(result, 'config') and not hasattr(result.config, 'configId'):
                del result.config
            if hasattr(result, 'component') and not hasattr(result.component, 'id'):
                del result.component
            result.update()




@pytest.fixture
def url(request):
    if hasattr(request.config.option, 'slick_url'):
        return request.config.option.slick_url


@pytest.fixture
def slick(request):
    if hasattr(request.config.option, 'slick_url'):
        return request.config.pluginmanager.getplugin('_slickqa')

