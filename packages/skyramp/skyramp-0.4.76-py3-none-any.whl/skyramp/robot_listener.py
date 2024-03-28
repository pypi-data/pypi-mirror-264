""" Robot Framework listener to add test cases to the current suite """
import json
import os
from robot.api.deco import keyword
from robot.libraries.BuiltIn  import BuiltIn
from skyramp.test_status import TesterStatusType

class RobotListener:
    """
    Robot Framework listener
    """
    ROBOT_LISTENER_API_VERSION = 3
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        # pylint: disable=invalid-name
        self.ROBOT_LIBRARY_LISTENER = self
        self.current_suite = None

    # pylint: disable=unused-argument
    def _start_suite(self, suite, result):
        self.current_suite = suite

    def add_test_case(self, name, kwname, *args):
        """Adds a test case to the current suite

        'name' is the test case name
        'kwname' is the keyword to call
        '*args' are the arguments to pass to the keyword

        Example:
            add_test_case  Example Test Case  
            ...  log  hello, world  WARN
        """
        test_case = self.current_suite.tests.create(name=name)
        test_case.body.create_keyword(name=kwname, args=args)

    def run_test_cases(self, file_path, address, override_code_path, global_vars, endpoint_addr):
        """
        Executes the test cases in file_path
        """
        base_file = os.path.basename(file_path)
        library = BuiltIn().get_library_instance(name=base_file.replace(".py", ""))
        if isinstance(global_vars, dict) is False:
            global_vars = dict(json.loads((global_vars)))
        if endpoint_addr == "":
            test_case_list =test_case_list = library.execute_tests(
                address=address,
                override_code_path=override_code_path,
                global_vars=global_vars)
        else:
            test_case_list = library.execute_tests(
                address=address,
                override_code_path=override_code_path,
                global_vars=global_vars,
                endpoint_address=endpoint_addr)
        for test_case in test_case_list:
            self.add_test_case(test_case[0].test_case_name, "Keyword To Execute", test_case)
    @keyword
    def keyword_to_execute(self, test_case):
        """Keyword to execute"""
        if test_case[0].test_case_status != "[]":
            BuiltIn().fail(test_case)
        elif test_case[0].status == TesterStatusType.Skipped:
            BuiltIn().skip(test_case)
        else:
            BuiltIn().log(test_case)
            