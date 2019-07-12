import os
import re
import textwrap

from collections import OrderedDict

import clang.cindex as cindex

import CommonEnvironment
import CommonEnvironment.FileSystem as fileSystem
import CommonEnvironment.CallOnExit as callOnExit
from CommonEnvironment.Shell.All import CurrentShell
import CommonEnvironment.Shell as CE_Shell

from DataPipelines.CppToJson.Impl.ClassLikeObject import ClassLikeObject
from DataPipelines.CppToJson.Impl.Constructor import Constructor
from DataPipelines.CppToJson.Impl.Function import Function

# ----------------------------------------------------------------------
def ObtainFunctions(
    input_filename,
    on_unsupported,
    policy,
):
    """
    This function will extract return value, name and parameters for every
    function given. input_filename can be a file name or a string that is the code
    itself.
    Return value:
        Returns a list of functions, every item in this list is a dictionary that
        has information about the function.
    """

    is_temp_file = False
    # Since clang can only parse from a file, if we are given a string we need to create
    #   a new temp file and put the string inside.
    if not fileSystem.IsFilename(input_filename):
        is_temp_file = True
        file_content = input_filename
        input_filename = CE_Shell.Shell.CreateTempFilename(suffix=".cpp")
        with open(input_filename, "w") as file_pointer:
            file_pointer.write(file_content)

    # ----------------------------------------------------------------------
    def DeleteFile():
        if is_temp_file:
            os.remove(input_filename)

    # ----------------------------------------------------------------------
    pattern_words = re.compile(r"[\w']+")
    def TestAndVerify(types):
        """
        This is an early version of TestAndVerify that checks if a type should be accepted or not.
        It will find all words in the type and check them against a policy. This will be adapted as we
        get more information about what is supported and what is not.
        """

        type_list = re.findall(pattern_words, types)

        for var_type in type_list:
            if not policy(var_type):
                return False
        return True
    # ----------------------------------------------------------------------

    with callOnExit.CallOnExit(DeleteFile):
        index = cindex.Index.create()
        args = []

        # On Windows, clang recognizes the INCLUDE and LIB environment variables, but
        # on Linux it does not. Recognize the INCLUDE var on Linux.
        if CurrentShell.CategoryName == "Linux":
            include_vars = [value for value in os.getenv("INCLUDE").split(":") if value.strip()]

            # In the past, we used the GCC repository which would prepopulate the INCLUDE environment
            # variable with standard includes. However, that repo had issues when attempting to link
            # compile binaries and has been temporarily disabled. Unfortunately, this code needs that
            # populated environment variable to function correctly in order to tokenize input.
            #
            # For now, add those includes here. When Clang's dependency on GCC is restored in the future,
            # we can remove this explicit step.
            include_vars.append("/usr/lib/gcc/x86_64-linux-gnu/7/include")

            args = ['-I{}'.format(include_var) for include_var in include_vars]

        pattern_const = re.compile(
            textwrap.dedent(
                r"""(?#
                Not a letter)(?<!\w)(?#
                Keyword)(?P<keyword>const)(?#
                Not a letter)(?!\w)(?#
                )"""
            )
        )
        # TODO: Dont support pointers (that use the '*' notation).
        pattern_star  = re.compile(r"\**(\* )*")
        pattern_amper = re.compile("&*(& )*")

        # ----------------------------------------------------------------------
        def SimpleVarType(name):
            """
            Remove 'const', '*' and '&'
            """
            # TODO: Dont support pointers (that use the '*' notation).
            name = re.sub(pattern_const,  "", name)
            name = re.sub(pattern_star,  "", name)
            name = re.sub(pattern_amper,  "", name)
            return name.strip()

        # ----------------------------------------------------------------------
        def ParseFile(filename):
            """
            Clang opens all files that are included in 'filename' at the same time. Only the functions on
            'filename' are processed, but all class-like objects are processed, because one of the functions
            in 'filename' might need to use it. The ones that are not in 'filename' and are not used are not
            exported.
            """

            translation_unit = index.parse(filename, args=args + ['-std=c++17'])

            diagnostics = list(translation_unit.diagnostics)
            if diagnostics:
                raise Exception("\n".join([str(diag) for diag in diagnostics]))

            cursor = translation_unit.cursor

            # ----------------------------------------------------------------------
            def GetAlias():
                """
                This function will process all 'typedef' and 'using' and it will map the underlying type to
                its definition.
                """
                alias = {}
                for child in cursor.get_children():
                    if (child.kind == cindex.CursorKind.TYPEDEF_DECL or child.kind == cindex.CursorKind.TYPE_ALIAS_DECL) and child.location.file.name == input_filename:
                        alias[child.spelling] = child.underlying_typedef_type.spelling
                return alias

            # ----------------------------------------------------------------------

            alias = GetAlias()

            alias_regex = re.compile(
                textwrap.dedent(
                    r"""(?#
                    Not a letter)(?<!\w)(?#
                    Keyword)(?P<keyword>{})(?#
                    Not a letter)(?!\w)(?#
                    )"""
                ).format("|".join([re.escape(key) for key in alias.keys()]))
            )

            struct_class_pattern = re.compile(
                textwrap.dedent(
                    r"""(?#
                    Not a letter)(?<!\w)(?#
                    Keyword with a space)(?P<keyword>struct\s|class\s)(?#
                    )"""
                )
            )

            # ----------------------------------------------------------------------
            def FullVarType(types):
                """
                This will undo all 'typedef' and 'using' by looking for the items in the 'alias' dict and substituting
                the corresponding definitions. It will also remove all occurences of the words 'struct' and 'class'.
                """
                num_subs = True
                while num_subs and alias:
                    types, num_subs = re.subn(alias_regex, lambda k: alias[k.group(1)], types)

                types = struct_class_pattern.sub(r'', types)
                return types

            # ----------------------------------------------------------------------

            object_type_list = []
            function_dict = {}

            # ----------------------------------------------------------------------
            def EnumerateObjType(node):
                if node.kind == cindex.CursorKind.NAMESPACE:
                    for child in node.get_children():
                        EnumerateObjType(child)

                if node.kind == cindex.CursorKind.STRUCT_DECL or node.kind == cindex.CursorKind.CLASS_DECL:
                    obj_type = _GetObjectType(node, SimpleVarType, FullVarType)

                    if obj_type:
                        object_type_list.append(obj_type)

            # ----------------------------------------------------------------------
            def EnumerateFuncs(node):
                if node.kind == cindex.CursorKind.NAMESPACE:
                    for child in node.get_children():
                        EnumerateFuncs(child)

                if node.kind == cindex.CursorKind.FUNCTION_DECL and node.location.file.name == filename:
                    ret_type = FullVarType(node.result_type.spelling)

                    arg_list = []
                    for arg in node.get_arguments():
                        arg_type = FullVarType(arg.type.spelling)
                        arg_list.append(arg_type)

                    # There is the need for arg_list to be a tuple here, because this will be the key
                    # to the dictionary of functions, and tuple are hashable unlike lists.
                    func_key = (_FullName(node), ret_type, tuple(arg_list))

                    is_def = False
                    for child in node.get_children():
                        if child.kind == cindex.CursorKind.COMPOUND_STMT:
                            is_def = True

                    if func_key not in function_dict.keys():
                        variable_info = []
                        for arg in node.get_arguments():
                            arg_type = FullVarType(arg.type.spelling)
                            variable_info.append((arg.displayname, arg_type, SimpleVarType(arg_type)))

                        # Create the instance of the function
                        function_dict[func_key] = Function(_FullName(node), ret_type, SimpleVarType(ret_type), variable_info, node.location.line)

                    if is_def:
                        function_dict[func_key].definition_line = node.location.line

            # ----------------------------------------------------------------------

            # EnumerateObjType needs to be separated from EnumerateFuncs because of constructors that might be out
            # of the function.
            for child in cursor.get_children():
                EnumerateObjType(child)

            for child in cursor.get_children():
                EnumerateFuncs(child)

            # ----------------------------------------------------------------------
            def GetIncludeList(filename):
                include_list = []
                for child in translation_unit.get_includes():
                    include_list.append((os.path.realpath(str(child.location.file.name)) if (not is_temp_file or child.location.file.name != input_filename) else None, os.path.realpath(os.path.join(filename, str(child.include)))))
                return include_list

            # ----------------------------------------------------------------------

            include_list = GetIncludeList(filename)

            function_list = [func for func in function_dict.values()]
            return {"function_list": function_list, "object_type_list": object_type_list, "include_list": include_list}

        clean_results = OrderedDict()

        # ----------------------------------------------------------------------
        def InitializeCleanResults(filename, raw_includes):
            clean_results[filename] = Results()
            for include_tuple in raw_includes:
                name, include = include_tuple
                if name == filename:
                    clean_results[filename].include_list.append(include)

        # ----------------------------------------------------------------------

        filename = os.path.realpath(input_filename)
        these_results = ParseFile(filename)

        # If the original file was a temp file, make the key None rather than
        # the name of the temporary file used.
        if not clean_results and is_temp_file:
            filename = None

        if not clean_results:
            InitializeCleanResults(filename, these_results["include_list"])

        needed_obj_type_list = []
        invalid_obj_type_list = []

        # ----------------------------------------------------------------------
        def GetObjType(obj_type_name):
            """
            Get ObjType from its name.
            """
            for obj_type in these_results["object_type_list"]:
                if obj_type.Name == obj_type_name:
                    return obj_type
            return None

        # ----------------------------------------------------------------------
        def VerifyObjType(obj_type):
            """
            Check all var types in this ObjType, this ObjType is valid if they are all valid. There is an assumption that
            this function will only be called for an ObjType that is required. If this ObjType depends on another ObjType,
            that means that the other ObjType is also required.
            """
            if obj_type is None or obj_type in invalid_obj_type_list:
                return False
            if obj_type in needed_obj_type_list:
                return True
            invalid_reasons = []
            for var_type, var_name in zip(obj_type.EnumerateSimpleVarTypes(), obj_type.EnumerateVarNames()):
                if GetObjType(var_type) != obj_type and not VerifyObjType(GetObjType(var_type)) and not TestAndVerify(var_type):
                    invalid_reasons.append("\t- Invalid var {} of type {}.".format(var_name, var_type))

            for constructor in obj_type.constructor_list:
                for arg_type in constructor.EnumerateSimpleVarTypes():
                    if GetObjType(arg_type) != obj_type and not VerifyObjType(GetObjType(arg_type)) and not TestAndVerify(arg_type):
                        invalid_reasons.append("\t- Invalid type {} on constructor argument.".format(arg_type))

            for parent_struct in obj_type.base_structs:
                if not VerifyObjType(GetObjType(parent_struct)):
                    invalid_reasons.append("\t- Invalid base struct {}".format(parent_struct))

            if not obj_type.has_move_constructor:
                invalid_reasons.append("\t- Struct doesn't have a move constructor.")
            if obj_type.has_copy_constructor:
                invalid_reasons.append("\t- Struct has a copy constructor.")
            if obj_type.has_private:
                invalid_reasons.append("\t- Struct has a private variable or inherits from a private struct.")
            if obj_type.has_other:
                invalid_reasons.append("\t- Struct has an unsupported definition.")

            if invalid_reasons:
                on_unsupported(textwrap.dedent(
                    """\
                        The struct {} is not supported:
                        {}
                    """
                ).format(obj_type.Name, "\n".join(invalid_reasons)),
                obj_type.Filename if (not is_temp_file or obj_type.Filename != input_filename) else None,
                obj_type.DefinitionLine
                )
                invalid_obj_type_list.append(obj_type)
                return False
            needed_obj_type_list.append(obj_type)
            return True

        # ----------------------------------------------------------------------
        def VerifyFunction(func, filename):
            """
            A function is valid if all var types are valid.
            """
            invalid_reasons = []
            for var_type, var_name in zip(func.EnumerateSimpleVarTypes(), func.EnumerateVarNames()):
                if not TestAndVerify(var_type):
                    invalid_reasons.append("\t- Invalid argument {} of type {}.".format(var_name, var_type))

            return_type = func.SimpleReturnType
            if not VerifyObjType(GetObjType(return_type)) and not TestAndVerify(return_type):
                invalid_reasons.append("\t- Invalid return type {}.".format(return_type))

            if invalid_reasons:
                on_unsupported(textwrap.dedent(
                    """\
                        The function {} is not supported:
                        {}
                    """
                ).format(func.Name, "\n".join(invalid_reasons)),
                filename if (not is_temp_file or filename != input_filename) else None,
                func.definition_line
                )
                return False
            return True

        # ----------------------------------------------------------------------

        for func in these_results["function_list"]:
            if VerifyFunction(func, filename):
                clean_results[filename].function_list.append(func.ToDict())

        # Add required ObjType to the clean_results list.
        for object_type in needed_obj_type_list:
            this_file_name = object_type.Filename

            if is_temp_file:
                this_file_name = None
            if this_file_name not in clean_results:
                InitializeCleanResults(this_file_name, these_results["include_list"])
            clean_results[this_file_name].object_type_list.append(object_type.ToDict())

        return dict([(filename, result.ToDict()) for  filename, result in clean_results.items()])

# ----------------------------------------------------------------------
# |
# |  Private Types
# |
# ----------------------------------------------------------------------
class Results(object):
    """Stores final versions of Includes, Functions and Class-like objects"""

    # ----------------------------------------------------------------------
    def __init__(
        self,
        function_list=None,
        object_type_list=None,
        include_list=None,
    ):
        self.function_list                 = function_list or []
        self.object_type_list              = object_type_list or []
        self.include_list                  = include_list or []

    # ----------------------------------------------------------------------
    def ToDict(self):
        new_dict = {}

        new_dict["function_list"] = self.function_list
        new_dict["struct_list"] = self.object_type_list
        new_dict["include_list"] = self.include_list

        return new_dict


# ----------------------------------------------------------------------
# |
# |  Private Methods
# |
# ----------------------------------------------------------------------
def _FullName(node):
    """
    This function will make the name of the function complete to include its namespace.
    """
    name = node.spelling
    parent = node.semantic_parent
    while parent.kind != cindex.CursorKind.TRANSLATION_UNIT:
        name = parent.spelling + "::" + name
        parent = parent.semantic_parent
    return name

# ----------------------------------------------------------------------

def _GetObjectType(node, SimpleVarType, FullVarType):
    """
    This function will return the Object Type that this node refers to. It will return None if there were
    errors.
    """
    struct_class_pattern = re.compile(
        textwrap.dedent(
            r"""(?#
            Not a letter)(?<!\w)(?#
            Keyword with a space)(?P<keyword>struct\s|class\s)(?#
            )"""
        )
    )
    is_def = True
    # There are a few kinds that are supported, even though they are not directly exposed.
    accepted_kinds = [cindex.CursorKind.CXX_ACCESS_SPEC_DECL]

    # ----------------------------------------------------------------------
    def DeleteDefault(node, speficier):
        """
        This function will receive a node and a specifier (default or deleted), and check if the
        node has the specifier in question.
        """
        token_list = []
        for token in node.get_tokens():
            token_list.append(token.spelling)
        return len(token_list) >= 2 and token_list[-1] == speficier and token_list[-2] == '='

    # ----------------------------------------------------------------------

    object_vars = []
    for child in node.get_children():
        if child.kind == cindex.CursorKind.FIELD_DECL:
            var_type = FullVarType(child.type.spelling)
            object_vars.append((child.spelling, var_type, SimpleVarType(var_type)))

    object_type = ClassLikeObject(_FullName(node), node.location.line, os.path.realpath(node.location.file.name), object_vars)

    for child in node.get_children():
        # The way to see if this is a definition or not, is to see if 'node' has any children.
        is_def = False
        if child.kind == cindex.CursorKind.CONSTRUCTOR:
            # If this constructor ends in "=delete", ignore it.
            if DeleteDefault(child, "delete"):
                continue

            constructor_args = []
            for arg in child.get_arguments():
                arg_type = FullVarType(arg.type.spelling)
                constructor_args.append((arg.spelling, arg_type, SimpleVarType(arg_type)))

            constructor = Constructor(child.location.line, constructor_args)

            object_type.constructor_list.append(constructor)

            if child.is_move_constructor() and child.access_specifier == cindex.AccessSpecifier.PUBLIC:
                object_type.has_move_constructor = True
                if DeleteDefault(child, "default"):
                    # If this is a default move constructor, there wont be a variable name for the
                    # argument in the function, so I create one when I return the dictionary representation.
                    assert len(constructor.VariableInfo) == 1

            elif child.is_copy_constructor() and child.access_specifier == cindex.AccessSpecifier.PUBLIC:
                # No public copy constructors are allowed.
                object_type.has_copy_constructor = True

        elif child.kind == cindex.CursorKind.FIELD_DECL:
            if child.access_specifier != cindex.AccessSpecifier.PUBLIC:
                object_type.has_private = True

        elif child.kind == cindex.CursorKind.CXX_METHOD:
            # If this method ends in "=delete", ignore it.
            if DeleteDefault(child, "delete"):
                continue

            # 'operator=' is supported as long as it is public and a move operator.
            move_operator_arg_type = FullVarType(node.spelling) + " &&"
            if child.spelling == "operator=" and child.access_specifier == cindex.AccessSpecifier.PUBLIC:
                for arg in child.get_arguments():
                    # Check the arguments to verify that this is a move operator.
                    if FullVarType(arg.type.spelling) != move_operator_arg_type:
                        object_type.has_other = True
            else:
                # No other functions besides move operators are allowed.
                object_type.has_other = True

        elif child.kind == cindex.CursorKind.CXX_BASE_SPECIFIER:
            if child.access_specifier != cindex.AccessSpecifier.PUBLIC:
                object_type.has_private = True
            struct_name = child.spelling
            struct_name = struct_class_pattern.sub(r'', struct_name)

            object_type.base_structs.append(struct_name.strip())

        elif child.kind not in accepted_kinds:
            object_type.has_other = True

    if not is_def:
        return object_type

    return None
