import subprocess
import sys
import unittest
from queue import Queue

from solution import generate_request, process_request, is_palindrome


class ServiceTests(unittest.TestCase):
    def test_fifo_unique_and_empty(self):
        queue = Queue()
        created = [generate_request(queue) for _ in range(50)]
        self.assertEqual(len({r.id for r in created}), 50)
        self.assertEqual([process_request(queue) for _ in created], created)
        self.assertIsNone(process_request(queue))
        self.assertEqual(queue.unfinished_tasks, 0)

    def test_palindromes(self):
        for value in ['', 'x', 'abba', 'Race car', 'А роза упала на лапу Азора', '\tАа\n']:
            with self.subTest(value=value):
                self.assertTrue(is_palindrome(value))
        for value in ['queue', 'ab', 'aba!']:
            with self.subTest(value=value):
                self.assertFalse(is_palindrome(value))

    def test_cli_finite_and_exit(self):
        result = subprocess.run([sys.executable, 'solution.py', 'service', '--cycles', '3'],
                                text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count('Processed request'), 3)
        result = subprocess.run([sys.executable, 'solution.py', 'service'], input='q\n',
                                text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
