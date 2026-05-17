# 📊 BB Market Predictor - LSTM Monitoring API

Projeto desenvolvido para predição de preços de ações utilizando redes neurais LSTM com monitoramento completo da aplicação e do modelo em produção.

A solução foi construída utilizando **FastAPI, TensorFlow/Keras, Docker, Prometheus e Grafana**, permitindo não apenas a realização de previsões financeiras, mas também o acompanhamento em tempo real da performance operacional e da qualidade preditiva do modelo.

---

# 🚀 API em Produção

A API está disponível em:

http://tech4.securitylinux.com.br:8000/docs#/

Documentação interativa via Swagger UI.

---

# 🚀 Tecnologias Utilizadas

- Python 3.11  
- FastAPI  
- TensorFlow / Keras  
- Scikit-Learn  
- SQLAlchemy  
- Supabase (PostgreSQL)  
- Docker  
- Prometheus  
- Grafana  
- Node Exporter  
- Linux Ubuntu Server 24.04 LTS  

---

# 🧠 Modelo de Machine Learning

O modelo utilizado é uma rede neural LSTM (Long Short-Term Memory), projetada para análise de séries temporais financeiras.

## 📌 Características do modelo

- Utiliza janela histórica mínima de 30 dias como entrada  
- Realiza previsão de 1 dia à frente (t+1)  
- Normalização e pré-processamento dos dados históricos  
- Exportação em formato TensorFlow SavedModel  
- Estrutura preparada para versionamento de modelos  

## 📉 Limitação do modelo

Cada inferência representa apenas um passo futuro (t+1), sendo necessário fornecer no mínimo 30 dias de histórico para execução da previsão.

---

# 🖥️ Infraestrutura

A aplicação foi implantada em um servidor Linux Ubuntu Server 24.04 LTS, utilizando containers Docker para gerenciamento dos serviços e monitoramento da infraestrutura em tempo real.

O ambiente conta com:

- API FastAPI containerizada  
- Monitoramento com Prometheus  
- Dashboards Grafana  
- Node Exporter para métricas do servidor  
- Banco de dados PostgreSQL via Supabase  

---

# 🧠 Funcionalidades

## 📈 API de Predição

- Endpoint para previsão de preços utilizando modelo LSTM  
- Entrada obrigatória de mínimo de 30 dias de dados históricos  
- Pipeline de inferência em produção  
- Retorno de previsão para o próximo dia (t+1)  

---

## 📊 Monitoramento do Modelo

O sistema implementa um loop contínuo de feedback baseado em dados reais.

São calculadas automaticamente as seguintes métricas:

- MAE (Mean Absolute Error)  
- RMSE (Root Mean Squared Error)  
- MAPE (Mean Absolute Percentage Error)  

As métricas são atualizadas continuamente conforme novos valores reais são registrados.

---

## 🔄 Pipeline de Feedback

O sistema implementa um ciclo contínuo de avaliação do modelo em produção, permitindo medir a performance real das previsões ao longo do tempo.

O fluxo funciona da seguinte forma:

- O modelo realiza uma previsão com base em 30 dias de dados históricos
- A previsão gerada (t+1) é armazenada no sistema
- Após a disponibilidade do valor real, ele é enviado para a API de feedback
- O sistema associa previsão vs valor real
- É calculado o erro da predição (MAE, RMSE e MAPE)
- As métricas globais do modelo são atualizadas automaticamente

Esse processo permite:

- Monitoramento contínuo da performance do modelo em produção  
- Identificação de degradação de desempenho (model drift)  
- Base para futuras estratégias de retreinamento  


---

# 📡 Observabilidade (Prometheus + Grafana)

A aplicação expõe métricas para monitoramento em tempo real via Prometheus.

## 📊 Métricas expostas

- `api_requests_total` → Total de requisições  
- `api_request_latency_seconds` → Latência da API  
- `model_mae` → Erro absoluto médio do modelo  
- `model_rmse` → Raiz do erro quadrático médio  
- `model_mape` → Erro percentual médio  

---

# 📊 Dashboards Grafana

O sistema possui dashboards dedicados no Grafana para observabilidade completa.

## 🖥️ Dashboard da API

- Volume de requisições  
- Latência por endpoint  
- Saúde da aplicação  
- Consumo de recursos do servidor  

## 🧠 Dashboard do Modelo

- Evolução do MAE ao longo do tempo  
- RMSE em produção  
- MAPE evolutivo  
- Quantidade de previsões avaliadas  
- Qualidade preditiva em tempo real  

---

# 🐳 Deploy

A aplicação é executada em containers Docker, garantindo:

- Isolamento dos serviços  
- Escalabilidade simplificada  
- Reprodutibilidade do ambiente  
- Facilidade de deploy em servidores Linux  

## 🔧 Componentes do deploy

- API FastAPI (serviço principal)  
- Prometheus (coleta de métricas)  
- Grafana (visualização e dashboards)  
- Node Exporter (métricas do servidor)  

---

# 📊 Objetivo do Projeto

Demonstrar um pipeline completo de Machine Learning em produção, incluindo:

- Inferência de modelo em tempo real  
- Monitoramento contínuo de performance  
- Observabilidade de infraestrutura e aplicação  
- Logging e rastreabilidade de previsões  
- Feedback loop para avaliação de modelo  
- Integração com práticas de DevOps/SRE  

---

# 🔥 Diferenciais Técnicos

- Monitoramento de ML em tempo real  
- Integração Prometheus + Grafana  
- Pipeline de feedback contínuo  
- API REST documentada via Swagger  
- Arquitetura preparada para produção  
- Infraestrutura em Linux Ubuntu Server 24.04 LTS  
- Modelo LSTM com janela temporal (30 dias → 1 dia)  
- Sistema completo de observabilidade e métricas de modelo  