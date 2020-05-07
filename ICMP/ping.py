"""　
ICMP使用したPING通信をPythonで実装してみる

Ping とは
サーバーの動作確認やネットワークとの接続確認を行うコマンド．
=> ping (IPアドレス) としてコマンド入力．
## エコー要求とエコー応答

ICMP （Internet Control Message Protocol）
IP Message が送信元空相手に届くまでの間に起きたエラー情報を送信元に通知する．

構成：EtherNetヘッダ，IPヘッダ，ICMPヘッダ
Socket関数が自動処理 →　EtherNet, IP

ICMPヘッダ =====
Type:8bit, Code:8bit, CheckSum:16bit
ID:16bit, Sequence:16bit, data:可変長
"""
"""
ICMP_ECHOREPLY	0	エコー応答
ICMP_UNREACH	3	終点到達不能
ICMP_SOURCEQUENCH	4	始点抑制
ICMP_REDIRECT	5	リダイレクト
ICMP_ECHO	    8	エコー要求
ICMP_TIMXCEED	11	時間超過
ICMP_PARAMPROB	12	パラメータエラー
"""
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_ICMP)


IPaddr = "192.168.11.2"

##エコー要求(8)
##受信側は[応答(0)]で元のパケットをそのまま返信
ICM_Type = (0x08)
ICM_Code = (0x00)
##自由に入力（区別するために使用する）
ICM_ID = (0x01)
ICM_Seq = (0x01)

ICM_LIST = [0]*6

ICM_LIST[0] = ICM_Type
ICM_LIST[1] = ICM_Code
ICM_LIST[2] = 0 #ICM_CheckSum1
ICM_LIST[3] = 0 #ICM_CheckSum2
ICM_LIST[4] = ICM_ID
ICM_LIST[5] = ICM_Seq

ICM_DATA = b'EchoData'
ICM_LIST.extend(ICM_DATA)
#[8, 0, 0, 0, 1, 1, 69, 99, 104, 111, 68, 97, 116, 97]

## CheckSum ===========
csum = 0
for i in range(int(len(ICM_LIST)/2)):
    csum += (ICM_LIST[i*2]<<8) | (ICM_LIST[i*2+1])

csum = (csum & 0xffff) + (csum>>16)
csum = 0xffff - (csum)

print('Checksum: ' + hex(csum))
## ====================

ICM_LIST[2] = (csum & 0xFF00)>>8 #ICM_CheckSum2
ICM_LIST[3] = csum & 0x00FF #ICM_CheckSum1

print("Send: ", bytes(ICM_LIST))
sock.sendto(bytes(ICM_LIST), (IPaddr, 0))

data = sock.recv(1024)
## 20番まで受信先IP情報
## 20番以降エコー応答情報
print("Recv: ", data[20:])