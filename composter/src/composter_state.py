import hyapi, math
import composter_constants as cc
from typing import Tuple


class ComposterState:
    def __init__(self, speed: int = 0, multi_drop: int = 0, fuel_cap: int = 0, organic_matter_cap: int = 0, cost_reduction: int = 0, speed_attribute: int = 0):
        self.speed = speed
        self.multi_drop = multi_drop
        self.fuel_cap = fuel_cap
        self.organic_matter_cap = organic_matter_cap
        self.cost_reduction = cost_reduction
        self.speed_attribute = speed_attribute
        
    def get_value(self, type: str) -> float:
        return cc.UPGRADE_BASE[type] + cc.UPGRADE_INCREASES[type] * getattr(self, type)
    
    
    def sim_composter(self) -> Tuple[float, float]:
        spd, md, fc, omc, cr, att = [self.get_value(x) for x in cc.UPGRADE_TYPES]
        
        fuel_cost = cc.BASE_FUEL_COST*(1-cr)
        organic_matter_cost = cc.BASE_ORGANIC_MATTER_COST*(1-cr)
        
        number_of_crafts = min(math.floor(fc/fuel_cost), math.floor(omc/organic_matter_cost))
        
        time = number_of_crafts * (cc.BASE_CRAFT_TIME/spd)/att
        output = number_of_crafts * md
        
        return time, output
    
    
    def get_fuel_used_hr(self) -> float:
        return (cc.BASE_FUEL_COST*(1-self.get_value("cost_reduction"))*self.get_value("speed")*self.get_value("speed_attribute")*3600)/cc.BASE_CRAFT_TIME
    
    
    def get_fuel_items_hr(self, fuel_source: str) -> float:
        return (self.get_fuel_used_hr()/cc.FUEL_SOURCES[fuel_source]["value"])*cc.FUEL_SOURCES[fuel_source].get("count", 1)
    
    
    def get_fuel_cost_hr(self, fuel_source: str) -> float:
        return hyapi.get_bz_price(fuel_source)*self.get_fuel_items_hr(fuel_source)
    
        
    def get_fuel_items_refill(self, fuel_source: str) -> int:
        return math.floor(self.get_value("fuel_cap")/cc.FUEL_SOURCES[fuel_source]["value"])*cc.FUEL_SOURCES[fuel_source].get("count", 1)
    
    
    def get_fuel_cost_refill(self, fuel_source: str) -> float:
        return hyapi.get_bz_price(fuel_source)*self.get_fuel_items_refill(fuel_source)
    
    
    def get_matter_used_hr(self) -> float:
        return (cc.BASE_ORGANIC_MATTER_COST*(1-self.get_value("cost_reduction"))*self.get_value("speed")*self.get_value("speed_attribute")*3600)/cc.BASE_CRAFT_TIME
    
    
    def get_matter_items_hr(self, matter_source: str) -> float:
        return (self.get_matter_used_hr()/cc.ORGANIC_MATTER_SOURCES[matter_source]["value"])*cc.ORGANIC_MATTER_SOURCES[matter_source].get("count", 1)
    
    
    def get_matter_cost_hr(self, matter_source: str) -> float:
        return hyapi.get_bz_price(matter_source)*self.get_matter_items_hr(matter_source)
    
    
    def get_matter_items_refill(self, matter_source: str) -> int:
        return math.floor(self.get_value("organic_matter_cap")/cc.ORGANIC_MATTER_SOURCES[matter_source]["value"])*cc.ORGANIC_MATTER_SOURCES[matter_source].get("count", 1)
    
    
    def get_matter_cost_refill(self, matter_source: str) -> float:
        return hyapi.get_bz_price(matter_source)*self.get_matter_items_refill(matter_source)
    
    
    def get_compost_generated_hr(self) -> float:
        time, output = self.sim_composter()
        return 3600*output/time
    
    
    def get_compost_value_hr(self) -> float:
        return hyapi.get_bz_price("COMPOST")*self.get_compost_generated_hr()
    
    
    def get_compost_value_refill(self) -> float:
        return hyapi.get_bz_price("COMPOST")*self.sim_composter()[1]
    
    
    def get_profit_hr(self, fuel_source: str, matter_source: str) -> float:
        return self.get_compost_value_hr()-self.get_fuel_cost_hr(fuel_source)-self.get_matter_cost_hr(matter_source)
    
    
    def get_profit_refill(self, fuel_source: str, matter_source: str) -> float:
        return self.get_compost_value_refill()-self.get_fuel_cost_refill(fuel_source)-self.get_matter_cost_refill(matter_source)
    
    
    def is_maxed(self, *upgrades: str) -> bool:
        for upg in upgrades if upgrades else cc.UPGRADE_TYPES:
            if getattr(self, upg) != cc.UPGRADE_CAP[upg]:
                return False
        return True