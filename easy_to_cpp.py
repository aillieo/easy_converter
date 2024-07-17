#!/usr/bin/python
# -*- coding: UTF-8 -*-

from easy_converter import *

template_cpp = {
    "field_declare": '''
        {field_type} {field_name};''',

    "field_ctor_primitive": '''
            this->{field_name} = {field_type_reader};''',

    "field_ctor_list": '''
            int {field_name}Len = buffer->ReadInt();
            this->{field_name} = std::vector<{list_element_type}>();
            for(int i = 0; i < {field_name}Len; ++i)
            {{
                this->{field_name}.push_back({list_element_type_reader});
            }}
        ''',

    "field_ctor_dictionary": '''
            int {field_name}Len = buffer->ReadInt();
            this->{field_name} = std::unordered_map<{dict_key_type},{dict_value_type}>();
            for(int i = 0; i < {field_name}Len; ++i)
            {{
                this->{field_name}.emplace({dict_key_type_reader}, {dict_value_type_reader});
            }}
        ''',

    "field_ctor_struct": '''
            this->{field_name} = new {field_type}(buffer);''',

    "field_ctor_enum": '''
            this->{field_name} = ({field_type})buffer->ReadInt();''',

    "class_declare": '''
#pragma once
#include <string>
#include <vector>
#include <unordered_map>
class DataBuffer;
{name_space_begin}

    {class_internal_types}

    class {table_name}
    {{
    public:

{fields}

        {table_name}(DataBuffer* buffer);

        std::string toString();
    }};

{name_space_end}
''',
    "class_implement": '''
#include "DataBuffer.h"
#include "{table_name}.h"
{name_space_begin}
    {table_name}::{table_name}(DataBuffer* buffer)
    {{
        {fields_construct}
    }}

    std::string {table_name}::toString()
    {{
        return "{fields_to_string}";
    }}

{class_internal_types_implement}

{name_space_end}
''',
    "class_internal_struct_declare":
        '''
    class {internal_struct_name}
    {{
        private:
{fields}

        public:
        {internal_struct_name}(DataBuffer* buffer)
        {{
            {fields_construct}
        }}

        std::string toString()
        {{
            return "{fields_to_string}";
        }}
    }};
''',
    "class_internal_enum_declare":
        '''
    enum class {internal_enum_name}
    {{
{enum_values}
    }};
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
        static std::unordered_map<{table_key_type},{table_name}> dict{table_name};
''',
    "class_dict_entry_initialize": '''
        std::unordered_map<{table_key_type},{table_name}> TableManager::dict{table_name} = std::unordered_map<{table_key_type},{table_name}>();
''',
    "class_ctor": '''
        static bool LoadDataFor{table_name}(std::function<std::string(std::string)> dataProvider);
    ''',
    "class_entry_declare": '''class {table_name};
''',
    "class_entry_include": '''#include "{table_name}.h";
''',
    "class_entry_getter": '''
        static {table_name} Get{table_name}({table_key_type} id);
    ''',
    "class_all_entries_getter": '''
        static std::unordered_map<{table_key_type},{table_name}> GetAll{table_name_plural}();
''',
"class_ctor_implement" : '''
        bool TableManager::LoadDataFor{table_name}(std::function<std::string(std::string)> dataProvider)
        {{
            std::string dataStr = dataProvider("{table_name}");
            std::vector<std::string> dataArr = splitstr(dataStr, '\\n');
            for (auto str : dataArr)
            {{
                if (str.empty())
                {{
                    continue;
                }}
                {table_name} table = {table_name}(new DataBuffer(str));
                dict{table_name}.emplace(table.{table_key_name}, table);
            }}
            return true;
        }}
''',
    "class_entry_getter_implement": '''
        {table_name} TableManager::Get{table_name}({table_key_type} id)
        {{
            std::unordered_map<int, {table_name}>::iterator o = dict{table_name}.find(id);
            if (o != dict{table_name}.end())
            {{
                return o->second;
            }}
            return nullptr;
        }}
    ''',
    "class_all_entries_getter_implement": '''
        std::unordered_map<{table_key_type},{table_name}> TableManager::GetAll{table_name_plural}()
        {{
            return dict{table_name};
        }}
''',
    "class_ctor_entry": '''
            LoadDataFor{table_name}(dataProvider);
''',
    "manager": '''
#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>
{name_space_begin}

    {class_entry_declares}

    class TableManager
    {{
        private:
        {class_dict_entries}

        public:
        static bool LoadData(std::function<std::string(std::string)> dataProvider);

        {class_entry_getters}

        {class_all_entries_getters}

        {class_ctor_functions}
    }};

{name_space_end}

''',
"manager_implement": '''
#include <string>
#include <vector>
#include <unordered_map>
#include "TableManager.h"
#include "DataBuffer.h"

{class_entry_includes}
{name_space_begin}

    {class_dict_entries_initialize}

    std::vector<std::string> splitstr(const std::string& str, const char sep = ',')
    {{
        std::vector<std::string> result = std::vector<std::string>();
        int start = 0;
        int end = str.find(sep);
        while (end != -1)
        {{
            result.push_back(str.substr(start, end - start));
            start = end + 1;
            end = str.find(sep, start);
        }}
        result.push_back(str.substr(start, end - start));
        return result;
    }}

    std::vector<std::string> splitstr(const std::string& str, const std::string sep = ",")
    {{
        std::vector<std::string> result = std::vector<std::string>();
        int start = 0;
        int end = str.find(sep);
        int seplen = sep.length();
        while (end != -1)
        {{
            result.push_back(str.substr(start, end - start));
            start = seplen;
            end = str.find(sep, start);
        }}
        result.push_back(str.substr(start, end - start));
        return result;
    }}

    {class_entry_getters_implement}

    {class_all_entries_getters_implement}

    bool TableManager::LoadData(std::function<std::string(std::string)> dataProvider)
    {{
        {class_ctor_entries}
        return true;
    }}

    {class_ctor_functions_implement}

{name_space_end}

''',
    "buffer": '''
#pragma once
#include <string>

{name_space_begin}

    class DataBuffer
    {{
        private:

            std::string data;
            int index;

        public:
            DataBuffer(std::string source);

            std::string ReadRaw();

            int ReadInt();

            long ReadLong();

            float ReadFloat();

            double ReadDouble();

            bool ReadBool();

            std::string ReadString();
    }};

{name_space_end}

''',

"buffer_implement": '''
#include <string>
#include "DataBuffer.h"

{name_space_begin}

    static const char* strN = "{table_special_str_n}";
    static const char* strS = "{table_special_str_s}";

    std::string replacestr(std::string rawstr, std::string oldstr, std::string newstr)
    {{
        std::string dst_str = rawstr;
        std::string::size_type pos = 0;
        while ((pos = dst_str.find(oldstr)) != std::string::npos)
        {{
            dst_str.replace(pos, oldstr.length(), newstr);
        }}
        return dst_str;
    }}

    DataBuffer::DataBuffer(std::string source)
    {{
        this->data = source;
        this->index = 0;
    }}

    std::string DataBuffer::ReadRaw()
    {{
        int pos = index;
        while (pos < this->data.length() && this->data[pos] != ',')
        {{
            pos++;
        }}
        std::string ret = this->data.substr(index, pos - index);
        index = pos + 1;
        return ret;
    }}

    int DataBuffer::ReadInt()
    {{
        return stoi(ReadRaw());
    }}

    long DataBuffer::ReadLong()
    {{
        return stol(ReadRaw());
    }}

    float DataBuffer::ReadFloat()
    {{
        return stof(ReadRaw());
    }}

    double DataBuffer::ReadDouble()
    {{
        return stod(ReadRaw());
    }}

    bool DataBuffer::ReadBool()
    {{
        std::string raw = ReadRaw();
        if (raw == "true")
        {{
            return true;
        }}

        for (int i = 0; i < raw.length(); ++i)
        {{
            raw[i] = tolower(i);
        }}

        return raw == "true";
    }}

    std::string DataBuffer::ReadString()
    {{
        std::string s = ReadRaw();
        s = replacestr(s, strN, "\\n");
        s = replacestr(s, strS, ",");
        return s;
    }}

{name_space_end}

'''
}


class CppWriter(TableWriter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.source_file_ext = self.get_script_file_ext()
        self.header_file_ext = self.get_header_file_ext()

    def get_type_name(self, field):
        if isinstance(field, FieldList):
            return f"std::vector<{self.get_type_name(field.list_element_type)}>"
        elif isinstance(field, FieldDictionary):
            return f"std::unordered_map<{self.get_type_name(field.dict_key_type)},{self.get_type_name(field.dict_value_type)}>"
        elif isinstance(field, FieldStruct):
            return f"{field.field_def}*"
        return self.get_primitive_type_name(field.field_def)

    def convert_miscs(self, tables, template, arg_list):

        arg_list.update({
            "table_special_str_s": Table.special_str['\\,'],
            "table_special_str_n": Table.special_str['\n']
        })

        text0 = template["buffer"].format(**arg_list)
        text1 = template["buffer_implement"].format(**arg_list)
        self.write_config("DataBuffer" + self.header_file_ext, text0)
        self.write_config("DataBuffer" + self.source_file_ext, text1)

    def get_primitive_type_name(self, field_def):
        return field_def.replace("string", "std::string")

    def get_field_reader(self, field_info):
        if isinstance(field_info, FieldStruct):
            return self.get_struct_reader(field_info.field_def)
        elif isinstance(field_info, FieldEnum):
            return self.get_enum_reader(field_info.field_def)
        return self.get_primitive_reader(field_info.field_def)

    def get_primitive_reader(self, type_def):
        return "buffer->Read" + upper_camel_case(type_def) + "()"

    def get_struct_reader(self, type_def):
        return "new " + type_def + "(buffer)"

    def get_enum_reader(self, type_def):
        return f"({type_def})buffer.ReadInt()"

    def get_field_ctor(self, field, index, template):
        field_args = {
            "field_name": field.field_name,
            "field_type": self.get_primitive_type_name(field.field_def),
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
        class_internal_types_implement = ""
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
            "class_internal_types": class_internal_types,
            "class_internal_types_implement": class_internal_types_implement,
        }

        table_args.update(arg_list)

        class_entry_declares = template["class_entry_declare"].format(**table_args)
        class_entry_includes = template["class_entry_include"].format(**table_args)
        class_ctor_functions = template["class_ctor"].format(**table_args)
        class_ctor_functions_implement = template["class_ctor_implement"].format(**table_args)
        class_dict_entries = template["class_dict_entry"].format(**table_args)
        class_dict_entries_initialize = template["class_dict_entry_initialize"].format(**table_args)
        class_ctor_entries = template["class_ctor_entry"].format(**table_args)
        class_entry_getters = template["class_entry_getter"].format(**table_args)
        class_entry_getters_implement = template["class_entry_getter_implement"].format(**table_args)
        class_all_entries_getters = template["class_all_entries_getter"].format(**table_args)
        class_all_entries_getters_implement = template["class_all_entries_getter_implement"].format(**table_args)

        arg_list["class_entry_declares"] += class_entry_declares
        arg_list["class_entry_includes"] += class_entry_includes
        arg_list["class_dict_entries"] += class_dict_entries
        arg_list["class_dict_entries_initialize"] += class_dict_entries_initialize
        arg_list["class_ctor_entries"] += class_ctor_entries
        arg_list["class_ctor_functions"] += class_ctor_functions
        arg_list["class_ctor_functions_implement"] += class_ctor_functions_implement
        arg_list["class_entry_getters"] += class_entry_getters
        arg_list["class_entry_getters_implement"] += class_entry_getters_implement
        arg_list["class_all_entries_getters"] += class_all_entries_getters
        arg_list["class_all_entries_getters_implement"] += class_all_entries_getters_implement

        text0 = template["class_declare"].format(**table_args)
        text1 = template["class_implement"].format(**table_args)
        self.write_config(f"{table_name}{self.header_file_ext}", text0)
        self.write_config(f"{table_name}{self.source_file_ext}", text1)

        text2 = self.pack_table_data(table)
        self.write_config_data(f"{table_name}.txt", text2)

    def convert_manager(self, tables, template, arg_list):

        arg_list["table_construct"] = ""
        text0 = template["manager"].format(**arg_list)
        text1 = template["manager_implement"].format(**arg_list)
        self.write_config("TableManager" + self.header_file_ext, text0)
        self.write_config("TableManager" + self.source_file_ext, text1)

    def get_script_file_ext(self):
        return '.cpp'

    def get_header_file_ext(self):
        return '.h'

    def write_all(self, tables):
        template = {}
        template.update(template_cpp)

        arg_list = {
            "class_entry_declares": "",
            "class_entry_includes": "",
            "class_ctor_functions": "",
            "class_ctor_functions_implement": "",
            "class_dict_entries": "",
            "class_dict_entries_initialize": "",
            "class_ctor_entries": "",
            "class_entry_getters": "",
            "class_entry_getters_implement": "",
            "class_all_entries_getters": "",
            "class_all_entries_getters_implement": "",
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
    EasyConverter.convert(TableReader(**parsed_args), CppWriter(**parsed_args))
