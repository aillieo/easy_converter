#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys

sys.path.append("..")
sys.path.append(".")

from easy_converter import BaseConverter

template_cs = {
    "field": '''
        public readonly {field_type} {field_name};''',

    "field_ctor_primitive": '''
            this.{field_name} = buffer.{field_type_reader}();''',

    "field_ctor_list": '''
            int {field_name}Len = buffer.ReadInt();
            this.{field_name} = new List<{type_arg_1}>();
            for(int i = 0; i < {field_name}Len; ++i)
            {{
                this.{field_name}.Add(buffer.{type_arg_1_reader}());
            }}
        ''',

    "field_ctor_dictionary": '''
            int {field_name}Len = buffer.ReadInt();
            this.{field_name} = new Dictionary<{type_arg_1},{type_arg_2}>();
            for(int i = 0; i < {field_name}Len; ++i)
            {{
                this.{field_name}.Add(buffer.{type_arg_1_reader}(),buffer.{type_arg_2_reader}());
            }}
        ''',

    "field_ctor_struct": '''
            this.{field_name} = default;''',

    "class": '''
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
    }}

{name_space_end}

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

    }}

{name_space_end}

'''
}


class CSharpConverter(BaseConverter):

    def __init__(self, *args, **kwargs):
        BaseConverter.__init__(self, *args, **kwargs)
        self.file_ext = ".cs"

    def get_type_name(self, field):
        if field.isStruct:
            return "object"
        return field.field_def.replace("Map", "Dictionary")


if __name__ == '__main__':
    # print(sys.argv)

    args = {}
    for index, arg in enumerate(sys.argv):
        if arg == '-source':
            args['source'] = sys.argv[index + 1]
        elif arg == '-out':
            args['out'] = sys.argv[index + 1]
        elif arg == '-outdata':
            args['out_data'] = sys.argv[index + 1]
        elif arg == '-namespace':
            args['name_space'] = sys.argv[index + 1]

    # print(args)

    converter = CSharpConverter(**args)
    converter.convert(template_cs)
