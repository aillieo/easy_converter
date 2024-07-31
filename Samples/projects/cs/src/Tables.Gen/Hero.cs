



using System.Collections.Generic;

namespace EasyConverter
{
    public class Hero
    {
        public readonly int id;
        public readonly string name;
        public readonly int quality;
        public readonly List<int> skills;
        public readonly Dictionary<string,int> attribute;
        public readonly Weapon weapon;
        public readonly State state;

        public Hero(DataBuffer buffer)
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

                        this.attribute = new Dictionary<string,int>();
    int attributeLen = buffer.ReadInt();
    for(int i = 0; i < attributeLen; ++i)
    {
        var key = buffer.ReadString();
        var value = buffer.ReadInt();
        this.attribute.Add(key, value);
    }

                    this.weapon = new Weapon(buffer);
                    this.state = buffer.ReadEnum<State>();
        }

        public override string ToString()
        {
            return "";
        }


            public class Weapon
            {
                    public readonly string name;
                    public readonly int score;

                public Weapon(DataBuffer buffer)
                {
                        buffer.ReadString();
                        buffer.ReadInt();
                }

                public override string ToString()
                {
                    return "";
                }
            }


            public enum State
            {
                    Locked = 1,
                    Available = 2,
            }
    }
}