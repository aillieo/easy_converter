


using System.Collections.Generic;

namespace EasyConverter
{
    public class Skill
    {
        public readonly int id;
        public readonly string name;
        public readonly int cd;
        public readonly Dictionary<int, int> buff_probability;

        public Skill(DataBuffer buffer)
        {
                    this.id = buffer.ReadInt();
                    this.name = buffer.ReadString();
                    this.cd = buffer.ReadInt();
                        this.buff_probability = new Dictionary<int, int>();
    int buff_probabilityLen = buffer.ReadInt();
    for(int i = 0; i < buff_probabilityLen; ++i)
    {
        var key = buffer.ReadInt();
        var value = buffer.ReadInt();
        this.buff_probability.Add(key, value);
    }

        }

        public override string ToString()
        {
            return "";
        }


    }
}