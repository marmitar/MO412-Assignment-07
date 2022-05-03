from math import nan
import os.path
import pandas as pd


DIRECTORY = os.path.dirname(__file__)
PARENT = os.path.dirname(DIRECTORY)

def parse(text: str):
    try:
        return float(text.strip(' *-'))
    except ValueError:
        return nan


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
    df['$N$'] = table['N'].map(int)
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


def kmax(gamma: float, N: int, kmin: int = 1):
    return kmin * (N ** (1 / (gamma - 1)))


if __name__ == '__main__':
    table = read()
    table['${k_{\\max}}_\\text{in}$'] = kmax(table[GAMMA_IN], table['$N$'])
    table['${k_{\\max}}_\\text{out}$'] = kmax(table[GAMMA_OUT], table['$N$'])
    save(table)
