#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import os

from enum import Enum
from openpyxl import load_workbook


class FieldType(Enum):
    Unknown = 0
    Primitive = 1
    List = 2
    Dictionary = 3
    Struct = 4
    Enum = 5


class Field:
    re_primitive = re.compile(r"^(int|long|string|float|bool)$")
    re_list = re.compile(r"^List<(\w+)>$")
    re_dict = re.compile(r"^Map<(\w+),(\w+)>$")
    re_struct = re.compile(r"^Struct<(\w+,\w+)(?:,(\w+,\w+))*>$")
    re_enum = re.compile(r"^Enum<(\w+,\d+)(?:,(\w+,\d+))*>$")
    re_struct_list = re.compile(r"^List<Struct<(\w+,\w+)(?:,(\w+,\w+))*>>$")
    re_struct_dict = re.compile(r"^Map<(\w+),Struct<(\w+,\w+)(?:,(\w+,\w+))*>>$")

    @staticmethod
    def create_field_info(field_name, field_def):
        match_primitive = Field.re_primitive.match(field_def)
        if match_primitive:
            return FieldPrimitive(field_name, field_def, match_primitive)
        match_list = Field.re_list.match(field_def)
        if match_list:
            return FieldList(field_name, field_def, match_list)
        match_dict = Field.re_dict.match(field_def)
        if match_dict:
            return FieldDictionary(field_name, field_def, match_dict)
        match_struct = Field.re_struct.match(field_def)
        if match_struct:
            return FieldStruct(field_name, field_def, match_struct)
        match_enum = Field.re_enum.match(field_def)
        if match_enum:
            return FieldEnum(field_name, field_def, match_enum)
        match_struct_list = Field.re_struct_list.match(field_def)
        if match_struct_list:
            return FieldStructList(field_name, field_def, match_struct_list)
        match_struct_dict = Field.re_struct_dict.match(field_def)
        if match_struct_dict:
            return FieldStructDictionary(field_name, field_def, match_struct_dict)
        raise Exception('invalid def' + field_def)

    def __init__(self, field_name, field_def):
        self.field_name = field_name
        self.field_def = field_def


class FieldPrimitive(Field):

    def __init__(self, field_name, field_def, reg_match):
        super().__init__(field_name, field_def)
        self.field_type = {reg_match.group(1)}


class FieldList(Field):
    def __init__(self, field_name, field_def, reg_match):
        super().__init__(field_name, field_def)
        self.type_args = []
        self.type_args.append(reg_match.group(1))
        self.list_element_type = reg_match.group(1)


class FieldDictionary(Field):
    def __init__(self, field_name, field_def, reg_match):
        super().__init__(field_name, field_def)
        self.type_args = []
        self.type_args.append(reg_match.group(1))
        self.type_args.append(reg_match.group(2))
        self.dict_key_type = reg_match.group(1)
        self.dict_value_type = reg_match.group(2)


class FieldStruct(Field):
    def __init__(self, field_name, field_def, reg_match):
        super().__init__(field_name, field_def)
        self.struct_fields = []
        print("FieldStruct " + field_def)
        for g in reg_match.groups():
            print(g)


class FieldEnum(Field):
    def __init__(self, field_name, field_def, reg_match):
        super().__init__(field_name, field_def)
        self.struct_fields = []
        print("FieldEnum " + field_def)
        for g in reg_match.groups():
            print(g)


class FieldStructDictionary(FieldDictionary):
    def __init__(self, field_name, field_def, reg_match):
        super().__init__(field_name, field_def, reg_match)
        self.struct_fields = []
        print("FieldStructDictionary " + field_def)
        for g in reg_match.groups():
            print(g)


class FieldStructList(FieldList):
    def __init__(self, field_name, field_def, reg_match):
        super().__init__(field_name, field_def, reg_match)
        self.struct_fields = []
        print("FieldStructList " + field_def)
        for g in reg_match.groups():
            print(g)


class Scheme:

    def __init__(self, name, fields):
        self.full_name = name
        self.name = name
        self.fields = fields


class Table:
    special_str = {
        '\n': ';l/~',
        '\\,': ':l/~',
    }

    def __init__(self, sheet):

        name = sheet.title

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
                fields = zip(field_names, field_defs)
                fields = [Field.create_field_info(*field) for field in fields]

                self.scheme = Scheme(name, fields)

            self.append_row(data, row)

        if self.scheme is None:
            print("invalid xlsx file")
            return
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
            raise Exception('syntax error:' + field.field_def)


class BaseConverter:
    default_template = {

        # 1. namespace text
        'name_space_begin': '',
        'name_space_end': '',

        # 2. Table class:
        # 2.1. Table body codes
        'class': '',

        # 2.2. field declaration
        'field': '',

        # 2.3. field constructor for different types
        'field_ctor_primitive': '',
        'field_ctor_list': '',
        'field_ctor_dictionary': '',
        'field_ctor_struct': '',

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

    def get_primitive_reader(self, type_def):
        return "Read" + type_def.capitalize()

    def get_field_ctor(self, field, index, template):
        field_args = {
            "field_name": field.field_name,
            "field_type": field.field_def,
            "field_type_reader": self.get_primitive_reader(field.field_def),
            "index": index}
        if hasattr(field, 'type_args') and field.type_args is not None:
            if len(field.type_args) > 0:
                field_args.update({
                    "type_arg_1": self.get_primitive_type_name(field.type_args[0]),
                    "type_arg_1_reader": self.get_primitive_reader(field.type_args[0])})
            if len(field.type_args) > 1:
                field_args.update({
                    "type_arg_2": self.get_primitive_type_name(field.type_args[1]),
                    "type_arg_2_reader": self.get_primitive_reader(field.type_args[1])})
        if isinstance(field, FieldPrimitive):
            return template["field_ctor_primitive"].format(**field_args)
        elif isinstance(field, FieldList):
            return template["field_ctor_list"].format(**field_args)
        elif isinstance(field, FieldDictionary):
            return template["field_ctor_dictionary"].format(**field_args)
        elif isinstance(field, FieldStruct):
            return template["field_ctor_struct"].format(**field_args)

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

        self.convert_miscs(template, arg_list)

        # text5 = template["test"].format(**arg_list)
        # self.write_config("TestCase" + self.file_ext, text5)

    def convert_table(self, table, template, arg_list):

        table_name = table.scheme.name
        fields = "\n".join([template["field"].format(
            **{"field_type": self.get_type_name(fld), "field_name": fld.field_name}) for fld in table.scheme.fields])

        fields_construct = ""
        for idx, fld in enumerate(table.scheme.fields):
            fields_construct += self.get_field_ctor(fld, idx, template)

        fields_to_string_list = []
        for idx, fld in enumerate(table.scheme.fields):
            fields_to_string_list.append(template["field_to_string"].format(**{"field_name": fld.field_name}))
        fields_to_string = template["field_to_string_sep"].join(fields_to_string_list)

        table_args = {
            "table_name": table_name,
            "fields": fields,
            "fields_construct": fields_construct,
            "fields_to_string": fields_to_string}

        table_args.update(arg_list)

        class_ctor_functions = template["class_ctor"].format(**table_args)

        class_dict_entries = template["class_dict_entry"].format(**table_args)

        class_ctor_entries = template["class_ctor_entry"].format(**table_args)

        class_entry_getters = template["class_entry_getter"].format(**table_args)

        arg_list["class_dict_entries"] += class_dict_entries

        arg_list["class_ctor_entries"] += class_ctor_entries

        arg_list["class_ctor_functions"] += class_ctor_functions

        arg_list["class_entry_getters"] += class_entry_getters

        text0 = template["class"].format(**table_args)

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

    def convert_miscs(self, template, arg_list):
        self.convert_buffer(template, arg_list)

    def convert_buffer(self, template, arg_list):
        text = template["buffer"].format(**arg_list)
        self.write_config("DataBuffer" + self.file_ext, text)
