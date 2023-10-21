import datetime
import re
import subprocess
import platform
import threading
import module.Logo
import module.Js_File
import module.Honeypot

class Channel:
    def __init__(self) -> None:
        self.name_file = ''
        self.host = ''
        self.port = None
        self.ck = False
        
    def print(self):
        print(
            f'>> self.name_file:   {self.name_file}\n'\
            f'>> self.host:    {self.host}\n'\
            f'>> self.port:    {self.port}\n'\
        )

    def resetValue(self,port):
        self.name_file = ''
        self.host = ''
        self.port = port
        self.ck = False

    def upsertPort(self):
        while True:
            no_chart = r'[\\/:*?"\'<>|]'
            if not self.name_file.strip():
                name_file = input('>> [*] Inserisci il nome del file: \n')
                if name_file.strip() and (not re.search(no_chart,name_file)):
                    self.name_file = name_file
                elif re.search(no_chart,name_file):
                    print('\n>> IL VALORE INSERITO NON DEVE CONTENERE I SEGUENTI CARRATTI [\\/:*?"\'<>|]\n')
                else: print('\n>> IL VALORE INSERITO È VUOTO O CONTIENE SOLO SPAZI!!!\n')
            else:
                if not self.host.strip():
                    host = input('\n>> Inserisci Host: \n')
                    if re.match(r'^\d+\.\d+\.\d+\.\d+$',host):
                        self.host = host
                    elif not host.strip():
                        self.host = '0.0.0.0'
                    elif not re.match(r'^\d+\.\d+\.\d+\.\d+$',host):
                        print('\n>> IL VALORE INSERITO NON È CORRETTO (EX. 0.0.0.0)\n')
                else:   
                    if not self.port is not None:
                        port = input('\n>> [*] Inserire la porta sulla quale mettersi in ascolto: \n')
                        if port.strip():
                            if not port.isdigit():
                                print(f'\n>> IL VALORE INSERITO [ {port} ] NON È INTERO!!\n')
                            else:
                                self.port = int(port)
                                self.ck = True
                        else: print('\n>> IL VALORE INSERITO È VUOTO O CONTIENE SOLO SPAZI!!!\n')
                    else: self.ck = True
            if self.ck:
                self.name_file = f'[{datetime.datetime.now().strftime('%Y-%m-%d')}]-[{self.name_file}]-[port({self.port})]'
                jsn = module.Js_File.JsonFile(self)
                ck_json = jsn.ck_port()
                print('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
                if ck_json:
                    print('\n>> Sicuro di voler sovrascrivere la configurazione della porta [{self.port}]? \n')
                    print('\n>> <<WARNIG>> se sceglierai [ no | n ] perderai tutte le modifiche!!! \n')
                    print('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
                    ck_js = input(f'\n>> [ yes | y | no | n ] ? \n').lower()
                    while True:
                        if ck_js not in ( 'yes','y','no','n'):
                            print('\nIL VALORE INSERITO NON È CORRETTO!!!\n')
                        elif ck_js in ( 'yes','y' ):
                            jsn.upsertFile()
                            break
                        else: 
                            break
                else:
                    jsn.upsertFile()

                self.resetValue(None)
                break
    
    def deletePort(self):
        jsn = module.Js_File.JsonFile(self)
        ck_json = jsn.ck_port()
        if ck_json:
            print('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
            print('\n>> Sicuro di voler eliminare la configurazione della porta [{self.port}]? \n')
            print('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
            ck_js = input(f'\n>> [ yes | y | no | n ] ? \n').lower()
            while True:
                if ck_js not in ( 'yes','y','no','n'):
                    print('\nIL VALORE INSERITO NON È CORRETTO!!!\n')
                elif ck_js in ( 'yes','y' ):
                    jsn.deletePort()
                    print(f'\n>> La configurazione della porta [ {self.port} ] è stata eliminata con successo!!\n')
                    break
                else: 
                    break
        self.resetValue(None)

module.Logo.IconLogo.copyright()
module.Logo.IconLogo.logo()

ck_exit = False
def startComand():
    try:
        if not ck_exit:
            operation = input(
                '\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'\
                '\nCosa vuoi fare? ( Usa il comando help per visualizzare le opzioni )\n'\
                '\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n'\
                '>> '\
            ).lower()
            match operation:
                case 'help':
                    print('\n________________________________________________________________________________________\n')
                    print(
                        'ELENCO COMANDI E ISTRUZIONI'\
                        '\n________________________________________________________________________________________\n'\
                        '\n>> lw:\n'\
                        '\n\t-> [ list view ] mostra la lista delle porte configuarate\n'\
                        '\n>> lwp:\n'\
                        '\n\t-> [ list view port ] mostra la lista delle principali porte TCP/UDP\n'\
                        '\n>> cls [windows] | clear [linux|macOS]:\n'\
                        '\n\t-> pulisce lo schermo della console\n'\
                        '\n>> insert:\n'\
                        '\n\t-> [name_file] inserire il nome del file per salvare i log([*]campo obbligatorio)'\
                        '\n\t-> [host] inserire l\'host di nostro interesse o sarà preso quello di default '\
                        '\n\t-> [port] inserire la porta sulla quale mettersi in ascolto([*]campo obbligatorio)'\
                        '\n>> update:\n'\
                        '\n\t-> [name_file] modificabile'\
                        '\n\t-> [host] modificabile '\
                        '\n\t-> [port] non modificabile'\
                        '\n>> delete:\n'\
                        '\n\t-> elimina la configurazione della porta indicata'\
                        '\n\t   ( assicurarsi prima che non sia attivo l\'ascolto su di essa!!\n'\
                        '\n>> start:\n'\
                        '\n\t   avvia l\'ascolto sulla porta selezionata!!\n'\
                        '\n>> stop:\n'\
                        '\n\t   termina l\'ascolto sulla porta\n'\
                        '\n>> exit:\n'
                        '\n\t-> chiuderà il programma'\
                        '\n\t   ( assicurarsi prima che non ci siano porte aperte con l\'ascolto attivo!!\n'\
                    )
                    print('\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n')
                case 'lw':
                    listVw_infoPorts = module.Js_File.list_view_port()
                    if not listVw_infoPorts:
                        print(f'\n>> Non sono presenti configurazioni!! usare il comando [ insert ]!!!\n')
                case 'lwp':
                    print(
                        '\n\n_____________________________________________________________________________________________________________\n'\
                        '| port number | Transport Protocol | Service Name                                | RFC                      |\n'\
                        '+-----------------------------------------------------------------------------------------------------------+\n'\
                        '| 20, 21      | TCP                | File Transfer Protocol (FTP)                | RFC 959                  |\n'\
                        '+-----------------------------------------------------------------------------------------------------------+\n'\
                        '| 22          | TCP and UDP        | Secure Shell (SSH)                          | RFC 4250-4256            |\n'\
                        '+-----------------------------------------------------------------------------------------------------------+\n'\
                        '| 23          | TCP                | Telnet                                      | RFC 854                  |\n'\
                        '+-----------------------------------------------------------------------------------------------------------+\n'\
                        '| 25          | TCP                | Simple Mail Transfer Protocol (SMTP)        | RFC 5321                 |\n'\
                        '+-----------------------------------------------------------------------------------------------------------+\n'\
                        '| 53          | TCP and UDP        | Domain Name Server (DNS)                    | RFC 1034-1035            |\n'\
                        '+-----------------------------------------------------------------------------------------------------------+\n'\
                        '| 67, 68      | UDP                | Dynamic Host Configuration Protocol (DHCP)  | RFC 2131                 |\n'\
                        '+-----------------------------------------------------------------------------------------------------------+\n'\
                        '| 69          | UDP                | Trivial File Transfer Protocol (TFTP)       | RFC 1350                 |\n'\
                        '+-----------------------------------------------------------------------------------------------------------+\n'\
                        '| 80          | TCP                | HyperText Transfer Protocol (HTTP)          | RFC 2616                 |\n'\
                        '+-----------------------------------------------------------------------------------------------------------+\n'\
                        '| 110         | TCP                | Post Office Protocol (POP3)                 | RFC 1939                 |\n'\
                        '+-----------------------------------------------------------------------------------------------------------+\n'\
                        '| 119         | TCP                | Network News Transport Protocol (NNTP)      | RFC 8977                 |\n'\
                        '+-----------------------------------------------------------------------------------------------------------+\n'\
                        '| 123         | UDP                | Network Time Protocol (NTP)                 | RFC 5905                 |\n'\
                        '+-----------------------------------------------------------------------------------------------------------+\n'\
                        '| 135-139     | TCP and UDP        | NetBIOS                                     | RFC 1001-1002            |\n'\
                        '+-----------------------------------------------------------------------------------------------------------+\n'\
                        '| 143         | TCP and UDP        | Internet Message Access Protocol (IMAP4)    | RFC 3501                 |\n'\
                        '+-----------------------------------------------------------------------------------------------------------+\n'\
                        '| 161, 162    | TCP and UDP        | Simple Network Management Protocol (SNMP)   | RFC 1901-1908, 3411-3418 |\n'\
                        '+-----------------------------------------------------------------------------------------------------------+\n'\
                        '| 179         | TCP                | Border Gateway Protocol (BGP)               | RFC 4271                 |\n'\
                        '+-----------------------------------------------------------------------------------------------------------+\n'\
                        '| 389         | TCP and UDP        | Lightweight Directory Access Protocol       | RFC 4510                 |\n'\
                        '+-----------------------------------------------------------------------------------------------------------+\n'\
                        '| 443         | TCP and UDP        | HTTP with Secure Sockets Layer (SSL)        | RFC 2818                 |\n'\
                        '+-----------------------------------------------------------------------------------------------------------+\n'\
                        '|             |                    | Internet Security Association and Key       |                          |\n'\
                        '| 500         | UDP                | Management Protocol (ISAKMP) / Internet Key | RFC 2408 - 2409          |\n'\
                        '|             |                    | Exchange (IKE) RFC 2408 - 2409              |                          |\n'\
                        '+-----------------------------------------------------------------------------------------------------------+\n'\
                        '| 636         | TCP and UDP        | Lightweight Directory Access Protocol       | RFC 4513                 |\n'\
                        '|             |                    | over TLS/SSL(LDAPS)                         | RFC 4513                 |\n'\
                        '+-----------------------------------------------------------------------------------------------------------+\n'\
                        '| 989/990     | TCP                | FTP over TLS/SSL                            | RFC 4217                 |\n'\
                        '+-----------------------------------------------------------------------------------------------------------+\n\n')
                case 'cls' | 'clear':
                    #Verifico il sistema operativo
                    os = platform.system()
                    if os == 'Windows':
                        subprocess.call('cls',shell=True)
                    else:
                        subprocess.call('clear',shell=True)
                case 'insert':
                    channel = Channel()
                    channel.upsertPort()
                case 'update':
                    
                    listVw_infoPorts = module.Js_File.list_view_port()
                    if not listVw_infoPorts:
                        print(f'\n>> Non sono presenti configurazioni!! usare il comando [ insert ]!!!\n')
                    else:
                        channel = Channel()
                        while True:
                            updt_js_step_1 = input('\n>> Quale porta vuoi modificare? ( usa la lettera [ c ] per tornare indietro) \n')
                            
                            if updt_js_step_1.strip():
                                if updt_js_step_1.lower() == 'c':
                                    break
                                if not updt_js_step_1.isdigit():
                                    print(f'\n>> IL VALORE INSERITO [ {updt_js_step_1} ] NON È INTERO O IL COMANDO È ERRATO!!\n')
                                else:
                                    for item in listVw_infoPorts:
                                        for index in listVw_infoPorts[item]:
                                            if index['port'] == int(updt_js_step_1):
                                                channel.port = index['port']
                                                channel.name_file = index['name_file']
                                                channel.host = index['host']
                                                
                                    if channel.port:
                                        channel.resetValue(channel.port)
                                        print(channel.port)
                                        channel.upsertPort()
                                        break
                                    else:
                                        print(f'\n>> La porta indicata [ {updt_js_step_1} ] non è presente nella lista!!!')
                            else: print('\n>> IL VALORE INSERITO È VUOTO O CONTIENE SOLO SPAZI!!!\n')
                case 'delete':
                    listVw_infoPorts = module.Js_File.list_view_port()
                    if not listVw_infoPorts:
                        print(f'\n>> Non sono presenti configurazioni!! usare il comando [ insert ]!!!\n')
                    else:
                        channel = Channel()
                        while True:
                            delete_js_step_1 = input(
                                '\n>> Quale configurazione vuoi eliminare? ( usa la lettera [ c ] per tornare indietro) \n'\
                                '>> Indica la porta (ex. 24)\n'
                            )
                            
                            if delete_js_step_1.strip():
                                if delete_js_step_1.lower() == 'c':
                                    break
                                if not delete_js_step_1.isdigit():
                                    print(f'\n>> IL VALORE INSERITO [ {delete_js_step_1} ] NON È INTERO O IL COMANDO È ERRATO!!\n')
                                else:
                                    for item in listVw_infoPorts:
                                        for index in listVw_infoPorts[item]:
                                            if index['port'] == int(delete_js_step_1):
                                                channel.port = index['port']
                                    if channel.port:
                                        channel.resetValue(channel.port)
                                        channel.deletePort()
                                        break
                                    else:
                                        print(f'\n>> La porta indicata [ {delete_js_step_1} ] non è presente nella lista!!!')
                            else: print('\n>> IL VALORE INSERITO È VUOTO O CONTIENE SOLO SPAZI!!!\n')
                case 'start':
                    listVw_infoPorts = module.Js_File.list_view_port()
                    if not listVw_infoPorts:
                        print(f'\n>> Non sono presenti configurazioni!! usare il comando [ insert ]!!!\n')
                    else:
                        channel = Channel()
                        while True:
                            listeningPort_js_step_1 = input(
                                '\n>> Su quale porta vuoi metterti in ascolto? ( usa la lettera [ c ] per tornare indietro) \n'\
                                '>> Indica la porta (ex. 24)\n'
                            )
                            
                            if listeningPort_js_step_1.strip():
                                if listeningPort_js_step_1.lower() == 'c':
                                    break
                                if not listeningPort_js_step_1.isdigit():
                                    print(f'\n>> IL VALORE INSERITO [ {listeningPort_js_step_1} ] NON È INTERO O IL COMANDO È ERRATO!!\n')
                                else:
                                    for item in listVw_infoPorts:
                                        for index in listVw_infoPorts[item]:
                                            if index['port'] == int(listeningPort_js_step_1):
                                                channel.port = index['port']
                                                channel.host = index['host']
                                                channel.name_file = index['name_file']
                                    if channel.port:

                                        honeypot = module.Honeypot.HoneypotServer(
                                            channel.host,
                                            channel.port,
                                            f'{channel.name_file}.txt'
                                        )

                                        channel.resetValue(None)

                                        honeypot_thread = threading.Thread(target=honeypot.start) 
                                        honeypot_thread.start()

                                        while True:
                                            cmd = input('>> Usa il comando [ stop ] per terminare l\'ascolto\n').lower()
                                            if not cmd.strip():
                                                print('\n>> IL VALORE INSERITO È VUOTO O CONTIENE SOLO SPAZI!!!\n')                              
                                            elif cmd == 'stop':
                                                honeypot.stop()
                                                honeypot_thread.join()
                                                break
                                            else:
                                                print(f'\n>> IL VALORE INSERITO [ {cmd} ] È ERRATO!!\n')
                                                
                                        break
                                    else:
                                        print(f'\n>> La porta indicata [ {listeningPort_js_step_1} ] non è presente nella lista!!!')
                            else: print('\n>> IL VALORE INSERITO È VUOTO O CONTIENE SOLO SPAZI!!!\n')
                                        
                case 'exit':
                    action = input('\n>> Confermi di voler uscire dal programma?\n')
                    if action.lower() in ('yes','y'):
                        return True
                    elif action.lower() not in ('yes','y'):
                        print('\n>> Inserire un valore corretto [yes|y]\n')
                case _:
                    print('\n>> Il comando inserito non è corretto o non presente '\
                        'usa [help] per maggiori informazioni\n')
        else: 
            print('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
            module.Logo.IconLogo.good_bye()
            print('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
    except KeyboardInterrupt:
        action = input('\n>> Confermi di voler uscire dal programma?\n')
        if action.lower() in ('yes','y'):
            return True
        elif action.lower() not in ('yes','y'):
            print('\n>> Inserire un valore corretto [yes|y]\n')
try:
    while not ck_exit:
        if startComand():
            ck_exit = True
            break
except KeyboardInterrupt:
    action = input('\n>> Confermi di voler uscire dal programma?\n')
    if action.lower() in ('yes','y'):
        ck_exit = True
    elif action.lower() not in ('yes','y'):
        print('\n>> Inserire un valore corretto [yes|y]\n')
