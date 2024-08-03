local TableManager = require("src/tables.gen/TableManager")

local hero = TableManager.GetHero(1001)
for k, v in pairs(hero) do
    print(k, v)
end
