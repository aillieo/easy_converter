
#pragma once
#include <string>
#include <vector>
#include <unordered_map>
class DataBuffer;
namespace EasyConverter {



    class NPCHero
    {
    public:

            int id;
            std::string name;
            int quality;
            std::vector<int> skills;
            bool display;

        NPCHero(DataBuffer* buffer);

        std::string toString();
    };
}