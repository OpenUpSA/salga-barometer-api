def density(queryset):
    """
    Calculate the density
    """
    calc = []
    for res in queryset:
        if res.iid.name.startswith("Area"):
            calc.insert(0, float(res.value.replace(',', '.')))
        else:
            calc.insert(1, float(res.value.replace(',', '.')))
    return calc[1] / calc[0], calc[1], calc[0]
