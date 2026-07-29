def detect_programare(text):

    keywords = [
        "programare",
        "programez",
        "vreau la medic",
        "vreau consultație",
        "vreau consultatie",
        "vreau un consult",
        "as vrea un consult",
        "aș vrea un consult",
        "cum mă programez",
        "cum ma programez",
        "aș vrea o consultație",
        "as vrea o consultatie",
        "aș vrea să fac o programare",
        "as vrea sa fac o programare",
        "vreau o programare",
        "doresc o programare",
        "doresc sa ma programez",
        "vreau sa ma programez"
    ]

    text = text.lower()

    return any(
        keyword in text
        for keyword in keywords
    )





def detect_locatie(text):

    keywords = [
        "unde consultă",
        "unde consulta",
        "unde lucrează",
        "unde lucreaza",
        "la ce clinică",
        "la ce clinica",
        "unde este cabinetul",
        "unde o găsesc",
        "unde o gasesc",
        "unde pot merge",
        "unde se află",
        "unde se afla",
        "locatie",
        "locație"
    ]

    text = text.lower()

    return any(
        keyword in text
        for keyword in keywords
    )





def detect_urgent_symptoms(text):

    keywords = [
        "sângerări în sarcină",
        "sangerari in sarcina",
        "sângerare în sarcină",
        "sangerare in sarcina",
        "sângerez",
        "sangerez",
        "am sângerări",
        "am sangerari",
        "sângerare",
        "sangerare",
        "durere puternică",
        "durere puternica",
        "durere severă",
        "durere severa",
        "durere foarte mare",
        "durere insuportabilă",
        "durere insuportabila",
        "amețeală",
        "ameteala",
        "leșin",
        "lesin",
        "pierdere de sânge",
        "pierdere de sange"
    ]

    text = text.lower()

    return any(
        keyword in text
        for keyword in keywords
    )





def detect_servicii(text):

    keywords = [
        "servicii",
        "ce servicii",
        "ce faceți",
        "ce faceti",
        "ce oferiți",
        "ce oferiti",
        "ce consultații aveți",
        "ce consultatii aveti"
    ]

    text = text.lower()

    return any(
        keyword in text
        for keyword in keywords
    )