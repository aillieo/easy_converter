
#pragma once
#include <string>
#include <vector>
#include <unordered_map>
class DataBuffer;
namespace EasyConverter {


        class Weapon
        {
            public:
                    std::string name;
                    int score;

                Weapon(DataBuffer* buffer);

                std::string toString();
        };



        enum class State
        {
                Locked = 1,
                Available = 2,
        };

    class Hero
    {
    public:

            int id;
            std::string name;
            int quality;
            std::vector<int> skills;
            std::unordered_map<std::string,int> attribute;
            Weapon weapon;
            State state;

        Hero(DataBuffer* buffer);

        std::string toString();
    };
}