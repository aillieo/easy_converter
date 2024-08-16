using System.Collections.Generic;
using System;
using System.Globalization;

namespace EasyConverter
{
    public class DataBuffer
    {
        private static readonly string strN = ";l/~";
        private static readonly string strS = ":l/~";

        private string data;
        private int index;

        public DataBuffer(string source)
        {
            this.data = source;
            this.index = 0;
        }

        private string ReadRaw()
        {
            int pos = index;
            while (pos < this.data.Length && this.data[pos] != ',')
            {
                pos++;
            }
            string ret = this.data.Substring(index, pos - index);
            index = pos + 1;
            return ret;
        }

        public int ReadInt()
        {
            return int.Parse(ReadRaw(), CultureInfo.InvariantCulture);
        }

        public long ReadLong()
        {
            return long.Parse(ReadRaw(), CultureInfo.InvariantCulture);
        }

        public float ReadFloat()
        {
            return float.Parse(ReadRaw(), CultureInfo.InvariantCulture);
        }

        public double ReadDouble()
        {
            return double.Parse(ReadRaw(), CultureInfo.InvariantCulture);
        }

        public bool ReadBool()
        {
            return ReadRaw().ToLower() == "true";
        }

        public string ReadString()
        {
            return ReadRaw().Replace(strN, "\\n").Replace(strS, ",");
        }

        public T ReadEnum<T>() where T : struct
        {
            int value = ReadInt();
            return (T)Enum.ToObject(typeof(T), value);
        }
    }
}