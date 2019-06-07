import os
import re
import clang.cindex as cindex
import CommonEnvironment.FileSystem as fileSystem
import CommonEnvironment.CallOnExit as callOnExit
import CommonEnvironment.Shell as CE_Shell

def ObtainFunctions(input_filename):
    '''
        This function will extract return value, name and parameters for every
        function given. input_filename can be a file name or a string that is the code
        itself.
        Return value:
            Returns a list of functions, every item in this list is a dictionary that 
            has information about the function.
    '''
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

    with callOnExit.CallOnExit(DeleteFile):
        funcs_list = []

        pattern_const = re.compile("^const ")
        pattern_star  = re.compile(r"( \*)*\**")
        pattern_amper = re.compile("( &)*&*") 

        # ----------------------------------------------------------------------
        def SimpleVarType(name):
            name = re.sub(pattern_const,  "", name)
            name = re.sub(pattern_star,  "", name)
            name = re.sub(pattern_amper,  "", name) 
            return name

        # ----------------------------------------------------------------------

        index = cindex.Index.create()
        args = []
        
        if os.name == 'posix':
            args = ['-I{}'.format(v) for v in os.environ['INCLUDE'].split(":") if v.strip()]

        translation_unit = index.parse(input_filename, args=args)
        cursor = translation_unit.cursor

        # ----------------------------------------------------------------------
        def Enumerate(node):
            if node.kind == cindex.CursorKind.NAMESPACE:
                for child in node.get_children():
                    Enumerate(child)

            if node.kind == cindex.CursorKind.FUNCTION_DECL and node.location.file.name == input_filename:
                func = {}
                func["func_name"] = node.spelling
                func["raw_return_type"] = node.result_type.spelling
                func["simple_return_type"] = SimpleVarType(node.result_type.spelling)
                func["var_names"] = []
                func["raw_var_types"] = []
                func["simple_var_types"] = []
                for arg in node.get_arguments():
                    func["var_names"].append(arg.displayname)
                    func["raw_var_types"].append(arg.type.spelling)
                    func["simple_var_types"].append(SimpleVarType(arg.type.spelling))
                funcs_list.append(func)

        # ----------------------------------------------------------------------
        for child in cursor.get_children():
            Enumerate(child)

        return funcs_list
    # ----------------------------------------------------------------------
