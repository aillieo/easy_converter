#!/usr/bin/python
# -*- coding: UTF-8 -*-

from typing import List, Dict
from easy_converter import *


class JavaWriter(TableWriter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_template_file_dir(self) -> str:
        return "templates/java"

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

    def convert_misc(self, tables: List[Table], context: Dict[str, Any]):
        context.update({
            "table_special_str_s": Table.special_str['\\,'],
            "table_special_str_n": Table.special_str['\n']
        })

        buffer_template = self.env.get_template('buffer_template.j2')
        text = buffer_template.render(context)
        self.write_config("DataBuffer" + self.file_ext, text)

        func_template = self.env.get_template('func_template.j2')
        text0 = func_template.render(context)
        self.write_config("FuncStr2Str" + self.file_ext, text0)

    def convert_manager(self, tables: List[Table], context: Dict[str, Any]) -> None:
        context["tables"] = tables
        manager_template = self.env.get_template('manager_template.j2')
        text = manager_template.render(context)
        self.write_config("TableManager" + self.file_ext, text)

    def get_script_file_ext(self):
        return '.java'

    def write_all(self, tables):
        context = {}

        for table in tables:
            self.convert_table(table, context)

        self.convert_manager(tables, context)

        self.convert_misc(tables, context)


if __name__ == '__main__':
    parsed_args = EasyConverter.parse_args()
    EasyConverter.convert(TableReader(**parsed_args), JavaWriter(**parsed_args))
