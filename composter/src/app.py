import hyapi, copy
import composter_constants as cc
from composter_state import ComposterState
from media import MEDIA_LINKS
from typing import Any, Tuple, cast, Literal
from datetime import time
import streamlit as st
import pandas as pd


def st_get(key: str, default: Any = None) -> Any:
    return st.session_state.get(key, default)


def attr_stacks_to_level(stacks: int, rarity: str) -> Tuple[int, int]:
    if rarity not in cc.ATTRIBUTE_RARITIES:
        raise KeyError(f"Invalid input: {rarity}")
    stack_sum = 0
    level = 0
    while stack_sum <= stacks and level < 10:
        stack_sum += cc.ATTRIBUTE_STACKS_PER_LEVEL[rarity][level]
        if stack_sum <= stacks:
            level += 1
    return level, stack_sum - stacks


def init_session_state() -> None:
    INIT_VALUES: dict[str, Any] = {
        "profile_id": "",
        "buy_mode": "instant",
        "sell_mode": "instant",
    }
    for key in INIT_VALUES:
        if key not in st.session_state:
            st.session_state[key] = INIT_VALUES[key]
        

def init_composter_data() -> None:
    if (st_get("last_profile") != st.session_state["profile_id"]) or st_get("reset_composter", False):
        for upgrade in cc.UPGRADE_TYPES:
            if cc.UPGRADE_USES_GENERAL[upgrade]:
                st.session_state[upgrade] = st.session_state["garden"].get("composter_data", {}).get("upgrades", {}).get(upgrade, 0)
        st.session_state["speed_attribute"] = st.session_state["attr"].get("stacks", {}).get("compost_speed", 0)
        st.session_state["last_profile"] = st.session_state["profile_id"]
        
        
def composter_state_from_session() -> ComposterState:
    return ComposterState(*[st_get(upg, 0) for upg in cc.UPGRADE_TYPES])


def upg_to_target_uptime(state: ComposterState, uptime: int) -> ComposterState:
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
                    
BottomlineMode = Literal["per_hour", "refill"]
BottomlineModeLabel: dict[BottomlineMode, str] = {
    "per_hour": "Profit/hr",
    "refill": "Refill",
}
def upg_to_bottomline(state: ComposterState, fuel_source: str, matter_source: str, buy_mode: hyapi.BuyMode = "instant", sell_mode: hyapi.SellMode = "instant", bottomline_mode: BottomlineMode = "per_hour", bottomline_goal: float = 0) -> ComposterState:
    if bottomline_mode not in ["per_hour", "refill"]:
        raise ValueError(f"Invalid {bottomline_mode = }")
    def profit_function(_state: ComposterState) -> float:
        return (_state.get_profit_hr if bottomline_mode == "per_hour" else _state.get_profit_refill)(fuel_source, matter_source, buy_mode, sell_mode)
    relevant_upg = ["multi_drop", "cost_reduction"]
    while (profit_function(state) < bottomline_goal and not state.is_maxed(*relevant_upg)):
        initial_profit = profit_function(state)
        best_value = float("inf")
        best_upg = state
        
        for upg in relevant_upg:
            if state.is_maxed(upg):
                continue
            
            temp = copy.deepcopy(state)
            setattr(temp, upg, getattr(temp, upg)+1)
            cost = coins_to_upgrade(*mats_to_upgrade(state, temp))
            profit_increase = profit_function(temp)-initial_profit
            
            if profit_increase == 0:
                continue
            
            if cost/profit_increase < best_value:
                best_value = cost/profit_increase
                best_upg = temp
        
        if state != best_upg:
            state = best_upg
        else: return state
    
    return state


def mats_to_upgrade(state: ComposterState, upgraded_state: ComposterState) -> Tuple[dict, int]:
    items = {}
    copper = 0
    for upg in cc.UPGRADE_TYPES:
        for i in range(getattr(state, upg), getattr(upgraded_state, upg)):
            id = cc.UPGRADE_COST[upg][i]["id"]
            count = cc.UPGRADE_COST[upg][i]["count"]
            
            gen_id = cc.UPGRADE_COST["general"][i]["id"]
            gen_count = cc.UPGRADE_COST["general"][i]["count"]
            
            copper += cc.UPGRADE_COST["general"][i]["copper"]
            items[id] = items.get(id, 0) + count
            items[gen_id] = items.get(gen_id, 0) + gen_count
    
    return items, copper
                
                
def coins_to_upgrade(items: dict, copper: int, copper_value: int = 0) -> float: # either refactor or make args based on ComposterStates later
    total_cost = 0
    for item in items.keys():
        total_cost += hyapi.get_bz_price(item) * items[item]
    total_cost += copper * copper_value
    return total_cost
                
                
def numerize(val: float) -> str:
    if val >= 1000000000: return f"{round(val/1000000000, 1)}b"
    if val > 1000000: return f"{round(val/1000000, 1)}m"
    if val > 1000: return f"{round(val/1000, 1)}k"
    return str(round(val, 1))


def float_to_time_str(time: float) -> str:
    mins, secs = divmod(time, 60)
    hrs, mins = divmod(mins, 60)
    return f"{int(hrs)}:{int(mins):02d}:{int(secs):02d}"


def time_to_int(time: time) -> int:
    return time.hour*3600 + time.minute*60 + time.second


def _set_sell_mode(widget: str) -> None:
    st.session_state["sell_mode"] = st.session_state[widget]
    

def sell_mode_pills(key: str) -> hyapi.SellMode:
    st.session_state[key] = st.session_state["sell_mode"]
    st.pills(
        "sell_mode", 
        hyapi.SELL_PRICE_FIELD.keys(), 
        selection_mode="single", 
        required=True, 
        format_func=hyapi.SELL_MODE_LABELS.__getitem__, 
        width="stretch", 
        label_visibility="collapsed", 
        key=key, 
        on_change=_set_sell_mode, 
        args=(key,)
    )
    return cast(hyapi.SellMode, st.session_state[key])


def _set_buy_mode(widget: str) -> None:
    st.session_state["buy_mode"] = st.session_state[widget]
    

def buy_mode_pills(key: str) -> hyapi.BuyMode:
    st.session_state[key] = st.session_state["buy_mode"]
    st.pills(
        "sell_mode", 
        hyapi.BUY_PRICE_FIELD.keys(), 
        selection_mode="single", 
        required=True, 
        format_func=hyapi.BUY_MODE_LABELS.__getitem__, 
        width="stretch", 
        label_visibility="collapsed", 
        key=key, 
        on_change=_set_buy_mode, 
        args=(key,)
    )
    return cast(hyapi.BuyMode, st.session_state[key])
    

def main():
    # DATA LOADING
    st.markdown("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>", unsafe_allow_html=True)
    
    init_session_state()
    
    profile_col1, profile_col2 = st.columns(2)
    
    with profile_col1:
        st.text_input("IGN:", max_chars=16, value="bigman7305", key="ign")
    
    uuid: str = ""
    profiles: list = []
    profile_id: str = ""
    profile_data: dict = {}
    garden: dict = {}
    player_dne_warning: bool = False
    
    with profile_col2:
        try:
            uuid = hyapi.get_uuid(st.session_state["ign"])
            profiles = hyapi.get_profiles(uuid)
        except hyapi.BadAPICallError as e:
            if e.code == hyapi.BadAPICallCode.NO_UUID:
                player_dne_warning = True
            else: st.error(e)
        if profiles:
            st.selectbox("Profile:", [profile["cute_name"] for profile in profiles], key="selected_profile")
        elif player_dne_warning:
            st.warning(f"Could not find player {st.session_state["ign"]!r}.", icon=":material/warning:")
        else:
            st.selectbox("Profile:", [])
            
        
    if profiles:
        profile_id = hyapi.get_profile_id(st.session_state["selected_profile"], uuid, profiles=profiles)
    st.session_state["profile_id"] = profile_id
    if profiles:
        for profile in range(0, len(profiles)):
            if profiles[profile]["profile_id"] == st.session_state["profile_id"]:
                profile_data = profiles[profile]
    try:
        garden = hyapi.get_garden_data(st_get("profile_id"))
    except hyapi.BadAPICallError as e:
        if e.code == hyapi.BadAPICallCode.NO_GARDEN_DATA:
            st.info("No garden data found for profile, assuming no upgrades", icon=":material/feedback:")
        else: st.error(e)
    
    st.session_state["attr"] = profile_data.get("members", {}).get(uuid, {}).get("attributes", {})
    st.session_state["garden"] = garden
    
    init_composter_data()
    
    # WEBSITE CONTENT
    state = composter_state_from_session()
    
    st.title("Composter Tools", text_alignment="center")
    
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
            valid_upgrades = list(filter(lambda x: not state.is_maxed(x), cc.UPGRADE_TYPES))
                    
            use_non_profitable = st.toggle("Show Non-profitable Upgrades")
                    
            def get_upgraded_state(state: ComposterState, upgrade: str) -> ComposterState:
                new = copy.deepcopy(state)
                setattr(new, upgrade, getattr(new, upgrade)+1)
                return new
            
            upgrade_states = { upgrade: { "state": get_upgraded_state(state, upgrade), "profit_hr": 0.0, } for upgrade in valid_upgrades }
            for upgrade in valid_upgrades:
                upgrade_states[upgrade]["profit_hr"] = upgrade_states[upgrade]["state"].get_profit_hr("SUNFLOWER_OIL", "ENCHANTED_SEEDS", st.session_state["buy_mode"], st.session_state["sell_mode"]) # add global fuel/matter selection later
                upgrade_states[upgrade]["cost"] = coins_to_upgrade(*mats_to_upgrade(state, upgrade_states[upgrade]["state"]), copper_value=0) # add copper value input later
                try:
                    upgrade_states[upgrade]["value"] = upgrade_states[upgrade]["cost"]/(upgrade_states[upgrade]["profit_hr"]-state.get_profit_hr("SUNFLOWER_OIL", "ENCHANTED_SEEDS", st.session_state["buy_mode"], st.session_state["sell_mode"])) # add global fuel/matter selection later
                except ZeroDivisionError:
                    upgrade_states[upgrade]["value"] = float("inf")
            good_states = {}
            bad_states = {}
            for upgrade_state in upgrade_states:
                if upgrade_states[upgrade_state]["value"] < 0 or upgrade_states[upgrade_state]["value"] in [float("inf"), float("-inf")]:
                    bad_states[upgrade_state] = upgrade_states[upgrade_state]
                else: good_states[upgrade_state] = upgrade_states[upgrade_state]
            good_states = dict(sorted(good_states.items(), key=lambda x: x[1]["value"]))
            bad_states = dict(sorted(bad_states.items(), key=lambda x: x[1]["value"], reverse=True))
            for state_select in [good_states, bad_states] if use_non_profitable else [good_states]:
                for upgrade in state_select:
                    with st.container(border=True):
                        left, right = st.columns([1, 1], vertical_alignment="center")
                        with left:
                            cols = st.columns([5,2], vertical_alignment="center")
                            with cols[0]:
                                st.markdown(f"##### {cc.UPGRADE_NAMES_MARKDOWN[upgrade]}")
                            with cols[1]:
                                with st.container(border=True, vertical_alignment="center"):
                                    st.markdown(f"**{getattr(state, upgrade)+1}**", text_alignment="center")
                        with right:
                            if upgrade_states[upgrade]["value"] in [float("inf"), float("-inf")]:
                                data = pd.DataFrame(data={"Profit Change": 0, "Upgrade Cost": [upgrade_states[upgrade]["cost"]]})
                            elif upgrade_states[upgrade]["value"] < 0:
                                data = pd.DataFrame(data={"Cost per -10,000/hr": [upgrade_states[upgrade]["value"]*-10000 if upgrade_states[upgrade]["value"] >= -100_000_000 else r"\> 1,000,000,000,000.0"], "Upgrade Cost": [upgrade_states[upgrade]["cost"]]})
                            else:
                                data = pd.DataFrame(data={"Cost per 10,000/hr": [upgrade_states[upgrade]["value"]*10000 if upgrade_states[upgrade]["value"] <= 100_000_000 else r"\> 1,000,000,000,000.0"], "Upgrade Cost": [upgrade_states[upgrade]["cost"]]})
                            st.table(data.style.format(precision=1, thousands=","))
                        items, copper = mats_to_upgrade(state, upgrade_states[upgrade]["state"])
                        with st.expander(f"Materials to Upgrade"):
                            with st.columns(1, border=True, vertical_alignment="center")[0]:
                                price = 0 # add global price per copper later
                                cols3 = st.columns([7, 2, 2, 3])
                                with cols3[0]:
                                    st.markdown(f":red[Copper]", text_alignment="left")
                                with cols3[1]:
                                    st.markdown(f":gray[x]{copper}", text_alignment="right")
                                with cols3[2]:
                                    st.markdown(f":orange[{numerize(copper * price)}]", text_alignment="right")
                                with cols3[3]:
                                    st.markdown(f":gray[({numerize(price)} ea.)]", text_alignment="right")
                                
                            for id in items.keys():
                                if items[id] == 0: continue
                                with st.columns(1, border=True, vertical_alignment="center")[0]:
                                    price = hyapi.get_bz_price(id)
                                    cols3 = st.columns([7, 2, 2, 3])
                                    with cols3[0]:
                                        st.markdown(f"{cc.UPGRADE_SOURCES[id]["pretty_print"]}", text_alignment="left")
                                    with cols3[1]:
                                        st.markdown(f":gray[x]{items[id]}", text_alignment="right")
                                    with cols3[2]:
                                        st.markdown(f":orange[{numerize(items[id]*price)}]", text_alignment="right")
                                    with cols3[3]:
                                        st.markdown(f":gray[({numerize(price)} ea.)]", text_alignment="right")
                    
        with sim_tab:
            with st.columns(1, vertical_alignment="center", border=True)[0]:
                left, mid, right = st.columns([1, 1, 1])
                
                with mid:
                    with st.columns(1, border=True)[0]:
                        st.image(MEDIA_LINKS.composter_img)
                
                with left:
                    st.markdown(f"### :green[Fuel Cap]<br>{state.get_value("fuel_cap"):,}", text_alignment="center", unsafe_allow_html=True)
                    st.markdown(f"### :yellow[Organic Matter Cap]<br>{state.get_value("organic_matter_cap"):,}", text_alignment="center", unsafe_allow_html=True)
                
                with right:
                    st.markdown(f"### :blue[Runtime]<br>{float_to_time_str(state.sim_composter()[0])}", text_alignment="center", unsafe_allow_html=True)
                    st.markdown(f"### :red[Avg. Compost Per Hour]<br>{round(state.get_compost_generated_hr(), 2):,}", text_alignment="center", unsafe_allow_html=True)
                
                matter = st_get("matter", next(iter(cc.ORGANIC_MATTER_SOURCES)))
                fuel = st_get("fuel", next(iter(cc.FUEL_SOURCES)))
                
                sim_tab_profit_per_hour, sim_tab_compost_cost = st.columns([1, 1], vertical_alignment="center")
                
                with sim_tab_profit_per_hour:
                    profit_hr = state.get_profit_hr(fuel, matter, buy_mode=st.session_state["buy_mode"], sell_mode=st.session_state["sell_mode"])
                    profit_refill = state.get_profit_refill(fuel, matter, buy_mode=st.session_state["buy_mode"], sell_mode=st.session_state["sell_mode"])
                    st.markdown(f"""
                        ### :rainbow[Profit Per Hour]<br>:orange[{round(profit_hr, 1):,}]<br>:blue[Profit Per Refill]<br>:orange[{round(profit_refill, 1):,}]
                        """, text_alignment="center", unsafe_allow_html=True
                    )
                
                with sim_tab_compost_cost:
                    with st.columns(1, vertical_alignment="center", border=True)[0]:
                        sell_mode_pills("sim_tab_sell_mode")
                        
                        sim_tab_compost_cost_price, sim_tab_compost_cost_img = st.columns([1,1], vertical_alignment="center")
                        
                        with sim_tab_compost_cost_price:
                            st.markdown(f"""
                                ##### Compost Sell Price<br>
                                :orange[{round(hyapi.get_bz_price("COMPOST", field=hyapi.SELL_PRICE_FIELD[st.session_state["sell_mode"]]), 1):,}]
                                """, text_alignment="center", unsafe_allow_html=True
                            )
                        with sim_tab_compost_cost_img:
                            with st.columns(1, border=True)[0]:
                                st.image(MEDIA_LINKS.compost_img)
                
                with st.columns(1, border=True)[0]:
                    with st.columns([1,2,1])[1]:
                        buy_mode_pills("sim_tab_buy_mode")
                        
                    matter_col, fuel_col = st.columns(2)
                    
                    with matter_col:
                        st.selectbox("Organic Matter Source:", cc.ORGANIC_MATTER_SOURCES.keys(), format_func=lambda x: cc.ORGANIC_MATTER_SOURCES[x]["pretty_print"], key="matter")
                        
                        txt_col = st.columns([3, 1])
                        with txt_col[0]:
                            f"Refill Cost: :orange[{round(state.get_matter_cost_refill(matter, buy_mode=st.session_state["buy_mode"]), 1):,}]"
                        with txt_col[1]:
                            st.markdown(f":gray[x{state.get_matter_items_refill(matter):>10,}]", text_alignment="right")
                    
                    with fuel_col:
                        st.selectbox("Fuel Source:", cc.FUEL_SOURCES.keys(), format_func=lambda x: cc.FUEL_SOURCES[x]["pretty_print"], key="fuel")
                        
                        txt_col = st.columns([3, 1])
                        with txt_col[0]:
                            f"Refill Cost: :orange[{round(state.get_fuel_cost_refill(fuel, buy_mode=st.session_state["buy_mode"]), 1):,}]"
                        with txt_col[1]:
                            st.markdown(f":gray[x{state.get_fuel_items_refill(fuel):>10,}]", text_alignment="right")
                
        
        with uptime_tab:
            with st.columns(1, vertical_alignment="center", border=True)[0]:
                st.session_state["target_uptime"] = time_to_int(st_get("target_uptime_datetime", time(4)))
                target_uptime_met = state.sim_composter()[0] >= st_get("target_uptime", float("inf"))
                    
                with st.columns(1, vertical_alignment="center", border=True)[0]:
                    st.markdown(f"### Current Uptime: :{"green" if target_uptime_met else "red"}[{float_to_time_str(state.sim_composter()[0])}]", text_alignment="center")
                    ""
                
                cols = st.columns([11, 5], vertical_alignment="center")
                with cols[0]:
                    st.time_input("Target Uptime:", "04:00:00", key="target_uptime_datetime")
                    
                    upg_state = upg_to_target_uptime(state, st.session_state["target_uptime"])
                    
                    cols2 = st.columns(3, border=True, vertical_alignment="center")
                    
                    with cols2[0]:
                        st.markdown(f"""
                            ###### :green[Fuel Cap]<br>{upg_state.fuel_cap}
                            """, text_alignment="center", unsafe_allow_html=True
                        )
                    
                    with cols2[1]:
                        st.markdown(f"""
                            ###### :yellow[Organic Matter Cap]<br>{upg_state.organic_matter_cap}
                            """, text_alignment="center", unsafe_allow_html=True
                        )
                    
                    with cols2[2]:
                        st.markdown(f"""
                            ###### :orange[Cost Reduction]<br>{upg_state.cost_reduction}
                            """, text_alignment="center", unsafe_allow_html=True
                        )
                    
                with cols[1]:
                    with st.columns(1, border=True)[0]:
                        st.image(MEDIA_LINKS.composter_img)
                
                if target_uptime_met:
                    st.markdown("## :gray[Target uptime met!]", text_alignment="center")
                    ""
                else:
                    with st.columns(1, vertical_alignment="center", border=True)[0]:
                        st.markdown(f"### Uptime After Upgrades: :green[{float_to_time_str(upg_state.sim_composter()[0])}]", text_alignment="center")
                        ""
                    with st.columns(1, border=True, vertical_alignment="center")[0]:
                        items, copper = mats_to_upgrade(state, upg_state)
                        total_cost = coins_to_upgrade(items, copper, copper_value=0)
                            
                        st.markdown(f"""
                            ## :rainbow[Cost of Upgrades]: :orange[{round(total_cost, 1):,}]<br>Copper Cost: :red[{copper:,}]
                            """, text_alignment="center", unsafe_allow_html=True
                        )
                        
                        with st.expander("Items"):
                            for id in items.keys():
                                with st.columns(1, border=True, vertical_alignment="center")[0]:
                                    price = hyapi.get_bz_price(id)
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
            with st.columns(1, vertical_alignment="center", border=True)[0]:
                
                target_bottomline_met = False
                if st_get("bottomline_mode", "per_hour") == "per_hour":
                    target_bottomline_met = profit_hr >= st_get("target_bottomline", float("inf"))
                if st_get("bottomline_mode", "per_hour") == "refill":
                    target_bottomline_met = profit_refill >= st_get("target_bottomline", float("inf"))
                
                bottomline_tab_buy_sell_selector, bottomline_tab_hr_refill_selector = st.columns([1,1], vertical_alignment="center")
                
                with bottomline_tab_buy_sell_selector:
                    with st.expander("Buy/Sell Modes"):
                        st.markdown("Buy Mode", text_alignment="center")
                        buy_mode_pills("bottomline_tab_buy_mode")
                        st.markdown("Sell Mode", text_alignment="center")
                        sell_mode_pills("bottomline_tab_sell_mode")
                    
                with bottomline_tab_hr_refill_selector:
                    st.session_state["bottomline_mode"] = cast(BottomlineMode, st.pills("mode", ["per_hour", "refill"], format_func=lambda x: BottomlineModeLabel[x], default="per_hour", selection_mode="single", required=True, width="stretch", label_visibility="collapsed"))
                
                with st.columns(1, vertical_alignment="center", border=True)[0]:  
                    if st_get("bottomline_mode", "per_hour") == "per_hour":
                        st.markdown(f"### Current Profit Per Hour: :{"green" if target_bottomline_met else "red"}[{round(profit_hr, 1):,}]", text_alignment="center")
                    if st_get("bottomline_mode", "per_hour") == "refill":
                        st.markdown(f"### Current Profit Per Refill: :{"green" if target_bottomline_met else "red"}[{round(profit_refill, 1):,}]", text_alignment="center")
                    ""
                    
                bottomline_state = upg_to_bottomline(state, fuel, matter, st.session_state["buy_mode"], st.session_state["sell_mode"], bottomline_mode=st_get("bottomline_mode", "per_hour"), bottomline_goal=st_get("target_bottomline", 0))
                    
                bottomline_tab_upgrades, bottomline_tab_anvil_img = st.columns([2,1])
                with bottomline_tab_upgrades:
                    st.number_input("Bottom Line:", value=0.0, format="%0.1f", key="target_bottomline")
                    bottomline_tab_upgrades_multi_drop, bottomline_tab_upgrades_cost_reduction = st.columns([1,1], border=True)
                    with bottomline_tab_upgrades_multi_drop:
                        st.markdown(f"""
                            ###### :blue[Multi Drop]<br>{bottomline_state.multi_drop}
                            """, text_alignment="center", unsafe_allow_html=True
                        )
                    with bottomline_tab_upgrades_cost_reduction:
                        st.markdown(f"""
                            ###### :orange[Cost Reduction]<br>{bottomline_state.cost_reduction}
                            """, text_alignment="center", unsafe_allow_html=True
                        )
                with bottomline_tab_anvil_img:
                    with st.columns(1, border=True)[0]:
                        st.image(MEDIA_LINKS.anvil_img)
                        
                if target_bottomline_met:
                    with st.columns(1, border=True, vertical_alignment="center")[0]:
                        st.markdown("## :gray[Target bottom line met!]", text_alignment="center")
                        ""
                else:
                    with st.columns(1, vertical_alignment="center", border=True)[0]:  
                        if st_get("bottomline_mode", "per_hour") == "per_hour":
                            st.markdown(f"### Profit Per Hour After Upgrades: :green[{round(bottomline_state.get_profit_hr(fuel, matter, st.session_state["buy_mode"], st.session_state["sell_mode"]), 1):,}]", text_alignment="center")
                        if st_get("bottomline_mode", "per_hour") == "refill":
                            st.markdown(f"### Profit Per Refill After Upgrades: :green[{round(bottomline_state.get_profit_refill(fuel, matter, st.session_state["buy_mode"], st.session_state["sell_mode"]), 1):,}]", text_alignment="center")
                        ""
                        
                    with st.columns(1, border=True, vertical_alignment="center")[0]:
                        items, copper = mats_to_upgrade(state, bottomline_state)
                        total_cost = 0
                        for item in items.keys():
                            total_cost += hyapi.get_bz_price(item) * items[item]
                        
                        st.markdown(f"""
                            ## :rainbow[Cost of Upgrades]: :orange[{round(total_cost, 1):,}]<br>Copper Cost: :red[{copper:,}]
                            """, text_alignment="center", unsafe_allow_html=True
                        )
                        
                        with st.expander("Items"):
                            for id in items.keys():
                                if items[id] == 0: continue
                                with st.columns(1, border=True, vertical_alignment="center")[0]:
                                    price = hyapi.get_bz_price(id)
                                    cols3 = st.columns([7, 2, 2, 3])
                                    with cols3[0]:
                                        st.markdown(f"{cc.UPGRADE_SOURCES[id]["pretty_print"]}", text_alignment="left")
                                    with cols3[1]:
                                        st.markdown(f":gray[x]{items[id]}", text_alignment="right")
                                    with cols3[2]:
                                        st.markdown(f":orange[{numerize(items[id]*price)}]", text_alignment="right")
                                    with cols3[3]:
                                        st.markdown(f":gray[({numerize(price)} ea.)]", text_alignment="right")

    footer = st.container()
    with footer:
        st.divider()
        st.space("xxlarge")
        
        footer_left, footer_right = st.columns([1, 3], vertical_alignment="center")
        with footer_left:
            st.link_button("Support this project", "https://ko-fi.com/bigman7305", icon=":material/favorite:")
        with footer_right:    
            st.markdown(":gray[Source code can be found [here](https://github.com/swilterdink1010/skyblock).]<br>:gray[*This project is not affiliated with or endorsed by Hypixel Inc. or Mojang Studios.*]", text_alignment="right", unsafe_allow_html=True)
                                            

if __name__ == "__main__":
    main()