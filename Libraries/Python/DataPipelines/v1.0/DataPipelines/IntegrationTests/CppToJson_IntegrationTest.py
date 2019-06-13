'''Integration tests for CppToJson.py
'''
import sys
import os
import json
import unittest
import CommonEnvironment

from DataPipelines import CppToJson


# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------


class FileTest(unittest.TestCase):
    '''
        The purpose of this function is to verify the file-based capabilities of the ObtainFunctions method. It will make sure
        that the files are being opened and the information inside is being correctly processed.
    '''
    def test_basic_file(self):
        func_list = CppToJson.ObtainFunctions(os.path.join(_script_dir, "basicFunc.cpp"), None, lambda type: True)
        
        self.assertEqual(func_list[0], {'func_name': 'add', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': ['a', 'b'], 'raw_var_types': ['int', 'int'], 'simple_var_types': ['int', 'int'], 'definition_line': 6, 'declaration_line': None})
        self.assertEqual(func_list[1], {'func_name': 'sub', 'raw_return_type': 'float', 'simple_return_type': 'float', 'var_names': ['a', 'b'], 'raw_var_types': ['float', 'float'], 'simple_var_types': ['float', 'float'], 'definition_line': 10, 'declaration_line': None})
        self.assertEqual(func_list[2], {'func_name': 'isPos', 'raw_return_type': 'bool', 'simple_return_type': 'bool', 'var_names': ['x'], 'raw_var_types': ['bool'], 'simple_var_types': ['bool'], 'definition_line': 14, 'declaration_line': None})
        self.assertEqual(func_list[3], {'func_name': 'three', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': [], 'raw_var_types': [], 'simple_var_types': [], 'definition_line': 18, 'declaration_line': None})
        self.assertEqual(func_list[4], {'func_name': 'nothing', 'raw_return_type': 'void', 'simple_return_type': 'void', 'var_names': [], 'raw_var_types': [], 'simple_var_types': [], 'definition_line': 22, 'declaration_line': None})
        self.assertEqual(func_list[5], {'func_name': 'main', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': [], 'raw_var_types': [], 'simple_var_types': [], 'definition_line': 27, 'declaration_line': None})
    
    def test_medium_file(self):
        func_list = CppToJson.ObtainFunctions(os.path.join(_script_dir, "mediumFunc.cpp"), None, lambda type: True)
        
        self.assertEqual(func_list[0], {'func_name': 'add', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': ['a', 'b'], 'raw_var_types': ['float', 'int'], 'simple_var_types': ['float', 'int'], 'definition_line': 5, 'declaration_line': None})
        self.assertEqual(func_list[1], {'func_name': 'mult', 'raw_return_type': 'float', 'simple_return_type': 'float', 'var_names': ['a', 'b', 'signal'], 'raw_var_types': ['int', 'float', 'bool'], 'simple_var_types': ['int', 'float', 'bool'], 'definition_line': 9, 'declaration_line': None})
        self.assertEqual(func_list[2], {'func_name': 'toUp', 'raw_return_type': 'std::string', 'simple_return_type': 'std::string', 'var_names': ['s'], 'raw_var_types': ['std::string'], 'simple_var_types': ['std::string'], 'definition_line': 13, 'declaration_line': None})
        self.assertEqual(func_list[3], {'func_name': 'fat', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': ['curr', 'at'], 'raw_var_types': ['int', 'int'], 'simple_var_types': ['int', 'int'], 'definition_line': 19, 'declaration_line': None})
        self.assertEqual(func_list[4], {'func_name': 'main', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': [], 'raw_var_types': [], 'simple_var_types': [], 'definition_line': 24, 'declaration_line': None})

    
    def test_hard_file(self):
        func_list = CppToJson.ObtainFunctions(os.path.join(_script_dir, "hardFunc.cpp"), None, lambda type: True)

        self.assertEqual(func_list[0], {'func_name': 'add', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': ['a'], 'raw_var_types': ['int'], 'simple_var_types': ['int'], 'definition_line': 10, 'declaration_line': None})
        self.assertEqual(func_list[1], {'func_name': 'main', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': [], 'raw_var_types': [], 'simple_var_types': [], 'definition_line': 17, 'declaration_line': None})
        self.assertEqual(func_list[2], {'func_name': 'bubbleSort', 'raw_return_type': 'vector<int>', 'simple_return_type': 'vector<int>', 'var_names': ['v'], 'raw_var_types': ['vector<int>'], 'simple_var_types': ['vector<int>'], 'definition_line': 22, 'declaration_line': None})
        self.assertEqual(func_list[3], {'func_name': 'sizeOfMap', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': ['mp'], 'raw_var_types': ['map<int, bool>'], 'simple_var_types': ['map<int, bool>'], 'definition_line': 32, 'declaration_line': None})
        self.assertEqual(func_list[4], {'func_name': 'keys', 'raw_return_type': 'vector<int>', 'simple_return_type': 'vector<int>', 'var_names': ['mp'], 'raw_var_types': ['map<int, int>'], 'simple_var_types': ['map<int, int>'], 'definition_line': 35, 'declaration_line': None})
        self.assertEqual(func_list[5], {'func_name': 'goCount', 'raw_return_type': 'map<float, int>', 'simple_return_type': 'map<float, int>', 'var_names': ['v', 'signal'], 'raw_var_types': ['vector<float>', 'bool'], 'simple_var_types': ['vector<float>', 'bool'], 'definition_line': 43, 'declaration_line': None})


    def test_convoluted_file(self):
        func_list = CppToJson.ObtainFunctions(os.path.join(_script_dir, "convolutedFunc.cpp"), None, lambda type: True)
        
        self.assertEqual(func_list[0], {'func_name': 'matrix', 'raw_return_type': 'vector<vector<int> >', 'simple_return_type': 'vector<vector<int> >', 'var_names': ['n'], 'raw_var_types': ['int'], 'simple_var_types': ['int'], 'definition_line': 9, 'declaration_line': None})
        self.assertEqual(func_list[1], {'func_name': 'nonsense', 'raw_return_type': 'map<map<int, vector<bool> >, vector<float> >', 'simple_return_type': 'map<map<int, vector<bool> >, vector<float> >', 'var_names': ['n'], 'raw_var_types': ['int'], 'simple_var_types': ['int'], 'definition_line': 19, 'declaration_line': None})
        self.assertEqual(func_list[2], {'func_name': 'vectorLine', 'raw_return_type': 'vector<vector<vector<vector<float> > > >', 'simple_return_type': 'vector<vector<vector<vector<float> > > >', 'var_names': ['mp'], 'raw_var_types': ['map<bool, int>'], 'simple_var_types': ['map<bool, int>'], 'definition_line': 30, 'declaration_line': None})
        self.assertEqual(func_list[3], {'func_name': 'countVector', 'raw_return_type': 'map<int, int>', 'simple_return_type': 'map<int, int>', 'var_names': ['v'], 'raw_var_types': ['vector<vector<int> >'], 'simple_var_types': ['vector<vector<int> >'], 'definition_line': 42, 'declaration_line': None})
        self.assertEqual(func_list[4], {'func_name': 'main', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': [], 'raw_var_types': [], 'simple_var_types': [], 'definition_line': 50, 'declaration_line': None})

    def test_mix_file(self):
        func_list = CppToJson.ObtainFunctions(os.path.join(_script_dir, "mixFunc.cpp"), None, lambda type: True)
        
        self.assertEqual(func_list[0], {'func_name': 'nonsense', 'raw_return_type': 'vector<map<int, float> > *', 'simple_return_type': 'vector<map<int, float> >', 'var_names': ['v', 'mp'], 'raw_var_types': ['vector<int> &', 'map<bool, bool> *'], 'simple_var_types': ['vector<int>', 'map<bool, bool>'], 'definition_line': 6, 'declaration_line': None}) 
        self.assertEqual(func_list[1], {'func_name': 'address', 'raw_return_type': 'vector<int> &', 'simple_return_type': 'vector<int>', 'var_names': ['v'], 'raw_var_types': ['vector<int> &'], 'simple_var_types': ['vector<int>'], 'definition_line': 11, 'declaration_line': None}) 
        self.assertEqual(func_list[2], {'func_name': 'even', 'raw_return_type': 'map<int, vector<bool> > **', 'simple_return_type': 'map<int, vector<bool> >', 'var_names': ['n'], 'raw_var_types': ['int'], 'simple_var_types': ['int'], 'definition_line': 15, 'declaration_line': None}) 
        self.assertEqual(func_list[3], {'func_name': 'dereference', 'raw_return_type': 'int **********', 'simple_return_type': 'int', 'var_names': ['ref'], 'raw_var_types': ['int ***********'], 'simple_var_types': ['int'], 'definition_line': 22, 'declaration_line': None}) 
        self.assertEqual(func_list[4], {'func_name': 'constDereference', 'raw_return_type': 'const int **********', 'simple_return_type': 'int', 'var_names': ['ref'], 'raw_var_types': ['const int ***********'], 'simple_var_types': ['int'], 'definition_line': 26, 'declaration_line': None}) 
        self.assertEqual(func_list[5], {'func_name': 'main', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': [], 'raw_var_types': [], 'simple_var_types': [], 'definition_line': 31, 'declaration_line': None}) 

    def test_class_file_unsupported(self):
        called_count = 0

        # ----------------------------------------------------------------------
        def onUnsupportedFunc(func, line):
            nonlocal called_count
            called_count += 1
            self.assertTrue([func, line] in [['operator+', 15], ['sum', 22], ['go', 26], ['main', 34]])
        
        # ----------------------------------------------------------------------

        func_list = CppToJson.ObtainFunctions(os.path.join(_script_dir, "classFunc.cpp"), onUnsupportedFunc, lambda type: False)
        
        self.assertEqual(called_count, 4)

        self.assertEqual(func_list, [])

    def test_namespace_file(self):
        func_list = CppToJson.ObtainFunctions(os.path.join(_script_dir, "arithmetic.cpp"), None, lambda type: True)
        
        self.assertEqual(func_list[0], {'func_name': 'DataPipelines::Arithmetic::Add', 'raw_return_type': 'int64_t', 'simple_return_type': 'int64_t', 'var_names': ['a', 'b'], 'raw_var_types': ['const int64_t', 'const int64_t'], 'simple_var_types': ['int64_t', 'int64_t'], 'definition_line': 12, 'declaration_line': None})
        self.assertEqual(func_list[1], {'func_name': 'DataPipelines::Arithmetic::Add', 'raw_return_type': 'uint64_t', 'simple_return_type': 'uint64_t', 'var_names': ['a', 'b'], 'raw_var_types': ['const uint64_t', 'const uint64_t'], 'simple_var_types': ['uint64_t', 'uint64_t'], 'definition_line': 13, 'declaration_line': None})
        self.assertEqual(func_list[2], {'func_name': 'DataPipelines::Arithmetic::Add', 'raw_return_type': 'uint32_t', 'simple_return_type': 'uint32_t', 'var_names': ['a', 'b'], 'raw_var_types': ['const uint32_t', 'const uint32_t'], 'simple_var_types': ['uint32_t', 'uint32_t'], 'definition_line': 14, 'declaration_line': None})
        self.assertEqual(func_list[3], {'func_name': 'DataPipelines::Arithmetic::Add', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': ['a', 'b'], 'raw_var_types': ['int', 'int'], 'simple_var_types': ['int', 'int'], 'definition_line': 30, 'declaration_line': 16})
        self.assertEqual(func_list[4], {'func_name': 'DataPipelines::Arithmetic::thisguy', 'raw_return_type': 'void', 'simple_return_type': 'void', 'var_names': ['a', 'b'], 'raw_var_types': ['int', 'int'], 'simple_var_types': ['int', 'int'], 'definition_line': 34, 'declaration_line': 18})
        self.assertEqual(func_list[5], {'func_name': 'DataPipelines::Arithmetic::Add', 'raw_return_type': 'double', 'simple_return_type': 'double', 'var_names': ['a', 'b'], 'raw_var_types': ['const double', 'const double'], 'simple_var_types': ['double', 'double'], 'definition_line': 23, 'declaration_line': None})
        self.assertEqual(func_list[6], {'func_name': 'DataPipelines::Arithmetic::Addi32', 'raw_return_type': 'int32_t', 'simple_return_type': 'int32_t', 'var_names': ['a', 'b'], 'raw_var_types': ['const int32_t', 'const int32_t'], 'simple_var_types': ['int32_t', 'int32_t'], 'definition_line': 26, 'declaration_line': None})
        self.assertEqual(func_list[7], {'func_name': 'Addu64', 'raw_return_type': 'uint64_t', 'simple_return_type': 'uint64_t', 'var_names': ['a', 'b'], 'raw_var_types': ['const uint64_t', 'const uint64_t'], 'simple_var_types': ['uint64_t', 'uint64_t'], 'definition_line': 38, 'declaration_line': None})
        self.assertEqual(func_list[8],  {'func_name': 'Addi64', 'raw_return_type': 'int64_t', 'simple_return_type': 'int64_t', 'var_names': ['a', 'b'], 'raw_var_types': ['const int64_t', 'const int64_t'], 'simple_var_types': ['int64_t', 'int64_t'], 'definition_line': 44, 'declaration_line': None})
        self.assertEqual(func_list[9],  {'func_name': 'Addu32', 'raw_return_type': 'uint32_t', 'simple_return_type': 'uint32_t', 'var_names': ['a', 'b'], 'raw_var_types': ['const uint32_t', 'const uint32_t'], 'simple_var_types': ['uint32_t', 'uint32_t'], 'definition_line': 48, 'declaration_line': None})

if __name__ == '__main__':
    unittest.main()
