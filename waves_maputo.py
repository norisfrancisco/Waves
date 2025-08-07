# =============================================================================
# OCORRÊNCIA E FREQUÊNCIA DE ONDAS DE CALOR E FRIO EM MAPUTO
# Baseado em padrões WMO/IPCC/FAO/INPE
# Autor: [Seu Nome]
# =============================================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from scipy.stats import linregress
from sklearn.preprocessing import StandardScaler
from fancyimpute import IterativeSVD
import calendar
import warnings

# === CONFIGURAÇÕES GERAIS ===
warnings.filterwarnings('ignore')
sns.set(style='whitegrid')

# === CAMINHOS ===
arquivo_entrada = "C:/Python/Waves/maputoo.xlsx"
saida = "C:/Python/Waves/Maputo"
os.makedirs(saida, exist_ok=True)

# =============================================================================
# 1. FUNÇÕES DE SUPORTE
# =============================================================================

def corrigir_ano(row):
    """Corrige datas considerando anos bissextos."""
    try:
        ano = int(row['YEAR'])
        dia_mes = row['DIA_MES']
        if not calendar.isleap(ano) and dia_mes.month == 2 and dia_mes.day == 29:
            return dia_mes.replace(day=28, year=ano)
        return dia_mes.replace(year=ano)
    except Exception:
        return pd.NaT

def identificar_ondas(df, col_extremo, min_dias=3):
    """Identifica sequências de dias consecutivos com extremos."""
    sequencias, atual = [], []
    for i, flag in enumerate(df[col_extremo]):
        if flag:
            atual.append(i)
        elif len(atual) >= min_dias:
            sequencias.append(atual)
            atual = []
        else:
            atual = []
    if len(atual) >= min_dias:
        sequencias.append(atual)
    return sequencias

def salvar_fig(fig, nome):
    """Salva figura com padrão de qualidade."""
    fig.tight_layout()
    fig.savefig(os.path.join(saida, nome), dpi=300)
    plt.close(fig)

# =============================================================================
# 2. LEITURA E PRÉ-PROCESSAMENTO
# =============================================================================

df = pd.read_excel(arquivo_entrada, engine='openpyxl')
df.columns = ['YEAR', 'DIA_MES', 'T2M_MAX', 'T2M_MIN']
df['DIA_MES'] = pd.to_datetime(df['DIA_MES'], errors='coerce')
df['DATA_COMPLETA'] = df.apply(corrigir_ano, axis=1)
df.dropna(subset=['DATA_COMPLETA'], inplace=True)
df.drop_duplicates(subset='DATA_COMPLETA', inplace=True)
df['T2M_MED'] = (df['T2M_MAX'] + df['T2M_MIN']) / 2

# =============================================================================
# 3. IMPUTAÇÃO COM IterativeSVD
# =============================================================================

variaveis = ['T2M_MAX', 'T2M_MIN', 'T2M_MED']
scaler = StandardScaler()
df[variaveis] = IterativeSVD(rank=2).fit_transform(scaler.fit_transform(df[variaveis]))

# =============================================================================
# 4. CLIMATOLOGIA DE REFERÊNCIA 1991–2020
# =============================================================================

df['DOY'] = df['DATA_COMPLETA'].dt.dayofyear
normal = df[(df['YEAR'] >= 1991) & (df['YEAR'] <= 2020)]
climatologia = normal.groupby('DOY').agg(
    Normal_Tmax=('T2M_MAX', 'mean'),
    Desvio_Tmax=('T2M_MAX', 'std'),
    Percentil90_Tmax=('T2M_MAX', lambda x: np.percentile(x, 90)),
    Percentil10_Tmax=('T2M_MAX', lambda x: np.percentile(x, 10)),
    Normal_Tmin=('T2M_MIN', 'mean'),
    Desvio_Tmin=('T2M_MIN', 'std'),
    Percentil90_Tmin=('T2M_MIN', lambda x: np.percentile(x, 90)),
    Percentil10_Tmin=('T2M_MIN', lambda x: np.percentile(x, 10)),
    Normal_Tmed=('T2M_MED', 'mean'),
    Desvio_Tmed=('T2M_MED', 'std')
).reset_index()

df = df.merge(climatologia, on='DOY', how='left')

# =============================================================================
# 5. EXTREMOS E ONDAS DE CALOR/FRIO
# =============================================================================

df['Anomalia_Tmax'] = df['T2M_MAX'] - df['Normal_Tmax']
df['Anomalia_Tmin'] = df['T2M_MIN'] - df['Normal_Tmin']
df['Extremo_Calor_Tmax'] = df['T2M_MAX'] > df['Percentil90_Tmax']
df['Extremo_Frío_Tmin'] = df['T2M_MIN'] < df['Percentil10_Tmin']
df['SU'] = df['T2M_MAX'] > 25

ondas_calor = identificar_ondas(df, 'Extremo_Calor_Tmax')
ondas_frio = identificar_ondas(df, 'Extremo_Frío_Tmin')

df['WSDI'] = False
df['CSDI'] = False
for seq in ondas_calor: df.loc[seq, 'WSDI'] = True
for seq in ondas_frio: df.loc[seq, 'CSDI'] = True

ondas_df = pd.DataFrame(
    [{"Inicio": df.loc[seq[0], 'DATA_COMPLETA'], "Fim": df.loc[seq[-1], 'DATA_COMPLETA'],
      "Duracao": len(seq), "Tipo": "Calor"} for seq in ondas_calor] +
    [{"Inicio": df.loc[seq[0], 'DATA_COMPLETA'], "Fim": df.loc[seq[-1], 'DATA_COMPLETA'],
      "Duracao": len(seq), "Tipo": "Frio"} for seq in ondas_frio]
)

# =============================================================================
# 6. ÍNDICES E ANÁLISE SAZONAL
# =============================================================================

dias_ano = df.groupby('YEAR').size()
tx90p = df.groupby('YEAR')['Extremo_Calor_Tmax'].sum() / dias_ano * 100
tn10p = df.groupby('YEAR')['Extremo_Frío_Tmin'].sum() / dias_ano * 100

df['MES'] = df['DATA_COMPLETA'].dt.month
df['SAZONAL'] = df['MES'].map(lambda m: 'DJF' if m in [12,1,2] else 'MAM' if m in [3,4,5] else 'JJA' if m in [6,7,8] else 'SON')
sazonal = df.groupby(['YEAR', 'SAZONAL']).agg(
    Dias_Calor=('Extremo_Calor_Tmax', 'sum'),
    Dias_Frio=('Extremo_Frío_Tmin', 'sum'),
    Media_Anom_Tmax=('Anomalia_Tmax', 'mean'),
    Media_Anom_Tmin=('Anomalia_Tmin', 'mean')
).reset_index()

group = df.groupby('YEAR')
etccdi = group.agg(
    TXx=('T2M_MAX', 'max'), TXn=('T2M_MAX', 'min'),
    TNx=('T2M_MIN', 'max'), TNn=('T2M_MIN', 'min'),
    FD=('T2M_MIN', lambda x: (x < 0).sum()),
    TR=('T2M_MIN', lambda x: (x > 20).sum()),
    ID=('T2M_MAX', lambda x: (x < 0).sum())
).reset_index()
etccdi['DTR'] = group['T2M_MAX'].mean().values - group['T2M_MIN'].mean().values

# =============================================================================
# 7. CLIMATOLOGIA DIÁRIA - GRÁFICO
# =============================================================================

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(climatologia['DOY'], climatologia['Normal_Tmax'], label='Normal Tmax', color='red')
ax.plot(climatologia['DOY'], climatologia['Normal_Tmin'], label='Normal Tmin', color='blue')
ax.fill_between(climatologia['DOY'], climatologia['Percentil10_Tmax'], climatologia['Percentil90_Tmax'],
                color='salmon', alpha=0.3, label='Tmax P10–P90')
ax.fill_between(climatologia['DOY'], climatologia['Percentil10_Tmin'], climatologia['Percentil90_Tmin'],
                color='lightblue', alpha=0.3, label='Tmin P10–P90')
ax.set_title("Climatologia Diária (1991–2020)")
ax.set_xlabel("Dia do Ano"); ax.set_ylabel("Temperatura (°C)")
ax.legend(); ax.grid(True)
salvar_fig(fig, "Climatologia_WMO_Tmax_Tmin.png")

# =============================================================================
# 8. EXPORTAÇÃO DOS RESULTADOS
# =============================================================================

df.to_excel(os.path.join(saida, "Serie_Completa_Tratada.xlsx"), index=False)
climatologia.to_excel(os.path.join(saida, "Climatologia_1991_2020.xlsx"), index=False)
tx90p.to_frame("TX90p (%)").join(tn10p.to_frame("TN10p (%)")).to_excel(
    os.path.join(saida, "Indices_TX90p_TN10p.xlsx"))
sazonal.to_excel(os.path.join(saida, "Resumo_Sazonal_Extremos.xlsx"), index=False)
etccdi.to_excel(os.path.join(saida, "Indices_ETCCDI_Adicionais.xlsx"), index=False)
ondas_df.to_excel(os.path.join(saida, "Ondas_Calor_Frio_Maputo.xlsx"), index=False)

print("\n✅ Análise finalizada com sucesso!")
print(f"📁 Arquivos salvos em: {saida}")

# =============================================================================
# FIM
# =============================================================================