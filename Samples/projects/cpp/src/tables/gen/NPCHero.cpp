










#include "DataBuffer.h"
#include "NPCHero.hpp"
namespace EasyConverter{
    NPCHero::NPCHero(DataBuffer* buffer)
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

                this->display = buffer->ReadBool();
    }

    std::string NPCHero::toString()
    {
        return "";
    }

}