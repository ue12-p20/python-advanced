nuancier_ratp = {
    '1': 'r242-v201-b49',
    '2': 'r33-v110-b180',
    '3': 'r154-v153-b64',
    '3B': 'r137-v199-b214',
    '4': 'r187-v77-b152',
    '5': 'r222-v139-b83',
    '6': 'r121-v187-b146',
    '7': 'r223-v154-b177',
    '7B': 'r121-v187-b146',
    '8': 'r197-v163-b202',
    '9': 'r205-v200-b63',
    '10': 'r223-v176-b57',
    '11': 'r142-v101-b56',
    '12': 'r50-v142-b91',
    '13': 'r137-v199-b214',
    '14': 'r103-v50-b142',
}

def convert(r_v_b):
    r, g, b = map(
        lambda x: int(x[1:]),
        r_v_b.split('-'))
    return f"#{r:02x}{g:02x}{b:02x}"

nuancier = {
    key: convert(value)
    for key, value in nuancier_ratp.items()
}
