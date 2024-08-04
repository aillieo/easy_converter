
#pragma once
#include <string>
#include <vector>
#include <unordered_map>
class DataBuffer;
namespace EasyConverter {



    class Skill
    {
    public:

            int id;
            std::string name;
            int cd;
            std::unordered_map<int,int> buff_probability;

        Skill(DataBuffer* buffer);

        std::string toString();
    };
}