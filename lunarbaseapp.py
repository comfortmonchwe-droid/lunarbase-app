import streamlit as st

#Page configuration
st.set_page_config(
    page_title="LUNA BASE",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

#Session state
defaults = {
    "page": "welcome",
    "day": 1,
    "oxygen": 60,
    "water": 70,
    "food": 80,
    "power": 70,
    "health": 80,
    "science": 0,
    "emergency_reserves": 2,
    "emergency_resolved": False,
    "emergency_message": "",
    "emergency_triggered": False,
    "action_done": False,
    "action_message": "",
    "mission_status": "Not Started",
    "mission_log": [],
    "completed_missions": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

#Helper Functions
def change_resource(resource, amount):
    """Change a resource without allowing it below 0 or above 100."""

    current = st.session_state[resource]

    st.session_state[resource] = max(
        0,
        min(100, current + amount)
    )


def reset_mission():
    st.session_state.day = 1

    st.session_state.oxygen = 60
    st.session_state.water = 70
    st.session_state.food = 80
    st.session_state.power = 70
    st.session_state.health = 80

    st.session_state.science = 0
    st.session_state.emergency_reserves = 2

    st.session_state.emergency_resolved = False
    st.session_state.emergency_message = ""
    st.session_state.emergency_triggered = False

    st.session_state.action_done = False
    st.session_state.action_message = ""

    st.session_state.mission_status = "In Progress"
    st.session_state.mission_log = []

    st.session_state.page = "mission"


def check_mission_failure():
    if st.session_state.oxygen <= 0:
        return "Oxygen supplies have been depleted."

    if st.session_state.health <= 0:
        return "Crew health has reached zero."

    if st.session_state.water <= 0:
        return "Water supplies have been depleted."

    if st.session_state.food <= 0:
        return "Food supplies have been depleted."

    return None

def perform_action(action):
    if action == "survey":

        change_resource("power", -5)
        st.session_state.science += 10

        message = (
            "Lunar surface survey completed. "
            "Scientific knowledge increased."
        )

    elif action == "maintenance":

        change_resource("power", -5)
        change_resource("oxygen", 8)

        message = (
            "Life-support maintenance completed. "
            "Oxygen production improved."
        )

    elif action == "water":

        change_resource("power", -8)
        st.session_state.science += 15

        message = (
            "Water-ice investigation completed. "
            "Scientific knowledge increased."
        )

    st.session_state.action_done = True
    st.session_state.action_message = message

    st.session_state.mission_log.append(
        f"Day {st.session_state.day}: {message}"
    )

def end_day():

    # Daily resource consumption

    change_resource("oxygen", -8)
    change_resource("water", -7)
    change_resource("food", -6)
    change_resource("power", -5)

    # Low resources affect crew health

    if st.session_state.oxygen < 20:
        change_resource("health", -10)

    if st.session_state.water < 20:
        change_resource("health", -5)

    if st.session_state.food < 20:
        change_resource("health", -5)

    st.session_state.mission_log.append(
        f"Day {st.session_state.day}: Daily resource consumption completed."
    )

    # Check mission failure

    failure = check_mission_failure()

    if failure:

        st.session_state.mission_status = "Failed"
        st.session_state.action_message = failure
        st.session_state.page = "failed"
        return

    # Check whether Day 3 is complete

    if st.session_state.day >= 3:

        st.session_state.mission_status = "Completed"

        if 1 not in st.session_state.completed_missions:
            st.session_state.completed_missions.append(1)

        st.session_state.page = "results"
        return

    # Move to the next day

    st.session_state.day += 1

    st.session_state.action_done = False
    st.session_state.action_message = ""

    # Trigger emergency at the beginning of Day 2

    if (
        st.session_state.day == 2
        and not st.session_state.emergency_triggered
    ):

        st.session_state.emergency_triggered = True
        st.session_state.emergency_resolved = False

        st.session_state.page = "emergency"

    else:

        st.session_state.page = "mission"

#Design
st.markdown("""
<style>

.stApp {
    background-color: #080D18;
    color: #FFFFFF;
}

.block-container {
    max-width: 1150px;
    padding-top: 3rem;
}

h1, h2, h3, h4 {
    color: #FFFFFF !important;
}

p, li, label {
    color: #E0E8F2;
}

.stMarkdown {
    color: #FFFFFF;
}

.stButton > button {
    background-color: #00A6C7;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 12px 20px;
    font-weight: bold;
    width: 100%;
}

.stButton > button:hover {
    background-color: #0086A3;
    color: #FFFFFF;
}

.info-panel {
    background-color: #111C2E;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #263B55;
    margin-bottom: 15px;
}

.small-label {
    color: #00C7E8;
    letter-spacing: 3px;
    font-size: 13px;
    font-weight: bold;
}

.tagline {
    color: #00C7E8;
    font-size: 20px;
    text-align: center;
}

.footer {
    color: #8191A8;
    text-align: center;
    font-size: 13px;
    margin-top: 50px;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF;
}

[data-testid="stMetricLabel"] {
    color: #C5D0DF;
}

</style>
""", unsafe_allow_html=True)

#Welcome screen
if st.session_state.page == "welcome":

    st.markdown(
        '<p class="small-label" style="text-align:center;">'
        'W.A.I.D. PRESENTS</p>',
        unsafe_allow_html=True
    )

    st.title("🌙 LUNA BASE")

    st.markdown(
        '<p class="tagline">'
        'Survive the Moon. Explore the Unknown. Build Beyond Earth.'
        '</p>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div style="text-align:center; padding:20px;">
        <h3>WELCOME, COMMANDER.</h3>
        <p>
        Your mission is to establish and maintain a lunar base.
        Manage resources, protect your crew, investigate the Moon
        and make decisions that will determine the future of your mission.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="info-panel">
            <h3>🫁 SURVIVAL</h3>
            <p>Manage oxygen, water, food and electricity.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-panel">
            <h3>🔬 EXPLORATION</h3>
            <p>Investigate lunar conditions and scientific discoveries.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-panel">
            <h3>🚀 PROGRESSION</h3>
            <p>Complete missions and unlock new challenges.</p>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 START YOUR ADVANTURE"):
            st.session_state.page = "missions"
            st.rerun()

    with col2:
        if st.button("📖 HOW TO PLAY"):
            st.session_state.page = "instructions"
            st.rerun()

    with st.expander("ABOUT LUNA BASE"):
        st.write("""
        LUNA BASE is an educational lunar survival and scientific
        exploration simulator.

        It uses fictional gameplay scenarios informed by lunar science.
        It is not real astronaut safety training or a certified
        life-support system.
        """)

    st.markdown(
        '<p class="footer">Developed by W.A.I.D. – Women in AI Development</p>',
        unsafe_allow_html=True
    )

#Mission Selection
elif st.session_state.page == "missions":

    st.markdown(
        '<p class="small-label">MISSION CONTROL</p>',
        unsafe_allow_html=True
    )

    st.title("🚀 MISSION SELECTION")

    st.write("Choose your mission, Commander.")

    st.markdown("""
    <div class="info-panel">
        <h3>MISSION 01: ESTABLISH THE LUNAR BASE</h3>
        <p><b>Duration:</b> 3 simulated days</p>
        <p><b>Difficulty:</b> Easy</p>
        <p><b>Objective:</b> Establish a functioning lunar base,
        maintain essential resources and protect the crew.</p>
        <p><b>Mission focus:</b> Survival and resource management.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("START MISSION 01"):

        reset_mission()
        st.rerun()

    st.subheader("UPCOMING MISSIONS")

    missions = [
        ("MISSION 02: LUNAR SURFACE EXPLORATION", "4 days", "Medium"),
        ("MISSION 03: SEARCH FOR LUNAR WATER", "5 days", "Hard"),
        ("MISSION 04: RESTORE BASE OPERATIONS", "2 days", "Hard"),
        ("MISSION 05: SUSTAINABLE LUNAR SETTLEMENT", "TBD", "Advanced")
    ]

    for index, mission in enumerate(missions, start=2):

        locked = index not in st.session_state.completed_missions

        if locked:
            symbol = "🔒"
            status = "LOCKED"
        else:
            symbol = "🔓"
            status = "UNLOCKED"

        st.markdown(f"""
        <div class="info-panel">
            <b>{symbol} {mission[0]}</b>
            <p>Duration: {mission[1]} | Difficulty: {mission[2]}</p>
            <p>{status}</p>
        </div>
        """, unsafe_allow_html=True)

    if st.button("← BACK TO HOME"):
        st.session_state.page = "welcome"
        st.rerun()

#How to play
elif st.session_state.page == "instructions":

    st.markdown(
        '<p class="small-label">COMMANDER TRAINING</p>',
        unsafe_allow_html=True
    )

    st.title("📖 HOW TO PLAY")

    st.subheader("Your responsibilities")

    st.write("""
    1. Keep oxygen levels high enough to protect the crew.
    2. Monitor water and food supplies.
    3. Manage electricity carefully.
    4. Protect crew health.
    5. Respond to emergencies.
    6. Complete the objectives of each mission.
    """)

    st.subheader("Understanding resources")

    st.write("""
    - Oxygen: Supports the crew.
    - Water: Essential for the crew.
    - Food: Provides supplies for the crew.
    - Electricity: Powers base systems.
    - Crew Health: Represents the crew's overall condition.
    """)

    st.info("""
    Every simulated day, the base consumes resources.
    Your decisions can help preserve supplies or increase scientific knowledge.
    """)

    if st.button("← BACK TO HOME"):
        st.session_state.page = "welcome"
        st.rerun()

#Mission dashboard

elif st.session_state.page == "mission":

    st.markdown(
        '<p class="small-label">ACTIVE LUNAR MISSION</p>',
        unsafe_allow_html=True
    )

    st.title("LUNA BASE - ESTABLISH THE LUNAR BASE")

    st.subheader(
        f"MISSION DAY {st.session_state.day} OF 3"
    )

    st.progress(st.session_state.day / 3)

    st.write("Commander, monitor the condition of your lunar base.")

    st.divider()

    #Resource indicators

    st.subheader("BASE RESOURCE STATUS")

    resources = [
        ("OXYGEN LEVEL", "oxygen"),
        ("WATER SUPPLY", "water"),
        ("FOOD SUPPLY", "food"),
        ("ELECTRICITY", "power"),
        ("CREW HEALTH", "health")
    ]

    for name, key in resources:

        value = st.session_state[key]

        st.write(f"**{name}: {value}%**")
        st.progress(value / 100)

    st.metric(
        "SCIENTIFIC KNOWLEDGE",
        st.session_state.science
    )

    st.metric(
        "EMERGENCY RESERVE UNITS",
        st.session_state.emergency_reserves
    )

    st.divider()

    #Mission objectives

    st.subheader("MISSION OBJECTIVES")

    st.write("""
    - Maintain sufficient oxygen, water and food.
    - Keep electricity available.
    - Protect crew health.
    - Complete all three mission days.
    """)

    st.divider()

    #Daily mission activities

    st.subheader("TODAY'S MISSION ACTIVITY")

    daily_actions = {
        1: {
            "title": "LUNAR SURFACE SURVEY",
            "description": (
                "Survey the surrounding lunar terrain "
                "and collect scientific information."
            ),
            "action": "survey"
        },

        2: {
            "title": "LIFE-SUPPORT MAINTENANCE",
            "description": (
                "Inspect the oxygen production system "
                "and maintain the base."
            ),
            "action": "maintenance"
        },

        3: {
            "title": "WATER-ICE INVESTIGATION",
            "description": (
                "Investigate a potential lunar water-ice location."
            ),
            "action": "water"
        }
    }

    today = daily_actions[st.session_state.day]

    st.markdown(
        f"""
        <div class="info-panel">
            <h3>{today['title']}</h3>
            <p>{today['description']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.action_done:

        if st.button("COMPLETE TODAY'S ACTIVITY"):

            perform_action(today["action"])
            st.rerun()

    else:

        st.success(st.session_state.action_message)

        if st.button("END MISSION DAY"):

            end_day()
            st.rerun()

    #DID YOU KNOW?

    with st.expander("DID YOU KNOW?"):

        st.write("""
        The Moon has an extremely thin atmosphere called an exosphere.
        Humans cannot breathe it.

        The Moon's gravity is approximately one-sixth of Earth's gravity.
        """)

    #Navigation

    if st.button("RETURN TO MISSION SELECTION"):

        st.session_state.page = "missions"
        st.rerun()

#Emergency scenario

elif st.session_state.page == "emergency":

    st.markdown(
        '<p class="small-label">LUNAR BASE ALERT SYSTEM</p>',
        unsafe_allow_html=True
    )

    st.title("⚠️ LIFE-SUPPORT EMERGENCY")

    st.subheader(
        f"MISSION DAY {st.session_state.day} - EMERGENCY ALERT"
        )

    st.error("OXYGEN PRODUCTION SYSTEM FAILURE!")

    st.write("""
    Commander, an unexpected malfunction has affected
    the oxygen production system.

    The crew needs an alternative oxygen supply.

    You must decide how to respond.
    """)

    st.divider()

    st.subheader("CURRENT BASE RESOURCES")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🫁 Oxygen", f"{st.session_state.oxygen}%")

    with col2:
        st.metric("⚡ Electricity", f"{st.session_state.power}%")

    with col3:
        st.metric("❤️ Crew Health", f"{st.session_state.health}%")

    st.metric(
        "🛟 Emergency Oxygen Reserves",
        st.session_state.emergency_reserves
    )

    st.divider()

    st.subheader("COMMANDER, WHAT WILL YOU DO?")

    if not st.session_state.emergency_resolved:

        #Option 1

        if st.button("🛟 USE EMERGENCY OXYGEN RESERVES"):

            if st.session_state.emergency_reserves > 0:

                change_resource("oxygen", 15)

                st.session_state.emergency_reserves -= 1

                change_resource("health", 5)

                st.session_state.emergency_message = (
                    "Emergency reserves activated. "
                    "Oxygen and crew health improved."
                )

            else:

                st.session_state.emergency_message = (
                    "WARNING: No emergency reserves are available."
                )

            st.session_state.emergency_resolved = True
            st.rerun()

        #Option 2

        if st.button("🔧 REPAIR OXYGEN PRODUCTION SYSTEM"):

            if st.session_state.power >= 15:

                change_resource("power", -15)
                change_resource("oxygen", 10)
                change_resource("health", 3)

                st.session_state.emergency_message = (
                    "The oxygen production system was repaired. "
                    "Electricity was consumed."
                )

            else:

                st.session_state.emergency_message = (
                    "INSUFFICIENT ELECTRICITY. "
                    "The repair could not be completed."
                )

            st.session_state.emergency_resolved = True
            st.rerun()

        #Option 3

        if st.button("🚨 IGNORE WARNING"):

            change_resource("oxygen", -20)
            change_resource("health", -15)

            st.session_state.emergency_message = (
                "The warning was ignored. Oxygen levels decreased "
                "and crew health was affected."
            )

            st.session_state.emergency_resolved = True
            st.rerun()

    else:

        st.success(st.session_state.emergency_message)

        st.subheader("UPDATED RESOURCE LEVELS")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🫁 Oxygen", f"{st.session_state.oxygen}%")

        with col2:
            st.metric("⚡ Electricity", f"{st.session_state.power}%")

        with col3:
            st.metric("❤️ Crew Health", f"{st.session_state.health}%")

        st.metric(
            "🛟 Emergency Reserves",
            st.session_state.emergency_reserves
        )

        failure = check_mission_failure()

        if failure:

            st.error(f"MISSION FAILED: {failure}")

            if st.button("VIEW MISSION FAILURE"):
                st.session_state.mission_status = "Failed"
                st.session_state.page = "failed"
                st.rerun()

        else:

            st.info(
                "Emergency response completed. "
                "Return to your mission to continue."
            )

            if st.button("RETURN TO MISSION"):

                st.session_state.page = "mission"
                st.rerun()

#Mission results
elif st.session_state.page == "results":

    st.markdown(
        '<p class="small-label">MISSION CONTROL REPORT</p>',
        unsafe_allow_html=True
    )

    st.title("🏆 MISSION 01 COMPLETED")

    st.success(
        "Congratulations, Commander! "
        "You survived all three simulated mission days."
    )

    st.subheader("FINAL RESOURCE REPORT")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🫁 Oxygen", f"{st.session_state.oxygen}%")

    with col2:
        st.metric("💧 Water", f"{st.session_state.water}%")

    with col3:
        st.metric("🍱 Food", f"{st.session_state.food}%")

    col4, col5 = st.columns(2)

    with col4:
        st.metric("⚡ Electricity", f"{st.session_state.power}%")

    with col5:
        st.metric("❤️ Crew Health", f"{st.session_state.health}%")

    st.metric(
        "🔬 Scientific Knowledge",
        st.session_state.science
    )

    st.subheader("MISSION ACTIVITY LOG")

    for entry in st.session_state.mission_log:
        st.write("•", entry)

    st.divider()

    st.info(
        "Mission 01 has been recorded as completed. "
        "Future missions will be unlocked as their gameplay is developed."
    )

    if st.button("RETURN"):

        st.session_state.page = "missions"
        st.rerun()

    if st.button("REPLAY MISSION 01"):

        reset_mission()
        st.rerun()

#Mission Failure
elif st.session_state.page == "failed":

    st.title("🚨 MISSION FAILED")

    st.error(st.session_state.action_message)

    st.write("""
    The lunar base could not maintain the minimum conditions
    required for the crew to survive in this game scenario.

    Review your resource decisions and try again.
    """)

    st.subheader("FINAL RESOURCE LEVELS")

    st.metric("Oxygen", f"{st.session_state.oxygen}%")
    st.metric("Water", f"{st.session_state.water}%")
    st.metric("Food", f"{st.session_state.food}%")
    st.metric("Electricity", f"{st.session_state.power}%")
    st.metric("Crew Health", f"{st.session_state.health}%")

    if st.button("🔄 RESTART MISSION"):

        reset_mission()
        st.rerun()

    if st.button("RETURN TO THE MISSION"):

        st.session_state.page = "missions"
        st.rerun()
