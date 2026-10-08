

def saluer(nom): return "Bonjour " + nom


def test_saluer(): assert saluer("YSN") == "Bonjour YSN" 

def test_saluer_vide(): assert saluer("") == "Bonjour "