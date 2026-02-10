# OLT GPON Manager

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey)
![Telnet](https://img.shields.io/badge/Telnet-Client-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange)

Uma aplicação web para gerenciamento de OLTs GPON via Telnet, com interface intuitiva para descoberta e monitoramento de ONUs.


## 🚀 Recursos Principais

- **🔌 Conexão Telnet**: Conecte-se a OLTs via protocolo Telnet
- **🔍 Descoberta Automática**: Detecte automaticamente todas as ONUs conectadas
- **📊 Dashboard Interativo**: Visualize ONUs em tabela organizada por PON e ONU ID
- **📡 Consultas Específicas**: Obtenha informações ópticas e gerais de ONUs específicas
- **🎨 Interface Moderna**: Design responsivo com feedback visual em tempo real
- **🐛 Modo Debug**: Ferramentas para depuração e análise de dados

## 📋 Requisitos

- Python 3.8 ou superior
- Flask 2.0+
- Acesso a uma OLT GPON via Telnet

## 🛠️ Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/karolinaveras/olt-web.git
cd olt-manager
```

2. **Crie um ambiente virtual (opcional, mas recomendado):**
```bash
python -m venv venv

# No Windows:
venv\Scripts\activate

# No Linux/Mac:
source venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

> **Nota:** Se o arquivo `requirements.txt` não existir, instale manualmente:
> ```bash
> pip install flask
> ```

## 📁 Estrutura do Projeto

```
olt-web/
├── app.py              # Aplicação Flask principal
├── templates/
│   └── index.html     # Interface web
├── requirements.txt    # Dependências Python
├── README.md          # Este arquivo

```

## 🚀 Como Usar

1. **Inicie o servidor:**
```bash
python app.py
```

2. **Acesse a interface:**
   Abra seu navegador e vá para `http://localhost:5000`

3. **Configure a conexão:**
   - IP da OLT (ex: 192.168.100.1)
   - Porta Telnet (geralmente 23)
   - Usuário (geralmente admin)
   - Senha (geralmente admin ou senha configurada)

4. **Operações disponíveis:**
   - **Conectar/Desconectar** da OLT
   - **Descobrir ONUs** (executa `show ont info all`)
   - **Consultar ONU específica** por PON e ONU ID
   - **Obter informações ópticas** (sinal, potência)
   - **Visualizar informações gerais** da ONU

## 🖥️ Interface

### Seção de Conexão
Configure os parâmetros de conexão Telnet com a OLT.

### Tabela de ONUs
Visualize todas as ONUs detectadas com:
- **PON**: Porta GPON (1-16)
- **ONU ID**: Identificador único (1-128)
- **Serial Number**: Número de série de 12 caracteres
- **Status**: Online/Offline com indicadores visuais
- **Ações rápidas**: Consulta direta de informações

### Consulta Específica
Consulte informações detalhadas de uma ONU específica selecionando PON e ONU ID.

### Resultados
Visualize os resultados brutos das consultas Telnet em formato de texto.

## ⚙️ Comandos Suportados

A aplicação executa comandos padrão de OLTs GPON:

| Comando | Descrição |
|---------|-----------|
| `show ont info all` | Lista todas as ONUs conectadas |
| `show ont optical-info <pon> <onu_id>` | Informações ópticas da ONU |
| `show ont info <pon> <onu_id>` | Informações gerais da ONU |

## 🔧 Personalização

### Adicionar novos comandos
Edite o arquivo `app.py` na classe `OLTManager`:

```python
def custom_command(self, pon, onu_id):
    cmd = f"show ont detail {pon} {onu_id}"
    return self.send_command(cmd)
```

### Modificar a interface
Edite `templates/index.html` para:
- Alterar cores e estilos no CSS
- Adicionar novas funcionalidades JavaScript
- Modificar layout e estrutura

## 🐛 Solução de Problemas

### Problema: Conexão Telnet falha
**Solução:**
- Verifique se o IP e porta estão corretos
- Confirme se a OLT aceita conexões Telnet
- Verifique firewall/regras de rede

### Problema: ONUs não são detectadas
**Solução:**
- Verifique os logs do console Python
- Ative o modo debug na interface
- Confirme o comando `show ont info all` funciona na CLI da OLT

### Problema: Parser não identifica dados
**Solução:**
- O formato de saída pode variar entre fabricantes
- Ajuste as expressões regulares em `parse_ont_info()`
- Use o modo debug para ver o output bruto

## 📝 Logs e Depuração

A aplicação possui três níveis de logs:

1. **Console Python**: Mostra comandos executados e respostas
2. **Modo Debug na Interface**: Exibe dados brutos e parseados
3. **Console do Navegador**: Logs JavaScript para interações

Para depurar, clique no botão **"Debug"** na interface.

## 🔒 Segurança

⚠️ **Avisos Importantes:**

1. **Não exponha publicamente** esta aplicação sem autenticação
2. **Use em rede local** ou com VPN
3. **Proteja as credenciais** da OLT
4. **Restrinja acesso** por firewall
5. **Não use credenciais padrão** em produção


## 👩‍💻 Autora

**Karolina Veras**
- GitHub: [@karolinaveras](https://github.com/karolinaveras)
- LinkedIn: [Karolina Veras](https://linkedin.com/in/karolinaveras)

---
**Versão:** 1.0.0  
**Última atualização:** Março 2024  
**Status:** Em desenvolvimento ativo

---

## 🚧 Roadmap Futuro

- [ ] Suporte a múltiplas OLTs simultâneas
- [ ] Exportação de relatórios (CSV, PDF)
- [ ] Gráficos de performance óptica
- [ ] Alertas automáticos por email
- [ ] API REST para integração
- [ ] Suporte a mais fabricantes de OLT
- [ ] Sistema de autenticação de usuários
- [ ] Banco de dados para histórico
- [ ] Backup automático de configurações
- [ ] Interface multi-idioma

### Versão 2.0 Planejada
- [ ] Dashboard com métricas em tempo real
- [ ] Mapa de rede visual
- [ ] Agendamento de tarefas
- [ ] API webhooks
- [ ] App mobile complementar

---

💡 **Dica Profissional:** Mantenha uma cópia local das configurações da sua OLT antes de fazer mudanças via esta ferramenta. Use sempre em ambiente de testes primeiro!

---

## 📚 Documentação Adicional

### Para Desenvolvedores:
- [Documentação da API Flask](https://flask.palletsprojects.com/)
- [Protocolo Telnet RFC 854](https://tools.ietf.org/html/rfc854)
- [GPON Standards ITU-T G.984](https://www.itu.int/rec/T-REC-G.984)

### Para Operadores de Rede:
- [Boas Práticas GPON](https://www.gpon.com)
- [Troubleshooting OLT](https://community.fs.com)
- [Segurança em Redes GPON](https://www.nist.gov)

---

**📊 Estatísticas do Projeto:**
- Linhas de código: ~500
- Tecnologias: Python, Flask, HTML, CSS, JavaScript
- Compatibilidade: OLTs com interface Telnet
- Nível: Intermediário/Avançado

**🎯 Público-Alvo:**
- Operadores de rede GPON
- Técnicos de telecomunicações
- Administradores de rede
- Estudantes de redes

---

**🚀 Próximos Passos:**
1. Teste a aplicação em sua OLT
2. Reporte bugs ou melhorias
3. Contribua com código ou documentação
4. Compartilhe com colegas da área

---

**🔗 Links Úteis:**
- [Repositório no GitHub](https://github.com/karolinaveras/olt-manager)
- [Issues e Bug Tracker](https://github.com/karolinaveras/olt-manager/issues)

---

**📢 Anúncios:**
- Versão 1.0 estável lançada!
- Novas funcionalidades em desenvolvimento
