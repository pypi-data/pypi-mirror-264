import unittest
from unittest import TestCase


from tool_use.tools.openai_tool_use import CompletionNoneException


class TestCompletionNoneException(TestCase):
    def test_counter(self):
        """Test the counter increments by 1 each time the exception is raised."""
        count = CompletionNoneException.count
        for i in range(10):
            CompletionNoneException()
            self.assertTrue(
                CompletionNoneException.count == count + i + 1,
                CompletionNoneException.count,
            )

    def test_check_function(self):
        """Test the check function returns False if the counter is greater than 1."""
        for i in range(10):
            exception = CompletionNoneException()
            if i == 0:
                self.assertTrue(exception.is_first_exception())
            else:
                self.assertFalse(exception.is_first_exception())


# Run the unit tests
if __name__ == "__main__":
    unittest.main()
