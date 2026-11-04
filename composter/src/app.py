import hyapi, copy, math
import composter_constants as cc
from composter_state import ComposterState
import streamlit as st
        
def st_get(key: str, default = None):
    return st.session_state.get(key, default)

def attr_stacks_to_level(stacks: int, rarity: str):
    if rarity not in cc.ATTRIBUTE_RARITIES:
        raise KeyError(f"Invalid input: {rarity}")
    stack_sum = 0
    level = 0
    while stack_sum <= stacks and level < 10:
        stack_sum += cc.ATTRIBUTE_STACKS_PER_LEVEL[rarity][level]
        if stack_sum <= stacks:
            level += 1
    return level, stack_sum - stacks


def init_session_state():
    if "api" not in st.session_state:
        st.session_state.api = { "bz": hyapi.get_bz_data(), }
    if "profile_id" not in st.session_state:
        st.session_state.profile_id = ""


def init_composter_data():
    if (st_get("last_profile") != st.session_state.profile_id) or st_get("reset_composter", False):
        for upgrade in cc.UPGRADE_TYPES:
            if cc.UPGRADE_USES_GENERAL[upgrade]:
                st.session_state[upgrade] = st.session_state.garden["composter_data"]["upgrades"].get(upgrade, 0)
        st.session_state["speed_attribute"] = st.session_state.attr.get("stacks", {}).get("compost_speed", 0)
        
        st.session_state.last_profile = st.session_state.profile_id
        
        
class ComposterStateFromSession(ComposterState):
    def __init__(self):
        super().__init__(*[st_get(upg, 0) for upg in cc.UPGRADE_TYPES])
        
    def get_fuel_cost_hr(self, fuel_source: str):
            return get_bz_price_cached(fuel_source)*self.get_fuel_items_hr(fuel_source)
        
    def get_fuel_cost_refill(self, fuel_source: str):
            return get_bz_price_cached(fuel_source)*self.get_fuel_items_refill(fuel_source)
        
    def get_matter_cost_hr(self, matter_source: str):
            return get_bz_price_cached(matter_source)*self.get_matter_items_hr(matter_source)
        
    def get_matter_cost_refill(self, matter_source: str):
            return get_bz_price_cached(matter_source)*self.get_matter_items_refill(matter_source)
        
    def get_compost_value_hr(self):
            return get_bz_price_cached("COMPOST")*self.get_compost_generated_hr()
        
    def get_compost_value_refill(self):
            return get_bz_price_cached("COMPOST")*self.sim_composter()[1]


def upg_to_target_uptime(uptime: int) -> ComposterState:
    state = ComposterStateFromSession()
    relevant_upg = ["fuel_cap", "organic_matter_cap", "cost_reduction"]
    while (state.sim_composter()[0] < uptime and not state.is_maxed(*relevant_upg)):
        initial_time = state.sim_composter()[0]
        best_value = float("inf")
        best_upg = state
        
        for upg in relevant_upg:
            if state.is_maxed(upg):
                continue
            
            temp = copy.deepcopy(state)
            setattr(temp, upg, getattr(temp, upg)+1)
            cost = coins_to_upgrade(*mats_to_upgrade(state, temp))
            dur = temp.sim_composter()[0]-initial_time
            
            if dur == 0:
                continue
            
            if cost/dur < best_value:
                best_value = cost/dur
                best_upg = temp
        
        if state != best_upg:
            state = best_upg
        else: return state
    
    return state


def mats_to_upgrade(state: ComposterState, upgraded: ComposterState):
    items = {}
    copper = 0
    for upg in cc.UPGRADE_TYPES:
        for i in range(getattr(state, upg), getattr(upgraded, upg)):
            id = cc.UPGRADE_COST[upg][i]["id"]
            count = cc.UPGRADE_COST[upg][i]["count"]
            
            gen_id = cc.UPGRADE_COST["general"][i]["id"]
            gen_count = cc.UPGRADE_COST["general"][i]["count"]
            
            copper += cc.UPGRADE_COST["general"][i]["copper"]
            items[id] = items.get(id, 0) + count
            items[gen_id] = items.get(gen_id, 0) + gen_count
    
    return items, copper
                
                
def coins_to_upgrade(items: dict, copper: int, copper_value: int = 0):
    total_cost = 0
    for item in items.keys():
        total_cost += get_bz_price_cached(item) * items[item]
    total_cost += copper * copper_value
    return total_cost
                
                
def numerize(val: int):
    if val >= 1000000000: return f"{round(val/1000000000, 1)}b"
    if val > 1000000: return f"{round(val/1000000, 1)}m"
    if val > 1000: return f"{round(val/1000, 1)}k"
    return round(val, 1)


def time_to_str(time: float):
    mins, secs = divmod(time, 60)
    hrs, mins = divmod(mins, 60)
    return f"{int(hrs)}:{int(mins):02d}:{int(secs):02d}"
        

def get_bz_price_cached(id: str):
    if not st.session_state.bz.get(id):
        raise KeyError(f"Invalid input: {id}")
    return st.session_state.bz[id]["quick_status"]["buyPrice"]


@st.cache_data(ttl=300)
def get_bz_cached():
    return hyapi.get_bz_data()    


@st.cache_data
def get_profiles_cached(ign: str):
    if not ign:
        raise KeyError(f"Invalid input: empty")
    uuid = hyapi.get_uuid(ign)
    profiles = hyapi.get_profiles(uuid)
    return uuid, profiles    


@st.cache_data(ttl=300)
def get_garden_cached(profile_id: str):
    if not profile_id:
        raise KeyError(f"Invalid input: empty")
    return hyapi.get_garden_data(profile_id)


def main():
    # DATA LOADING
    st.markdown("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>", unsafe_allow_html=True)
    
    init_session_state()
    
    profile_col1, profile_col2 = st.columns(2)
    
    with profile_col1:
        st.text_input("IGN:", max_chars=16, value="bigman7305", key="ign")
    with profile_col2:
        uuid, profiles = get_profiles_cached(st.session_state.ign)
        st.selectbox("Profile:", [profile["cute_name"] for profile in profiles], key="selected_profile")
        st.session_state.profile_id = hyapi.get_profile_id(st.session_state.selected_profile, uuid, profiles=profiles)
        for profile in range(0, len(profiles)):
            if profiles[profile]["profile_id"] == st.session_state.profile_id:
                profile_data = profiles[profile]
    
    st.session_state.attr = profile_data["members"][uuid].get("attributes", {}) # type: ignore
    st.session_state.bz = get_bz_cached()
    st.session_state.garden = get_garden_cached(st.session_state.profile_id)
    init_composter_data()
    
    # WEBSITE CONTENT
    st.title("Composter Tools")
    
    values_col, content_col = st.columns([1, 4])
    
    with values_col:
        st.tabs([""])
        for upgrade in cc.UPGRADE_TYPES:
            st.number_input(
                cc.UPGRADE_NAMES[upgrade]+":", 
                min_value=0,
                max_value=cc.UPGRADE_CAP[upgrade],
                key=upgrade
            )
        st.button("Reset", key="reset_composter")
    
    with content_col:
        upgrade_tab, sim_tab, uptime_tab, bottomline_tab \
            = st.tabs(["Best Value Upgrades", "Compost Rates", "Target Uptime Upgrades", "Bottom Line Upgrades"])
        with upgrade_tab:
            valid_upgrades = []
            for upgrade in cc.UPGRADE_TYPES:
                if not ComposterStateFromSession().is_maxed(upgrade):
                    valid_upgrades.append(upgrade)
                    
            upgrade_states = {}
            for upgrade in valid_upgrades:
                upgrade_states[upgrade] = {
                    
                }
                    
        with sim_tab:
            with st.columns(1, vertical_alignment="center", border=True)[0]:
                left, mid, right = st.columns([1, 1, 1])
                
                state = ComposterStateFromSession()
                
                with mid:
                    with st.columns(1, border=True)[0]:
                        st.image("https://hypixelskyblock.minecraft.wiki/images/Composter_%28system%29.png?77ef3")
                
                with left:
                    st.markdown(f"### :green[Fuel Cap]<br>{state.get_value("fuel_cap")}", text_alignment="center", unsafe_allow_html=True)
                    st.markdown(f"### :yellow[Organic Matter Cap]<br>{state.get_value("organic_matter_cap")}", text_alignment="center", unsafe_allow_html=True)
                
                with right:
                    time, output = state.sim_composter()
                    st.markdown(f"### :blue[Runtime]<br>{time_to_str(time)}", text_alignment="center", unsafe_allow_html=True)
                    st.markdown(f"### :red[Avg. Compost Per Hour]<br>{round(state.get_compost_generated_hr(), 2)}", text_alignment="center", unsafe_allow_html=True)
                
                matter = st_get("matter", next(iter(cc.ORGANIC_MATTER_SOURCES)))
                fuel = st_get("fuel", next(iter(cc.FUEL_SOURCES)))
                
                st.markdown(f"## :rainbow[Profit Per Hour]: :orange[{round(state.get_profit_hr(fuel, matter), 1):,}]<br>:blue[Profit Per Refill]: :orange[{round(state.get_profit_refill(fuel, matter), 1):,}]", text_alignment="center", unsafe_allow_html=True)
                
                with st.columns(1, border=True)[0]:
                    matter_col, fuel_col = st.columns(2)
                    
                    with matter_col:
                        st.selectbox("Organic Matter Source:", cc.ORGANIC_MATTER_SOURCES.keys(), format_func=lambda x: cc.ORGANIC_MATTER_SOURCES[x]["pretty_print"], key="matter")
                        
                        txt_col = st.columns([5, 1])
                        with txt_col[0]:
                            f"Refill Cost: :orange[{round(state.get_matter_cost_refill(matter), 1):,}]"
                        with txt_col[1]:
                            f":gray[x{state.get_matter_items_refill(matter)}]"
                    
                    with fuel_col:
                        st.selectbox("Fuel Source:", cc.FUEL_SOURCES.keys(), format_func=lambda x: cc.FUEL_SOURCES[x]["pretty_print"], key="fuel")
                        
                        txt_col = st.columns([5, 1])
                        with txt_col[0]:
                            f"Refill Cost: :orange[{round(state.get_fuel_cost_refill(fuel), 1):,}]"
                        with txt_col[1]:
                            f":gray[x{state.get_fuel_items_refill(fuel)}]"
                
        
        with uptime_tab:
            with st.columns(1, vertical_alignment="center", border=True)[0]:
                cols = st.columns([11, 5], vertical_alignment="center")
                with cols[0]:
                    target_uptime = st.time_input("Target Uptime:", "04:00:00")
                    uptime_seconds = target_uptime.hour*3600 + target_uptime.minute*60 + target_uptime.second
                    upg_state = upg_to_target_uptime(uptime_seconds)
                    
                    cols2 = st.columns(3, border=True, vertical_alignment="center")
                    
                    with cols2[0]:
                        st.markdown(f"###### :green[Fuel Cap]<br>{upg_state.fuel_cap}", text_alignment="center", unsafe_allow_html=True)
                    
                    with cols2[1]:
                        st.markdown(f"###### :yellow[Organic Matter Cap]<br>{upg_state.organic_matter_cap}", text_alignment="center", unsafe_allow_html=True)
                    
                    with cols2[2]:
                        st.markdown(f"###### :orange[Cost Reduction]<br>{upg_state.cost_reduction}", text_alignment="center", unsafe_allow_html=True)
                    
                with cols[1]:
                    with st.columns(1, border=True)[0]:
                        st.image("https://hypixelskyblock.minecraft.wiki/images/Composter_%28system%29.png?77ef3")
                
                with st.columns(1, border=True, vertical_alignment="center")[0]:
                    items, copper = mats_to_upgrade(ComposterStateFromSession(), upg_state)
                    total_cost = 0
                    for item in items.keys():
                        total_cost += get_bz_price_cached(item) * items[item]
                        
                    st.markdown(f"## :rainbow[Cost of Upgrades]: :orange[{round(total_cost, 1):,}]<br>Copper Cost: :red[{copper:,}]", text_alignment="center", unsafe_allow_html=True)
                    
                    with st.expander("Items"):
                        for id in items.keys():
                            with st.columns(1, border=True, vertical_alignment="center")[0]:
                                price = get_bz_price_cached(id)
                                cols3 = st.columns([7, 2, 2, 3])
                                with cols3[0]:
                                    st.markdown(f"{cc.UPGRADE_SOURCES[id]["pretty_print"]}", text_alignment="left")
                                with cols3[1]:
                                    st.markdown(f":gray[x]{items[id]}", text_alignment="right")
                                with cols3[2]:
                                    st.markdown(f":orange[{numerize(items[id]*price)}]", text_alignment="right")
                                with cols3[3]:
                                    st.markdown(f":gray[({numerize(price)} ea.)]", text_alignment="right")
                                    
        with bottomline_tab:
            pass

if __name__ == "__main__":
    main()