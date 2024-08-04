
#pragma once
#include <string>
#include <vector>
#include <unordered_map>
class DataBuffer;
namespace EasyConverter {



    class Buff
    {
    public:

            int id;
            std::string name;

        Buff(DataBuffer* buffer);

        std::string toString();
    };
}