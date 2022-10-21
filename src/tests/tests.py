import unittest
from tests.cmd.package.TestVersion import TestVersion


def suite():
    # pass
    suite = unittest.TestSuite()
    suite.addTest(TestVersion())
    # suite.addTest(TestState())
    # suite.addTest(TestPreCheck())
    # suite.addTest(TestPackageScheme())
    # suite.addTest(TestGitFlow())
    # suite.addTest(TestGitFlowInit())
    # suite.addTest(TestGitFlowHotfix())
    # suite.addTest(TestReportFileReader())
    return suite


if __name__ == '__main__':
    # pass
    runner = unittest.TextTestRunner()
    runner.run(suite())
