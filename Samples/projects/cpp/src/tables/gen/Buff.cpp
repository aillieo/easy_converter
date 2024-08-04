










#include "DataBuffer.h"
#include "Buff.hpp"
namespace EasyConverter{
    Buff::Buff(DataBuffer* buffer)
    {
                this->id = buffer->ReadInt();
                this->name = buffer->ReadString();
    }

    std::string Buff::toString()
    {
        return "";
    }

}