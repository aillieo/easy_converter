#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import os

from enum import Enum
from openpyxl import load_workbook


class TokenType(Enum):
    PrimitiveType = 1 << 0
    BeginList = 1 << 1
    VariableName = 1 << 2
    ClosingBracket = 1 << 3
    BeginDictionary = 1 << 4
    BeginStruct = 1 << 5
    BeginEnum = 1 << 6
    Number = 1 << 7
    Comma = 1 << 8


class Token:
    primitive_types = ['int', 'long', 'string', 'float', 'bool']
    value_to_token_types = {
        'List<': TokenType.BeginList,
        'Map<': TokenType.BeginDictionary,
        'Struct<': TokenType.BeginStruct,
        'Enum<': TokenType.BeginEnum,
        '>': TokenType.ClosingBracket,
        ',': TokenType.Comma,
    }
    re_variable_name = re.compile(r"^\w+\d*$")

    def __init__(self, value):
        self.value = value
        self.token_type = None
        if value in self.primitive_types:
            self.token_type = TokenType.PrimitiveType
            return
        self.token_type = self.value_to_token_types.get(value)
        if self.token_type is not None:
            return
        if str.isdigit(value):
            self.token_type = TokenType.Number
            return
        if self.re_variable_name.match(value):
            self.token_type = TokenType.VariableName
            return
        raise Exception(value)


class FieldParser:
    re_token = re.compile(r'[\d\w]+<?|[>,]')

    def __init__(self, table_name, field_name, field_def):
        self.table_name = table_name
        self.field_name = field_name
        self.field_def = field_def
        self.tokens = self.tokenize()
        self.cursor = 0
        self.field_info = self.parse_field_info(self.field_name)
        if self.cursor != len(self.tokens):
            raise Exception("")

    def tokenize(self):
        print(self.field_def)
        return [Token(t) for t in self.re_token.findall(self.field_def)]

    def parse_field_info(self, field_name):
        if self.cursor >= len(self.tokens):
            raise Exception("")
        token = self.tokens[self.cursor]
        if token.token_type == TokenType.PrimitiveType:
            return self.parse_primitive(field_name)
        elif token.token_type == TokenType.BeginList:
            return self.parse_list(field_name)
        elif token.token_type == TokenType.BeginDictionary:
            return self.parse_dictionary(field_name)
        elif token.token_type == TokenType.BeginStruct:
            return self.parse_struct(field_name)
        elif token.token_type == TokenType.BeginEnum:
            return self.parse_enum(field_name)
        raise Exception(token.token_type)

    def parse_primitive(self, field_name):
        token = self.tokens[self.cursor]
        self.cursor += 1
        return FieldPrimitive(field_name, token.value)

    def parse_list(self, field_name):
        self.cursor += 1
        element_type = self.parse_field_info('')
        token = self.tokens[self.cursor]
        assert token.token_type == TokenType.ClosingBracket
        self.cursor += 1
        return FieldList(field_name, element_type)

    def parse_dictionary(self, field_name):
        self.cursor += 1
        key_type = self.parse_field_info('')
        token = self.tokens[self.cursor]
        assert token.token_type == TokenType.Comma
        self.cursor += 1
        value_type = self.parse_field_info('')
        token = self.tokens[self.cursor]
        assert token.token_type == TokenType.ClosingBracket
        self.cursor += 1
        return FieldDictionary(field_name, key_type, value_type)

    def parse_struct(self, field_name):
        self.cursor += 1
        struct_fields = []
        while True:
            field_info = self.parse_field_info('')
            struct_fields.append(field_info)
            token = self.tokens[self.cursor]
            assert token.token_type == TokenType.Comma
            self.cursor += 1
            token = self.tokens[self.cursor]
            assert token.token_type == TokenType.VariableName
            field_info.field_name = token.value
            self.cursor += 1
            token = self.tokens[self.cursor]
            if token.token_type == TokenType.ClosingBracket:
                break
            assert token.token_type == TokenType.Comma
            self.cursor += 1

        token = self.tokens[self.cursor]
        assert token.token_type == TokenType.ClosingBracket
        self.cursor += 1
        return FieldStruct(self.table_name, field_name, struct_fields)

    def parse_enum(self, field_name):
        self.cursor += 1
        enum_values = []
        while True:
            token = self.tokens[self.cursor]
            assert token.token_type == TokenType.VariableName
            enum_name = token.value
            self.cursor += 1
            token = self.tokens[self.cursor]
            assert token.token_type == TokenType.Comma
            self.cursor += 1
            token = self.tokens[self.cursor]
            assert token.token_type == TokenType.Number
            enum_value = token.value
            enum_values.append({"enum_name": enum_name, "enum_value": enum_value})
            self.cursor += 1
            token = self.tokens[self.cursor]
            if token.token_type == TokenType.ClosingBracket:
                break
            assert token.token_type == TokenType.Comma
            self.cursor += 1

        token = self.tokens[self.cursor]
        assert token.token_type == TokenType.ClosingBracket
        self.cursor += 1
        return FieldEnum(self.table_name, field_name, enum_values)

    def get_field_info(self):
        return self.field_info


class Field:
    def __init__(self, field_name, field_def):
        self.field_name = field_name
        self.field_def = field_def


class FieldPrimitive(Field):
    def __init__(self, field_name, field_type):
        super().__init__(field_name, field_type)


class FieldList(Field):
    def __init__(self, field_name, element_type):
        super().__init__(field_name, '')
        self.list_element_type = element_type


class FieldDictionary(Field):
    def __init__(self, field_name, key_type, value_type):
        super().__init__(field_name, '')
        self.dict_key_type = key_type
        self.dict_value_type = value_type


class FieldStruct(Field):
    def __init__(self, table_name, field_name, struct_fields):
        field_def = field_name.capitalize()
        if field_def == field_name:
            field_def = 'S' + field_name
        super().__init__(field_name, field_def)
        self.struct_fields = struct_fields


class FieldEnum(Field):
    def __init__(self, table_name, field_name, enum_values):
        field_def = field_name.capitalize()
        if field_def == field_name:
            field_def = 'E' + field_name
        super().__init__(field_name, field_def)
        self.enum_values = enum_values


class Scheme:

    def __init__(self, name, fields):
        self.full_name = name
        self.name = name
        self.fields = fields

    def get_associated_structs(self):
        return [x for x in self.fields if isinstance(x, FieldStruct)]

    def get_associated_enums(self):
        return [x for x in self.fields if isinstance(x, FieldEnum)]


class Table:
    special_str = {
        '\n': ';l/~',
        '\\,': ':l/~',
    }

    def __init__(self, sheet):

        table_name = sheet.title

        data = []
        self.scheme = None

        field_names, field_defs = None, None

        for row in sheet.iter_rows(values_only=True):

            if len(row) == 0:
                continue
            if row[0] is None:
                continue
            if self.scheme is None:
                if field_names is None:
                    field_names = self.try_read_field_names(row)
                    continue
                if field_defs is None:
                    field_defs = self.try_read_field_defs(row)
                    continue
                pairs = zip(field_names, field_defs)
                fields = [FieldParser(table_name, field_name, field_def).get_field_info()
                          for field_name, field_def in pairs]

                self.scheme = Scheme(table_name, fields)

            self.append_row(data, row)

        if self.scheme is None:
            raise Exception("invalid sheet file" + sheet.title)
        if len(data) > 0:
            self.data = data

    def try_read_field_names(self, row):
        return [str(x) for x in row if x is not None and x != '']

    def try_read_field_defs(self, row):
        return [str(x) for x in row if x is not None and x != '']

    def to_safe_str(self, raw_str):
        if raw_str is None:
            return ''
        new_str = str(raw_str)
        for old, new in self.special_str.items():
            new_str = new_str.replace(old, new)
        return new_str

    def append_row(self, data, row):
        row_data = []
        count = len(self.scheme.fields)
        for index, cell in enumerate(row):
            if index < count:
                self.append_cell(row_data, cell, self.scheme.fields[index])
        data.append(row_data)

    def append_cell(self, row, cell, field):
        if isinstance(field, FieldPrimitive):
            row.append(self.to_safe_str(cell))
        elif isinstance(field, FieldList):
            # row.append(str(str.count(cell, ',') + 1))
            row.append(self.to_safe_str(cell))
        elif isinstance(field, FieldDictionary):
            # row.append(str((str.count(cell, ',') + 1) // 2))
            row.append(self.to_safe_str(cell))
        elif isinstance(field, FieldStruct):
            # struct ?
            row.append(self.to_safe_str(cell))
        elif isinstance(field, FieldEnum):
            # enum ?
            row.append(self.to_safe_str(cell))
        else:
            print(field)
            raise Exception('syntax error:' + field.field_def)


class BaseConverter:
    default_template = {

        # 1. namespace text
        'name_space_begin': '',
        'name_space_end': '',

        # 2. Table class:
        # 2.1. Table body codes
        'class_declare': '',
        'class_internal_struct_declare': '',
        'class_internal_enum_declare': '',
        'class_internal_enum_value': '',

        # 2.2. field declaration
        'field_declare': '',

        # 2.3. field constructor for different types
        'field_ctor_primitive': '',
        'field_ctor_list': '',
        'field_ctor_dictionary': '',
        'field_ctor_struct': '',
        'field_ctor_enum': '',

        # 2.4. field tostring method
        'field_to_string': '',
        'field_to_string_sep': '',

        # 3. TableManager class:
        # 3.1. TableManager body codes
        'manager': '',

        # 3.2. dictionary to hold Tables by id
        'class_dict_entry': '',

        # 3.3. Table constructor
        'class_ctor': '',

        # 3.4. get one Table from dictionary
        'class_entry_getter': '',

        # 3.5. calling a Table constructor
        'class_ctor_entry': '',

        # 4. Misc classes
        # 4.1. DataBuffer class
        'buffer': '',
    }

    def __init__(self, *args, **kwargs):
        self.path_source = kwargs.get("source") or '.'
        self.path_out = kwargs.get("out") or './out'
        self.path_out_data = kwargs.get("outdata") or './out_data'
        self.name_space = kwargs.get("namespace") or 'EasyConverter'
        self.file_ext = ""

    def ensure_path(self, path):
        file_dir = os.path.dirname(path)
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)

    def write_config(self, filename, text):
        path = "{0}/{1}".format(self.path_out, filename)
        self.ensure_path(path)

        with open(path, "w") as f:
            f.write(text)

    def write_config_data(self, filename, text):
        path = "{0}/{1}".format(self.path_out_data, filename)
        self.ensure_path(path)
        with open(path, "w") as f:
            f.write(text)

    def find_files(self):
        if self.path_source is None:
            self.path_source = os.getcwd()
        source_files = []
        for root, dirs, files in os.walk(self.path_source):
            source_files.extend([os.path.join(root, f) for f in files if f.endswith('.xlsx') and not f.startswith('_')])
        return source_files

    def create_tables(self):
        source_files = self.find_files()
        tables = []
        for file in source_files:
            wb = load_workbook(filename=file, read_only=True, data_only=True)
            for sheet in wb:
                if not sheet.title.startswith('_'):
                    tables.append(Table(sheet))
        return tables

    def get_type_name(self, field):
        return field.field_def

    def get_primitive_type_name(self, field_def):
        return field_def

    def get_field_reader(self, field_info):
        if isinstance(field_info, FieldStruct):
            return self.get_struct_reader(field_info.field_def)
        elif isinstance(field_info, FieldEnum):
            return self.get_enum_reader(field_info.field_def)
        return self.get_primitive_reader(field_info.field_def)

    def get_primitive_reader(self, type_def):
        return "Read" + type_def.capitalize()

    def get_struct_reader(self, type_def):
        return "new " + type_def + "(buffer);"

    def get_enum_reader(self, type_def):
        return "ReadEnum<" + type_def + '>'

    def get_field_ctor(self, field, index, template):
        field_args = {
            "field_name": field.field_name,
            "field_type": field.field_def,
            "field_type_reader": self.get_field_reader(field),
            "index": index}
        if isinstance(field, FieldList):
            field_args.update({
                "list_element_type": self.get_primitive_type_name(field.list_element_type.field_def),
                "list_element_type_reader": self.get_field_reader(field.list_element_type)})
        if isinstance(field, FieldDictionary):
            field_args.update({
                "dict_key_type": self.get_primitive_type_name(field.dict_key_type.field_def),
                "dict_key_type_reader": self.get_field_reader(field.dict_key_type)})
            field_args.update({
                "dict_value_type": self.get_primitive_type_name(field.dict_value_type.field_def),
                "dict_value_type_reader": self.get_field_reader(field.dict_value_type)})
        if isinstance(field, FieldPrimitive):
            return template["field_ctor_primitive"].format(**field_args)
        elif isinstance(field, FieldList):
            return template["field_ctor_list"].format(**field_args)
        elif isinstance(field, FieldDictionary):
            return template["field_ctor_dictionary"].format(**field_args)
        elif isinstance(field, FieldStruct):
            return template["field_ctor_struct"].format(**field_args)
        elif isinstance(field, FieldEnum):
            return template["field_ctor_enum"].format(**field_args)

        return ""

    def pack_table_data(self, table):
        fields = table.scheme.fields
        for row in table.data:
            for index, cell in enumerate(row):
                field = fields[index]
                if isinstance(field, FieldList):
                    prefix = str(str.count(cell, ',') + 1)
                    row[index] = prefix + ',' + cell
                elif isinstance(field, FieldDictionary):
                    prefix = str((str.count(cell, ',') + 1) // 2)
                    row[index] = prefix + ',' + cell
        data_arr = [str.join(",", row) for row in table.data]
        return str.join('\n', data_arr)

    def convert(self, template):

        template, default_template = BaseConverter.default_template, template
        template.update(default_template)

        arg_list = {
            "class_ctor_functions": "",
            "class_dict_entries": "",
            "class_ctor_entries": "",
            "class_entry_getters": ""
        }

        name_space_args = {"name_space": self.name_space}
        name_space_begin = template["name_space_begin"].format(**name_space_args)
        name_space_end = template["name_space_end"].format(**name_space_args)

        arg_list["name_space_begin"] = name_space_begin
        arg_list["name_space_end"] = name_space_end

        tables = self.create_tables()

        for table in tables:
            self.convert_table(table, template, arg_list)

        self.convert_manager(tables, template, arg_list)

        for table in tables:
            for struct in table.scheme.get_associated_structs():
                self.convert_struct(table, struct, template, arg_list)
            for enum in table.scheme.get_associated_enums():
                self.convert_struct(table, enum, template, arg_list)

        self.convert_miscs(tables, template, arg_list)

    def convert_table(self, table, template, arg_list):

        table_name = table.scheme.name
        fields = "\n".join([template["field_declare"].format(
            **{"field_type": self.get_type_name(fld), "field_name": fld.field_name}) for fld in table.scheme.fields])

        fields_construct = ""
        for idx, fld in enumerate(table.scheme.fields):
            fields_construct += self.get_field_ctor(fld, idx, template)

        fields_to_string_list = []
        for idx, fld in enumerate(table.scheme.fields):
            fields_to_string_list.append(template["field_to_string"].format(**{"field_name": fld.field_name}))
        fields_to_string = template["field_to_string_sep"].join(fields_to_string_list)

        class_internal_types = ""
        for idx, s in enumerate(table.scheme.get_associated_structs()):
            s_fields = ""
            s_fields_construct = ""
            s_fields_to_string = ""
            for s_idx, fld in enumerate(s.struct_fields):
                s_fields += template["field_declare"].format(
                    **{"field_type": self.get_type_name(fld), "field_name": fld.field_name})
                s_fields += '\n'
                s_fields_construct += self.get_field_ctor(fld, s_idx, template)
            class_internal_types += template["class_internal_struct_declare"].format(**{
                "internal_struct_name": s.field_def,
                "fields": s_fields,
                "fields_construct": s_fields_construct,
                "fields_to_string": s_fields_to_string
            })
        for idx, e in enumerate(table.scheme.get_associated_enums()):
            enum_values = ""
            for f_idx, value in enumerate(e.enum_values):
                enum_values += template["class_internal_enum_value"].format(**value)
            class_internal_types += template["class_internal_enum_declare"].format(**{
                "internal_enum_name": e.field_def,
                "enum_values": enum_values,
            })

        table_args = {
            "table_name": table_name,
            "fields": fields,
            "fields_construct": fields_construct,
            "fields_to_string": fields_to_string,
            "class_internal_types": class_internal_types
        }

        table_args.update(arg_list)

        class_ctor_functions = template["class_ctor"].format(**table_args)

        class_dict_entries = template["class_dict_entry"].format(**table_args)

        class_ctor_entries = template["class_ctor_entry"].format(**table_args)

        class_entry_getters = template["class_entry_getter"].format(**table_args)

        arg_list["class_dict_entries"] += class_dict_entries

        arg_list["class_ctor_entries"] += class_ctor_entries

        arg_list["class_ctor_functions"] += class_ctor_functions

        arg_list["class_entry_getters"] += class_entry_getters

        text0 = template["class_declare"].format(**table_args)

        self.write_config("{0}{1}".format(table_name, self.file_ext), text0)

        text1 = self.pack_table_data(table)

        self.write_config_data("{0}.txt".format(table_name), text1)

    def convert_manager(self, tables, template, arg_list):

        arg_list.update({
            "table_special_str_s": Table.special_str['\\,'],
            "table_special_str_n": Table.special_str['\n']
        })

        arg_list["table_construct"] = ""
        text = template["manager"].format(**arg_list)
        self.write_config("TableManager" + self.file_ext, text)

    def convert_struct(self, table, struct, template, arg_list):
        print(table.scheme.name + struct.field_def)

    def convert_enums(self, table, enum, template, arg_list):
        print(table.scheme.name + enum.field_def)

    def convert_miscs(self, tables, template, arg_list):
        pass
