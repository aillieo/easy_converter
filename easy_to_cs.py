#!/usr/bin/python
# -*- coding: UTF-8 -*-

from easy_converter import *

template_cs = {
    "field_declare": '''
        public readonly {field_type} {field_name};''',

    "field_ctor_primitive": '''
            this.{field_name} = {field_type_reader};''',

    "field_ctor_list": '''
            int {field_name}Len = buffer.ReadInt();
            this.{field_name} = new List<{list_element_type}>();
            for(int i = 0; i < {field_name}Len; ++i)
            {{
                this.{field_name}.Add({list_element_type_reader});
            }}
        ''',

    "field_ctor_dictionary": '''
            int {field_name}Len = buffer.ReadInt();
            this.{field_name} = new Dictionary<{dict_key_type},{dict_value_type}>();
            for(int i = 0; i < {field_name}Len; ++i)
            {{
                this.{field_name}.Add({dict_key_type_reader}, {dict_value_type_reader});
            }}
        ''',

    "field_ctor_struct": '''
            this.{field_name} = new {field_type}(buffer);''',

    "field_ctor_enum": '''
            this.{field_name} = buffer.ReadEnum<{field_type}>();''',

    "class_declare": '''
using System.Collections.Generic;

{name_space_begin}

    public class {table_name}
    {{
{fields}

        public {table_name}(DataBuffer buffer)
        {{
            {fields_construct}
        }}

        public override string ToString()
        {{
            return $"{fields_to_string}";
        }}

{class_internal_types}

    }}

{name_space_end}

''',
    "class_internal_struct_declare":
        '''
        public class {internal_struct_name}
        {{
{fields}

            public {internal_struct_name}(DataBuffer buffer)
            {{
                {fields_construct}
            }}

            public override string ToString()
            {{
                return $"{fields_to_string}";
            }}
        }}
''',
    "class_internal_enum_declare":
        '''
        public enum {internal_enum_name}
        {{
{enum_values}
        }}
''',
    "class_internal_enum_value":
        '''
            {enum_name} = {enum_value},
''',
    "field_to_string":
        ''' {field_name}={{{field_name}}} ''',

    "field_to_string_sep": ''',''',

    "name_space_begin":
        '''namespace {name_space}
{{ ''',
    "name_space_end": '''}}
''',

    "class_dict_entry": '''
        private static Dictionary<{table_key_type},{table_name}> dict{table_name} = new Dictionary<{table_key_type},{table_name}>();
''',
    "class_ctor": '''
        private static bool LoadDataFor{table_name}(Func<string,string> dataProvider)
        {{
            string dataStr = dataProvider("{table_name}");
            string[] dataArr = dataStr.Split('\\n','\\r');
            foreach (var str in dataArr)
            {{
                if (string.IsNullOrEmpty(str))
                {{
                    continue;
                }}
                {table_name} table = new {table_name}(new DataBuffer(str));
                dict{table_name}.Add(table.{table_key_name}, table);
            }}
            return true;
        }}
    ''',
    "class_entry_getter": '''
        public static {table_name} Get{table_name}({table_key_type} id)
        {{
            if (dict{table_name}.TryGetValue(id, out {table_name} value))
            {{
                return value;
            }}
            return null;
        }}
    ''',
    "class_all_entries_getter": '''
        public static Dictionary<{table_key_type},{table_name}> GetAll{table_name_plural}()
        {{
            return dict{table_name};
        }}
''',
    "class_ctor_entry": '''
            LoadDataFor{table_name}(dataProvider);
''',
    "manager": '''
using System.Collections.Generic;
using System;

{name_space_begin}

    public static class TableManager
    {{
        {class_dict_entries}

        {class_entry_getters}

        {class_all_entries_getters}

        public static bool LoadData(Func<string,string> dataProvider)
        {{
            {class_ctor_entries}
            return true;
        }}

        {class_ctor_functions}
    }}

{name_space_end}

''',
    "buffer": '''
using System.Collections.Generic;
using System;
using System.Globalization;

{name_space_begin}

    public class DataBuffer
    {{
        private static readonly string strN = "{table_special_str_n}";
        private static readonly string strS = "{table_special_str_s}";

        private string data;
        private int index;

        public DataBuffer(string source)
        {{
            this.data = source;
            this.index = 0;
        }}

        private string ReadRaw()
        {{
            int pos = index;
            while (pos < this.data.Length && this.data[pos] != ',')
            {{
                pos++;
            }}
            string ret = this.data.Substring(index, pos - index);
            index = pos + 1;
            return ret;
        }}

        public int ReadInt()
        {{
            return int.Parse(ReadRaw(), CultureInfo.InvariantCulture);
        }}

        public long ReadLong()
        {{
            return long.Parse(ReadRaw(), CultureInfo.InvariantCulture);
        }}

        public float ReadFloat()
        {{
            return float.Parse(ReadRaw(), CultureInfo.InvariantCulture);
        }}

        public double ReadDouble()
        {{
            return double.Parse(ReadRaw(), CultureInfo.InvariantCulture);
        }}

        public bool ReadBool()
        {{
            return ReadRaw().ToLower() == "true";
        }}

        public string ReadString()
        {{
            return ReadRaw().Replace(strN, "\\n").Replace(strS, ",");
        }}

        public T ReadEnum<T>() where T : struct
        {{
            string name = ReadString();
            if (Enum.TryParse(name, out T e))
            {{
                return e;
            }}

            throw new Exception($"invalid enum name for {{typeof(T).Name}}: {{name}}");
        }}

    }}

{name_space_end}

'''
}


class CSharpWriter(TableWriter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_type_name(self, field):
        if isinstance(field, FieldList):
            return f"List<{self.get_type_name(field.list_element_type)}>"
        elif isinstance(field, FieldDictionary):
            return f"Dictionary<{self.get_type_name(field.dict_key_type)},{self.get_type_name(field.dict_value_type)}>"
        return field.field_def

    def convert_miscs(self, tables, template, arg_list):

        arg_list.update({
            "table_special_str_s": Table.special_str['\\,'],
            "table_special_str_n": Table.special_str['\n']
        })

        text = template["buffer"].format(**arg_list)
        self.write_config("DataBuffer" + self.file_ext, text)

    def get_primitive_type_name(self, field_def):
        return field_def

    def get_field_reader(self, field_info):
        if isinstance(field_info, FieldStruct):
            return self.get_struct_reader(field_info.field_def)
        elif isinstance(field_info, FieldEnum):
            return self.get_enum_reader(field_info.field_def)
        return self.get_primitive_reader(field_info.field_def)

    def get_primitive_reader(self, type_def):
        return "buffer.Read" + upper_camel_case(type_def) + "()"

    def get_struct_reader(self, type_def):
        return "new " + type_def + "(buffer)"

    def get_enum_reader(self, type_def):
        return "buffer.ReadEnum<" + type_def + ">()"

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

    def get_table_key_type(self, field):
        if isinstance(field, FieldPrimitive):
            return field.field_def
        elif isinstance(field, FieldEnum):
            return f"{field.table_name}.{field.field_def}"
        else:
            raise Exception('not supported key type :' + field.field_def)

    def convert_table(self, table, template, arg_list):

        table_name = table.scheme.name
        table_name_plural = plural_form(table_name)
        fields = "\n".join([template["field_declare"].format(
            **{"field_type": self.get_type_name(fld), "field_name": fld.field_name}) for fld in table.scheme.fields])

        fields_construct = ""
        table_key_type = ""
        table_key_name = ""
        for idx, fld in enumerate(table.scheme.fields):
            if idx == 0:
                table_key_type = self.get_table_key_type(fld)
                table_key_name = fld.field_name
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
            "table_name_plural": table_name_plural,
            "table_key_type": table_key_type,
            "table_key_name": table_key_name,
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
        class_all_entries_getters = template["class_all_entries_getter"].format(**table_args)

        arg_list["class_dict_entries"] += class_dict_entries
        arg_list["class_ctor_entries"] += class_ctor_entries
        arg_list["class_ctor_functions"] += class_ctor_functions
        arg_list["class_entry_getters"] += class_entry_getters
        arg_list["class_all_entries_getters"] += class_all_entries_getters

        text0 = template["class_declare"].format(**table_args)
        self.write_config(f"{table_name}{self.file_ext}", text0)

        text1 = self.pack_table_data(table)
        self.write_config_data(f"{table_name}.txt", text1)

    def convert_manager(self, tables, template, arg_list):

        arg_list["table_construct"] = ""
        text = template["manager"].format(**arg_list)
        self.write_config("TableManager" + self.file_ext, text)

    def get_script_file_ext(self):
        return '.cs'

    def write_all(self, tables):
        template = {}
        template.update(template_cs)

        arg_list = {
            "class_ctor_functions": "",
            "class_dict_entries": "",
            "class_ctor_entries": "",
            "class_entry_getters": "",
            "class_all_entries_getters": "",
        }

        name_space_args = {"name_space": self.name_space}
        name_space_begin = template["name_space_begin"].format(**name_space_args)
        name_space_end = template["name_space_end"].format(**name_space_args)

        arg_list["name_space_begin"] = name_space_begin
        arg_list["name_space_end"] = name_space_end

        for table in tables:
            self.convert_table(table, template, arg_list)

        self.convert_manager(tables, template, arg_list)

        self.convert_miscs(tables, template, arg_list)


if __name__ == '__main__':
    parsed_args = EasyConverter.parse_args()
    EasyConverter.convert(TableReader(**parsed_args), CSharpWriter(**parsed_args))
