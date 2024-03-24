import os
import subprocess
import unittest


class TestNvidiaHtop(unittest.TestCase):
    def do_test(self, stdin, stdout, fake_ps='FAKE_PS', call_args=None):
        if call_args is None:
            call_args = list()
        with open(stdin, 'r') as fake_stdin:
            env = os.environ.copy()
            env['FORCE_COLOR'] = '1'
            test_call = subprocess.run(["../nvidia-htop.py", "--fake-ps", fake_ps] + call_args, stdin=fake_stdin, stdout=subprocess.PIPE, env=env)
            self.assertEqual(test_call.returncode, 0)
            with open(stdout, 'r') as desired_stdout:
                out = desired_stdout.read()
                self.assertEqual(out, test_call.stdout.decode())

    def test_with_processes(self):
        self.do_test('FAKE_STDIN', 'DESIRED_STDOUT')

    def test_new_format(self):
        self.do_test('FAKE_STDIN_NEW_FORMAT', 'DESIRED_STDOUT_NEW_FORMAT')

    def test_new_format_users(self):
        self.do_test('FAKE_STDIN_NEW_FORMAT', 'DESIRED_STDOUT_NEW_FORMAT_USERS', call_args=["-u", "root,test"])

    # The --id option cannot be tested in this way. So we just check that the option is considered valid.
    def test_new_format_filter_ids(self):
        self.do_test('FAKE_STDIN_NEW_FORMAT', 'DESIRED_STDOUT_NEW_FORMAT', call_args=["-i", "1,2"])

    def test_long_pids(self):
        self.do_test('FAKE_STDIN_LONG_PIDS', 'DESIRED_STDOUT_LONG_PIDS', fake_ps='FAKE_PS_LONG_PIDS')

    def test_with_processes_color(self):
        self.do_test('FAKE_STDIN', 'DESIRED_STDOUT_COLOR', call_args=["-c"])

    def test_new_format_with_processes_color(self):
        self.do_test('FAKE_STDIN_NEW_FORMAT', 'DESIRED_STDOUT_NEW_FORMAT_COLOR', call_args=["-c"])

    def test_with_processes_long(self):
        self.do_test('FAKE_STDIN', 'DESIRED_STDOUT_L', call_args=["-l"])

    def test_with_processes_very_long(self):
        self.do_test('FAKE_STDIN', 'DESIRED_STDOUT_L150', call_args=["-l", "150"])

    def test_no_processes(self):
        self.do_test('FAKE_STDIN_NO_PROCESSES', 'DESIRED_STDOUT_NO_PROCESSES')

    def test_no_processes_docker(self):
        self.do_test('FAKE_STDIN_NO_PROCESSES_DOCKER', 'DESIRED_STDOUT_NO_PROCESSES_DOCKER')

    def test_with_meters(self):
        self.do_test('FAKE_STDIN_NEW_FORMAT', 'DESIRED_STDOUT_NEW_FORMAT_METER', call_args=["-m"])

    def test_with_meters_color(self):
        self.do_test('FAKE_STDIN_NEW_FORMAT', 'DESIRED_STDOUT_NEW_FORMAT_METER_COLOR', call_args=["-m", "-c"])
    
    def test_with_meters_long_pids(self):
        self.do_test('FAKE_STDIN_LONG_PIDS', 'DESIRED_STDOUT_NEW_FORMAT_METER_LONG_PIDS', call_args=["-m"], fake_ps='FAKE_PS_LONG_PIDS')

    def test_with_meters_long(self):
        self.do_test('FAKE_STDIN_NEW_FORMAT', 'DESIRED_STDOUT_NEW_FORMAT_METER_L', call_args=["-m", "-l"])
    
    def test_with_meters_very_long(self):
        self.do_test('FAKE_STDIN_NEW_FORMAT', 'DESIRED_STDOUT_NEW_FORMAT_METER_L150', call_args=["-m", "-l", "150"])



if __name__ == '__main__':
    unittest.main()
