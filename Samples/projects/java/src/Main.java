import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import EasyConverter.*;

public class Main {
    public static void main(String[] args) {
        TableManager.LoadData((name) -> {
            try (BufferedReader reader = new BufferedReader(new FileReader("./data/" + name + ".txt"))){
                String line;
                while ((line = reader.readLine()) != null) {
                    return line;
                }
            } catch (IOException e) {
                e.printStackTrace();
            }

            return null;
        });

        Hero hero = TableManager.GetHero(0);
        System.out.println("hero " + hero.name);
    }
}