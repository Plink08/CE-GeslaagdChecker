import streamlit as st

# --- Pagina Configuratie ---
st.set_page_config(page_title="VWO Examen Dashboard", layout="centered")

# Kleuren en Styling
COLOR_SUCCESS = "#2ecc71"
COLOR_DANGER = "#e74c3c"

# --- Profiel Data ---
PROFILES = {
    "Natuur & Techniek": [
        ("Nederlands", True, 6.0, True), ("Engels", True, 6.0, True), ("Wiskunde B", True, 6.0, True),
        ("Natuurkunde", False, 6.0, True), ("Scheikunde", False, 6.0, True), ("Vak 6", False, 6.0, True)
    ],
    "Natuur & Gezondheid": [
        ("Nederlands", True, 6.0, True), ("Engels", True, 6.0, True), ("Wiskunde A", True, 6.0, True),
        ("Biologie", False, 6.0, True), ("Scheikunde", False, 6.0, True), ("Vak 6", False, 6.0, True)
    ],
    "Economie & Maatschappij": [
        ("Nederlands", True, 6.0, True), ("Engels", True, 6.0, True), ("Wiskunde A", True, 6.0, True),
        ("Economie", False, 6.0, True), ("Geschiedenis", False, 6.0, True), ("Vak 6", False, 6.0, True)
    ],
     "Cultuur & Maatschappij": [
        ("Nederlands", True, "6.0", True), ("Engels", True, "6.0", True), ("Wiskunde A", True, "6.0", True),
        ("Geschiedenis", False, "6.0", True), ("Vak 6", False, "6.0", True), ("Vak 7", False, "6.0", True)
    ]
}

# --- Logica Functies ---
def rond_af(cijfer):
    return int(cijfer + 0.5) if cijfer >= 0 else int(cijfer - 0.5)

def bereken_status(vakken_data, combinatie, lo_status):
    eindcijfers = [combinatie]
    ce_cijfers = []
    kernvak_cijfers = []
    
    for vak in vakken_data:
        se, ce, has_ce, is_kern = vak['se'], vak['ce'], vak['has_ce'], vak['is_kern']
        eind = rond_af((se + ce) / 2) if has_ce else rond_af(se)
        eindcijfers.append(eind)
        if has_ce: ce_cijfers.append(ce)
        if is_kern: kernvak_cijfers.append(eind)

    # 1. CE Gemiddelde
    if ce_cijfers:
        gem_ce = sum(ce_cijfers) / len(ce_cijfers)
        if gem_ce < 5.5:
            return False, f"GEZAKT: CE-gemiddelde ({gem_ce:.2f}) < 5.5", gem_ce
    else: gem_ce = 0.0

    # 2. Kernvakken
    onv_kern = [c for c in kernvak_cijfers if c < 6]
    if any(c < 5 for c in kernvak_cijfers):
        return False, "GEZAKT: Kernvak lager dan 5", gem_ce
    if len(onv_kern) > 1:
        return False, "GEZAKT: Te veel onvoldoendes in kernvakken", gem_ce

    # 3. Algemene regels
    onv = [c for c in eindcijfers if c < 6]
    gem_eind = sum(eindcijfers) / len(eindcijfers)

    if any(c < 4 for c in eindcijfers):
        return False, "GEZAKT: Eindcijfer lager dan een 4", gem_ce
    if len(onv) == 2 and gem_eind < 6.0:
        return False, f"GEZAKT: Gemiddelde ({gem_eind:.2f}) te laag voor 2 onvoldoendes", gem_ce
    elif len(onv) > 2:
        return False, f"GEZAKT: Te veel onvoldoendes ({len(onv)})", gem_ce

    if lo_status != "Voldoende/Goed":
        return False, "GEZAKT: LO niet voldoende", gem_ce

    return True, f"GESLAAGD! Gemiddelde: {gem_eind:.2f}", gem_ce

# --- UI Opbouw ---
st.title("VWO Slaag/Zak Indicator")
st.markdown("Bereken direct of je geslaagd bent op basis van de wettelijke VWO-regels.")

# Profiel Kiezer
gekozen_profiel = st.selectbox("Snelvullen met profiel:", list(PROFILES.keys()), index=0)

# Input Sectie
vakken_invoer = []
st.subheader("Cijfers per vak")

# Headers voor de kolommen
col1, col2, col3, col4, col5 = st.columns([3, 1.5, 1, 1.5, 1])
col1.caption("Vaknaam")
col2.caption("SE")
col3.caption("CE?")
col4.caption("CE")
col5.caption("Eind")

for i, (naam, is_kern, se_default, heeft_ce) in enumerate(PROFILES[gekozen_profiel]):
    with st.container():
        c1, c2, c3, c4, c5 = st.columns([3, 1.5, 1, 1.5, 1])
        
        # Vaknaam & Type
        v_naam = c1.text_input(f"Vak {i}", value=naam, label_visibility="collapsed")
        if is_kern: c1.caption("Kernvak (N/E/W)")

        # SE Cijfer
        se_val = c2.number_input(f"SE {i}", 1.0, 10.0, float(se_default), 0.1, label_visibility="collapsed")
        
        # CE Checkbox
        has_ce = c3.checkbox("CE", value=heeft_ce, key=f"ce_check_{i}", label_visibility="collapsed")
        
        # CE Cijfer
        if has_ce:
            ce_val = c4.number_input(f"CE {i}", 1.0, 10.0, 6.0, 0.1, label_visibility="collapsed")
            eind = rond_af((se_val + ce_val) / 2)
        else:
            ce_val = 0.0
            c4.write("N.v.t.")
            eind = rond_af(se_val)
        
        # Eindcijfer display
        color = COLOR_SUCCESS if eind >= 6 else COLOR_DANGER
        c5.markdown(f"<h3 style='text-align: center; color: {color}; margin:0;'>{eind}</h3>", unsafe_allow_html=True)
        
        vakken_invoer.append({'se': se_val, 'ce': ce_val, 'has_ce': has_ce, 'is_kern': is_kern})

st.divider()

# Footer Inputs
f_col1, f_col2 = st.columns(2)
comb = f_col1.number_input("Combinatiecijfer (PWS/Maat.):", 1, 10, 6)
lo = f_col2.selectbox("LO Status:", ["Voldoende/Goed", "Onvoldoende"])

# --- Resultaat ---
geslaagd, bericht, gem_ce = bereken_status(vakken_invoer, comb, lo)

if geslaagd:
    st.success(bericht)
else:
    st.error(bericht)

# Extra statistieken
st.info(f"**CE Gemiddelde:** {gem_ce:.2f} (Minimaal 5.50 nodig)")
