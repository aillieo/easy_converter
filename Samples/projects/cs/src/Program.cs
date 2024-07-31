using System;
using System.Collections.Generic;
using System.IO;
using EasyConverter;

public class Program
{
    private static void Main(string[] args)
    {
        TableManager.LoadData(name => File.ReadAllText($"./data/{name}.txt"));

        var heroes = TableManager.GetAllHeroes();
        Console.WriteLine("heroes " + heroes.Count);
    }
}