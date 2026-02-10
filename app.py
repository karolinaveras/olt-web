from flask import Flask, render_template, request, jsonify
import telnetlib
import time
import re

app = Flask(__name__)

class OLTManager:
    def __init__(self):
        self.connection = None
        self.is_connected = False
        self.onu_list = []
    
    def send_command(self, command, wait_time=2):
        """Envia comando e retorna resposta"""
        try:
            print(f"Executando: {command}")
            self.connection.write(command.encode('ascii') + b"\n")
            time.sleep(wait_time)
            response = self.connection.read_very_eager().decode('ascii', errors='ignore')
            return response
        except Exception as e:
            return f"Erro: {str(e)}"
    
    def connect(self, host, port, username, password):
        try:
            print(f"Conectando à OLT {host}:{port}...")
            self.connection = telnetlib.Telnet(host, port, timeout=15)
            time.sleep(2)
            
            # Ler banner inicial
            login_prompt = self.connection.read_until(b"login:", timeout=5)
            print(f"Prompt de login detectado")
            
            # Enviar usuário
            self.connection.write(username.encode('ascii') + b"\n")
            time.sleep(1)
            
            # Aguardar password prompt
            self.connection.read_until(b"Password:", timeout=5)
            
            # Enviar senha
            self.connection.write(password.encode('ascii') + b"\n")
            time.sleep(2)
            
            # Ler resposta do login
            login_response = self.connection.read_very_eager().decode('ascii', errors='ignore')
            print(f"Login realizado")
            
            # Entrar no modo enable
            print("Entrando no modo enable...")
            self.send_command("enable", 1)
            
            # Entrar no modo config
            print("Entrando no modo config...")
            self.send_command("config", 1)
            
            # Entrar na interface gpon 0/0
            print("Entrando na interface gpon 0/0...")
            self.send_command("interface gpon 0/0", 2)
            
            self.is_connected = True
            return True, f"Conectado à OLT {host}"
            
        except Exception as e:
            error_msg = f"Erro de conexão: {str(e)}"
            print(error_msg)
            return False, error_msg
    
    def discover_onus(self):
        """Descobre todas as ONUs usando 'show ont info all'"""
        try:
            if not self.is_connected or not self.connection:
                return False, "Não conectado à OLT"
            
            print("Executando comando: show ont info all")
            
            # Enviar comando
            output = self.send_command("show ont info all", 3)
            print(f"Saída do comando recebida, tamanho: {len(output)} caracteres")
            
            # Parsear resultado
            self.onu_list = self.parse_ont_info(output)
            
            return True, {
                'raw_output': output,
                'onu_count': len(self.onu_list),
                'onu_list': self.onu_list
            }
            
        except Exception as e:
            error_msg = f"Erro na descoberta: {str(e)}"
            print(error_msg)
            return False, error_msg
    
    def parse_ont_info(self, ont_info_text):
        """Parseia o resultado do 'show ont info all' - PARSER SIMPLIFICADO E CORRETO"""
        onus = []
        lines = ont_info_text.split('\n')
        
        print(f"=== INICIANDO PARSER ===")
        print(f"Total de linhas: {len(lines)}")
        
        # Parser simplificado - busca por padrões específicos
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Ignorar linhas irrelevantes
            if not line or line.startswith('-') or "Total:" in line:
                continue
                
            if "F/S" in line or "ONT SN" in line or "Control" in line:
                continue
            
            print(f"Linha {i}: '{line}'")
            
            # Tentar múltiplos padrões regex para capturar dados
            patterns = [
                # Padrão 1: "0/0 1 1 ITBS5B0E707F Active Online success match --"
                r'(\d+/\d+)\s+(\d+)\s+(\d+)\s+([A-Z0-9]{12})\s+(\w+)\s+(\w+)(?:\s+\w+\s+\w+\s+--)?',
                # Padrão 2: "0/0 1 1 ITBS5B0E707F Online" (mais simples)
                r'(\d+/\d+)\s+(\d+)\s+(\d+)\s+([A-Z0-9]{12})\s+(\w+)',
                # Padrão 3: Qualquer coisa com 12 caracteres alfanuméricos (serial)
                r'(\d+/\d+)\s+(\d+)\s+(\d+)\s+([A-Z0-9]{12})',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    try:
                        frame_slot = match.group(1)  # "0/0"
                        pon = match.group(2)        # PON (1, 2, 3...)
                        onu_id = match.group(3)     # ONU ID (1, 2, 3...)
                        serial = match.group(4)     # Serial (ITBS5B0E707F)
                        
                        # Determinar status (Online/Offline)
                        status = "Unknown"
                        if len(match.groups()) >= 6:
                            status = match.group(6) if match.group(6) in ['Online', 'Offline'] else match.group(5)
                        elif len(match.groups()) >= 5:
                            status = match.group(5)
                        
                        # Normalizar status
                        if 'online' in status.lower():
                            status = 'Online'
                        elif 'offline' in status.lower():
                            status = 'Offline'
                        
                        onu_data = {
                            'frame_slot': frame_slot,
                            'pon': pon,
                            'onu_id': onu_id,
                            'serial': serial,
                            'status': status,
                            'description': f"PON {pon}/ONU {onu_id} - {serial} - {status}"
                        }
                        
                        print(f"  ONU parseada: {onu_data}")
                        onus.append(onu_data)
                        break  # Parar após encontrar um padrão válido
                        
                    except Exception as e:
                        print(f"  Erro ao parsear com regex: {e}")
                        continue
        
        # Método alternativo: busca direta por serial numbers (12 caracteres)
        if not onus:
            print("Usando método alternativo de busca por serial...")
            for line in lines:
                line = line.strip()
                # Buscar por padrão de 12 caracteres alfanuméricos (serial)
                serial_match = re.search(r'([A-Z0-9]{12})', line)
                if serial_match:
                    serial = serial_match.group(1)
                    
                    # Tentar extrair PON e ONU ID
                    pon_match = re.search(r'(\d+/\d+)\s+(\d+)\s+(\d+)', line)
                    if pon_match:
                        pon = pon_match.group(2)
                        onu_id = pon_match.group(3)
                    else:
                        # Tentar encontrar números na linha
                        numbers = re.findall(r'\b\d+\b', line)
                        if len(numbers) >= 3:
                            pon = numbers[1] if len(numbers) > 1 else "1"
                            onu_id = numbers[2] if len(numbers) > 2 else "1"
                        else:
                            pon = "1"
                            onu_id = "1"
                    
                    # Determinar status
                    status = "Online" if "online" in line.lower() else "Offline" if "offline" in line.lower() else "Unknown"
                    
                    onu_data = {
                        'frame_slot': '0/0',
                        'pon': pon,
                        'onu_id': onu_id,
                        'serial': serial,
                        'status': status,
                        'description': f"PON {pon}/ONU {onu_id} - {serial} - {status}"
                    }
                    
                    print(f"  ONU parseada (alternativo): {onu_data}")
                    onus.append(onu_data)
        
        # Ordenar por PON e ONU ID
        try:
            onus.sort(key=lambda x: (int(x['pon']), int(x['onu_id'])))
        except:
            pass
        
        print(f"=== PARSER FINALIZADO ===")
        print(f"Total de ONUs encontradas: {len(onus)}")
        
        return onus
    
    def query_specific_ont(self, pon, onu_id, query_type='both'):
        """Consulta uma ONU específica"""
        try:
            if not self.is_connected or not self.connection:
                return False, "Não conectado à OLT"
            
            print(f"Consultando PON {pon} ONU {onu_id}...")
            
            results = {}
            
            if query_type in ['optical', 'both']:
                cmd = f"show ont optical-info {pon} {onu_id}"
                print(f"Executando: {cmd}")
                optical_result = self.send_command(cmd, 3)
                results['optical'] = optical_result
            
            if query_type in ['info', 'both']:
                cmd = f"show ont info {pon} {onu_id}"
                print(f"Executando: {cmd}")
                info_result = self.send_command(cmd, 3)
                results['info'] = info_result
            
            return True, results
            
        except Exception as e:
            error_msg = f"Erro na consulta: {str(e)}"
            print(error_msg)
            return False, error_msg
    
    def disconnect(self):
        if self.connection:
            try:
                self.send_command("quit", 1)
                self.send_command("quit", 1)
                self.send_command("quit", 1)
                time.sleep(1)
                self.connection.close()
            except:
                pass
            self.connection = None
            self.is_connected = False
            self.onu_list = []

# Instanciar o gerenciador OLT
olt_manager = OLTManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connect', methods=['POST'])
def connect():
    try:
        data = request.json
        success, message = olt_manager.connect(
            data['host'],
            int(data['port']),
            data['username'],
            data['password']
        )
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'message': f"Erro: {str(e)}"})

@app.route('/discover-onus', methods=['POST'])
def discover_onus():
    """Descobre todas as ONUs conectadas"""
    try:
        success, result = olt_manager.discover_onus()
        if success:
            return jsonify({
                'success': True,
                'message': f"Encontradas {result['onu_count']} ONUs",
                'onu_count': result['onu_count'],
                'onu_list': result['onu_list']
            })
        else:
            return jsonify({'success': False, 'message': result})
    except Exception as e:
        return jsonify({'success': False, 'message': f"Erro: {str(e)}"})

@app.route('/query-ont', methods=['POST'])
def query_ont():
    """Consulta uma ONU específica"""
    try:
        data = request.json
        success, result = olt_manager.query_specific_ont(
            str(data['pon']),
            str(data['onu_id']),
            data.get('type', 'both')
        )
        return jsonify({'success': success, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'result': f"Erro: {str(e)}"})

@app.route('/get-onu-list', methods=['GET'])
def get_onu_list():
    """Retorna a lista de ONUs já descobertas"""
    return jsonify({
        'success': True,
        'onu_count': len(olt_manager.onu_list),
        'onu_list': olt_manager.onu_list
    })

@app.route('/disconnect', methods=['POST'])
def disconnect():
    olt_manager.disconnect()
    return jsonify({'success': True, 'message': 'Desconectado'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)