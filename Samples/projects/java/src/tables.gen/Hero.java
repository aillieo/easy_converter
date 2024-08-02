




package EasyConverter;

import java.util.HashMap;
import java.util.ArrayList;

public class Hero
{
    public final int id;
    public final String name;
    public final int quality;
    public final ArrayList<Integer> skills;
    public final HashMap<String,Integer> attribute;
    public final Weapon weapon;
    public final State state;

    public Hero(DataBuffer buffer)
    {
                this.id = buffer.ReadInt();
                this.name = buffer.ReadString();
                this.quality = buffer.ReadInt();
                    this.skills = new ArrayList<Integer>();
    int skillsLen = buffer.ReadInt();
    for(int i = 0; i < skillsLen; ++i)
    {
        var item = buffer.ReadInt();
        this.skills.add(item);
    }

                    this.attribute = new HashMap<String,Integer>();
    int attributeLen = buffer.ReadInt();
    for(int i = 0; i < attributeLen; ++i)
    {
        var key = buffer.ReadString();
        var value = buffer.ReadInt();
        this.attribute.put(key, value);
    }

                this.weapon = new Weapon(buffer);
                this.state = State.valueOf(buffer.ReadInt());
    }

    @Override
    public String toString()
    {
        return "";
    }


        public class Weapon
        {
                public final String name;
                public final int score;

            public Weapon(DataBuffer buffer)
            {
                    this.name = buffer.ReadString();
                    this.score = buffer.ReadInt();
            }

            @Override
            public String toString()
            {
                return "";
            }
        }



        enum State
        {
                Locked(1),
                Available(2),
            ;

            public final int value;
            State(int v)
            {
                value = v;
            }

            public static State valueOf(int v)
            {
                switch (v)
                {
                        case 1: return Locked;
                        case 2: return Available;

                    default:
                        throw new EnumConstantNotPresentException(State.class, Integer.toString(v));
                }
            }
        }
}