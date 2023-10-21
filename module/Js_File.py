import os
import json

nome_file = 'Info_ports.json'

class JsonFile:
    def __init__(self,data) -> None:
        self.nameList = 'System'
        self.nome_file = nome_file
        self.data = data
        self.newJs = []

    def ck_port(self):
        response_ckPort = False
        if os.path.exists(self.nome_file):

            with open(self.nome_file,'r') as file_json:
                js_file = json.loads(file_json.read())

            for item in js_file:
                for index in js_file[item]:
                    if index['port'] == self.data.port:
                        response_ckPort = True
            file_json.close()
            
        return response_ckPort

    def upsertFile(self):
        
        if os.path.exists(self.nome_file):

            with open(self.nome_file,'r') as file_oldJs:
                js_file = json.loads(file_oldJs.read())

            for item in js_file:
                for index in js_file[item]:
                    
                    if index['port'] == self.data.port:
                        self.newJs = [ js for js in js_file[item] if js != index ]
                        self.newJs.append(
                            {
                                'port' : self.data.port,
                                'name_file' : self.data.name_file,
                                'host' : self.data.host
                            }
                        )
            
                if not self.newJs: 
                    self.newJs = [ js for js in js_file[item] ]
                    self.newJs.append(
                        {
                            'port' : self.data.port,
                            'name_file' : self.data.name_file,
                            'host' : self.data.host
                        }
                    )

                    
            with open(self.nome_file,'w') as file_newJs:
                json.dump(
                    {'info_ports':self.newJs},
                    file_newJs
                )
                file_newJs.close()

            file_oldJs.close()

        else:
            with open(self.nome_file,'w') as file:
                body = {
                    'info_ports':[
                        {
                            'port' : self.data.port,
                            'name_file' : self.data.name_file,
                            'host' : self.data.host
                        }
                    ]
                }
                json.dump(body,file)
                file.close()

    def deletePort(self):
        
        if os.path.exists(self.nome_file):

            with open(self.nome_file,'r') as file_oldJs:
                js_file = json.loads(file_oldJs.read())

            for item in js_file:
                for index in js_file[item]:
                    
                    if index['port'] == self.data.port:
                        self.newJs = [ js for js in js_file[item] if js != index ]
            
            if not self.newJs:
                os.remove(self.nome_file)
            else:
                with open(self.nome_file,'w') as file_newJs:
                    json.dump(
                        {'info_ports':self.newJs},
                        file_newJs
                    )
                    file_newJs.close()

            file_oldJs.close()
        
def list_view_port():
    if os.path.exists(nome_file):
        with open(nome_file,'r') as file_json:
            js_file = json.loads(file_json.read())
        for item in js_file:
            print('\n*********************************************************************\n')
            print('+++++++++++++++++++++++++ [ LIST VIEW PORT ] ++++++++++++++++++++++++\n')
            print('*********************************************************************\n')
            print('\n\n---------------------------------------------------------------------\n')
            for index in js_file[item]:
                for k,v in index.items():
                    print(f'\n{k}:{v}')
                print('\n\n---------------------------------------------------------------------\n')
        list_ports = js_file
        file_json.close()
        return list_ports
    else: return None
        