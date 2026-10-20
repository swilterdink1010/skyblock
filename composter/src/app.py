import hyapi, copy, math
import composter_constants as cc
import streamlit as st


def init_session_state():
    if "api" not in st.session_state:
        st.session_state.api = { "bz": hyapi.get_bz_data, }
    if "profile_id" not in st.session_state:
        st.session_state.profile_id = ""


def init_composter_data():
    if (st.session_state.get("last_profile") != st.session_state.profile_id) or st.session_state.get("reset_composter", False):
        for upgrade in ["speed", "multi_drop", "fuel_cap", "organic_matter_cap", "cost_reduction"]:
            st.session_state[upgrade] = st.session_state.garden["composter_data"]["upgrades"].get(upgrade, 0)
        st.session_state.last_profile = st.session_state.profile_id
        
        
class ComposterState:
    def __init__(self, speed, multi_drop, fuel_cap, organic_matter_cap, cost_reduction):
        self.speed = speed
        self.multi_drop = multi_drop
        self.fuel_cap = fuel_cap
        self.organic_matter_cap = organic_matter_cap
        self.cost_reduction = cost_reduction
        
        
    def sim_composter(self):
        spd, md, fc, omc, cr = [calc_composter_value(x, getattr(self, x)) for x in cc.UPGRADE_TYPES]
                
        time = 0
        output = 0
        
        fuel_level = fc-cc.BASE_FUEL_COST*(1-cr)
        organic_matter_level = omc-cc.BASE_ORGANIC_MATTER_COST*(1-cr)
        
        while fuel_level >= 0 and organic_matter_level >= 0:
            fuel_level -= cc.BASE_FUEL_COST*(1-cr)
            organic_matter_level -= cc.BASE_ORGANIC_MATTER_COST*(1-cr)
            time += cc.BASE_CRAFT_TIME/spd
            output += md
        
        return time, output
        
    
    def is_maxed(self, *upgrades: str):
        for upg in upgrades:
            if getattr(self, upg) != 25:
                return False
        
        
class ComposterStateFromSession(ComposterState):
    def __init__(self):
        super().__init__(*[st.session_state.get(upg, 0) for upg in cc.UPGRADE_TYPES])
        
        
def calc_composter_value(upgrade: str, level: int = None): # type: ignore
    if level is None:
        level = st.session_state.get(upgrade, 0)
    return cc.UPGRADE_BASE[upgrade] + cc.UPGRADE_INCREASES[upgrade] * level


def upg_to_target_uptime(uptime: int) -> ComposterState:
    state = ComposterStateFromSession()
    relevant_upg = ["fuel_cap", "organic_matter_cap", "cost_reduction"]
    while (state.sim_composter()[0] < uptime and not state.is_maxed(*relevant_upg)):
        best_dur = 0
        best_upg = state
        
        for upg in relevant_upg:
            if state.is_maxed(upg):
                continue
            
            temp = copy.deepcopy(state)
            setattr(temp, upg, getattr(temp, upg)+1)
            dur = temp.sim_composter()[0]
            
            if dur > best_dur:
                best_dur = dur
                best_upg = temp
        
        state = best_upg
    
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
                


def time_to_str(time: float):
    mins, secs = divmod(time, 60)
    hrs, mins = divmod(mins, 60)
    return f"{int(hrs)}:{int(mins):02d}:{int(secs):02d}"
        

def get_bz_price(id: str):
    if not st.session_state.bz.get(id):
        raise KeyError(f"Invalid input")
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
        
    st.session_state.bz = get_bz_cached()
    st.session_state.garden = get_garden_cached(st.session_state.profile_id)
    init_composter_data()
    
    # WEBSITE CONTENT
    st.title("Composter Tools")
    
    values_col, content_col = st.columns([1, 4])
    
    with values_col:
        st.tabs([""])
        st.number_input("Composter Speed:", min_value=0, max_value=25, key="speed")
        st.number_input("Multi Drop:", min_value=0, max_value=25, key="multi_drop")
        st.number_input("Fuel Cap:", min_value=0, max_value=25, key="fuel_cap")
        st.number_input("Organic Matter Cap:", min_value=0, key="organic_matter_cap")
        st.number_input("Cost Reduction:", min_value=0, key="cost_reduction")
        st.button("Reset", key="reset_composter")
    
    with content_col:
        upgrade_tab, sim_tab, uptime_tab = st.tabs(["Best Value Upgrades", "Compost Rates", "Target Uptime Upgrades"])
        with upgrade_tab:
            pass
        
        with sim_tab:
            with st.columns(1, vertical_alignment="center", border=True)[0]:
                left, mid, right = st.columns([1, 1, 1])
                
                with mid:
                    with st.columns(1, border=True)[0]:
                        st.image("https://hypixelskyblock.minecraft.wiki/images/Composter_%28system%29.png?77ef3")
                
                with left:
                    st.markdown(f"### :green[Fuel Cap]<br>{calc_composter_value("fuel_cap")}", text_alignment="center", unsafe_allow_html=True)
                    st.markdown(f"### :yellow[Organic Matter Cap]<br>{calc_composter_value("organic_matter_cap")}", text_alignment="center", unsafe_allow_html=True)
                
                with right:
                    time, output = ComposterStateFromSession().sim_composter()
                    st.markdown(f"### :blue[Runtime]<br>{time_to_str(time)}", text_alignment="center", unsafe_allow_html=True)
                    compost_per_hr = output/(time/3600)
                    st.markdown(f"### :red[Avg. Compost Per Hour]<br>{round(compost_per_hr, 2)}", text_alignment="center", unsafe_allow_html=True)
                
                matter_upkeep_hr, fuel_upkeep_hr = 0, 0
                st.markdown(f"## :rainbow[Profit Per Hour]: :orange[{round((get_bz_price("COMPOST") * compost_per_hr)-matter_upkeep_hr-fuel_upkeep_hr, 1):,}]", text_alignment="center")
                
                with st.columns(1, border=True)[0]:
                    matter_col, fuel_col = st.columns(2)
                    
                    with matter_col:
                        matter = st.selectbox("Organic Matter Source:", cc.ORGANIC_MATTER_SOURCES.keys(), format_func=lambda x: cc.ORGANIC_MATTER_SOURCES[x]["pretty_print"])
                        
                        matter_used_per_hr = calc_composter_value("speed")*cc.BASE_ORGANIC_MATTER_COST*(1-calc_composter_value("cost_reduction"))
                        matter_items_per_hr = (matter_used_per_hr/cc.ORGANIC_MATTER_SOURCES[matter]["value"])*cc.ORGANIC_MATTER_SOURCES[matter].get("count", 1)

                        matter_upkeep_hr = get_bz_price(matter)*matter_items_per_hr
                        matter_upkeep = matter_upkeep_hr*time/3600
                        f"Upkeep: :orange[{round(matter_upkeep, 1):,}]"
                    
                    with fuel_col:
                        fuel = st.selectbox("Fuel Source:", cc.FUEL_SOURCES.keys(), format_func=lambda x: cc.FUEL_SOURCES[x]["pretty_print"])
                        
                        fuel_used_per_hr = calc_composter_value("speed")*cc.BASE_FUEL_COST*(1-calc_composter_value("cost_reduction"))
                        fuel_items_per_hr = (fuel_used_per_hr/cc.FUEL_SOURCES[fuel]["value"])*cc.FUEL_SOURCES[fuel].get("count", 1)
                    
                        fuel_upkeep_hr = get_bz_price(fuel)*fuel_items_per_hr
                        fuel_upkeep = fuel_upkeep_hr*time/3600
                        f"Upkeep: :orange[{round(fuel_upkeep, 1):,}]"
                
        
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
                        total_cost += get_bz_price(item) * items[item]
                        
                    st.markdown(f"## :rainbow[Cost of Upgrades]: :orange[{round(total_cost, 1):,}]<br>Copper Cost: :red[{copper:,}]", text_alignment="center", unsafe_allow_html=True)
                    
                    with st.expander("Items"):
                        for id in items.keys():
                            with st.columns(1, border=True, vertical_alignment="center")[0]:
                                cols3 = st.columns(2)
                                with cols3[0]:
                                    st.markdown(f":gray[{cc.UPGRADE_SOURCES[id]["pretty_print"]}]", text_alignment="left")
                                with cols3[1]:
                                    st.markdown(f":gray[x{items[id]}]", text_alignment="right")
                                    
                

if __name__ == "__main__":
    main()