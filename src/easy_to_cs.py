#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import List, Dict
from easy_converter import *


class CSharpWriter(TableWriter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_template_file_dir(self) -> str:
        return "templates/cs"

    def get_display_def(self, field: Field):
        if isinstance(field, FieldList):
            return f"List<{self.get_display_def(field.list_element_type)}>"
        elif isinstance(field, FieldDictionary):
            display_def_for_key = self.get_display_def(field.dict_key_type)
            display_def_for_value = self.get_display_def(field.dict_value_type)
            return f"Dictionary<{display_def_for_key}, {display_def_for_value}>"
        elif isinstance(field, FieldStruct) or isinstance(field, FieldEnum):
            return f"{field.table_name}.{field.field_def}"
        elif isinstance(field, FieldReference):
            return self.get_display_def(field.ref_type)
        else:
            return field.field_def

    def convert_misc(self, tables: List[Table], context: Dict[str, Any]):

        context.update({
            "table_special_str_s": Table.special_str['\\,'],
            "table_special_str_n": Table.special_str['\n']
        })

        buffer_template = self.env.get_template('buffer_template.j2')
        text = buffer_template.render(context)
        self.write_config("DataBuffer" + self.file_ext, text)

    def convert_table(self, table: Table, context: Dict[str, Any]):
        assert isinstance(table.scheme, Scheme)
        class_template = self.env.get_template('class_template.j2')
        class_context = {"table": table.scheme}
        class_context.update(context)

        table_name = table.scheme.name

        text0 = class_template.render(class_context)

        self.write_config(f"{table_name}{self.file_ext}", text0)

        text1 = self.pack_table_data(table)
        self.write_config_data(f"{table_name}.txt", text1)

    def convert_manager(self, tables: List[Table], context: Dict[str, Any]) -> None:
        context["tables"] = tables
        manager_template = self.env.get_template('manager_template.j2')
        text = manager_template.render(context)
        self.write_config("TableManager" + self.file_ext, text)

    def get_script_file_ext(self):
        return '.cs'

    def write_all(self, tables):
        context = {}

        for table in tables:
            self.convert_table(table, context)

        self.convert_manager(tables, context)

        self.convert_misc(tables, context)


if __name__ == '__main__':
    parsed_args = EasyConverter.parse_args()
    EasyConverter.convert(TableReader(**parsed_args), CSharpWriter(**parsed_args))
