#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import easy_converter

template_lua = {
    "value_entry": '''{field_name}={value_data}''',
    "row_entry": '''[{key}]={{{row_data}}}''',
    "class_declare": '''local {table_name} = {{

{table_data}

}}

return {table_name}

''',
    "manager": '''local TableManager = {{}}
function TableManager.GetTable(tableName)
    return require("{path_to_table}." .. tostring(tableName))
end
function TableManager.GetEntry(tableName, id)
    return TableManager.GetTable(tableName)[id]
end
return TableManager
''',

    "enums": '''local TableEnums = {{
    {enum_data}
}}
return TableEnums
'''
}


class LuaConverter(easy_converter.BaseConverter):

    def __init__(self, *args, **kwargs):
        easy_converter.BaseConverter.__init__(self, *args, **kwargs)
        self.file_ext = ".lua"

    def value_to_string(self, value, field):
        if isinstance(field, easy_converter.FieldList):
            return '{' + value + '}'
        if isinstance(field, easy_converter.FieldDictionary):
            value_list = str.split(value, ',')
            data = []
            for index in range(len(value_list) // 2):
                one_data = value_list[index * 2] + '=' + (value_list[index * 2 + 1])
                data.append(one_data)
            return '{' + ','.join(data) + '}'
        if isinstance(field, easy_converter.FieldPrimitive):
            if field.field_def == 'string':
                return "'" + value + "'"
            else:
                return value
        if isinstance(field, easy_converter.FieldStruct):
            value_list = str.split(value, ',')
            data = []
            for idx, s_field in enumerate(field.struct_fields):
                k = s_field.field_name
                v = value_list[idx]
                if s_field.field_def == "string":
                    v = "'" + v + "'"
                one_data = k + '=' + v
                data.append(one_data)
            return '{' + ','.join(data) + '}'
        if isinstance(field, easy_converter.FieldEnum):
            match_pair = next((p for p in field.enum_values if p.get("enum_name") == value), None)
            if match_pair is not None:
                return match_pair.get("enum_value")
        return value

    def pack_row_as_lua_table(self, row, scheme):
        data = []
        for index, value in enumerate(row):
            field = scheme.fields[index]
            data.append(template_lua["value_entry"].format(
                **{"field_name": field.field_name, "value_data": self.value_to_string(value, field)}))
        return template_lua["row_entry"].format(**{"key": row[0], "row_data": ",".join(data)})

    def convert_table(self, table, template, arg_list):

        table_name = table.scheme.name
        table_data = []

        for row in table.data:
            table_data.append(self.pack_row_as_lua_table(row, table.scheme))

        table_args = {
            "table_name": table_name,
            "table_data": str.join(',\n', table_data),
        }

        text0 = template["class_declare"].format(**table_args)

        self.write_config("{0}{1}".format(table_name, self.file_ext), text0)

    def convert_manager(self, tables, template, arg_list):
        arg_list.update({"path_to_table": self.name_space})
        text = template["manager"].format(**arg_list)
        self.write_config("TableManager" + self.file_ext, text)

    def convert_structs(self, tables, template, arg_list):
        pass

    def convert_enums(self, tables, template, arg_list):
        text0 = ""
        for table in tables:
            associated_enums = table.scheme.get_associated_enums()
            for enum in associated_enums:
                if text0 == "":
                    text0 += table.scheme.name + "={"
                text0 += self.get_enum_def(enum.field_def, enum.enum_values)
                text0 += ","
            if text0 != "":
                text0 += "},"
        if text0 != "":
            arg_list.update({"enum_data": text0})
            text = template["enums"].format(**arg_list)
            self.write_config("TableEnums" + self.file_ext, text)

    def get_enum_def(self, enum_name, enum_values):
        data = []
        for pair in enum_values:
            data.append(pair.get("enum_name") + "=" + pair.get("enum_value"))
        return enum_name + "={" + ",".join(data) + "}"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-source", type=str)
    parser.add_argument("-out", type=str, default='./out')
    parser.add_argument("-outdata", type=str, default='./out/data')
    parser.add_argument("-namespace", type=str, default='easyConverter')
    parsed_args = vars(parser.parse_args())

    converter = LuaConverter(**parsed_args)
    converter.convert(template_lua)
