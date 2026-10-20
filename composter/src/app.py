import hyapi
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
        
        
def calc_composter_value(upgrade: str):
    return cc.UPGRADE_BASE[upgrade] + cc.UPGRADE_INCREASES[upgrade] * st.session_state.get(upgrade, 0)


def sim_composter():
    s = calc_composter_value("speed")
    md = calc_composter_value("multi_drop")
    f = calc_composter_value("fuel_cap")
    om = calc_composter_value("organic_matter_cap")
    cr = calc_composter_value("cost_reduction")
    
    time = 0
    output = 0
    while (f := f-cc.BASE_FUEL_COST*(1-cr)) >= 0 and (om := om-cc.BASE_ORGANIC_MATTER_COST*(1-cr)) >= 0:
        time += cc.BASE_CRAFT_TIME/s
        output += md
    
    return time, output


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
                    time, output = sim_composter()
                    st.markdown(f"### :blue[Runtime]<br>{time_to_str(time)}", text_alignment="center", unsafe_allow_html=True)
                    compost_per_hr = output/(time/3600)
                    st.markdown(f"### :red[Avg. Compost Per Hour]<br>{round(compost_per_hr, 2)}", text_alignment="center", unsafe_allow_html=True)
                with st.columns(1, border=True)[0]:
                    matter_col, fuel_col = st.columns(2)
                    with matter_col:
                        matter = st.selectbox("Organic Matter Source:", cc.ORGANIC_MATTER_SOURCES.keys(), format_func=lambda x: cc.ORGANIC_MATTER_SOURCES[x]["pretty_print"])
                    with fuel_col:
                        fuel = st.selectbox("Fuel Source:", cc.FUEL_SOURCES.keys(), format_func=lambda x: cc.FUEL_SOURCES[x]["pretty_print"])
                        
                fuel_used_per_hr = calc_composter_value("speed")*cc.BASE_FUEL_COST*(1-calc_composter_value("cost_reduction"))
                matter_used_per_hr = calc_composter_value("speed")*cc.BASE_ORGANIC_MATTER_COST*(1-calc_composter_value("cost_reduction"))
                
                fuel_items_per_hr = (fuel_used_per_hr/cc.FUEL_SOURCES[fuel]["value"])*cc.FUEL_SOURCES[fuel].get("count", 1)
                matter_items_per_hr = (matter_used_per_hr/cc.ORGANIC_MATTER_SOURCES[matter]["value"])*cc.ORGANIC_MATTER_SOURCES[matter].get("count", 1)
                
                fuel_upkeep = get_bz_price(fuel)*fuel_items_per_hr
                matter_upkeep = get_bz_price(matter)*matter_items_per_hr
                
                st.markdown(f"## :rainbow[Profit Per Hour]: :orange[{round((get_bz_price("COMPOST") * compost_per_hr)-matter_upkeep-fuel_upkeep, 1)}]", text_alignment="center")
        
        with uptime_tab:
            pass
    

if __name__ == "__main__":
    main()