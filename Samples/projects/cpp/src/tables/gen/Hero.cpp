










#include "DataBuffer.h"
#include "Hero.hpp"
namespace EasyConverter{
    Hero::Hero(DataBuffer* buffer)
    {
                this->id = buffer->ReadInt();
                this->name = buffer->ReadString();
                this->quality = buffer->ReadInt();
                    this->skills = new std::vector<int>();
    int skillsLen = buffer.ReadInt();
    for(int i = 0; i < skillsLen; ++i)
    {
        auto item = buffer->ReadInt();
        this->skills.add(item);
    }

                    this->attribute = new std::unordered_map<std::string,int>();
    int attributeLen = buffer.ReadInt();
    for(int i = 0; i < attributeLen; ++i)
    {
        auto key = buffer->ReadString();
        auto value = buffer->ReadInt();
        this->attribute.put(key, value);
    }

                this->weapon = new Weapon(buffer);
                this->state = State.valueOf(buffer.ReadInt());
    }

    std::string Hero::toString()
    {
        return "";
    }


        public Weapon::Weapon(DataBuffer buffer)
        {
                this->name = buffer->ReadString();
                this->score = buffer->ReadInt();
        }

        std::string Weapon::toString()
        {
            return "";
        }

}