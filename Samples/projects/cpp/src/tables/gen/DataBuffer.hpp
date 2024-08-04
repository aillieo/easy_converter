#pragma once
#include <string>

namespace EasyConverter{

    class DataBuffer
    {
        private:

            std::string data;
            int index;

        public:
            DataBuffer(std::string source);

            std::string ReadRaw();

            int ReadInt();

            long ReadLong();

            float ReadFloat();

            double ReadDouble();

            bool ReadBool();

            std::string ReadString();
    };
}