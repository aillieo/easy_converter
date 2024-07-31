



using System.Collections.Generic;

namespace EasyConverter
{
    public class NPCHero
    {
        public readonly int id;
        public readonly string name;
        public readonly int quality;
        public readonly List<int> skills;
        public readonly bool display;

        public NPCHero(DataBuffer buffer)
        {
                    this.id = buffer.ReadInt();
                    this.name = buffer.ReadString();
                    this.quality = buffer.ReadInt();
                        this.skills = new List<int>();
    int skillsLen = buffer.ReadInt();
    for(int i = 0; i < skillsLen; ++i)
    {
        var item = buffer.ReadInt();
        this.skills.Add(item);
    }

                    this.display = buffer.ReadBool();
        }

        public override string ToString()
        {
            return "";
        }


    }
}