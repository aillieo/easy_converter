










#include "DataBuffer.h"
#include "Skill.hpp"
namespace EasyConverter{
    Skill::Skill(DataBuffer* buffer)
    {
                this->id = buffer->ReadInt();
                this->name = buffer->ReadString();
                this->cd = buffer->ReadInt();
                    this->buff_probability = new std::unordered_map<int,int>();
    int buff_probabilityLen = buffer.ReadInt();
    for(int i = 0; i < buff_probabilityLen; ++i)
    {
        auto key = buffer->ReadInt();
        auto value = buffer->ReadInt();
        this->buff_probability.put(key, value);
    }

    }

    std::string Skill::toString()
    {
        return "";
    }

}