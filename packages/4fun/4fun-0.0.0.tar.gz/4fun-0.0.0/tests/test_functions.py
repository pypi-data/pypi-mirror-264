import pytest
from 4fun import magic_8_ball

class Tests:
    def test_roll(self):
        '''
        Verify roll returns a non-empty string.
        '''
        actual = magic_8_ball.roll() # get the actual return value of the function
        assert isinstance(actual, str), f"Expected some_function() to return a string. Instead, it returned {actual}"
        assert len(actual) > 0, f"Expected some_function() not to be empty. Instead, it returned a string with {len(actual)} characters"