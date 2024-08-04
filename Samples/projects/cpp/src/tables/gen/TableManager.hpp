
#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace EasyConverter{

        class Buff;
        class Hero;
        class NPCHero;
        class Skill;

    class TableManager
    {
        private:
                static std::unordered_map<int,Buff> dictBuff;
                static std::unordered_map<int,Hero> dictHero;
                static std::unordered_map<int,NPCHero> dictNPCHero;
                static std::unordered_map<int,Skill> dictSkill;

                static bool LoadDataForBuff(std::function<std::string(std::string)> dataProvider);
                static bool LoadDataForHero(std::function<std::string(std::string)> dataProvider);
                static bool LoadDataForNPCHero(std::function<std::string(std::string)> dataProvider);
                static bool LoadDataForSkill(std::function<std::string(std::string)> dataProvider);

        public:
        static bool LoadData(std::function<std::string(std::string)> dataProvider);


            static Buff GetBuff(int id);
            static std::unordered_map<int,Buff>  GetAllBuffs();


            static Hero GetHero(int id);
            static std::unordered_map<int,Hero>  GetAllHeroes();


            static NPCHero GetNPCHero(int id);
            static std::unordered_map<int,NPCHero>  GetAllNPCHeroes();


            static Skill GetSkill(int id);
            static std::unordered_map<int,Skill>  GetAllSkills();

    };
}