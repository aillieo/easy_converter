


using System.Collections.Generic;

namespace EasyConverter
{
    public class Buff
    {
        public readonly int id;
        public readonly string name;

        public Buff(DataBuffer buffer)
        {
                    this.id = buffer.ReadInt();
                    this.name = buffer.ReadString();
        }

        public override string ToString()
        {
            return "";
        }


    }
}