import pytest
import tempfile
import subprocess
import sys
import os

def test_skip_teardown_with_pdb():
    """Test that tearDown is not called on skipped tests when running with --pdb"""
    test_code = '''
import unittest

class MyTestCase(unittest.TestCase):
    def setUp(self):
        raise NameError("xxx in setUp")
    
    @unittest.skip("hello")
    def test_one(self):
        pass
    
    def tearDown(self):
        raise NameError("xxx in tearDown")
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        f.flush()
        
        try:
            # Test normal behavior (without --pdb) - should be skipped without errors
            normal_result = subprocess.run([
                sys.executable, '-m', 'pytest', f.name, '-v'
            ], capture_output=True, text=True, cwd=os.path.dirname(__file__))
            
            print("Normal result (without --pdb):")
            print("STDOUT:", normal_result.stdout)
            print("STDERR:", normal_result.stderr)
            print("Return code:", normal_result.returncode)
            
            # Test with --pdb - should be skipped without running tearDown
            pdb_result = subprocess.run([
                sys.executable, '-m', 'pytest', f.name, '--pdb', '-v'
            ], capture_output=True, text=True, input='q\n', cwd=os.path.dirname(__file__))
            
            print("\nWith --pdb result:")
            print("STDOUT:", pdb_result.stdout)
            print("STDERR:", pdb_result.stderr)
            print("Return code:", pdb_result.returncode)
            
            # Check if tearDown was executed (should not be)
            teardown_executed = "NameError: name 'xxx' is not defined" in pdb_result.stdout
            
            if teardown_executed:
                print("\nBUG CONFIRMED: tearDown was executed on skipped test with --pdb")
            else:
                print("\nOK: tearDown was not executed on skipped test with --pdb")
                
        finally:
            os.unlink(f.name)

if __name__ == "__main__":
    test_skip_teardown_with_pdb()