# Waves Maputo

Este repositório apresenta uma análise abrangente da ocorrência e frequência de extremos térmicos (ondas de calor e frio), com base em dados de reanálise ERA5-Land, utilizando métodos reconhecidos pela OMM, IPCC e FAO.

## Objetivo

Investigar padrões sazonais e tendências climáticas no período de 1991 a 2020, identificando eventos extremos e gerando índices climáticos relevantes para análise de risco e suporte à tomada de decisão em setores como agricultura e saúde pública.

## Estrutura do Projeto

```
Waves_Maputo/
├── data/                 # Dados originais e processados (.xlsx)
├── notebooks/            # Notebooks Jupyter com a análise
├── outputs/              # Figuras geradas (PNG)
├── src/                  # Scripts Python reutilizáveis (.py)
├── README.md             # Este arquivo
├── .gitignore            # Arquivos ignorados pelo Git
```

## Principais Ferramentas e Bibliotecas

* Python 3
* pandas, numpy, matplotlib, seaborn
* fancyimpute (IterativeSVD)
* scikit-learn (StandardScaler)

## Metodologia

* **Fonte dos dados:** ERA5-Land (ECMWF)
* **Período:** 1991–2020
* **Climatologia:** Calculada com base na média e percentis diários
* **Critério de extremos:**

  * **TX90p:** Temperaturas máximas acima do percentil 90
  * **TN10p:** Temperaturas mínimas abaixo do percentil 10
* **Ondas de calor/frio:** Eventos com ≥3 dias consecutivos de extremos
* **Imputação:** IterativeSVD + Padronização (StandardScaler)

## Resultados Produzidos

* **Série temporal tratada** (`Cleaned_Full_Series.xlsx`)
* **Climatologia 1991-2020** (`Climatology_1991_2020.xlsx`)
* **Índices de extremos** (`Extreme_Indices_TX90p_TN10p.xlsx`)
* **Resumo sazonal** (`Seasonal_Summary.xlsx`)
* **Ondas de calor e frio** (`Heat_Cold_Waves_Maputo.xlsx`)
* **Gráficos PNG salvos em `outputs/`**

## Como Executar

1. Clone o repositório:

   ```bash
   git clone https://github.com/norisfrancisco/Waves_Maputo.git
   cd Waves_Maputo
   ```
2. Instale as dependências (recomendado usar virtualenv ou conda):

   ```bash
   pip install -r requirements.txt
   ```
3. Execute os notebooks em `notebooks/` ou scripts em `src/`

## Autor

**Francisco Noris**
Maputo, Moçambique

---

Projeto em conformidade com os padrões WMO/IPCC/FAO.
Para colaborações ou sugestões, abra uma *issue* ou envie um *pull request*.
