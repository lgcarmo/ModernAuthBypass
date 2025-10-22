# ModernAuthBypass

**Teste controlado para identificar exposição de protocolos legados (POP3/IMAP/SMTP) em ambientes Microsoft 365.**

> Aviso rápido: este projeto é uma ferramenta de auditoria **para uso em ambientes autorizados apenas**. Não utilize sem permissão explícita do proprietário do tenant/ambiente. Consultar políticas internas e leis vigentes.

---

## Descrição
Este repositório contém um script em Python para verificar se servidores Office 365 (ou servidores compatíveis) aceitam autenticações via protocolos legados e, opcionalmente, realizar testes de força bruta controlados. O objetivo é ajudar equipes de segurança a identificar pontos cegos onde *Modern Authentication* pode ser contornado via clientes antigos ou protocolos legados.

Script principal: `ModerAuthBypass_V2.py`. :contentReference[oaicite:1]{index=1}

---

## Aviso legal / Ética
- **Somente** realize testes em ambientes que você tem autorização explícita por escrito.
- O autor não se responsabiliza por uso indevido.
- Recomenda-se executar testes em janela controlada, com alertas para o time de TI / SOC.

---

## Funcionalidades
- `check`: testa uma combinação email + senha via POP3 (ou servidor configurado).
- `brute`: gera combinações a partir de um vetor (ex.: `key1:key2`) e tenta autenticar (uso controlado).
- `wordlist`: testa senhas a partir de um arquivo wordlist.
- `config`: cria um arquivo de configuração (`conf/config.json`) com host/porta.
- `passFile`: processa um arquivo com linhas no formato `user@domain.com:password`.

---

## Pré-requisitos
- Python 3.8+
- Dependências padrão (nenhuma lib externa necessária além das stdlib usadas no script).
- Acesso à rede com permissão para conectar na porta POP3/SSL do servidor alvo.

---

## Instalação rápida
1. Clone o repositório:
```bash
git clone https://github.com/<seu-usuario>/ModernAuthBypass.git
cd ModernAuthBypass
python3 -m venv venv
source venv/bin/activate
mkdir -p conf
cp config.example.json conf/config.json
# editar conf/config.json com SMTP/POP3 e porta corretos
```

## Exemplo de conf/config.json

Veja o arquivo config.json.
Formato:

```json 
{
  "smtp_url": "outlook.office365.com",
  "smtp_port": 995
}
```

```python
python ModerAuthBypass_V2.py --module check -e usuario@dominio.com -p "SenhaTeste123"

python ModerAuthBypass_V2.py --module brute -e usuario@dominio.com -m 0 -M 3 -w key1:key2:key3

python ModerAuthBypass_V2.py --module wordlist -e usuario@dominio.com -f wordlist.txt

python ModerAuthBypass_V2.py --module config
# Preencha SMTP/POP3 e porta quando solicitado
```

## Boas práticas ao executar

* Execute em janela de manutenção ou com autorização.
* Limite a taxa de tentativas para evitar bloqueios e false-positives.
* Monitore logs (Sign-in logs / SIEM).
* Notifique o time de operações/segurança antes do teste.


