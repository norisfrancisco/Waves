# Waves_Maputo

Este projeto realiza uma análise da ocorrência e frequência de extremos térmicos — ondas de calor e ondas de frio, com base em dados diários de temperatura do conjunto de reanálise ERA5-Land, desenvolvido pelo Centro Europeu de Previsões Meteorológicas de Médio Prazo (ECMWF). O período analisado compreende 30 anos (1991–2020), fornecendo uma base robusta para identificação de tendências climáticas e variabilidade sazonal.

Os dados brutos foram inicialmente obtidos com resolução horária e, posteriormente, agregados em valores diários de temperatura máxima (Tmax), mínima (Tmin) e média (Tmed). O pré-processamento dos dados incluiu tratamento de ausências utilizando imputação multivariada por IterativeSVD, precedida de normalização com StandardScaler. A qualidade da imputação foi verificada com validação cruzada, resultando em um RMSE inferior a 1 °C.

A climatologia de referência foi construída conforme as diretrizes da Organização Meteorológica Mundial (WMO, 2024), considerando o período de 1991 a 2020. As normais diárias e os percentis 10 e 90 para Tmax e Tmin foram calculados para representar os limites naturais da variabilidade térmica local.

Extremos térmicos foram identificados com base nos percentis: eventos de calor extremo quando a Tmax ultrapassa o percentil 90 (TX90p) e de frio extremo quando a Tmin fica abaixo do percentil 10 (TN10p). Ondas de calor e de frio foram definidas como sequências de ao menos três dias consecutivos de extremos, em conformidade com padrões ETCCDI, WMO e IPCC. Foram quantificados os índices WSDI (Warm Spell Duration Index) e CSDI (Cold Spell Duration Index), além da frequência e duração dos eventos.

Índices adicionais calculados incluem:  
• TXx – temperatura máxima anual mais alta  
• TXn – temperatura máxima anual mais baixa  
• TNx – temperatura mínima anual mais alta  
• TNn – temperatura mínima anual mais baixa  
• FD – dias com geada (Tmin < 0 °C)  
• TR – noites tropicais (Tmin > 20 °C)  
• ID – dias frios (Tmax < 0 °C)  
• DTR – amplitude térmica diária média (Tmax − Tmin)

Todos os procedimentos foram implementados em Python, utilizando bibliotecas como `pandas`, `numpy`, `matplotlib`, `scikit-learn` e `fancyimpute`. O projeto é reprodutível e escalável, fornecendo arquivos de saída organizados, gráficos informativos e relatórios exportáveis.

---

**Licença:** MIT  
**Autor:** Francisco Noris  
**Dados:** ERA5-Land – ECMWF  
