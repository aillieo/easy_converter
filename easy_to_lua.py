#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import easy_converter

template_lua = {
    "value_entry": '''{field_name}={value_data}''',
    "row_entry": '''[{key}]={{{row_data}}}''',
    "class": '''
local {table_name} = {{

{table_data}

}}

return {table_name}

''',
    "manager": '''
    local TableManager = {{}}
    function TableManager.GetTable(tableName)
        return require("{path_to_table}." .. tostring(table_name))
    end
    function TableManager.GetEntry(tableName, id)
        return TableManager.GetTable(tableName)[id]
    end
    return TableManager
'''
}


class LuaConverter(easy_converter.BaseConverter):

    def __init__(self, *args, **kwargs):
        easy_converter.BaseConverter.__init__(self, *args, **kwargs)
        self.file_ext = ".lua"

    def value_to_string(self, value, field):
        if field.isList:
            return '{' + value + '}'
        if field.isDictionary:
            value_list = str.split(value, ',')
            data = []
            for index in range(len(value_list) // 2):
                one_data = value_list[index * 2] + '=' + (value_list[index * 2 + 1])
                data.append(one_data)
            return '{' + ','.join(data) + '}'
        if field.isPrimitive:
            if field.field_def == 'string':
                return "'" + value + "'"
        return value

    def pack_row_as_lua_table(self, row, scheme):
        data = []
        for index, value in enumerate(row):
            field = scheme.fields[index]
            data.append(template_lua["value_entry"].format(
                **{"field_name": field.field_name, "value_data": self.value_to_string(value, field)}))
        return template_lua["row_entry"].format(**{"key":row[0], "row_data": ",".join(data)})

    def convert_table(self, table, template, arg_list):

        table_name = table.scheme.name
        table_data = []

        for row in table.data:
            table_data.append(self.pack_row_as_lua_table(row, table.scheme))

        table_args = {
            "table_name": table_name,
            "table_data": str.join(',\n', table_data),
        }

        text0 = template["class"].format(**table_args)

        self.write_config("{0}{1}".format(table_name, self.file_ext), text0)

    def convert_manager(self, tables, template, arg_list):
        arg_list.update({"path_to_table": self.name_space})
        text = template["manager"].format(**arg_list)
        self.write_config("TableManager" + self.file_ext, text)

    def convert_miscs(self, template, arg_list):
        pass


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-source", type=str)
    parser.add_argument("-out", type=str, default='./out')
    parser.add_argument("-outdata", type=str, default='./out/data')
    parser.add_argument("-namespace", type=str, default='easyConverter')
    parsed_args = vars(parser.parse_args())

    converter = LuaConverter(**parsed_args)
    converter.convert(template_lua)
