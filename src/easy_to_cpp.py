#!/usr/bin/python
# -*- coding: UTF-8 -*-

from typing import Dict
from easy_converter import *


class CppWriter(TableWriter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.source_file_ext = self.get_script_file_ext()
        self.header_file_ext = self.get_header_file_ext()

    def get_template_file_dir(self) -> str:
        return "templates/cpp"

    def convert_misc(self, tables: List[Table], context: Dict[str, Any]):

        context.update({
            "table_special_str_s": Table.special_str['\\,'],
            "table_special_str_n": Table.special_str['\n']
        })

        buffer_inc_template = self.env.get_template('buffer_inc_template.j2')
        text = buffer_inc_template.render(context)
        self.write_config("DataBuffer" + self.header_file_ext, text)
        buffer_src_template = self.env.get_template('buffer_src_template.j2')
        text = buffer_src_template.render(context)
        self.write_config("DataBuffer" + self.source_file_ext, text)

    def convert_table(self, table: Table, context: Dict[str, Any]):
        assert isinstance(table.scheme, Scheme)
        class_context = {"table": table.scheme}
        class_context.update(context)

        table_name = table.scheme.name

        class_inc_template = self.env.get_template('class_inc_template.j2')
        text0 = class_inc_template.render(class_context)
        self.write_config(f"{table_name}{self.header_file_ext}", text0)
        class_src_template = self.env.get_template('class_src_template.j2')
        text0 = class_src_template.render(class_context)
        self.write_config(f"{table_name}{self.source_file_ext}", text0)

        text1 = self.pack_table_data(table)
        self.write_config_data(f"{table_name}.txt", text1)

    def convert_manager(self, tables: List[Table], context: Dict[str, Any]) -> None:
        context["tables"] = tables
        manager_inc_template = self.env.get_template('manager_inc_template.j2')
        text = manager_inc_template.render(context)
        self.write_config("TableManager" + self.header_file_ext, text)
        manager_src_template = self.env.get_template('manager_src_template.j2')
        text = manager_src_template.render(context)
        self.write_config("TableManager" + self.source_file_ext, text)

    def get_script_file_ext(self):
        return '.cpp'

    def get_header_file_ext(self):
        return '.hpp'

    def get_display_def(self, field: Field):
        return field.field_def

    def write_all(self, tables):
        context = {}

        for table in tables:
            self.convert_table(table, context)

        self.convert_manager(tables, context)

        self.convert_misc(tables, context)


if __name__ == '__main__':
    parsed_args = EasyConverter.parse_args()
    EasyConverter.convert(TableReader(**parsed_args), CppWriter(**parsed_args))
