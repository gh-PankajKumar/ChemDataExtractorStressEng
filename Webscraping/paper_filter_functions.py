def is_incomplete_paper(fstring, filename):
    if "<xocs:rawtext>" in fstring:
        return True
    return False


def is_openaccess(fstring, filename):
    if "<openaccess>1</openaccess>" in fstring:
        return True
    elif "<openaccess>0</openaccess>" in fstring:
        return False
    return "Error"


def is_paper(fstring, filename):
    if "<xocs:document-subtype>fla</xocs:document-subtype>" in fstring:
        return True

    return False
