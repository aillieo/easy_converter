
package EasyConverter;

import java.util.HashMap;

public class TableManager
{
    private static final String strN = "";
    private static final String strS = "";

            private static HashMap<Integer,Buff> dictBuff = new HashMap<Integer,Buff>();
            private static HashMap<Integer,Hero> dictHero = new HashMap<Integer,Hero>();
            private static HashMap<Integer,NPCHero> dictNPCHero = new HashMap<Integer,NPCHero>();
            private static HashMap<Integer,Skill> dictSkill = new HashMap<Integer,Skill>();

    public static boolean LoadData(FuncStr2Str dataProvider)
    {
            LoadDataForBuff(dataProvider);
            LoadDataForHero(dataProvider);
            LoadDataForNPCHero(dataProvider);
            LoadDataForSkill(dataProvider);

        return true;
    }

            private static boolean LoadDataForBuff(FuncStr2Str dataProvider)
            {
                String dataStr = dataProvider.invoke("Buff");
                String[] dataArr = dataStr.split("\n");
                for (String str : dataArr)
                {
                    if (str == null || str.equals(""))
                    {
                        continue;
                    }
                    Buff table = new Buff(new DataBuffer(str));
                    dictBuff.put(table.id, table);
                }
                return true;
            }
            private static boolean LoadDataForHero(FuncStr2Str dataProvider)
            {
                String dataStr = dataProvider.invoke("Hero");
                String[] dataArr = dataStr.split("\n");
                for (String str : dataArr)
                {
                    if (str == null || str.equals(""))
                    {
                        continue;
                    }
                    Hero table = new Hero(new DataBuffer(str));
                    dictHero.put(table.id, table);
                }
                return true;
            }
            private static boolean LoadDataForNPCHero(FuncStr2Str dataProvider)
            {
                String dataStr = dataProvider.invoke("NPCHero");
                String[] dataArr = dataStr.split("\n");
                for (String str : dataArr)
                {
                    if (str == null || str.equals(""))
                    {
                        continue;
                    }
                    NPCHero table = new NPCHero(new DataBuffer(str));
                    dictNPCHero.put(table.id, table);
                }
                return true;
            }
            private static boolean LoadDataForSkill(FuncStr2Str dataProvider)
            {
                String dataStr = dataProvider.invoke("Skill");
                String[] dataArr = dataStr.split("\n");
                for (String str : dataArr)
                {
                    if (str == null || str.equals(""))
                    {
                        continue;
                    }
                    Skill table = new Skill(new DataBuffer(str));
                    dictSkill.put(table.id, table);
                }
                return true;
            }


        public static Buff GetBuff(int id)
        {
            return dictBuff.getOrDefault(id, null);
        }


        public static Hero GetHero(int id)
        {
            return dictHero.getOrDefault(id, null);
        }


        public static NPCHero GetNPCHero(int id)
        {
            return dictNPCHero.getOrDefault(id, null);
        }


        public static Skill GetSkill(int id)
        {
            return dictSkill.getOrDefault(id, null);
        }

}