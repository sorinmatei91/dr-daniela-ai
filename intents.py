def detect_programare(text):

    keywords = [
        "programare",
        "programez",
        "vreau la medic",
        "vreau consultație",
        "vreau consultatie",
        "cum mă programez",
        "cum ma programez",
        "aș vrea o consultație",
        "as vrea o consultatie"
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
        "unde o gasesc"
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
        "amețeală",
        "ameteala",
        "leșin",
        "lesin"
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
        "ecografie",
        "papanicolau",
        "test papanicolau",
        "sterilet",
        "menopauză",
        "menopauza",
        "contracepție",
        "contraceptie"
    ]

    text = text.lower()

    return any(
        keyword in text
        for keyword in keywords
    )