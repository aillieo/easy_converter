
#include <string>
#include <vector>
#include <unordered_map>
#include "TableManager.hpp"
#include "DataBuffer.hpp"

     #include "Buff.hpp"
     #include "Hero.hpp"
     #include "NPCHero.hpp"
     #include "Skill.hpp"

namespace EasyConverter{

            std::unordered_map<int,Buff> TableManager::dictBuff = std::unordered_map<int,Buff>();
            std::unordered_map<int,Hero> TableManager::dictHero = std::unordered_map<int,Hero>();
            std::unordered_map<int,NPCHero> TableManager::dictNPCHero = std::unordered_map<int,NPCHero>();
            std::unordered_map<int,Skill> TableManager::dictSkill = std::unordered_map<int,Skill>();

    std::vector<std::string> splitstr(const std::string& str, const char sep = ',')
    {
        std::vector<std::string> result = std::vector<std::string>();
        int start = 0;
        int end = str.find(sep);
        while (end != -1)
        {
            result.push_back(str.substr(start, end - start));
            start = end + 1;
            end = str.find(sep, start);
        }
        result.push_back(str.substr(start, end - start));
        return result;
    }

    std::vector<std::string> splitstr(const std::string& str, const std::string sep = ",")
    {
        std::vector<std::string> result = std::vector<std::string>();
        int start = 0;
        int end = str.find(sep);
        int seplen = sep.length();
        while (end != -1)
        {
            result.push_back(str.substr(start, end - start));
            start = seplen;
            end = str.find(sep, start);
        }
        result.push_back(str.substr(start, end - start));
        return result;
    }

    bool TableManager::LoadData(std::function<std::string(std::string)> dataProvider)
    {
            LoadDataForBuff(dataProvider);
            LoadDataForHero(dataProvider);
            LoadDataForNPCHero(dataProvider);
            LoadDataForSkill(dataProvider);

        return true;
    }

            bool TableManager::LoadDataForBuff(std::function<std::string(std::string)> dataProvider)
            {
                std::string dataStr = dataProvider("Buff");
                std::vector<std::string> dataArr = splitstr(dataStr, '\\n');
                for (auto str : dataArr)
                {
                    if (str.empty())
                    {
                        continue;
                    }
                    Buff table = Buff(new DataBuffer(str));
                    dictBuff.emplace(table.id, table);
                }
                return true;
            }
            bool TableManager::LoadDataForHero(std::function<std::string(std::string)> dataProvider)
            {
                std::string dataStr = dataProvider("Hero");
                std::vector<std::string> dataArr = splitstr(dataStr, '\\n');
                for (auto str : dataArr)
                {
                    if (str.empty())
                    {
                        continue;
                    }
                    Hero table = Hero(new DataBuffer(str));
                    dictHero.emplace(table.id, table);
                }
                return true;
            }
            bool TableManager::LoadDataForNPCHero(std::function<std::string(std::string)> dataProvider)
            {
                std::string dataStr = dataProvider("NPCHero");
                std::vector<std::string> dataArr = splitstr(dataStr, '\\n');
                for (auto str : dataArr)
                {
                    if (str.empty())
                    {
                        continue;
                    }
                    NPCHero table = NPCHero(new DataBuffer(str));
                    dictNPCHero.emplace(table.id, table);
                }
                return true;
            }
            bool TableManager::LoadDataForSkill(std::function<std::string(std::string)> dataProvider)
            {
                std::string dataStr = dataProvider("Skill");
                std::vector<std::string> dataArr = splitstr(dataStr, '\\n');
                for (auto str : dataArr)
                {
                    if (str.empty())
                    {
                        continue;
                    }
                    Skill table = Skill(new DataBuffer(str));
                    dictSkill.emplace(table.id, table);
                }
                return true;
            }


        Buff TableManager::GetBuff(int id)
        {
            std::unordered_map<int, Buff>::iterator o = dictBuff.find(id);
            if (o != dictBuff.end())
            {
                return o->second;
            }
            return nullptr;
        }

        std::unordered_map<int,Buff> TableManager::GetAllBuffs()
        {
            return dictBuff;
        }


        Hero TableManager::GetHero(int id)
        {
            std::unordered_map<int, Hero>::iterator o = dictHero.find(id);
            if (o != dictHero.end())
            {
                return o->second;
            }
            return nullptr;
        }

        std::unordered_map<int,Hero> TableManager::GetAllHeroes()
        {
            return dictHero;
        }


        NPCHero TableManager::GetNPCHero(int id)
        {
            std::unordered_map<int, NPCHero>::iterator o = dictNPCHero.find(id);
            if (o != dictNPCHero.end())
            {
                return o->second;
            }
            return nullptr;
        }

        std::unordered_map<int,NPCHero> TableManager::GetAllNPCHeroes()
        {
            return dictNPCHero;
        }


        Skill TableManager::GetSkill(int id)
        {
            std::unordered_map<int, Skill>::iterator o = dictSkill.find(id);
            if (o != dictSkill.end())
            {
                return o->second;
            }
            return nullptr;
        }

        std::unordered_map<int,Skill> TableManager::GetAllSkills()
        {
            return dictSkill;
        }

}