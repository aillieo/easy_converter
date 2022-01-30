#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import easy_converter

template_cs = {
    "field_declare": '''
        public readonly {field_type} {field_name};''',

    "field_ctor_primitive": '''
            this.{field_name} = buffer.{field_type_reader}();''',

    "field_ctor_list": '''
            int {field_name}Len = buffer.ReadInt();
            this.{field_name} = new List<{list_element_type}>();
            for(int i = 0; i < {field_name}Len; ++i)
            {{
                this.{field_name}.Add(buffer.{list_element_type_reader}());
            }}
        ''',

    "field_ctor_dictionary": '''
            int {field_name}Len = buffer.ReadInt();
            this.{field_name} = new Dictionary<{dict_key_type},{dict_value_type}>();
            for(int i = 0; i < {field_name}Len; ++i)
            {{
                this.{field_name}.Add(buffer.{dict_key_type_reader}(),buffer.{dict_value_type_reader}());
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
        private static Dictionary<int,{table_name}> dict{table_name} = new Dictionary<int,{table_name}>();
''',
    "class_ctor": '''
        private static bool LoadDataFor{table_name}(Func<string,string> dataProvider)
        {{
            string dataStr = dataProvider("{table_name}");
            string[] dataArr = dataStr.Split('\\n');
            foreach (var str in dataArr)
            {{
                if (string.IsNullOrEmpty(str))
                {{
                    continue;
                }}
                {table_name} table = new {table_name}(new DataBuffer(str));
                dict{table_name}.Add(table.id, table);
            }}
            return true;
        }}
    ''',
    "class_entry_getter": '''
        public static {table_name} Get{table_name}(int id)
        {{
            if (dict{table_name}.TryGetValue(id, out {table_name} value))
            {{
                return value;
            }}
            return null;
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

        private static readonly string strN = "{table_special_str_n}";
        private static readonly string strS = "{table_special_str_s}";

        {class_dict_entries}
        
        {class_entry_getters}

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

{name_space_begin}

    public class DataBuffer
    {{
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
            return int.Parse(ReadRaw());
        }}

        public long ReadLong()
        {{
            return long.Parse(ReadRaw());
        }}

        public float ReadFloat()
        {{
            return float.Parse(ReadRaw());
        }}

        public double ReadDouble()
        {{
            return double.Parse(ReadRaw());
        }}

        public bool ReadBool()
        {{
            return ReadRaw().ToLower() == "true";
        }}

        public string ReadString()
        {{
            string ret = ReadRaw();
            return ret;
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


class CSharpConverter(easy_converter.BaseConverter):

    def __init__(self, *args, **kwargs):
        easy_converter.BaseConverter.__init__(self, *args, **kwargs)
        self.file_ext = ".cs"

    def get_type_name(self, field):
        if isinstance(field, easy_converter.FieldList):
            return f"List<{self.get_type_name(field.list_element_type)}>"
        elif isinstance(field, easy_converter.FieldDictionary):
            return f"Dictionary<{self.get_type_name(field.dict_key_type)},{self.get_type_name(field.dict_value_type)}>"
        return super().get_type_name(field)

    def convert_miscs(self, tables, template, arg_list):
        text = template["buffer"].format(**arg_list)
        self.write_config("DataBuffer" + self.file_ext, text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-source", type=str)
    parser.add_argument("-out", type=str, default='./out')
    parser.add_argument("-outdata", type=str, default='./out/data')
    parser.add_argument("-namespace", type=str, default='EasyConverter')
    parsed_args = vars(parser.parse_args())

    converter = CSharpConverter(**parsed_args)
    converter.convert(template_cs)
