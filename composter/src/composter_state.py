import hyapi, math
import composter_constants as cc

def get_bz_price(id: str):
    bz_data = hyapi.get_bz_data()
    if not bz_data.get(id):
        raise KeyError(f"Invalid input: {id}")
    return bz_data[id]["quick_status"]["buyPrice"]

class ComposterState:
    def __init__(self, speed, multi_drop, fuel_cap, organic_matter_cap, cost_reduction, speed_attribute):
        self.speed = speed
        self.multi_drop = multi_drop
        self.fuel_cap = fuel_cap
        self.organic_matter_cap = organic_matter_cap
        self.cost_reduction = cost_reduction
        self.speed_attribute = speed_attribute
        
    def get_value(self, type: str):
        return cc.UPGRADE_BASE[type] + cc.UPGRADE_INCREASES[type] * getattr(self, type)
        
    def sim_composter(self):
        spd, md, fc, omc, cr, att = [self.get_value(x) for x in cc.UPGRADE_TYPES]
                
        time = 0
        output = 0
        
        fuel_level = fc-cc.BASE_FUEL_COST*(1-cr)
        organic_matter_level = omc-cc.BASE_ORGANIC_MATTER_COST*(1-cr)
        
        while fuel_level >= 0 and organic_matter_level >= 0:
            fuel_level -= cc.BASE_FUEL_COST*(1-cr)
            organic_matter_level -= cc.BASE_ORGANIC_MATTER_COST*(1-cr)
            time += (cc.BASE_CRAFT_TIME/spd)/att
            output += md
        
        return time, output
    
    
    def get_fuel_used_hr(self):
        return (cc.BASE_FUEL_COST*(1-self.get_value("cost_reduction"))*self.get_value("speed")*self.get_value("speed_attribute")*3600)/cc.BASE_CRAFT_TIME
    
    def get_fuel_items_hr(self, fuel_source: str):
        return (self.get_fuel_used_hr()/cc.FUEL_SOURCES[fuel_source]["value"])*cc.FUEL_SOURCES[fuel_source].get("count", 1)
    
    def get_fuel_cost_hr(self, fuel_source: str):
        return get_bz_price(fuel_source)*self.get_fuel_items_hr(fuel_source)
        
    def get_fuel_items_refill(self, fuel_source: str):
        return math.floor(self.get_value("fuel_cap")/cc.FUEL_SOURCES[fuel_source]["value"])*cc.FUEL_SOURCES[fuel_source].get("count", 1)
    
    def get_fuel_cost_refill(self, fuel_source: str):
        return get_bz_price(fuel_source)*self.get_fuel_items_refill(fuel_source)
    
    def get_matter_used_hr(self):
        return (cc.BASE_ORGANIC_MATTER_COST*(1-self.get_value("cost_reduction"))*self.get_value("speed")*self.get_value("speed_attribute")*3600)/cc.BASE_CRAFT_TIME
    
    def get_matter_items_hr(self, matter_source: str):
        return (self.get_matter_used_hr()/cc.ORGANIC_MATTER_SOURCES[matter_source]["value"])*cc.ORGANIC_MATTER_SOURCES[matter_source].get("count", 1)
    
    def get_matter_cost_hr(self, matter_source: str):
        return get_bz_price(matter_source)*self.get_matter_items_hr(matter_source)
    
    def get_matter_items_refill(self, matter_source: str):
        return math.floor(self.get_value("organic_matter_cap")/cc.ORGANIC_MATTER_SOURCES[matter_source]["value"])*cc.ORGANIC_MATTER_SOURCES[matter_source].get("count", 1)
    
    def get_matter_cost_refill(self, matter_source: str):
        return get_bz_price(matter_source)*self.get_matter_items_refill(matter_source)
    
    def get_compost_generated_hr(self):
        time, output = self.sim_composter()
        return 3600*output/time
    
    def get_compost_value_hr(self):
        return get_bz_price("COMPOST")*self.get_compost_generated_hr()
    
    def get_compost_value_refill(self):
        return get_bz_price("COMPOST")*self.sim_composter()[1]
    
    def get_profit_hr(self, fuel_source: str, matter_source: str):
        return self.get_compost_value_hr()-self.get_fuel_cost_hr(fuel_source)-self.get_matter_cost_hr(matter_source)
    
    def get_profit_refill(self, fuel_source: str, matter_source: str):
        return self.get_compost_value_refill()-self.get_fuel_cost_refill(fuel_source)-self.get_matter_cost_refill(matter_source)
    
    def is_maxed(self, *upgrades: str):
        for upg in upgrades:
            if getattr(self, upg) != cc.UPGRADE_CAP[upg]:
                return False
        return True