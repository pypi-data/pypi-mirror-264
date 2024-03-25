import re

def isEmail(email):
    # Pemeriksaan validitas email sederhana
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False

def isHTML(html):
    # Pemeriksaan validitas HTML sederhana
    # Anda dapat menggunakan library HTML parser yang lebih canggih untuk pemeriksaan yang lebih akurat
    if "<html>" in html:
        return True
    return False