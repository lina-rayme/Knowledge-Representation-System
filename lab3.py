import json
import streamlit as st
import base64

with open("background.png", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/png;base64,{encoded_image}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.stApp {
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.stButton > button {
    color: red !important;
    border: 1px solid red !important;
    background-color: white !important;
}

.stButton > button p {
    color: red !important;
}
</style>
""", unsafe_allow_html=True)

rules_json = '''
[
    {
        "name": "Top merit candidate",
        "priority": 100,
        "conditions": [
            ["cgpa", ">=", 3.7],
            ["co_curricular_score", ">=", 80],
            ["family_income", "<=", 8000],
            ["disciplinary_actions", "==", 0]
        ],
        "action": {
            "decision": "AWARD_FULL",
            "reason": "Excellent academic & co-curricular performance, with acceptable need"
        }
    },
    {
        "name": "Good candidate - partial scholarship",
        "priority": 80,
        "conditions": [
            ["cgpa", ">=", 3.3],
            ["co_curricular_score", ">=", 60],
            ["family_income", "<=", 12000],
            ["disciplinary_actions", "<=", 1]
        ],
        "action": {
        "decision": "AWARD_PARTIAL",
        "reason": "Good academic & involvement record with moderate need"
        }
    },
    {
        "name": "Need-based review",
        "priority": 70,
        "conditions": [
            ["cgpa", ">=", 2.5],
            ["family_income", "<=", 4000]
        ],
        "action": {
        "decision": "REVIEW",
        "reason": "High need but borderline academic score"
        }
    },
    {
        "name": "Low CGPA – not eligible",
        "priority": 95,
        "conditions": [
            ["cgpa", "<", 2.5]
        ],
        "action": {
        "decision": "REJECT",
        "reason": "CGPA below minimum scholarship requirement"
        }
    },
    {
        "name": "Serious disciplinary record",
        "priority": 90,
        "conditions": [
            ["disciplinary_actions", ">=", 2]
        ],
        "action": {
        "decision": "REJECT",
        "reason": "Too many disciplinary records"
        }
    }
]
'''

rules = json.loads(rules_json)

def check_condition(applicant, condition):
    attribute, operator, value = condition
    actual_value = applicant[attribute]

    if operator == ">=":
        return actual_value >= value
    elif operator == "<=":
        return actual_value <= value
    elif operator == "==":
        return actual_value == value
    elif operator == "<":
        return actual_value < value
    elif operator == ">":
        return actual_value > value

    return False

def evaluate_rules(applicant, rules):

    sorted_rules = sorted(
        rules,
        key=lambda rule: rule["priority"],
        reverse=True
    )

    for rule in sorted_rules:

        if all(
            check_condition(applicant, condition)
            for condition in rule["conditions"]
        ):

            return rule["name"], rule["action"]

    return "No matching rule", {
        "decision": "NO_DECISION",
        "reason": "No scholarship rule matched"
    }

st.title("🎓 Scholarship Advisory System")
st.write("Enter applicant information to determine scholarship eligibility.")

st.subheader("Applicant Information")
st.write("Select an option from the dropdown or enter your own value.")

# CGPA
cgpa = st.selectbox(
    "CGPA",
    options=[round(x * 0.1, 2) for x in range(41)],
    index=35,
    accept_new_options=True,
    format_func=lambda x: f"{float(x):.2f}"
)
cgpa = float(cgpa)


# CO-CURRICULAR SCORE
co_curricular_score = st.selectbox(
    "Co-curricular Score",
    options=list(range(0, 101, 5)),
    index=14,
    accept_new_options=True
)
co_curricular_score = float(co_curricular_score)


# FAMILY INCOME
family_income = st.selectbox(
    "Family Income (RM)",
    options=list(range(0, 20001, 500)),
    index=6,
    accept_new_options=True,
    format_func=lambda x: f"RM {float(x):,.2f}"
)
family_income = float(family_income)


# DISCIPLINARY ACTIONS
disciplinary_actions = st.selectbox(
    "Disciplinary Actions",
    options=list(range(0, 11)),
    index=1,
    accept_new_options=True
)
disciplinary_actions = int(disciplinary_actions)

# EVALUATE SCHOLARSHIP
if st.button("Evaluate Scholarship"):

    applicant = {
        "cgpa": cgpa,
        "co_curricular_score": co_curricular_score,
        "family_income": family_income,
        "disciplinary_actions": disciplinary_actions
    }

    rule_name, action = evaluate_rules(applicant, rules)

    st.subheader("Scholarship Decision")
    st.write("Matched Rule:", rule_name)

    decision = action["decision"]

    if decision == "AWARD_FULL":
        color = "#14532D"
        result = "FULL SCHOLARSHIP"

    elif decision == "AWARD_PARTIAL":
        color = "#1E40AF"
        result = "PARTIAL SCHOLARSHIP"

    elif decision == "REVIEW":
        color = "#92400E"
        result = "REQUIRES FURTHER REVIEW"

    elif decision == "REJECT":
        color = "#991B1B"
        result = "APPLICATION REJECTED"

    else:
        color = "#374151"
        result = "NO DECISION"

    st.markdown(f"""
    <div style="
        background-color: {color};
        padding: 20px;
        border-radius: 10px;
        color: white;
        font-weight: bold;
    ">
        {result}
    </div>
    """, unsafe_allow_html=True)

    st.write("Decision Code:", decision)
    st.write("Reason:", action["reason"])