local TableManager = {}

function TableManager.GetTable(tableName)
        return require("src/tables/gen/" .. tostring(tableName))
end


    function TableManager.GetAllBuffs()
        return TableManager.GetTable("Buff")
    end

    function TableManager.GetBuff(id)
        local tb = TableManager.GetTable("Buff")
        return tb and tb[id] or nil
    end


    function TableManager.GetAllHeroes()
        return TableManager.GetTable("Hero")
    end

    function TableManager.GetHero(id)
        local tb = TableManager.GetTable("Hero")
        return tb and tb[id] or nil
    end


    function TableManager.GetAllNPCHeroes()
        return TableManager.GetTable("NPCHero")
    end

    function TableManager.GetNPCHero(id)
        local tb = TableManager.GetTable("NPCHero")
        return tb and tb[id] or nil
    end


    function TableManager.GetAllSkills()
        return TableManager.GetTable("Skill")
    end

    function TableManager.GetSkill(id)
        local tb = TableManager.GetTable("Skill")
        return tb and tb[id] or nil
    end


return TableManager