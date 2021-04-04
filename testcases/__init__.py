import unittest

from app_remote.app_remote import AppRemote


class Testcase(unittest.TestCase):

    def __init__(self, method_name: str = 'runTest', app_remote: AppRemote = None, test_data: dict = None):
        super(Testcase, self).__init__(method_name)
        self.app = app_remote
        self.test_data = test_data

    def runTest(self):
        self.assertEqual(True, True)

    @staticmethod
    def parametrize(testcase_klass, app_remote: AppRemote, test_data: dict = None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, app_remote=app_remote, test_data=test_data))
        return suite


class MonolithicTestcase(Testcase):

    def __init__(self, method_name: str = 'runTest', app_remote: AppRemote = None, test_data: dict = None):
        super(MonolithicTestcase, self).__init__(method_name, app_remote, test_data)

    def _steps(self):
        for name in dir(self):  # dir() result is implicitly sorted
            if name.startswith("step"):
                yield name, getattr(self, name)

    def test_steps(self):
        for name, step in self._steps():
            try:
                step()
            except Exception as e:
                self.fail("{} failed ({}: {})".format(step, type(e), e))