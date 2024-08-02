




package EasyConverter;

import java.util.HashMap;
import java.util.ArrayList;

public class Skill
{
    public final int id;
    public final String name;
    public final int cd;
    public final HashMap<Integer,Integer> buff_probability;

    public Skill(DataBuffer buffer)
    {
                this.id = buffer.ReadInt();
                this.name = buffer.ReadString();
                this.cd = buffer.ReadInt();
                    this.buff_probability = new HashMap<Integer,Integer>();
    int buff_probabilityLen = buffer.ReadInt();
    for(int i = 0; i < buff_probabilityLen; ++i)
    {
        var key = buffer.ReadInt();
        var value = buffer.ReadInt();
        this.buff_probability.put(key, value);
    }

    }

    @Override
    public String toString()
    {
        return "";
    }


}