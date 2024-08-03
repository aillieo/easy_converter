#!/usr/bin/python
# -*- coding: UTF-8 -*-

from typing import Dict
from easy_converter import *


class LuaWriter(TableWriter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.env.globals['zip'] = zip

    def get_template_file_dir(self) -> str:
        return "templates/lua"

    def convert_table(self, table: Table, context: Dict[str, Any]):
        assert isinstance(table.scheme, Scheme)
        class_template = self.env.get_template('class_template.j2')
        class_context = {
            "table": table.scheme,
            "data": table.data,
        }
        class_context.update(context)

        table_name = table.scheme.name

        text0 = class_template.render(class_context)
        self.write_config(f"{table_name}{self.file_ext}", text0)

    def convert_manager(self, tables: List[Table], context: Dict[str, Any]) -> None:
        context["tables"] = tables
        context["path_to_table"] = self.path_out_data
        manager_template = self.env.get_template('manager_template.j2')
        text = manager_template.render(context)
        self.write_config("TableManager" + self.file_ext, text)

    def convert_misc(self, tables: List[Table], context: Dict[str, Any]):
        enum_template = self.env.get_template('enum_template.j2')
        text = enum_template.render(context)
        self.write_config("TableEnums" + self.file_ext, text)

    def get_script_file_ext(self):
        return '.lua'

    def write_all(self, tables):
        context = {}

        for table in tables:
            self.convert_table(table, context)

        self.convert_manager(tables, context)

        self.convert_misc(tables, context)


if __name__ == '__main__':
    parsed_args = EasyConverter.parse_args()
    EasyConverter.convert(TableReader(**parsed_args), LuaWriter(**parsed_args))
