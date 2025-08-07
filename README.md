# Waves

Este repositório apresenta uma análise detalhada da ocorrência e frequência de ondas de calor e de frio em Maputo, Moçambique, utilizando dados de reanálise ERA5-Land (ECMWF) e métodos estatísticos reconhecidos por instituições como a OMM e o IPCC.

## Objetivo

Investigar a variabilidade sazonal e as tendências climáticas associadas a extremos térmicos no período de 1991 a 2020, contribuindo para o entendimento local dos efeitos das mudanças climáticas.

## Estrutura do Projeto

```
Waves/
├── data/                 # Arquivos de entrada (.xlsx)
├── notebooks/            # Jupyter Notebooks com análise e gráficos
├── outputs/              # Figuras e resultados exportados
├── src/                  # Scripts em Python (.py)
├── .gitignore            # Arquivos ignorados pelo Git
├── README.md             # Este documento
```

## Bibliotecas Utilizadas

* `pandas`, `numpy` para manipulação de dados
* `matplotlib`, `seaborn` para visualização
* `fancyimpute` para imputar valores faltantes (IterativeSVD)
* `scikit-learn` para padronização de variáveis

## Metodologia

* **Base de dados:** ERA5-Land (resolução horária agregada a diária)
* **Período:** 1991 a 2020 (30 anos)
* **Climatologia:** Calculada com base em médias e percentis diários
* **Definição de extremos:**

  * Ondas de calor: Tmax > percentil 90 por ≥3 dias consecutivos
  * Ondas de frio: Tmin < percentil 10 por ≥3 dias consecutivos
* **Cálculo de índices climáticos (ETCCDI):** TXx, TNx, FD, TR, DTR, entre outros

## Resultados Exportados

* `Cleaned_Full_Series.xlsx`
* `Climatology_1991_2020.xlsx`
* `Extreme_Indices_TX90p_TN10p.xlsx`
* `Seasonal_Summary.xlsx`
* `Heat_Cold_Waves_Maputo.xlsx`
* Gráficos salvos em PNG (mapas, boxplots, linhas temporais)

## Como Usar

```bash
# Clone o repositório
https://github.com/norisfrancisco/Waves.git
cd Waves

# Instale as dependências
pip install -r requirements.txt

# Execute os notebooks ou scripts em src/
```

## Autor

**Francisco Noris**

Para sugestões, dúvidas ou colaborações, utilize a aba de Issues ou envie um Pull Request.

---

Projeto desenvolvido com base em recomendações da World Meteorological Organization (WMO), Intergovernmental Panel on Climate Change (IPCC) e literatura científica recente.
