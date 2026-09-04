"""Shared Streamlit styles for the application."""

import json

import streamlit as st


def inject_navigation_styles(organization_name, mode_name):
    st.html(f"""
        <style>
        [class*="st-key-nav-organization"] div.stButton > button > div::after {{
            content: {json.dumps(f"(현재: {organization_name})", ensure_ascii=False)};
            display: block;
            font-size: 12px !important;
            font-weight: 700;
            line-height: 1.2;
        }}
        [class*="st-key-nav-assessment"] div.stButton > button > div::after {{
            content: {json.dumps(f"(현재: {mode_name})", ensure_ascii=False)};
            display: block;
            font-size: 12px !important;
            font-weight: 700;
            line-height: 1.2;
        }}
        </style>
    """)


def inject_styles():
    st.html("""
<style>

:root {

    --blue:#246FE5;
    --blue-dark:#175FC9;

    --navy:#17324D;

    --muted:#6B7D90;

    --border:#D5E1EC;

    --soft:#EEF6FF;

    --danger:#D92D20;
}


html,
body,
[class*="css"] {

    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        "Noto Sans KR",
        Arial,
        sans-serif;
}


.stApp {

    background:
        linear-gradient(
            180deg,
            #F8FBFF 0%,
            #FFFFFF 46%
        );

    color:
        var(--navy);
}


.block-container {

    max-width:
        840px;

    padding:
        .85rem
        1.55rem
        2.8rem;
}


#MainMenu,
footer,
header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] {

    display:
        none !important;
}


/* COMMON */

.section-label {

    color:
        var(--navy);

    font-size:
        14px;

    font-weight:
        900;

    margin:
        15px
        0
        7px;
}


.optional {

    color:
        #8A9AAB;

    font-size:
        11px;

    font-weight:
        700;

    margin-left:
        4px;
}


.helper {

    color:
        #7B8DA0;

    font-size:
        11px;

    line-height:
        1.45;

    margin:
        -1px
        0
        6px;
}


.notice {

    background:
        var(--soft);

    border:
        1px solid
        #DBEAFF;

    border-radius:
        13px;

    padding:
        11px
        14px;

    color:
        #50667A;

    font-size:
        12px;

    line-height:
        1.5;

    text-align:
        center;

    margin:
        0
        0
        16px;
}


.notice b {

    color:
        #1F66C7;
}


.validation-error {

    color:
        var(--danger);

    font-size:
        12px;

    font-weight:
        900;

    line-height:
        1.5;

    margin:
        8px
        0
        3px;
}


/* INPUT */

div[data-testid="stTextInput"] input {

    min-height:
        47px !important;

    height:
        47px !important;

    background:
        #FFFFFF !important;

    color:
        #17324D !important;

    -webkit-text-fill-color:
        #17324D !important;

    border:
        1px solid
        #CFDBE7 !important;

    border-radius:
        11px !important;

    font-size:
        16px !important;
}


div[data-testid="stTextInput"]
input::placeholder {

    color:
        #9AABBC !important;

    -webkit-text-fill-color:
        #9AABBC !important;
}


/* BUTTON */

div[data-testid="stButton"] button,
.stButton > button,
button[kind="primary"],
button[kind="secondary"] {

    box-sizing:
        border-box !important;
        100% !important;

    display:
        flex !important;

    flex-direction:
        column !important;

    align-items:
        center !important;

    justify-content:
        center !important;

    text-align:
        center !important;

    margin:
        0 !important;

    padding:
        0 !important;
}

div[data-testid="stButton"] > button p,
div[data-testid="stButton"] > button span,
.stButton > button p,
.stButton > button span {

    margin:
        0 !important;

    padding:
        0 !important;

    text-align:
        center !important;

    line-height:
        1.15 !important;
}


div[data-testid="stButton"] button[kind="secondary"],
div.stButton > button[kind="secondary"] {

    background:
        #FFFFFF !important;

    color:
        #17324D !important;

    border:
        1px solid
        #CFDBE7 !important;
}


div[data-testid="stButton"] button[kind="secondary"] *,
div.stButton > button[kind="secondary"] * {

    color:
        #17324D !important;

    -webkit-text-fill-color:
        #17324D !important;
}


div[data-testid="stButton"] button[kind="primary"],
div.stButton > button[kind="primary"] {

    background:
        #246FE5 !important;

    color:
        #FFFFFF !important;

    border:
        1px solid
        #246FE5 !important;
}


div[data-testid="stButton"] button[kind="primary"] *,
div.stButton > button[kind="primary"] * {

    color:
        #FFFFFF !important;

    -webkit-text-fill-color:
        #FFFFFF !important;
}


[data-testid="stVerticalBlock"] {

    gap:
        .46rem !important;
}


[data-testid="stHorizontalBlock"] {

    gap:
        .58rem !important;
}


[class*="st-key-organization-grid"] div.stButton > button,
[class*="st-key-organization-grid"] div.stButton > button p,
[class*="st-key-organization-grid"] div.stButton > button span {

    min-height:
        85px !important;

    text-align:
        center !important;

    white-space:
        nowrap !important;

    padding:
        .2rem
        .25rem !important;

    font-size:
        28px !important;
}


[class*="st-key-organization-selection"] h1 {

    text-align:
        center !important;

    margin-top:
        1.5rem !important;

    margin-bottom:
        1.5rem !important;
}


[class*="st-key-organization-bureau"] div.stButton > button,
[class*="st-key-organization-bureau"] div.stButton > button p,
[class*="st-key-organization-bureau"] div.stButton > button span {

    min-height:
        90px !important;

    text-align:
        center !important;

    white-space:
        nowrap !important;

    padding:
        .2rem
        .25rem !important;

    font-size:
        28px !important;
}


[class*="st-key-organization-navigation"] div.stButton > button,
[class*="st-key-organization-navigation"] div.stButton > button p,
[class*="st-key-organization-navigation"] div.stButton > button span {

    min-height:
        68px !important;

    text-align:
        center !important;

    white-space:
        normal !important;

    padding:
        .25rem
        .3rem !important;

    font-size:
        28px !important;
}


[class*="st-key-organization-navigation"] div.stButton > button {

    line-height:
        1.15 !important;
}


[class*="st-key-assessment-selection"] h1 {

    text-align:
        center !important;

    margin-top:
        1.5rem !important;

    margin-bottom:
        1.25rem !important;
}


[class*="st-key-assessment-selection"] div.stButton > button,
[class*="st-key-assessment-selection"] div.stButton > button p,
[class*="st-key-assessment-selection"] div.stButton > button span {

    min-height:
        68px !important;

    text-align:
        center !important;

    white-space:
        normal !important;

    padding:
        .4rem
        .3rem !important;

    font-size:
        24px !important;
}


[class*="st-key-assessment-selection"] div.stButton > button {

    line-height:
        1.15 !important;
}


[class*="st-key-assessment-selection"] div.stButton > button p::after {

    display:
        block;

    margin-top:
        4px;

    font-size:
        12px !important;

    font-weight:
        700;

    line-height:
        1.2 !important;
}


[class*="st-key-assessment-guardian"] div.stButton > button p::after {

    content:
        "우리아이의 모습을 체크해주세요";
}


[class*="st-key-assessment-academic"] div.stButton > button p::after {

    content:
        "현재 학습상태를 확인합니다.";
}


[class*="st-key-assessment-selection"] [data-testid="stCaptionContainer"] {

    text-align:
        center !important;

    font-size:
        14px !important;
}


/* HOME */

.hero {

    text-align:
        center;

    margin:
        0
        0
        20px;
}


.badge {

    display:
        inline-block;

    background:
        #EAF3FF;

    color:
        var(--blue);

    padding:
        7px
        14px;

    border-radius:
        999px;

    font-size:
        13px;

    font-weight:
        900;

    margin-bottom:
        13px;
}


.hero-title {

    margin:
        0;

    color:
        var(--navy);

    font-size:
        35px;

    line-height:
        1.22;

    font-weight:
        900;

    letter-spacing:
        -1.1px;
}


.hero-title .accent {

    color:
        var(--blue);
}


.hero-sub {

    margin-top:
        10px;

    color:
        var(--muted);

    font-size:
        14px;

    line-height:
        1.6;
}


.features {

    display:
        grid;

    grid-template-columns:
        repeat(3,1fr);

    gap:
        12px;

    margin:
        17px
        0
        15px;
}


.feature {

    background:
        #FFFFFF;

    border:
        1px solid
        var(--border);

    border-radius:
        16px;

    padding:
        15px
        10px
        13px;

    text-align:
        center;
}


.feature .icon {

    font-size:
        20px;

    color:
        var(--blue);

    font-weight:
        900;

    margin-bottom:
        5px;
}


.feature .title {

    font-size:
        13px;

    color:
        var(--navy);

    font-weight:
        900;
}


.feature .sub {

    font-size:
        10px;

    color:
        #8A9AAB;

    margin-top:
        3px;
}


.start-note {

    margin:
        10px
        0
        4px;

    color:
        #8A9AAB;

    font-size:
        10px;

    text-align:
        center;
}


/* TEST */

.exam-head {

    margin:
        0
        0
        18px;
}


.exam-kicker {

    color:
        var(--blue);

    font-size:
        12px;

    font-weight:
        900;

    margin-bottom:
        4px;
}


.exam-title {

    color:
        var(--navy);

    font-size:
        28px;

    line-height:
        1.25;

    font-weight:
        900;

    margin:
        0
        0
        4px;
}


.exam-meta {

    color:
        var(--muted);

    font-size:
        12px;
}


.progress-wrap {

    margin:
        12px
        0
        22px;
}


.progress-top {

    display:
        flex;

    justify-content:
        space-between;

    color:
        #66788A;

    font-size:
        11px;

    margin-bottom:
        6px;
}


.progress-track {

    height:
        8px;

    background:
        #E5EDF6;

    border-radius:
        999px;

    overflow:
        hidden;
}


.progress-fill {

    height:
        100%;

    background:
        var(--blue);

    border-radius:
        999px;
}


.question-card {

    background:
        #FFFFFF;

    border:
        1px solid
        var(--border);

    border-radius:
        18px;

    padding:
        30px
        26px;

    margin:
        0
        0
        20px;

    box-shadow:
        0
        6px
        20px
        rgba(43,76,110,.04);
}


.question-no {

    color:
        var(--blue);

    font-size:
        11px;

    font-weight:
        900;

    margin-bottom:
        10px;
}


.question-area {

    color:
        #7A8DA1;

    font-size:
        11px;

    margin-bottom:
        7px;
}


.question-text {

    color:
        var(--navy);

    font-size:
        21px;

    line-height:
        1.7;

    font-weight:
        900;

    word-break:
        keep-all;
}


.time-hint {

    color:
        #8B9BAD;

    font-size:
        10px;

    text-align:
        right;

    margin-top:
        16px;
}


.pass-note {

    color:
        #7B8DA0;

    font-size:
        11px;

    text-align:
        center;

    margin-top:
        5px;
}


/* RESULT */

.result-hero {

    text-align:
        center;

    margin:
        4px
        0
        20px;
}


.result-mark {

    width:
        54px;

    height:
        54px;

    border-radius:
        50%;

    background:
        #EAF3FF;

    color:
        var(--blue);

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    margin:
        0
        auto
        10px;

    font-size:
        25px;

    font-weight:
        900;
}


.result-title {

    color:
        var(--navy);

    font-size:
        27px;

    font-weight:
        900;
}


.result-sub {

    color:
        var(--muted);

    font-size:
        12px;

    margin-top:
        5px;
}


.metrics {

    display:
        grid;

    grid-template-columns:
        repeat(4,1fr);

    gap:
        10px;

    margin:
        0
        0
        14px;
}


.metric {

    background:
        #FFFFFF;

    border:
        1px solid
        var(--border);

    border-radius:
        15px;

    padding:
        14px
        8px;

    text-align:
        center;
}


.metric .label {

    color:
        #7B8DA0;

    font-size:
        10px;

    margin-bottom:
        4px;
}


.metric .value {

    color:
        var(--navy);

    font-size:
        20px;

    font-weight:
        900;
}


.result-card {

    background:
        #FFFFFF;

    border:
        1px solid
        var(--border);

    border-radius:
        17px;

    padding:
        18px;

    margin-bottom:
        12px;
}


.card-title {

    color:
        var(--navy);

    font-size:
        15px;

    font-weight:
        900;

    margin-bottom:
        14px;
}


.bar-row {

    margin-bottom:
        14px;
}


.bar-head {

    display:
        flex;

    justify-content:
        space-between;

    color:
        #4D6277;

    font-size:
        12px;

    margin-bottom:
        5px;
}


.bar-track {

    height:
        8px;

    background:
        #E8EEF5;

    border-radius:
        999px;

    overflow:
        hidden;
}


.bar-fill {

    height:
        100%;

    background:
        var(--blue);

    border-radius:
        999px;
}


.time-grid {

    display:
        grid;

    grid-template-columns:
        repeat(2,1fr);

    gap:
        8px;
}


.time-box {

    background:
        #F8FBFE;

    border:
        1px solid
        #E4ECF4;

    border-radius:
        12px;

    padding:
        11px
        12px;
}


.time-box .t-title {

    color:
        var(--navy);

    font-size:
        12px;

    font-weight:
        900;
}


.time-box .t-sub {

    color:
        #72859A;

    font-size:
        10px;
}


.recommend {

    background:
        #F8FBFE;

    border:
        1px solid
        #E4ECF4;

    border-radius:
        12px;

    padding:
        11px
        12px;

    margin-bottom:
        7px;
}


.recommend .r-label {

    color:
        var(--blue);

    font-size:
        10px;

    font-weight:
        900;
}


.recommend .r-text {

    color:
        var(--navy);

    font-size:
        13px;

    font-weight:
        900;
}


/* RECORDS */

.records-title {

    color:
        var(--navy);

    font-size:
        24px;

    font-weight:
        900;
}


.records-sub {

    color:
        var(--muted);

    font-size:
        11px;

    margin-bottom:
        14px;
}


.record-card {

    background:
        #FFFFFF;

    border:
        1px solid
        var(--border);

    border-radius:
        14px;

    padding:
        13px
        14px;

    margin-bottom:
        8px;
}


.record-top {

    display:
        flex;

    justify-content:
        space-between;

    gap:
        10px;
}


.record-name {

    color:
        var(--navy);

    font-size:
        14px;

    font-weight:
        900;
}


.record-meta {

    color:
        #72859A;

    font-size:
        10px;
}


.record-phone {

    color:
        var(--blue);

    font-size:
        11px;

    font-weight:
        900;

    text-align:
        right;
}


.record-score {

    color:
        var(--navy);

    font-size:
        12px;

    margin-top:
        8px;
}


.delete-note {

    color:
        var(--danger);

    font-size:
        11px;

    font-weight:
        800;

    margin:
        6px
        0;
}


/* MOBILE */

@media(max-width:699px) {

    .block-container {

        padding-left:
            .85rem;

        padding-right:
            .85rem;
    }


    .hero-title {

        font-size:
            27px;
    }


    .question-text {

        font-size:
            18px;
    }


    .metrics {

        grid-template-columns:
            repeat(2,1fr);
    }


    .time-grid {

        grid-template-columns:
            1fr;
    }
}


/* FINAL BUTTON ALIGNMENT OVERRIDE */

div[data-testid="stButton"] > button,
div.stButton > button,
button[kind="primary"],
button[kind="secondary"] {

    display:
        flex !important;

    flex-direction:
        column !important;

    align-items:
        center !important;

    justify-content:
        center !important;

    text-align:
        center !important;

    padding-top:
        0 !important;

    padding-bottom:
        0 !important;
}


div[data-testid="stButton"] > button > div,
div.stButton > button > div,
div[data-testid="stButton"] > button [data-testid="stMarkdownContainer"],
div.stButton > button [data-testid="stMarkdownContainer"] {

    display:
        flex !important;

    flex-direction:
        column !important;

    align-items:
        center !important;

    justify-content:
        center !important;

    text-align:
        center !important;

    width:
        100% !important;

    height:
        auto !important;

    min-height:
        0 !important;

    flex:
        0 0 auto !important;

    gap:
        4px !important;

    margin:
        0 !important;

    padding:
        0 !important;
}


div[data-testid="stButton"] > button p,
div[data-testid="stButton"] > button span,
div.stButton > button p,
div.stButton > button span {

    display:
        flex !important;

    flex-direction:
        column !important;

    align-items:
        center !important;

    justify-content:
        center !important;

    text-align:
        center !important;

    margin:
        0 !important;

    padding:
        0 !important;

    line-height:
        1.15 !important;
}

</style>""")
