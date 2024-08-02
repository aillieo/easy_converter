




package EasyConverter;

import java.util.HashMap;
import java.util.ArrayList;

public class Buff
{
    public final int id;
    public final String name;

    public Buff(DataBuffer buffer)
    {
                this.id = buffer.ReadInt();
                this.name = buffer.ReadString();
    }

    @Override
    public String toString()
    {
        return "";
    }


}