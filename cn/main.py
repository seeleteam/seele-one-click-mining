# -*- coding: utf-8 -*-
import PySimpleGUI as sg  
import subprocess
import datetime
import json
import requests

now = datetime.datetime.now()
now_fmt= now.strftime("%Y-%m-%d %H:%M")

def ExecuteCommandSubprocess(soutput, command, *args):   
    try:      
        sp = subprocess.Popen([command, *args], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)      
        out, err = sp.communicate()      
        if out:  
            if soutput=='s1':
                window.FindElement('_s1_out_').Update(now_fmt + "\n\n" + checkEncoding(out))
            if soutput=='s2':
                window.FindElement('_s2_out_').Update(now_fmt + "\n\n" + checkEncoding(out))
            if soutput=='s3':
                window.FindElement('_s3_out_').Update(now_fmt + "\n\n" + checkEncoding(out))
            if soutput=='s4':
                window.FindElement('_s4_out_').Update(now_fmt + "\n\n" +checkEncoding(out))
        if err:      
            if soutput=='s1':
                window.FindElement('_s1_out_').Update(now_fmt + '\n\n' + checkEncoding(err)) 
            if soutput=='s2':
                window.FindElement('_s2_out_').Update(now_fmt + '\n\n' + checkEncoding(err))
            if soutput=='s3':
                window.FindElement('_s3_out_').Update(now_fmt + '\n\n' + checkEncoding(err))
            if soutput=='s4':
                window.FindElement('_s4_out_').Update(now_fmt + '\n\n' + checkEncoding(err))      
    except OSError as e:      
            sg.Print("ExecuteCommandSubprocess Error:" + str(e)) 

def checkEncoding(out):
    try:
        return str(out.decode("UTF-8"))    
    except:
        return str(out.decode("gbk"))
    else:
        sg.Print("Output decoding error!")

def GetRemoteBlock(shard):
    if shard == 's1':
        url = "https://api.seelescan.net/api/v1/blocks?p=1&ps=1&s=1"
    if shard == 's2':
        url = "https://api.seelescan.net/api/v1/blocks?p=1&ps=1&s=2"
    if shard == 's3':
        url = "https://api.seelescan.net/api/v1/blocks?p=1&ps=1&s=3"
    if shard == 's4':
        url = "https://api.seelescan.net/api/v1/blocks?p=1&ps=1&s=4"
    try:
        r = requests.get(url)
        return r.text
    except requests.ConnectionError as e:
        sg.Print(str(e))            
    except requests.Timeout as e:
        sg.Print(str(e))
    except requests.RequestException as e:
        sg.Print(str(e))

def UpdateConfigFile(shard, coinbase, mode):
    if shard == '1':
       fname = "node1"
    if shard == '2':
       fname = "node2"
    if shard == '3':
       fname = "node3"
    if shard == '4':
       fname = "node4"
    
    pkey=GetPrivateKey(shard)
    privatekey_str='"privateKey": "'+ pkey +'",'
    coinbase_str ='"coinbase": "'+ coinbase +'",'
    src_file = "config/" + fname + ".json.tmp"
    des_file = "config/" + fname + ".json"
    key_file = "keys/" + "shard" + shard + ".txt"

    if mode == 'new':
       with open(key_file, 'a+') as file :
           file.write(coinbase + "\n")

    with open(src_file, 'r') as file :
        filedata = file.read()
        filedata = filedata.replace('_coinbase_', coinbase_str)
        filedata = filedata.replace('_privateKey_', privatekey_str)

    with open(des_file, 'w') as file:
        file.write(filedata)

def KeyGen(shard):
    try:  
        command = ["client", "key", "--shard", shard]
        sp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)      
        out, err = sp.communicate()    
        if out:
            coinbase=out.decode('utf-8').split('private key: ')[0].rstrip().strip('public key:').strip()
            UpdateConfigFile(shard, coinbase, "new")
            return "Shard" + shard + "\n" + out.decode('utf-8')
        if err:
            sg.Print(err.decode('utf-8'))
    except OSError as e:
        sg.Print("KeyGen Error:" + str(e))

def GetPrivateKey(shard):
    try:
        command = ["client", "key", "--shard", shard]
        sp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)      
        out, err = sp.communicate()    
        if out:
            privatekey=out.decode('utf-8').split('private key: ')[1].rstrip()
            return privatekey
        if err:
            sg.Print("GetPrivateKey Error: " + err.decode('utf-8'))
    except OSError as e:
        sg.Print("GetPrivateKey Error:" + str(e))

def GetKeyList(shard):
    key_file='./keys/' + shard + '.txt'
    try:
        with open(key_file) as f:
            lineList = f.readlines()
            return lineList
    except IOError as e:
        sg.Print("GetKeyList Error: " + str(e))

#ui string values
account_safe_str="请务必妥善保管以下公密钥信息！"
existing_shard1_key_str = "输入现有分片1公钥"
existing_shard1_key_list_str = "选择现有分片1公钥"
existing_shard2_key_str = "输入现有分片2公钥"
existing_shard2_key_list_str = "选择现有分片2公钥"
existing_shard3_key_str = "输入现有分片3公钥"
existing_shard3_key_list_str = "选择现有分片3公钥"
existing_shard4_key_str = "输入现有分片4公钥"
existing_shard4_key_list_str = "选择现有分片4公钥"
update_shard1_config_with_str= "更新分片1配置coin base值至 "
update_shard2_config_with_str= "更新分片2配置coin base值至 "
update_shard3_config_with_str= "更新分片3配置coin base值至 "
update_shard4_config_with_str= "更新分片4配置coin base值至 "
update_shard1_coinbase_with_str="更新分片1配置coin base值至 "
update_shard2_coinbase_with_str="更新分片2配置coin base值至 "
update_shard3_coinbase_with_str="更新分片3配置coin base值至 "
update_shard4_coinbase_with_str="更新分片4配置coin base值至 "
no_shard_1_public_key_selected_str="未选择分片1公钥！"
no_shard_2_public_key_selected_str="未选择分片2公钥！"
no_shard_3_public_key_selected_str="未选择分片3公钥！"
no_shard_4_public_key_selected_str="未选择分片4公钥！"
key_field_empty_str="字段是空的！"
update_config_btn="更新配置"
start_btn="启动"
stop_btn="停止"
status_btn="状态"
log_btn="日志"
local_btn="本机区块高度"
network_btn="主网区块高度"
config_btn="查看配置"
generate_key_pairs_btn="生成密钥对"
shard1_key_gen_win_title_str=" 分片1密钥对生成"
shard2_key_gen_win_title_str=" 分片2密钥对生成"
shard3_key_gen_win_title_str=" 分片3密钥对生成"
shard4_key_gen_win_title_str=" 分片4密钥对生成"
shard1_existing_key_win_title_str=" 分片1现有公钥"
shard2_existing_key_win_title_str=" 分片2现有公钥"
shard3_existing_key_win_title_str=" 分片3现有公钥"
shard4_existing_key_win_title_str=" 分片4现有公钥"
shard1_key_window_active = False
shard2_key_window_active = False
shard3_key_window_active = False
shard4_key_window_active = False
shard1_key_exist_window_active = False
shard2_key_exist_window_active = False
shard3_key_exist_window_active = False
shard4_key_exist_window_active = False
help_window_active = False
about_window_active = False

menu_def = [['&文件', ['E&xit']],
           ['密钥', ['分片 1',['新建::_key_s1_','现有::_key_s1_',], '分片 2',['新建::_key_s2_','现有::_key_s2_',], '分片 3',['新建::_key_s3_','现有::_key_s3_',], '分片 4',['新建::_key_s4_','现有::_key_s4_',]]],
           ['帮助', ['帮助::_help_mining_', '关于::_help_about_']],
           ]

shard_1_layout = [
                   [sg.Output(size=(88, 12), key='_s1_out_')],
                   [sg.Button(start_btn, key='_start_s1_'), sg.Button(stop_btn, key='_stop_s1_'),  sg.Button(status_btn, key='_status_s1_'), sg.Button(log_btn, key='_log_s1_'), sg.Button(local_btn, key='_local_s1_'), sg.Button(network_btn, key='_network_s1_'),sg.Button(config_btn, key='_config_s1_')],
                 ]

shard_2_layout = [
                   [sg.Output(size=(88, 12), key='_s2_out_')],
                   [sg.Button(start_btn, key='_start_s2_'), sg.Button(stop_btn, key='_stop_s2_'), sg.Button(status_btn, key='_status_s2_'), sg.Button(log_btn, key='_log_s2_'), sg.Button(local_btn, key='_local_s2_'), sg.Button(network_btn, key='_network_s2_'),sg.Button(config_btn, key='_config_s2_')],
                 ]

shard_3_layout = [
                   [sg.Output(size=(88, 12), key='_s3_out_')],
                   [sg.Button(start_btn, key='_start_s3_'), sg.Button(stop_btn, key='_stop_s3_'), sg.Button(status_btn, key='_status_s3_'), sg.Button(log_btn, key='_log_s3_'), sg.Button(local_btn, key='_local_s3_'), sg.Button(network_btn, key='_network_s3_'),sg.Button(config_btn, key='_config_s3_')],
                 ]

shard_4_layout = [
                   [sg.Output(size=(88, 12), key='_s4_out_')],
                   [sg.Button(start_btn, key='_start_s4_'), sg.Button(stop_btn, key='_stop_s4_'), sg.Button(status_btn, key='_status_s4_'), sg.Button(log_btn, key='_log_s4_'), sg.Button(local_btn, key='_local_s4_'), sg.Button(network_btn, key='_network_s4_'),sg.Button(config_btn, key='_config_s4_')],
                 ]

layout = [
            [sg.Menu(menu_def, )],
            [sg.TabGroup([[sg.Tab('分片 1', shard_1_layout, key='_shard1_'), sg.Tab('分片 2', shard_2_layout, key='_shard2_'),sg.Tab('分片 3', shard_3_layout, key='_shard3_'),sg.Tab('分片 4', shard_4_layout, key='_shard4_')]])],
            [sg.T('')]        
         ]

window = sg.Window(' Seele一键挖矿', layout, icon='icon/seele.ico', resizable=True,  font=("Arial", 10), element_padding=((5,5),(5,5))).Finalize() 

while True:
    (event, value) = window.Read()
    if event == 'Exit' or event is None:      
        break         
    #shard 1 events
    if event == '_local_s1_':      
        ExecuteCommandSubprocess('s1','client.exe','getblockheight', '-a', '127.0.0.1:8027')  
    if event == '_stop_s1_':      
        ExecuteCommandSubprocess('s1', 'sc','stop', 'seele_shard_1')
    if event == '_start_s1_':      
        ExecuteCommandSubprocess('s1', 'sc','start', 'seele_shard_1')
    if event == '_status_s1_':      
        ExecuteCommandSubprocess('s1', 'sc','query', 'seele_shard_1')
    if event == '_log_s1_':      
        ExecuteCommandSubprocess('s1', 'type','shard1.out.log', )
    if event == '_network_s1_':
        remote_block=GetRemoteBlock('s1')
        window.FindElement('_s1_out_').Update(now_fmt + "\n\n" + remote_block)
    if event == '_config_s1_':
        ExecuteCommandSubprocess('s1', 'type', 'config\\node1.json')
    #shard 2 events
    if event == '_local_s2_':      
        ExecuteCommandSubprocess('s2','client.exe','getblockheight', '-a', '127.0.0.1:8028')  
    if event == '_stop_s2_':      
        ExecuteCommandSubprocess('s2', 'sc','stop', 'seele_shard_2')
    if event == '_start_s2_':      
        ExecuteCommandSubprocess('s2', 'sc','start', 'seele_shard_2')
    if event == '_status_s2_':      
        ExecuteCommandSubprocess('s2', 'sc','query', 'seele_shard_2')
    if event == '_log_s2_':      
        ExecuteCommandSubprocess('s2', 'type','shard2.out.log', )
    if event == '_network_s2_':
        remote_block=GetRemoteBlock('s2')
        window.FindElement('_s2_out_').Update(now_fmt + "\n\n" + remote_block)
    if event == '_config_s2_':
        ExecuteCommandSubprocess('s2', 'type', 'config\\node2.json')
    #shard 3 events
    if event == '_local_s3_':      
        ExecuteCommandSubprocess('s3','client.exe','getblockheight', '-a', '127.0.0.1:8029')  
    if event == '_stop_s3_':      
        ExecuteCommandSubprocess('s3', 'sc','stop', 'seele_shard_3')
    if event == '_start_s3_':      
        ExecuteCommandSubprocess('s3', 'sc','start', 'seele_shard_3')
    if event == '_status_s3_':      
        ExecuteCommandSubprocess('s3', 'sc','query', 'seele_shard_3')
    if event == '_log_s3_':      
        ExecuteCommandSubprocess('s3', 'type','shard3.out.log', )
    if event == '_network_s3_':
        remote_block=GetRemoteBlock('s3')
        window.FindElement('_s3_out_').Update(now_fmt + "\n\n" + remote_block)
    if event == '_config_s3_':
        ExecuteCommandSubprocess('s3', 'type', 'config\\node3.json')
    #shard 4 events
    if event == '_local_s4_':      
        ExecuteCommandSubprocess('s4','client.exe','getblockheight', '-a', '127.0.0.1:8026')  
    if event == '_stop_s4_':      
        ExecuteCommandSubprocess('s4', 'sc','stop', 'seele_shard_4')
    if event == '_start_s4_':      
        ExecuteCommandSubprocess('s4', 'sc','start', 'seele_shard_4')
    if event == '_status_s4_':      
        ExecuteCommandSubprocess('s4', 'sc','query', 'seele_shard_4')
    if event == '_log_s4_':      
        ExecuteCommandSubprocess('s4', 'type','shard4.out.log', )
    if event == '_network_s4_':
        remote_block=GetRemoteBlock('s4')
        window.FindElement('_s4_out_').Update(now_fmt + "\n\n" + remote_block)
    if event == '_config_s4_':
        ExecuteCommandSubprocess('s4', 'type', 'config\\node4.json')
    #shard 1 new key generation
    if not shard1_key_window_active and event == '新建::_key_s1_':
        shard1_key_window_active = True
        layout_shard1_key = [
                                [sg.Text('', size=(80,1), font=("Arial", 9), key='_key_gen_s1_msg_')],
                                [sg.Multiline('', size=(80,3), key='_key_gen_s1_')],
                                [sg.Button(generate_key_pairs_btn, key='_gen_key_pair_s1_')]
                            ]
        win_key_1 = sg.Window(shard1_key_gen_win_title_str, icon='icon/seele.ico', resizable=True, font=("Arial", 10), element_padding=((5,5),(5,5))).Layout(layout_shard1_key)
    
    if shard1_key_window_active:
        while True: 
            event_key_1, value_key1 = win_key_1.Read(timeout=100)
            if event_key_1 == "_gen_key_pair_s1_":
               keys=KeyGen("1")
               win_key_1.FindElement('_key_gen_s1_msg_').Update(account_safe_str)
               win_key_1.FindElement('_key_gen_s1_').Update(keys)
               
            if event_key_1 is None or event_key_1 == 'Exit':
                shard1_key_window_active = False   
                win_key_1.Close()
                break
    #shard2 new key generation
    if not shard2_key_window_active and event == '新建::_key_s2_':
        shard2_key_window_active = True
        layout_shard2_key = [
                                [sg.Text('', size=(80,1), font=("Arial", 9), key='_key_gen_s2_msg_')],
                                [sg.Multiline('', size=(80,3), key='_key_gen_s2_')],
                                [sg.Button(generate_key_pairs_btn, key='_gen_key_pair_s2_')]
                            ]
        win_key_2 = sg.Window(shard2_key_gen_win_title_str, icon='icon/seele.ico', resizable=True, font=("Arial", 10), element_padding=((5,5),(5,5))).Layout(layout_shard2_key)
    
    if shard2_key_window_active:
        while True: 
            event_key_2, value_key2 = win_key_2.Read(timeout=100)
            if event_key_2 == "_gen_key_pair_s2_":
               keys=KeyGen("2")
               win_key_2.FindElement('_key_gen_s2_msg_').Update(account_safe_str)
               win_key_2.FindElement('_key_gen_s2_').Update(keys)
               
            if event_key_2 is None or event_key_2 == 'Exit':
                shard2_key_window_active = False   
                win_key_2.Close()
                break
    #shard3 new key generation
    if not shard3_key_window_active and event == '新建::_key_s3_':
        shard3_key_window_active = True
        layout_shard3_key = [
                                [sg.Text('', size=(80,1), font=("Arial", 9), key='_key_gen_s3_msg_')],
                                [sg.Multiline('', size=(80,3), key='_key_gen_s3_')],
                                [sg.Button(generate_key_pairs_btn, key='_gen_key_pair_s3_')]
                            ]
        win_key_3 = sg.Window(shard3_key_gen_win_title_str, icon='icon/seele.ico', resizable=True, font=("Arial", 10), element_padding=((5,5),(5,5))).Layout(layout_shard3_key)
    
    if shard3_key_window_active:
        while True: 
            event_key_3, value_key3 = win_key_3.Read(timeout=100)
            if event_key_3 == "_gen_key_pair_s3_":
               keys=KeyGen("3")
               win_key_3.FindElement('_key_gen_s3_msg_').Update(account_safe_str)
               win_key_3.FindElement('_key_gen_s3_').Update(keys)
               
            if event_key_3 is None or event_key_3 == 'Exit':
                shard3_key_window_active = False   
                win_key_3.Close()
                break
    #shard4 new key generation
    if not shard4_key_window_active and event == '新建::_key_s4_':
        shard4_key_window_active = True
        layout_shard4_key = [
                                [sg.Text('', size=(80,1), font=("Arial", 9), key='_key_gen_s4_msg_')],
                                [sg.Multiline('', size=(80,3), key='_key_gen_s4_')],
                                [sg.Button(generate_key_pairs_btn, key='_gen_key_pair_s4_')]
                            ]
        win_key_4 = sg.Window(shard4_key_gen_win_title_str, icon='icon/seele.ico', resizable=True, font=("Arial", 10), element_padding=((5,5),(5,5))).Layout(layout_shard4_key)
    
    if shard4_key_window_active:
        while True: 
            event_key_4, value_key4 = win_key_4.Read(timeout=100)
            if event_key_4 == "_gen_key_pair_s4_":
               keys=KeyGen("4")
               win_key_4.FindElement('_key_gen_s4_msg_').Update(account_safe_str)
               win_key_4.FindElement('_key_gen_s4_').Update(keys)
               
            if event_key_4 is None or event_key_4 == 'Exit':
                shard4_key_window_active = False   
                win_key_4.Close()
                break
    #shard1 use existing key
    if not shard1_key_exist_window_active and event == '现有::_key_s1_':
        shard1_key_exist_window_active = True
        key_list = GetKeyList("shard1")
        layout_shard1_existing_key = [
                                [sg.Text(existing_shard1_key_list_str, size=(80,1), font=("Arial", 10), key='_existing_key_list_s1_msg_')],
                                [sg.Listbox(key_list, size=(80,8), font=("Arial", 10), select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, key='_existing_key_list_box_s1_')],
                                [sg.Button(update_config_btn, key='_update_config_list_s1_', pad=((5,0),(5,0)) )],
                                [sg.Text('_'*80, text_color="#C0C0C0")],
                                [sg.Text(existing_shard1_key_str, size=(80,1), font=("Arial", 10), key='_existing_key_s1_msg_')],
                                [sg.InputText('', size=(80,1), key='_existing_key_input_s1_')],
                                [sg.Button(update_config_btn, key='_update_config_key_input_s1_')],
                            ]
        win_key_exist_s1 = sg.Window(shard1_existing_key_win_title_str, icon='icon/seele.ico', resizable=True, font=("Arial", 10), element_padding=((5,5),(5,5))).Layout(layout_shard1_existing_key)

    if shard1_key_exist_window_active:
        while True:
            event_key_exist_s1, value_existing_key_s1 = win_key_exist_s1.Read(timeout=100)
            if event_key_exist_s1 == '_update_config_list_s1_':
                if value_existing_key_s1['_existing_key_list_box_s1_'] == []:
                    sg.Popup(no_shard_1_public_key_selected_str)
                else:
                    coinbase = value_existing_key_s1['_existing_key_list_box_s1_'][0].rstrip('\n')
                    if sg.PopupYesNo(update_shard1_config_with_str + coinbase) == "Yes":
                        UpdateConfigFile("1", coinbase, "")
                        win_key_exist_s1.FindElement('_existing_key_list_s1_msg_').Update(update_shard1_coinbase_with_str + coinbase)

            if event_key_exist_s1 == '_update_config_key_input_s1_':
                if value_existing_key_s1['_existing_key_input_s1_'] == "":
                    sg.Popup(key_field_empty_str)
                else:
                    coinbase = value_existing_key_s1['_existing_key_input_s1_'].strip()
                    if sg.PopupYesNo(update_shard1_config_with_str + coinbase) == "Yes":
                        UpdateConfigFile("1", coinbase, "")
                        win_key_exist_s1.FindElement('_existing_key_s1_msg_').Update(update_shard1_coinbase_with_str + coinbase)

            if event_key_exist_s1 is None or event_key_exist_s1 == 'Exit':
                shard1_key_exist_window_active = False
                win_key_exist_s1.Close()
                break
    #shard2 use existing key
    if not shard2_key_exist_window_active and event == '现有::_key_s2_':
        shard2_key_exist_window_active = True
        key_list = GetKeyList("shard2")
        layout_shard2_existing_key = [
                                [sg.Text(existing_shard2_key_list_str, size=(80,1), font=("Arial", 10), key='_existing_key_list_s2_msg_')],
                                [sg.Listbox(key_list, size=(80,8), font=("Arial", 10), select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, key='_existing_key_list_box_s2_')],
                                [sg.Button(update_config_btn, key='_update_config_list_s2_', pad=((5,0),(5,0)) )],
                                [sg.Text('_'*80, text_color="#C0C0C0")],
                                [sg.Text(existing_shard2_key_str, size=(80,1), font=("Arial", 10), key='_existing_key_s2_msg_')],
                                [sg.InputText('', size=(80,1), key='_existing_key_input_s2_')],
                                [sg.Button(update_config_btn, key='_update_config_key_input_s2_')],
                            ]
        win_key_exist_s2 = sg.Window(shard2_existing_key_win_title_str, icon='icon/seele.ico', resizable=True, font=("Arial", 10), element_padding=((5,5),(5,5))).Layout(layout_shard2_existing_key)

    if shard2_key_exist_window_active:
        while True:
            event_key_exist_s2, value_existing_key_s2 = win_key_exist_s2.Read(timeout=100)
            if event_key_exist_s2 == '_update_config_list_s2_':
                if value_existing_key_s2['_existing_key_list_box_s2_'] == []:
                    sg.Popup(no_shard_2_public_key_selected_str)
                else:
                    coinbase = value_existing_key_s2['_existing_key_list_box_s2_'][0].rstrip('\n')
                    if sg.PopupYesNo(update_shard2_config_with_str + coinbase) == "Yes":
                        UpdateConfigFile("2", coinbase, "")
                        win_key_exist_s2.FindElement('_existing_key_list_s2_msg_').Update(update_shard2_coinbase_with_str + coinbase)

            if event_key_exist_s2 == '_update_config_key_input_s2_':
                if value_existing_key_s2['_existing_key_input_s2_'] == "":
                    sg.Popup(key_field_empty_str)
                else:
                    coinbase = value_existing_key_s2['_existing_key_input_s2_'].strip()
                    if sg.PopupYesNo(update_shard2_config_with_str + coinbase) == "Yes":
                        UpdateConfigFile("2", coinbase, "")
                        win_key_exist_s2.FindElement('_existing_key_s2_msg_').Update(update_shard2_coinbase_with_str + coinbase)

            if event_key_exist_s2 is None or event_key_exist_s2 == 'Exit':
                shard2_key_exist_window_active = False
                win_key_exist_s2.Close()
                break
    #shard3 use existing key
    if not shard3_key_exist_window_active and event == '现有::_key_s3_':
        shard3_key_exist_window_active = True
        key_list = GetKeyList("shard3")
        layout_shard3_existing_key = [
                                [sg.Text(existing_shard3_key_list_str, size=(80,1), font=("Arial", 10), key='_existing_key_list_s3_msg_')],
                                [sg.Listbox(key_list, size=(80,8), font=("Arial", 10), select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, key='_existing_key_list_box_s3_')],
                                [sg.Button(update_config_btn, key='_update_config_list_s3_', pad=((5,0),(5,0)) )],
                                [sg.Text('_'*80, text_color="#C0C0C0")],
                                [sg.Text(existing_shard3_key_str, size=(80,1), font=("Arial", 10), key='_existing_key_s3_msg_')],
                                [sg.InputText('', size=(80,1), key='_existing_key_input_s3_')],
                                [sg.Button(update_config_btn, key='_update_config_key_input_s3_')],
                            ]
        win_key_exist_s3 = sg.Window(shard3_existing_key_win_title_str, icon='icon/seele.ico', resizable=True, font=("Arial", 10), element_padding=((5,5),(5,5))).Layout(layout_shard3_existing_key)

    if shard3_key_exist_window_active:
        while True:
            event_key_exist_s3, value_existing_key_s3 = win_key_exist_s3.Read(timeout=100)
            if event_key_exist_s3 == '_update_config_list_s3_':
                if value_existing_key_s3['_existing_key_list_box_s3_'] == []:
                    sg.Popup(no_shard_3_public_key_selected_str)
                else:
                    coinbase = value_existing_key_s3['_existing_key_list_box_s3_'][0].rstrip('\n')
                    if sg.PopupYesNo(update_shard3_config_with_str + coinbase) == "Yes":
                        UpdateConfigFile("3", coinbase, "")
                        win_key_exist_s3.FindElement('_existing_key_list_s3_msg_').Update(update_shard3_coinbase_with_str + coinbase)

            if event_key_exist_s3 == '_update_config_key_input_s3_':
                if value_existing_key_s3['_existing_key_input_s3_'] == "":
                    sg.Popup(key_field_empty_str)
                else:
                    coinbase = value_existing_key_s3['_existing_key_input_s3_'].strip()
                    if sg.PopupYesNo(update_shard3_config_with_str + coinbase) == "Yes":
                        UpdateConfigFile("3", coinbase, "")
                        win_key_exist_s3.FindElement('_existing_key_s3_msg_').Update(update_shard3_coinbase_with_str + coinbase)

            if event_key_exist_s3 is None or event_key_exist_s3 == 'Exit':
                shard3_key_exist_window_active = False
                win_key_exist_s3.Close()
                break
    #shard4 use existing key
    if not shard4_key_exist_window_active and event == '现有::_key_s4_':
        shard4_key_exist_window_active = True
        key_list = GetKeyList("shard4")
        layout_shard4_existing_key = [
                                [sg.Text(existing_shard4_key_list_str, size=(80,1), font=("Arial", 10), key='_existing_key_list_s4_msg_')],
                                [sg.Listbox(key_list, size=(80,8), font=("Arial", 10), select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, key='_existing_key_list_box_s4_')],
                                [sg.Button(update_config_btn, key='_update_config_list_s4_', pad=((5,0),(5,0)) )],
                                [sg.Text('_'*80, text_color="#C0C0C0")],
                                [sg.Text(existing_shard4_key_str, size=(80,1), font=("Arial", 10), key='_existing_key_s4_msg_')],
                                [sg.InputText('', size=(80,1), key='_existing_key_input_s4_')],
                                [sg.Button(update_config_btn, key='_update_config_key_input_s4_')],
                            ]
        win_key_exist_s4 = sg.Window(shard4_existing_key_win_title_str, icon='icon/seele.ico', resizable=True, font=("Arial", 10), element_padding=((5,5),(5,5))).Layout(layout_shard4_existing_key)

    if shard4_key_exist_window_active:
        while True:
            event_key_exist_s4, value_existing_key_s4 = win_key_exist_s4.Read(timeout=100)
            if event_key_exist_s4 == '_update_config_list_s4_':
                if value_existing_key_s4['_existing_key_list_box_s4_'] == []:
                    sg.Popup(no_shard_4_public_key_selected_str)
                else:
                    coinbase = value_existing_key_s4['_existing_key_list_box_s4_'][0].rstrip('\n')
                    if sg.PopupYesNo(update_shard4_config_with_str + coinbase) == "Yes":
                        UpdateConfigFile("4", coinbase, "")
                        win_key_exist_s4.FindElement('_existing_key_list_s4_msg_').Update(update_shard4_coinbase_with_str + coinbase)

            if event_key_exist_s4 == '_update_config_key_input_s4_':
                if value_existing_key_s4['_existing_key_input_s4_'] == "":
                    sg.Popup(key_field_empty_str)
                else:
                    coinbase = value_existing_key_s4['_existing_key_input_s4_'].strip()
                    if sg.PopupYesNo(update_shard4_config_with_str + coinbase) == "Yes":
                        UpdateConfigFile("4", coinbase, "")
                        win_key_exist_s4.FindElement('_existing_key_s4_msg_').Update(update_shard4_coinbase_with_str + coinbase)

            if event_key_exist_s4 is None or event_key_exist_s4 == 'Exit':
                shard4_key_exist_window_active = False
                win_key_exist_s4.Close()
                break
    #help window
    if not help_window_active and event == '帮助::_help_mining_':
        help_window_active = True
        with open(".\\help\\help.txt", "r", encoding="utf-8") as file:
            help_text = file.read()
        layout_help = [
                                [sg.Multiline(help_text, size=(80,15))],
                                [sg.Exit()],
                            ]
        win_help = sg.Window("帮助", icon='icon\\seele.ico', resizable=True, font=("Arial", 10), element_padding=((5,5),(5,5))).Layout(layout_help)

        if help_window_active:
            while True:
                event_help, value_help = win_help.Read(timeout=100)
                if event_help == '帮助::_help_mining_':
                    pass
            
                if event_help is None or event_help == 'Exit':
                    help_window_active = False
                    win_help.Close()
                    break
    #about window
    if not about_window_active and event == '关于::_help_about_':
        about_window_active = True
        about_text="Seele Mining Control\nVersion: 1.0.0\nOS: Windows_NT X64\n© 2019 SeeleTech"
        layout_about = [
                                [sg.Text(about_text, size=(25,5))],
                                [sg.Ok()]
                        ]
        win_about = sg.Window("", icon='icon/seele.ico', resizable=True, font=("Arial", 10), element_padding=((5,5),(5,5))).Layout(layout_about)

        if about_window_active:
            while True:
                event_about, value_about = win_about.Read(timeout=100)
                if event_about == "关于::_help_about_":
                    pass
            
                if event_about is None or event_about == 'Ok':
                    about_window_active = False
                    win_about.Close()
                    break


window.Close()