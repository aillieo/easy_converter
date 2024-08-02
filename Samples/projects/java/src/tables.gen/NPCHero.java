




package EasyConverter;

import java.util.HashMap;
import java.util.ArrayList;

public class NPCHero
{
    public final int id;
    public final String name;
    public final int quality;
    public final ArrayList<Integer> skills;
    public final boolean display;

    public NPCHero(DataBuffer buffer)
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

                this.display = buffer.ReadBool();
    }

    @Override
    public String toString()
    {
        return "";
    }


}