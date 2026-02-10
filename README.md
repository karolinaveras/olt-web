# OLT Web Manager - Cianet

Ferramenta web para gerenciar OLTs GPON da Cianet via Telnet.

## Funcionalidades
- Conexão Telnet com OLTs Cianet
- Descoberta automática de ONUs
- Consulta de informações por ONU específica
- Interface simples em HTML/JavaScript
- Containerização com Docker

## Requisitos
- Python 3.8+ **ou** Docker

## Instalação com Docker (Recomendado)

### Opção 1: Docker Compose
```bash
git clone https://github.com/karolinaveras/olt-web.git
cd olt-web
docker-compose up
```

### Opção 2: Docker direto
```bash
docker build -t olt-web .
docker run -p 5000:5000 olt-web
```

## Instalação tradicional
```bash
git clone https://github.com/karolinaveras/olt-web.git
cd olt-web
pip install Flask==2.1.0
python app.py
```

## Uso
1. Acesse `http://localhost:5000`
2. Configure conexão com sua OLT Cianet
3. Use os botões para conectar, descobrir ONUs e fazer consultas

## Comandos Cianet suportados
- `show ont info all`
- `show ont optical-info gpon <pon> <onu_id>`
- `show ont info gpon <pon> <onu_id>`

## Estrutura do projeto
```
app.py              # Lógica principal
templates/index.html # Interface
Dockerfile          # Configuração do container
docker-compose.yml  # Orquestração Docker
requirements.txt    # Dependências Python
```

## Configuração Docker
- Porta padrão: 5000
- Modo desenvolvimento: código montado em volume
- Build otimizado com cache de dependências

## Segurança
- Use em rede local
- Não exponha na internet
- Proteja credenciais da OLT

## Autor
Karolina Veras - Para uso com OLTs Cianet GPON