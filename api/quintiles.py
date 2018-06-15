import math

from .models import Gov


def calculate(government):
    """
    calculate the quantiles for this government
    """
    score_quintile = {}
    ranking_total = Gov.objects.filter(gcid=government.govid.gcid).count()

    range_dict = quntiles(ranking_total)

    benchmarks = {
        'idp_score': government.idpscore,
        'service_del_score': government.servicedelscore,
        'finance_score': government.financescore,
        'hr_score': government.hrscore
    }
    for name, score in benchmarks.items():
        for quintile, full_range in range_dict.items():
            if score in full_range:
                score_quintile[name] = int(quintile)
                break

    return score_quintile


def quntiles(total):
    """
    calculate range of each of the quintiles
    """
    max_first = math.ceil(total * 0.2)
    max_second = math.ceil(total * 0.4)
    max_third = math.ceil(total * 0.6)
    max_fourth = math.ceil(total * 0.8)

    q1 = range(0, max_first + 1)
    q2 = range(max_first, max_second + 1)
    q3 = range(max_second, max_third + 1)
    q4 = range(max_third, max_fourth + 1)
    q5 = range(max_fourth, total + 1)
    return {
        '1': q1,
        '2': q2,
        '3': q3,
        '4': q4,
        '5': q5
    }
