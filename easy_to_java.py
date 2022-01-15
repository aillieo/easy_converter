#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import easy_converter

template_java = {
    "field": '''
    public final {field_type} {field_name};''',

    "field_ctor_primitive": '''
        this.{field_name} = buffer.{field_type_reader}();''',

    "field_ctor_list": '''
        int {field_name}Len = buffer.ReadInt();
        this.{field_name} = new ArrayList<{type_arg_1}>();
        for(int i = 0; i < {field_name}Len; ++i)
        {{
            this.{field_name}.add(buffer.{type_arg_1_reader}());
        }}
        ''',

    "field_ctor_dictionary": '''
        int {field_name}Len = buffer.ReadInt();
        this.{field_name} = new HashMap<{type_arg_1},{type_arg_2}>();
        for(int i = 0; i < {field_name}Len; ++i)
        {{
            this.{field_name}.put(buffer.{type_arg_1_reader}(),buffer.{type_arg_2_reader}());
        }}
        ''',

    "field_ctor_struct": '''
        this.{field_name} = null;''',

    "class": '''{name_space_begin}

import java.util.HashMap;
import java.util.ArrayList;

public class {table_name}
{{
{fields}

    public {table_name}(DataBuffer buffer)
    {{
        {fields_construct}
    }}

    @Override
    public String toString()
    {{
        return "{table_name}{{" + 
{fields_to_string}
                  "}}";
    }}
}}

{name_space_end}

''',
    "field_to_string":
        '''                  "{field_name}" + {field_name} + ''',

    "field_to_string_sep": '''\n''',

    "name_space_begin":
        '''package {name_space};''',
    "name_space_end": ''' ''',

    "class_dict_entry": '''
        private static HashMap<Integer,{table_name}> dict{table_name} = new HashMap<Integer,{table_name}>();
''',
    "class_ctor": '''
        private static Boolean LoadDataFor{table_name}(FuncStr2Str dataProvider)
        {{
            String dataStr = dataProvider.invoke("{table_name}");
            String[] dataArr = dataStr.split("\\n");
            for (String str : dataArr)
            {{
                if (str == null || str.equals(""))
                {{
                    continue;
                }}
                {table_name} table = new {table_name}(new DataBuffer(str));
                dict{table_name}.put(table.id, table);
            }}
            return true;
        }}
    ''',
    "class_entry_getter": '''
        public static {table_name} Get{table_name}(int id)
        {{
            return dict{table_name}.getOrDefault(id, null);
        }}
    ''',
    "class_ctor_entry": '''
            LoadDataFor{table_name}(dataProvider);
''',
    "manager": '''{name_space_begin}
import java.util.HashMap;

    public class TableManager
    {{

        private static final String strN = "{table_special_str_n}";
        private static final String strS = "{table_special_str_s}";

        {class_dict_entries}
        
        {class_entry_getters}

        public static Boolean LoadData(FuncStr2Str dataProvider)
        {{
            {class_ctor_entries}
            return true;
        }}

        {class_ctor_functions}
    }}

{name_space_end}

''',
    "buffer": '''{name_space_begin}

public class DataBuffer
{{
    private String data;
    private int index;

    public DataBuffer(String source)
    {{
        this.data = source;
        this.index = 0;
    }}

    private String ReadRaw()
    {{
        int pos = index;
        while (pos < this.data.length() && this.data.charAt(pos) != ',')
        {{
            pos++;
        }}
        String ret = this.data.substring(index, pos - index);
        index = pos + 1;
        return ret;
    }}

    public int ReadInt()
    {{
        return Integer.parseInt(ReadRaw());
    }}

    public long ReadLong()
    {{
        return Long.parseLong(ReadRaw());
    }}

    public float ReadFloat()
    {{
        return Float.parseFloat(ReadRaw());
    }}

    public double ReadDouble()
    {{
        return Double.parseDouble(ReadRaw());
    }}

    public boolean ReadBool()
    {{
        return ReadRaw().toLowerCase().equals("true");
    }}

    public String ReadString()
    {{
        String ret = ReadRaw();
        return ret;
    }}

}}

{name_space_end}

''',
    "func": '''{name_space_begin}

@FunctionalInterface
public interface FuncStr2Str
{{
    String invoke(String str);
}}
{name_space_end}
    '''
}


class JavaConverter(easy_converter.BaseConverter):

    def __init__(self, *args, **kwargs):
        easy_converter.BaseConverter.__init__(self, *args, **kwargs)
        self.file_ext = ".java"

    def get_type_name(self, field):
        if isinstance(field, easy_converter.FieldStruct):
            return "Object"
        if field.field_def == "int":
            return "Integer"
        if field.field_def == "bool":
            return "boolean"
        if field.field_def == "string":
            return "String"
        return field.field_def.replace("Map", "HashMap").replace("List", "ArrayList").replace("int", "Integer").replace(
            "string", "String")

    def get_primitive_type_name(self, field_def):
        return field_def.replace("int", "Integer").replace("string", "String")

    def get_primitive_reader(self, type_def):
        if type_def == "int":
            return "ReadInt"
        elif type_def == "string":
            return "ReadString"
        elif type_def == "bool":
            return "ReadBool"
        return type_def

    def convert_miscs(self, template, arg_list):
        easy_converter.BaseConverter.convert_miscs(self, template, arg_list)
        self.convert_func(template, arg_list)

    def convert_func(self, template, arg_list):
        text = template["func"].format(**arg_list)
        self.write_config("FuncStr2Str" + self.file_ext, text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-source", type=str)
    parser.add_argument("-out", type=str, default='./out')
    parser.add_argument("-outdata", type=str, default='./out/data')
    parser.add_argument("-namespace", type=str, default='easyConverter')
    parsed_args = vars(parser.parse_args())

    converter = JavaConverter(**parsed_args)
    converter.convert(template_java)
