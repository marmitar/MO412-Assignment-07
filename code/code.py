from math import floor, gamma, nan
from typing import Sequence
import os.path
import pandas as pd
from scipy.optimize import minimize
from scipy.special import zeta


DIRECTORY = os.path.dirname(__file__)
PARENT = os.path.dirname(DIRECTORY)

def parse(text: str):
    try:
        return float(text.strip(' *-'))
    except ValueError:
        return nan


NUM = '$N$'
GAMMA_IN = '$\\gamma_\\text{in}$'
GAMMA_OUT = '$\\gamma_\\text{out}$'

def read(path: str = os.path.join(DIRECTORY, 'chapter4.html')):
    [table] = pd.read_html(path, attrs={'id': 'table-4-1'})

    gamma = table['γ'].map(parse)
    g_in = table['γin'].map(parse)
    g_out = table['γout'].map(parse)

    g_in[g_in.isna()] = gamma[g_in.isna()]
    g_out[g_out.isna()] = gamma[g_out.isna()]

    df = table[['Network']].copy()
    df[NUM] = table['N'].map(int)
    df[GAMMA_IN] = g_in
    df[GAMMA_OUT] = g_out
    return df.dropna()

def save(table: pd.DataFrame, path: str = os.path.join(PARENT, 'texts/table.tex')):
    columns = 'c' * len(table.columns)

    content: str = (
        table.style
            .hide()
            .format_index(escape='latex')
            .format(escape='latex', precision=2)
            .to_latex(hrules=True, column_format=columns)
    )
    for rule in ('bottomrule', 'toprule'):
        content = content.replace(f'\\{rule}', f'\\{rule}\\{rule}')

    with open(path, 'w') as file:
        file.write(content)


def kmax_solver(gamma: float, N: int, kmin: int = 1):
    zg = zeta(gamma, kmin)
    def fun(kmax: float):
        [diff] = (zeta(gamma, kmax) / zg) - 1/N
        return abs(diff)

    res = minimize(fun, x0=[N/2], method='Nelder-Mead', tol=1e-6)
    if not res.success:
        raise ValueError(res.message)

    kmax = floor(res.x[0])
    while zeta(gamma, kmax) > 1/N:
        kmax += 1

    print(f"kmax({gamma=:5}, {N=:6}, {kmin=}) = {kmax:6}")
    return kmax

def kmax(gamma: pd.Series, N: pd.Series, *, continuous: bool, kmin: int = 1):
    if continuous:
        return kmin * N**(1 / (gamma - 1))
    else:
        return [kmax_solver(g, n, kmin) for g, n in zip(gamma, N)]


if __name__ == '__main__':
    table = read()
    table['${k_{\\max}}_\\text{in}$ C'] = kmax(table[GAMMA_IN], table[NUM], continuous=True)
    table['${k_{\\max}}_\\text{out}$ C'] = kmax(table[GAMMA_OUT], table[NUM], continuous=True)
    table['${k_{\\max}}_\\text{in}$ D'] = kmax(table[GAMMA_IN], table[NUM], continuous=False)
    table['${k_{\\max}}_\\text{out}$ D'] = kmax(table[GAMMA_OUT], table[NUM], continuous=False)
    save(table)
