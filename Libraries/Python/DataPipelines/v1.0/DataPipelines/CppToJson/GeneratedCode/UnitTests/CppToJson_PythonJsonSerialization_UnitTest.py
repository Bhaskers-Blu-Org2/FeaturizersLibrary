# ----------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License
# ----------------------------------------------------------------------
"""Unit tests for CppToJson_PythonJsonSerialization.py"""

import os
import sys
import unittest

import CommonEnvironment
from DataPipelines.CppToJson.GeneratedCode.CppToJson_PythonJsonSerialization import *

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
class TestSuite(unittest.TestCase):
    # ----------------------------------------------------------------------
    def test_Empty(self):
        self.assertEqual(Deserialize([]), [])

    # ----------------------------------------------------------------------
    def test_NoArgs(self):
        result = Deserialize(
            [
                {
                    "function_list": [
                        {
                            "name": "Name",
                            "raw_return_type": "int1",
                            "simple_return_type": "int2",
                        }
                    ],
                },
            ],
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].function_list[0].name, "Name")
        self.assertEqual(result[0].function_list[0].raw_return_type, "int1")
        self.assertEqual(result[0].function_list[0].simple_return_type, "int2")
        self.assertTrue(not hasattr(result[0].function_list[0], "var_names"))
        self.assertTrue(not hasattr(result[0].function_list[0], "raw_var_types"))
        self.assertTrue(not hasattr(result[0].function_list[0], "simple_var_types"))
        self.assertTrue(not hasattr(result[0].function_list[0], "declaration_line"))
        self.assertTrue(not hasattr(result[0].function_list[0], "definition_line"))

        self.assertTrue(not hasattr(result[0], "struct_list"))
        self.assertTrue(not hasattr(result[0], "include_list"))

    # ----------------------------------------------------------------------
    def test_WithArgs(self):
        result = Deserialize(
            [
                {
                    "function_list": [{
                        "name": "Name",
                        "raw_return_type": "int1",
                        "simple_return_type": "int2",
                        "var_names": ["a", "b"],
                        "raw_var_types": ["c", "d"],
                        "simple_var_types": ["e", "f"],
                        "declaration_line": 3,
                        "definition_line": 7,
                    }],
                },
            ],
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].function_list[0].name, "Name")
        self.assertEqual(result[0].function_list[0].raw_return_type, "int1")
        self.assertEqual(result[0].function_list[0].simple_return_type, "int2")
        self.assertEqual(result[0].function_list[0].var_names, ["a", "b"])
        self.assertEqual(result[0].function_list[0].raw_var_types, ["c", "d"])
        self.assertEqual(result[0].function_list[0].simple_var_types, ["e", "f"])
        self.assertEqual(result[0].function_list[0].declaration_line, 3)
        self.assertEqual(result[0].function_list[0].definition_line, 7)

        self.assertTrue(not hasattr(result[0], "struct_list"))
        self.assertTrue(not hasattr(result[0], "include_list"))

    # ----------------------------------------------------------------------
    def test_Multiple(self):
        result = Deserialize(
            [
                {
                    "function_list": [
                        {
                            "name": "Name1",
                            "raw_return_type": "int1",
                            "simple_return_type": "int2",
                            "definition_line": 12,
                        },
                        {
                            "name": "Name2",
                            "raw_return_type": "int3",
                            "simple_return_type": "int4",
                            "definition_line": 34,
                        },
                    ],
                },
            ],
        )

        self.assertEqual(len(result[0].function_list), 2)

        self.assertEqual(result[0].function_list[0].name, "Name1")
        self.assertEqual(result[0].function_list[0].raw_return_type, "int1")
        self.assertEqual(result[0].function_list[0].simple_return_type, "int2")
        self.assertEqual(result[0].function_list[0].definition_line, 12)
        self.assertTrue(not hasattr(result[0].function_list[0], "var_names"))
        self.assertTrue(not hasattr(result[0].function_list[0], "raw_var_types"))
        self.assertTrue(not hasattr(result[0].function_list[0], "simple_var_types"))
        self.assertTrue(not hasattr(result[0].function_list[0], "declaration_line"))

        self.assertEqual(result[0].function_list[1].name, "Name2")
        self.assertEqual(result[0].function_list[1].raw_return_type, "int3")
        self.assertEqual(result[0].function_list[1].simple_return_type, "int4")
        self.assertEqual(result[0].function_list[1].definition_line, 34)
        self.assertTrue(not hasattr(result[0].function_list[1], "var_names"))
        self.assertTrue(not hasattr(result[0].function_list[1], "raw_var_types"))
        self.assertTrue(not hasattr(result[0].function_list[1], "simple_var_types"))
        self.assertTrue(not hasattr(result[0].function_list[1], "declaration_line"))

        self.assertTrue(not hasattr(result[0], "struct_list"))
        self.assertTrue(not hasattr(result[0], "include_list"))

    # ----------------------------------------------------------------------
    def test_NoConstructor(self):
        result = Deserialize(
            [
                {
                    "struct_list": [{
                        "name": "Name",
                        "var_names": ["a", "b"],
                        "raw_var_types": ["c", "d"],
                        "simple_var_types": ["e", "f"],
                        "definition_line": 7,
                    }],
                },
            ],
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].struct_list[0].name, "Name")
        self.assertEqual(result[0].struct_list[0].var_names, ["a", "b"])
        self.assertEqual(result[0].struct_list[0].raw_var_types, ["c", "d"])
        self.assertEqual(result[0].struct_list[0].simple_var_types, ["e", "f"])
        self.assertEqual(result[0].struct_list[0].definition_line, 7)
        self.assertTrue(not hasattr(result[0].struct_list[0], "constructor_list"))

        self.assertTrue(not hasattr(result[0], "function_list"))
        self.assertTrue(not hasattr(result[0], "include_list"))

    # ----------------------------------------------------------------------
    def test_WithConstructor(self):
        result = Deserialize(
            [
                {
                    "struct_list": [{
                        "name": "Name",
                        "var_names": ["a", "b"],
                        "raw_var_types": ["c", "d"],
                        "simple_var_types": ["e", "f"],
                        "definition_line": 7,
                        "constructor_list": [{
                            "var_names": ["arg1", "arg2"],
                            "raw_var_types": ["a", "b"],
                            "simple_var_types": ["c", "d"],
                            "definition_line": 13,
                        }],
                    }],
                },
            ],
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].struct_list[0].name, "Name")
        self.assertEqual(result[0].struct_list[0].var_names, ["a", "b"])
        self.assertEqual(result[0].struct_list[0].raw_var_types, ["c", "d"])
        self.assertEqual(result[0].struct_list[0].simple_var_types, ["e", "f"])
        self.assertEqual(result[0].struct_list[0].definition_line, 7)

        self.assertEqual(
            result[0].struct_list[0].constructor_list[0].var_names,
            ["arg1", "arg2"],
        )
        self.assertEqual(
            result[0].struct_list[0].constructor_list[0].raw_var_types,
            ["a", "b"],
        )
        self.assertEqual(
            result[0].struct_list[0].constructor_list[0].simple_var_types,
            ["c", "d"],
        )
        self.assertEqual(result[0].struct_list[0].constructor_list[0].definition_line, 13)

        self.assertTrue(not hasattr(result[0], "function_list"))
        self.assertTrue(not hasattr(result[0], "include_list"))

    # ----------------------------------------------------------------------
    def test_WithMultipleConstructors(self):
        result = Deserialize(
            [
                {
                    "struct_list": [{
                        "name": "Name",
                        "var_names": ["a", "b"],
                        "raw_var_types": ["c", "d"],
                        "simple_var_types": ["e", "f"],
                        "definition_line": 7,
                        "constructor_list": [
                            {
                                "var_names": ["arg1", "arg2"],
                                "raw_var_types": ["a", "b"],
                                "simple_var_types": ["c", "d"],
                                "definition_line": 13,
                            },
                            {
                                "var_names": ["arg12", "arg22"],
                                "raw_var_types": ["a2", "b2"],
                                "simple_var_types": ["c2", "d2"],
                                "definition_line": 132,
                            },
                        ],
                    }],
                },
            ],
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].struct_list[0].name, "Name")
        self.assertEqual(result[0].struct_list[0].var_names, ["a", "b"])
        self.assertEqual(result[0].struct_list[0].raw_var_types, ["c", "d"])
        self.assertEqual(result[0].struct_list[0].simple_var_types, ["e", "f"])
        self.assertEqual(result[0].struct_list[0].definition_line, 7)

        self.assertEqual(
            result[0].struct_list[0].constructor_list[0].var_names,
            ["arg1", "arg2"],
        )
        self.assertEqual(
            result[0].struct_list[0].constructor_list[0].raw_var_types,
            ["a", "b"],
        )
        self.assertEqual(
            result[0].struct_list[0].constructor_list[0].simple_var_types,
            ["c", "d"],
        )
        self.assertEqual(result[0].struct_list[0].constructor_list[0].definition_line, 13)

        self.assertEqual(
            result[0].struct_list[0].constructor_list[1].var_names,
            ["arg12", "arg22"],
        )
        self.assertEqual(
            result[0].struct_list[0].constructor_list[1].raw_var_types,
            ["a2", "b2"],
        )
        self.assertEqual(
            result[0].struct_list[0].constructor_list[1].simple_var_types,
            ["c2", "d2"],
        )
        self.assertEqual(
            result[0].struct_list[0].constructor_list[1].definition_line,
            132,
        )

        self.assertTrue(not hasattr(result[0], "function_list"))
        self.assertTrue(not hasattr(result[0], "include_list"))

    # ----------------------------------------------------------------------
    def test_WithBaseStruct(self):
        result = Deserialize(
            [
                {
                    "struct_list": [{
                        "name": "Name",
                        "var_names": ["a", "b"],
                        "raw_var_types": ["c", "d"],
                        "simple_var_types": ["e", "f"],
                        "definition_line": 7,
                        "base_structs": ["struct1"],
                    }],
                },
            ],
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].struct_list[0].name, "Name")
        self.assertEqual(result[0].struct_list[0].var_names, ["a", "b"])
        self.assertEqual(result[0].struct_list[0].raw_var_types, ["c", "d"])
        self.assertEqual(result[0].struct_list[0].simple_var_types, ["e", "f"])
        self.assertEqual(result[0].struct_list[0].definition_line, 7)
        self.assertTrue(not hasattr(result[0].struct_list[0], "constructor_list"))
        self.assertEqual(result[0].struct_list[0].base_structs, ["struct1"])

        self.assertTrue(not hasattr(result[0], "function_list"))
        self.assertTrue(not hasattr(result[0], "include_list"))

    # ----------------------------------------------------------------------
    def test_WithMultipleBaseStruct(self):
        result = Deserialize(
            [
                {
                    "struct_list": [{
                        "name": "Name",
                        "var_names": ["a", "b"],
                        "raw_var_types": ["c", "d"],
                        "simple_var_types": ["e", "f"],
                        "definition_line": 7,
                        "base_structs": ["struct1", "struct2", "struct3"],
                    }],
                },
            ],
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].struct_list[0].name, "Name")
        self.assertEqual(result[0].struct_list[0].var_names, ["a", "b"])
        self.assertEqual(result[0].struct_list[0].raw_var_types, ["c", "d"])
        self.assertEqual(result[0].struct_list[0].simple_var_types, ["e", "f"])
        self.assertEqual(result[0].struct_list[0].definition_line, 7)
        self.assertTrue(not hasattr(result[0].struct_list[0], "constructor_list"))
        self.assertEqual(
            result[0].struct_list[0].base_structs,
            ["struct1", "struct2", "struct3"],
        )

        self.assertTrue(not hasattr(result[0], "function_list"))
        self.assertTrue(not hasattr(result[0], "include_list"))

    # ----------------------------------------------------------------------
    def test_include(self):
        result = Deserialize([{"include_list": ["vector"]}])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].include_list, ["vector"])

        self.assertTrue(not hasattr(result[0], "function_list"))
        self.assertTrue(not hasattr(result[0], "struct_list"))

    # ----------------------------------------------------------------------
    def test_multiple_includes(self):
        result = Deserialize(
            [
                {
                    "include_list": [
                        "vector",
                        "a",
                        "b",
                        "c",
                    ],
                },
            ],
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0].include_list,
            [
                "vector",
                "a",
                "b",
                "c",
            ],
        )

        self.assertTrue(not hasattr(result[0], "function_list"))
        self.assertTrue(not hasattr(result[0], "struct_list"))

    # ----------------------------------------------------------------------
    def test_InvalidName(self):
        self.assertRaisesRegex(
            Exception,
            "An item was expected",
            lambda: Deserialize(
                [
                    {
                        "function_list": [
                            {
                                "name": None,
                                "raw_return_type": "int1",
                                "simple_return_type": "int2",
                            },
                        ],
                    },
                ],
            ),
        )

        self.assertRaisesRegex(
            Exception,
            "'' is not a valid 'String' string - Value must have at least 1 character",
            lambda: Deserialize(
                [
                    {
                        "function_list": [
                            {
                                "name": "",
                                "raw_return_type": "int1",
                                "simple_return_type": "int2",
                            },
                        ],
                    },
                ],
            ),
        )

    # ----------------------------------------------------------------------
    def test_InvalidRawReturnType(self):
        self.assertRaisesRegex(
            Exception,
            "An item was expected",
            lambda: Deserialize(
                [
                    {
                        "function_list": [
                            {
                                "name": "Name",
                                "raw_return_type": None,
                                "simple_return_type": "int2",
                            },
                        ],
                    },
                ],
            ),
        )

        self.assertRaisesRegex(
            Exception,
            "'' is not a valid 'String' string - Value must have at least 1 character",
            lambda: Deserialize(
                [
                    {
                        "function_list": [
                            {
                                "name": "Name",
                                "raw_return_type": "",
                                "simple_return_type": "int2",
                            },
                        ],
                    },
                ],
            ),
        )

    # ----------------------------------------------------------------------
    def test_InvalidSimpleReturnType(self):
        self.assertRaisesRegex(
            Exception,
            "An item was expected",
            lambda: Deserialize(
                [
                    {
                        "function_list": [
                            {
                                "name": "Name",
                                "raw_return_type": "int1",
                                "simple_return_type": None,
                            },
                        ],
                    },
                ],
            ),
        )

        self.assertRaisesRegex(
            Exception,
            "'' is not a valid 'String' string - Value must have at least 1 character",
            lambda: Deserialize(
                [
                    {
                        "function_list": [
                            {
                                "name": "Name",
                                "raw_return_type": "int1",
                                "simple_return_type": "",
                            },
                        ],
                    },
                ],
            ),
        )

    # ----------------------------------------------------------------------
    def test_InvalidVarName(self):
        self.assertRaisesRegex(
            Exception,
            "expected string or bytes-like object",                         # TODO
            lambda: Deserialize(
                [
                    {
                        "function_list": [
                            {
                                "name": "Name",
                                "raw_return_type": "int1",
                                "simple_return_type": "int2",
                                "var_names": [None, "b"],
                                "raw_var_types": ["c", "d"],
                                "simple_var_types": ["e", "f"],
                            },
                        ],
                    },
                ],
            ),
        )

        self.assertRaisesRegex(
            Exception,
            "'' is not a valid 'String' string - Value must have at least 1 character",
            lambda: Deserialize(
                [
                    {
                        "function_list": [
                            {
                                "name": "Name",
                                "raw_return_type": "int1",
                                "simple_return_type": "int2",
                                "var_names": ["", "b"],
                                "raw_var_types": ["c", "d"],
                                "simple_var_types": ["e", "f"],
                            },
                        ],
                    },
                ],
            ),
        )

    # ----------------------------------------------------------------------
    def test_InvalidRawVarType(self):
        self.assertRaisesRegex(
            Exception,
            "expected string or bytes-like object",                         # TODO
            lambda: Deserialize(
                [
                    {
                        "function_list": [
                            {
                                "name": "Name",
                                "raw_return_type": "int1",
                                "simple_return_type": "int2",
                                "var_names": ["a", "b"],
                                "raw_var_types": ["c", None],
                                "simple_var_types": ["e", "f"],
                            },
                        ],
                    },
                ],
            ),
        )

        self.assertRaisesRegex(
            Exception,
            "'' is not a valid 'String' string - Value must have at least 1 character",
            lambda: Deserialize(
                [
                    {
                        "function_list": [
                            {
                                "name": "Name",
                                "raw_return_type": "int1",
                                "simple_return_type": "int2",
                                "var_names": ["a", "b"],
                                "raw_var_types": ["c", ""],
                                "simple_var_types": ["e", "f"],
                            },
                        ],
                    },
                ],
            ),
        )

    # ----------------------------------------------------------------------
    def test_InvalidSimpleVarType(self):
        self.assertRaisesRegex(
            Exception,
            "expected string or bytes-like object",                         # TODO
            lambda: Deserialize(
                [
                    {
                        "function_list": [
                            {
                                "name": "Name",
                                "raw_return_type": "int1",
                                "simple_return_type": "int2",
                                "var_names": ["a", "b"],
                                "raw_var_types": ["c", "d"],
                                "simple_var_types": ["e", None, "g"],
                            },
                        ],
                    },
                ],
            ),
        )

        self.assertRaisesRegex(
            Exception,
            "'' is not a valid 'String' string - Value must have at least 1 character",
            lambda: Deserialize(
                [
                    {
                        "function_list": [
                            {
                                "name": "Name",
                                "raw_return_type": "int1",
                                "simple_return_type": "int2",
                                "var_names": ["", "b"],
                                "raw_var_types": ["c", "d"],
                                "simple_var_types": ["e", "", "g"],
                            },
                        ],
                    },
                ],
            ),
        )

    # ----------------------------------------------------------------------
    def test_InvalidDeclarationLine(self):
        self.assertRaisesRegex(
            Exception,
            "0 is not >= 1",
            lambda: Deserialize(
                [
                    {
                        "function_list": [
                            {
                                "name": "Name",
                                "raw_return_type": "int1",
                                "simple_return_type": "int1",
                                "declaration_line": 0,
                            },
                        ],
                    },
                ],
            ),
        )
        self.assertRaisesRegex(
            Exception,
            "'String' is not a valid 'Integer' string - Value must be >= 1",
            lambda: Deserialize(
                [
                    {
                        "function_list": [
                            {
                                "name": "Name",
                                "raw_return_type": "int1",
                                "simple_return_type": "int1",
                                "declaration_line": "String",
                            },
                        ],
                    },
                ],
            ),
        )

    # ----------------------------------------------------------------------
    def test_InvalidDefinitionLine(self):
        self.assertRaisesRegex(
            Exception,
            "0 is not >= 1",
            lambda: Deserialize(
                [
                    {
                        "function_list": [
                            {
                                "name": "Name",
                                "raw_return_type": "int1",
                                "simple_return_type": "int1",
                                "definition_line": 0,
                            },
                        ],
                    },
                ],
            ),
        )
        self.assertRaisesRegex(
            Exception,
            "'String' is not a valid 'Integer' string - Value must be >= 1",
            lambda: Deserialize(
                [
                    {
                        "function_list": [
                            {
                                "name": "Name",
                                "raw_return_type": "int1",
                                "simple_return_type": "int1",
                                "definition_line": "String",
                            },
                        ],
                    },
                ],
            ),
        )

    # ----------------------------------------------------------------------
    def test_InvalidNameStruct(self):
        self.assertRaisesRegex(
            Exception,
            "An item was expected",
            lambda: Deserialize(
                [
                    {
                        "struct_list": [{
                            "name": None,
                            "var_names": ["a", "b"],
                            "raw_var_types": ["c", "d"],
                            "simple_var_types": ["e", "f"],
                            "definition_line": 7,
                        }],
                    },
                ],
            ),
        )

        self.assertRaisesRegex(
            Exception,
            "'' is not a valid 'String' string - Value must have at least 1 character",
            lambda: Deserialize(
                [
                    {
                        "struct_list": [{
                            "name": "",
                            "var_names": ["a", "b"],
                            "raw_var_types": ["c", "d"],
                            "simple_var_types": ["e", "f"],
                            "definition_line": 7,
                        }],
                    },
                ],
            ),
        )

    # ----------------------------------------------------------------------
    def test_InvalidVarNameStruct(self):
        self.assertRaisesRegex(
            Exception,
            "expected string or bytes-like object",
            lambda: Deserialize(
                [
                    {
                        "struct_list": [{
                            "name": "name",
                            "var_names": [None, "b"],
                            "raw_var_types": ["c", "d"],
                            "simple_var_types": ["e", "f"],
                            "definition_line": 7,
                        }],
                    },
                ],
            ),
        )

        self.assertRaisesRegex(
            Exception,
            "'' is not a valid 'String' string - Value must have at least 1 character",
            lambda: Deserialize(
                [
                    {
                        "struct_list": [{
                            "name": "name",
                            "var_names": ["", "b"],
                            "raw_var_types": ["c", "d"],
                            "simple_var_types": ["e", "f"],
                            "definition_line": 7,
                        }],
                    },
                ],
            ),
        )

    # ----------------------------------------------------------------------
    def test_InvalidRawVarTypeStruct(self):
        self.assertRaisesRegex(
            Exception,
            "expected string or bytes-like object",
            lambda: Deserialize(
                [
                    {
                        "struct_list": [{
                            "name": "name",
                            "var_names": ["a", "b"],
                            "raw_var_types": [None, "d"],
                            "simple_var_types": ["e", "f"],
                            "definition_line": 7,
                        }],
                    },
                ],
            ),
        )

        self.assertRaisesRegex(
            Exception,
            "'' is not a valid 'String' string - Value must have at least 1 character",
            lambda: Deserialize(
                [
                    {
                        "struct_list": [{
                            "name": "name",
                            "var_names": ["a", "b"],
                            "raw_var_types": ["", "d"],
                            "simple_var_types": ["e", "f"],
                            "definition_line": 7,
                        }],
                    },
                ],
            ),
        )

    # ----------------------------------------------------------------------
    def test_InvalidSimpleVarTypeStruct(self):
        self.assertRaisesRegex(
            Exception,
            "expected string or bytes-like object",
            lambda: Deserialize(
                [
                    {
                        "struct_list": [{
                            "name": "name",
                            "var_names": ["a", "b"],
                            "raw_var_types": ["c", "d"],
                            "simple_var_types": [None, "f"],
                            "definition_line": 7,
                        }],
                    },
                ],
            ),
        )

        self.assertRaisesRegex(
            Exception,
            "'' is not a valid 'String' string - Value must have at least 1 character",
            lambda: Deserialize(
                [
                    {
                        "struct_list": [{
                            "name": "name",
                            "var_names": ["a", "b"],
                            "raw_var_types": ["c", "d"],
                            "simple_var_types": ["", "f"],
                            "definition_line": 7,
                        }],
                    },
                ],
            ),
        )

    # ----------------------------------------------------------------------
    def test_InvalidDefinitionLineStruct(self):
        self.assertRaisesRegex(
            Exception,
            "0 is not >= 1",
            lambda: Deserialize(
                [
                    {
                        "struct_list": [{
                            "name": "name",
                            "var_names": ["a", "b"],
                            "raw_var_types": ["c", "d"],
                            "simple_var_types": ["e", "f"],
                            "definition_line": 0,
                        }],
                    },
                ],
            ),
        )

        self.assertRaisesRegex(
            Exception,
            "'String' is not a valid 'Integer' string - Value must be >= 1",
            lambda: Deserialize(
                [
                    {
                        "struct_list": [{
                            "name": "name",
                            "var_names": ["a", "b"],
                            "raw_var_types": ["c", "d"],
                            "simple_var_types": ["e", "f"],
                            "definition_line": "String",
                        }],
                    },
                ],
            ),
        )

    # ----------------------------------------------------------------------
    def test_InvalidBaseStructs(self):
        self.assertRaisesRegex(
            Exception,
            "expected string or bytes-like object",
            lambda: Deserialize(
                [
                    {
                        "struct_list": [{
                            "name": "name",
                            "var_names": ["a", "b"],
                            "raw_var_types": ["c", "d"],
                            "simple_var_types": ["e", "f"],
                            "definition_line": 7,
                            "base_structs": [None, "struct2"],
                        }],
                    },
                ],
            ),
        )

        self.assertRaisesRegex(
            Exception,
            "'' is not a valid 'String' string - Value must have at least 1 character",
            lambda: Deserialize(
                [
                    {
                        "struct_list": [{
                            "name": "name",
                            "var_names": ["a", "b"],
                            "raw_var_types": ["c", "d"],
                            "simple_var_types": ["e", "f"],
                            "definition_line": 7,
                            "base_structs": ["", "struct2"],
                        }],
                    },
                ],
            ),
        )

    # ----------------------------------------------------------------------
    def test_InvalidArgNamesConstructor(self):
        self.assertRaisesRegex(
            Exception,
            "expected string or bytes-like object",
            lambda: Deserialize(
                [
                    {
                        "struct_list": [{
                            "name": "name",
                            "var_names": ["a", "b"],
                            "raw_var_types": ["c", "d"],
                            "simple_var_types": ["e", "f"],
                            "definition_line": 7,
                            "constructor_list": [{
                                "var_names": [None, "cb"],
                                "raw_var_types": ["cc", "cd"],
                                "simple_var_types": ["ce", "cf"],
                                "definition_line": 14,
                            }],
                        }],
                    },
                ],
            ),
        )

        self.assertRaisesRegex(
            Exception,
            "'' is not a valid 'String' string - Value must have at least 1 character",
            lambda: Deserialize(
                [
                    {
                        "struct_list": [{
                            "name": "name",
                            "var_names": ["a", "b"],
                            "raw_var_types": ["c", "d"],
                            "simple_var_types": ["e", "f"],
                            "definition_line": 7,
                            "constructor_list": [{
                                "var_names": ["", "cb"],
                                "raw_var_types": ["cc", "cd"],
                                "simple_var_types": ["ce", "cf"],
                                "definition_line": 14,
                            }],
                        }],
                    },
                ],
            ),
        )

    # ----------------------------------------------------------------------
    def test_InvalidRawArgTypesConstructor(self):
        self.assertRaisesRegex(
            Exception,
            "expected string or bytes-like object",
            lambda: Deserialize(
                [
                    {
                        "struct_list": [{
                            "name": "name",
                            "var_names": ["a", "b"],
                            "raw_var_types": ["c", "d"],
                            "simple_var_types": ["e", "f"],
                            "definition_line": 7,
                            "constructor_list": [{
                                "var_names": ["ca", "cb"],
                                "raw_var_types": [None, "cd"],
                                "simple_var_types": ["ce", "cf"],
                                "definition_line": 14,
                            }],
                        }],
                    },
                ],
            ),
        )

        self.assertRaisesRegex(
            Exception,
            "'' is not a valid 'String' string - Value must have at least 1 character",
            lambda: Deserialize(
                [
                    {
                        "struct_list": [{
                            "name": "name",
                            "var_names": ["a", "b"],
                            "raw_var_types": ["c", "d"],
                            "simple_var_types": ["e", "f"],
                            "definition_line": 7,
                            "constructor_list": [{
                                "var_names": ["ca", "cb"],
                                "raw_var_types": ["", "cd"],
                                "simple_var_types": ["ce", "cf"],
                                "definition_line": 14,
                            }],
                        }],
                    },
                ],
            ),
        )

    # ----------------------------------------------------------------------
    def test_InvalidSimpleArgTypesConstructor(self):
        self.assertRaisesRegex(
            Exception,
            "expected string or bytes-like object",
            lambda: Deserialize(
                [
                    {
                        "struct_list": [{
                            "name": "name",
                            "var_names": ["a", "b"],
                            "raw_var_types": ["c", "d"],
                            "simple_var_types": ["e", "f"],
                            "definition_line": 7,
                            "constructor_list": [{
                                "var_names": ["ca", "cb"],
                                "raw_var_types": ["cc", "cd"],
                                "simple_var_types": [None, "cf"],
                                "definition_line": 14,
                            }],
                        }],
                    },
                ],
            ),
        )

        self.assertRaisesRegex(
            Exception,
            "'' is not a valid 'String' string - Value must have at least 1 character",
            lambda: Deserialize(
                [
                    {
                        "struct_list": [{
                            "name": "name",
                            "var_names": ["a", "b"],
                            "raw_var_types": ["c", "d"],
                            "simple_var_types": ["e", "f"],
                            "definition_line": 7,
                            "constructor_list": [{
                                "var_names": ["ca", "cb"],
                                "raw_var_types": ["cc", "cd"],
                                "simple_var_types": ["", "cf"],
                                "definition_line": 14,
                            }],
                        }],
                    },
                ],
            ),
        )

    # ----------------------------------------------------------------------
    def test_InvalidDefinitionLineConstructor(self):
        self.assertRaisesRegex(
            Exception,
            "0 is not >= 1",
            lambda: Deserialize(
                [
                    {
                        "struct_list": [{
                            "name": "name",
                            "var_names": ["a", "b"],
                            "raw_var_types": ["c", "d"],
                            "simple_var_types": ["e", "f"],
                            "definition_line": 0,
                            "constructor_list": [{
                                "var_names": ["ca", "cb"],
                                "raw_var_types": ["cc", "cd"],
                                "simple_var_types": ["ce", "cf"],
                                "definition_line": 0,
                            }],
                        }],
                    },
                ],
            ),
        )

        self.assertRaisesRegex(
            Exception,
            "'String' is not a valid 'Integer' string - Value must be >= 1",
            lambda: Deserialize(
                [
                    {
                        "struct_list": [{
                            "name": "name",
                            "var_names": ["a", "b"],
                            "raw_var_types": ["c", "d"],
                            "simple_var_types": ["e", "f"],
                            "definition_line": "String",
                            "constructor_list": [{
                                "var_names": ["ca", "cb"],
                                "raw_var_types": ["cc", "cd"],
                                "simple_var_types": ["ce", "cf"],
                                "definition_line": "String",
                            }],
                        }],
                    },
                ],
            ),
        )

    # ----------------------------------------------------------------------
    def test_InvalidIncludeList(self):
        self.assertRaisesRegex(
            Exception,
            "expected string or bytes-like object",
            lambda: Deserialize([{"include_list": [None, "vector"]}]),
        )

        self.assertRaisesRegex(
            Exception,
            "'' is not a valid 'String' string - Value must have at least 1 character",
            lambda: Deserialize([{"include_list": ["", "vector"]}]),
        )

    # ----------------------------------------------------------------------
    def test_ProcessAdditionalData(self):
        input = [
            {
                "name": "Name",
                "raw_return_type": "int1",
                "simple_return_type": "int2",
                "another_value": {"hello": "world"},
                "another_value2": "a string",
                "optional_list": [1, 2, 3],
            },
        ]

        result = Deserialize(input)

        self.assertEqual(len(result), 1)
        self.assertTrue(not hasattr(result[0], "another_value"))

        result = Deserialize(
            input,
            process_additional_data=True,
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].another_value.hello, "world")
        self.assertEqual(result[0].another_value2, "a string")
        self.assertEqual(result[0].optional_list, [1, 2, 3])


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        sys.exit(
            unittest.main(
                verbosity=2,
            ),
        )
    except KeyboardInterrupt:
        pass
