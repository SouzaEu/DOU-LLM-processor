# Core do SaaS de Alertas Regulatórios

## Visão Geral

Este repositório contém a implementação do back-end **core** para um SaaS de alertas regulatórios, focado em automatizar a extração de informações regulatórias de órgãos oficiais como ANVISA, Receita Federal, IBAMA, entre outros. O sistema irá monitorar mudanças de regulamentos, realizar análise de texto usando NLP (Processamento de Linguagem Natural) e notificar os usuários de forma automatizada sobre essas mudanças.

## 🚀 Funcionalidades Futuras

### 1. **Crawler de Reguladores**
   - O sistema irá baixar periodicamente arquivos de fontes regulatórias (DOU, Receita Federal, ANVISA, IBAMA, etc).
   - Suporte para diferentes tipos de arquivos, como XML, PDF e HTML.
   - Integração com APIs públicas e privadas de órgãos reguladores.

### 2. **Processamento de Dados (Parsing e Limpeza)**
   - **Limpeza de XML**: Scripts dedicados a limpar e extrair as informações relevantes dos arquivos XML.
   - **Análise de PDF**: Extração de dados estruturados de documentos PDF.
   - **Parse de Dados**: Usaremos a biblioteca `lxml` para parse de XML e outros métodos para dados extraídos de PDFs e HTML.
   - **NLP para Tradução Simples**: Integração com a API da OpenAI para traduzir os textos extraídos para uma linguagem mais acessível, sem jargões, destacando pontos de ação.

### 3. **Notificação e Alerta**
   - **Notificações Personalizadas**: O sistema enviará alertas via e-mail, Slack, SMS, ou até via webhook, dependendo da preferência do usuário.
   - **Dashboard para Usuário**: Usuários poderão visualizar um histórico de alertas e mudanças com filtros específicos (por órgão, tipo de regulamento, etc).
   - **API de Notificação**: Para integração com sistemas externos de monitoramento ou ERPs.

### 4. **Sistema de Usuários**
   - Cadastro e login de usuários com gerenciamento de permissões.
   - Configuração de preferências de alertas (quais órgãos, tipos de mudança, canais de notificação).
   - Histórico de alertas e notificações.
   - **Gestão de Planos**: Suporte para planos Freemium, Basic, Pro e Enterprise, com controle de limite de alertas e funcionalidades.

### 5. **Escalabilidade e Infraestrutura**
   - **Microserviços**: Arquitetura orientada a microserviços, permitindo escalar individualmente cada parte do sistema (crawler, parser, NLP, notificação).
   - **Infraestrutura em Nuvem**: Utilização do AWS Lambda para escalabilidade dos crawlers e integração com S3 para armazenamento dos arquivos.
   - **Banco de Dados**: PostgreSQL para metadados e Elasticsearch para busca avançada de texto.

---

## 🛠 Arquitetura Técnica

### **Back-End**
- **Linguagem**: Java / Python (Dependendo da camada de processamento)
- **Framework**: Spring Boot (Java) / Flask/Django (Python)
- **Banco de Dados**: PostgreSQL (metadados), Elasticsearch (busca full-text)
- **APIs de Integração**: Conectores com APIs de órgãos reguladores (como DOU, Receita Federal, ANVISA)
- **Processamento de Dados**:
  - NLP para simplificação de textos (OpenAI API)
  - Lógica de Parse e limpeza de arquivos com `lxml` e `PyPDF2` (para PDF)

### **Front-End**
- **Tecnologias**: React + TailwindCSS
- **Função**: Dashboard responsivo, exibição de alertas e configurações de preferências de usuário.

### **Infraestrutura**
- **Nuvem**: AWS (Lambda, RDS, S3, Elasticsearch)
- **DevOps**: GitLab CI/CD, Docker para containerização

---

## ⚙️ Como Funciona

### Etapa 1: **Captura de Dados**
   - O sistema fará requisições regulares para baixar documentos dos sites oficiais dos órgãos reguladores.
   - Isso inclui a consulta a APIs (DOU, Receita Federal) ou download direto de arquivos XML e PDF.
   - O sistema usará credenciais de login, se necessário, para acessar essas fontes.

### Etapa 2: **Processamento e Análise**
   - Os arquivos baixados são limpos, estruturados e analisados usando técnicas de NLP para gerar resumos e destacar informações críticas.
   - O sistema extrai os pontos principais como "o que mudou", "quando entra em vigor" e "como se adequar", criando resumos de fácil leitura.

### Etapa 3: **Notificação**
   - Após a análise, o sistema envia notificações aos usuários registrados através dos canais escolhidos (E-mail, Slack, etc).
   - A notificação inclui um resumo com os pontos principais e um link para o documento original.

### Etapa 4: **Dashboard**
   - Os usuários poderão acessar um dashboard para visualizar o histórico de mudanças e alertas recebidos.
   - Filtros de pesquisa serão oferecidos para refinar a visualização de alertas por órgão, data e tipo de documento.

---

## 🧑‍💻 Como Contribuir

1. **Clone o Repositório**:
   - `git clone https://github.com/complyly/BackEnd-Core.git`
   
2. **Configuração Local**:
   - Instale as dependências necessárias:
     - Para Java (Spring Boot): `mvn install`
     - Para Python (Flask/Django): `pip install -r requirements.txt`
   
3. **Criação de Branch**:
   - Crie uma branch para desenvolvimento de novas funcionalidades ou correções.
   - `git checkout -b nome-da-branch`
   
4. **Commit e Push**:
   - Realize alterações e faça commits de forma descritiva.
   - `git add .`
   - `git commit -m "Mensagem explicativa"`
   - `git push origin nome-da-branch`
   
5. **Pull Request**:
   - Abra um pull request no GitHub para que a equipe revise e integre as alterações.

---

## 📦 Dependências

- **Java**: Spring Boot
- **Python**: Flask/Django, lxml, requests, PyPDF2
- **Banco de Dados**: PostgreSQL, Elasticsearch
- **Outras**: Docker, AWS SDK

---

## 🔒 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais informações.

---

## 📝 TODO

- Completar integração com todos os órgãos reguladores (ANVISA, Receita Federal, IBAMA).
- Implementar funções de personalização de alertas e notificação.
- Melhorar a interface do usuário no dashboard.

---

## 🌐 Links Úteis

- [Documentação da API do DOU](https://www.dou.gov.br)
- [Documentação da API Receita Federal](https://www.receita.fazenda.gov.br)
