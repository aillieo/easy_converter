using System.Collections.Generic;
using System;

namespace EasyConverter
{
    public static class TableManager
    {
                    private static Dictionary<int,Buff> dictBuff = new Dictionary<int,Buff>();
                    private static Dictionary<int,Hero> dictHero = new Dictionary<int,Hero>();
                    private static Dictionary<int,NPCHero> dictNPCHero = new Dictionary<int,NPCHero>();
                    private static Dictionary<int,Skill> dictSkill = new Dictionary<int,Skill>();

        public static bool LoadData(Func<string,string> dataProvider)
        {
                LoadDataForBuff(dataProvider);
                LoadDataForHero(dataProvider);
                LoadDataForNPCHero(dataProvider);
                LoadDataForSkill(dataProvider);

            return true;
        }

                private static bool LoadDataForBuff(Func<string,string> dataProvider)
                {
                    string dataStr = dataProvider("Buff");
                    string[] dataArr = dataStr.Split('\n','\r');
                    foreach (var str in dataArr)
                    {
                        if (string.IsNullOrEmpty(str))
                        {
                            continue;
                        }
                        var table = new Buff(new DataBuffer(str));
                        dictBuff.Add(table.id, table);
                    }
                    return true;
                }
                private static bool LoadDataForHero(Func<string,string> dataProvider)
                {
                    string dataStr = dataProvider("Hero");
                    string[] dataArr = dataStr.Split('\n','\r');
                    foreach (var str in dataArr)
                    {
                        if (string.IsNullOrEmpty(str))
                        {
                            continue;
                        }
                        var table = new Hero(new DataBuffer(str));
                        dictHero.Add(table.id, table);
                    }
                    return true;
                }
                private static bool LoadDataForNPCHero(Func<string,string> dataProvider)
                {
                    string dataStr = dataProvider("NPCHero");
                    string[] dataArr = dataStr.Split('\n','\r');
                    foreach (var str in dataArr)
                    {
                        if (string.IsNullOrEmpty(str))
                        {
                            continue;
                        }
                        var table = new NPCHero(new DataBuffer(str));
                        dictNPCHero.Add(table.id, table);
                    }
                    return true;
                }
                private static bool LoadDataForSkill(Func<string,string> dataProvider)
                {
                    string dataStr = dataProvider("Skill");
                    string[] dataArr = dataStr.Split('\n','\r');
                    foreach (var str in dataArr)
                    {
                        if (string.IsNullOrEmpty(str))
                        {
                            continue;
                        }
                        var table = new Skill(new DataBuffer(str));
                        dictSkill.Add(table.id, table);
                    }
                    return true;
                }


            public static Dictionary<int,Buff> GetAllBuffs()
            {
                return dictBuff;
            }

            public static Buff GetBuff(int id)
            {
                if (dictBuff.TryGetValue(id, out var value))
                {
                    return value;
                }

                return default;
            }


            public static Dictionary<int,Hero> GetAllHeroes()
            {
                return dictHero;
            }

            public static Hero GetHero(int id)
            {
                if (dictHero.TryGetValue(id, out var value))
                {
                    return value;
                }

                return default;
            }


            public static Dictionary<int,NPCHero> GetAllNPCHeroes()
            {
                return dictNPCHero;
            }

            public static NPCHero GetNPCHero(int id)
            {
                if (dictNPCHero.TryGetValue(id, out var value))
                {
                    return value;
                }

                return default;
            }


            public static Dictionary<int,Skill> GetAllSkills()
            {
                return dictSkill;
            }

            public static Skill GetSkill(int id)
            {
                if (dictSkill.TryGetValue(id, out var value))
                {
                    return value;
                }

                return default;
            }

    }
}