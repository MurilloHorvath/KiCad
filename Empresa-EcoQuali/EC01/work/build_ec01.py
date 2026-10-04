from pathlib import Path
import json,csv,math,html,collections,zipfile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs'/'EC01_ESQUEMATICO_REV0_1'
OUT.mkdir(parents=True,exist_ok=True)
COMPS=[]
SECTIONS=['01 Alimentacao e bateria','02 ESP32 e inicializacao','03 BLE e cristal','04 Radio LoRa','05 Expansao e display','06 Sensores e CAN','07 USB de servico']
def add(ref,value,pkg,pins,sec,pos,fit='SIM',note=''):
    # pins: number -> (pin name, electrical net or None)
    c=dict(ref=ref,value=value,package=pkg,pins={str(k):(v if isinstance(v,tuple) else (str(k),v)) for k,v in pins.items()},section=sec,pos=pos,fit=fit,note=note)
    COMPS.append(c);return c
def two(ref,val,a,b,sec,pos,pkg='0603',fit='SIM',note=''):
    return add(ref,val,pkg,{1:('1',a),2:('2',b)},sec,pos,fit,note)
def cap(ref,val,net,sec,pos,pkg='0603',fit='SIM',note=''):
    return two(ref,val,net,'GND',sec,pos,pkg,fit,note)

# 01 Supply: single PROTECTED removable cell; no charger or USB powering.
add('BT1','BH-18650-A1AJ005','PENDENTE_BH18650',{1:('+','BAT_RAW'),2:('-','GND')},0,(43,59),note='Envelope reservado 80x23 mm; NAO e footprint verificado. Exigir celula 1S protegida e conferir comprimento admissivel.')
two('F1','Fusivel 1A lento','BAT_RAW','BAT_FUSED',0,(78,43),'1206',note='Selecionar MPN e curva I2t antes de liberar BOM.')
add('Q1','AO3401A','SOT23',{1:('G','GND'),2:('S','BAT_PROT'),3:('D','BAT_FUSED')},0,(73,43),note='PMOS de inversao: D no positivo da bateria, S na carga, G em GND.')
add('SW1','CHAVE GERAL','HDR2',{1:('IN','BAT_PROT'),2:('OUT','BAT_SW')},0,(86,43),note='Header 2.54 mm para chave externa; selecionar chave >=1A DC.')
add('U1','TPS63802DLAR','DLA10',{1:('EN','PSU_EN'),2:('MODE','GND'),3:('AGND','GND'),4:('FB','PSU_FB'),5:('PG','PSU_PG'),6:('VOUT','3V3'),7:('L2','SW_L2'),8:('PGND','GND'),9:('L1','SW_L1'),10:('VIN','BAT_SW')},0,(67,35))
two('L1','XFL4015-471MEC 0.47uH','SW_L1','SW_L2',0,(67,31),'L4X4',note='Conferir sufixo fornecido, pads e Isat; referencia TI XFL4015-471ME.')
cap('C1','10uF 10V X5R','BAT_SW',0,(64,34),'0805')
cap('C2','100nF 16V X7R','BAT_SW',0,(63,37))
cap('C3','22uF 10V X5R','3V3',0,(71,34),'0805')
cap('C4','22uF 10V X5R','3V3',0,(74,34),'0805')
two('R1','511k 1%','3V3','PSU_FB',0,(69,39))
two('R2','91k 1%','PSU_FB','GND',0,(66,39))
two('R3','200k 1%','BAT_SW','PSU_EN',0,(61,41))
two('R4','100k 1%','PSU_EN','GND',0,(64,41),note='UVLO nominal: liga 3.30V; desliga 3.00V. Conferir tolerancias e queda da bateria.')
two('R5','100k','3V3','PSU_PG',0,(73,38))
two('R6','100k 0.1%','BAT_SW','BAT_ADC',0,(45,35))
two('R7','100k 0.1%','BAT_ADC','GND',0,(45,38))
cap('C5','100nF','BAT_ADC',0,(42,37))

# 02 MCU: reserved flash pins are deliberately unconnected externally.
pin_names={1:'LNA_IN',2:'VDD3P3',3:'VDD3P3',4:'GPIO0',5:'GPIO1',6:'GPIO2',7:'CHIP_EN',8:'GPIO3',9:'GPIO4',10:'GPIO5',11:'VDD3P3_RTC',12:'GPIO6',13:'GPIO7',14:'GPIO8',15:'GPIO9',16:'GPIO10',17:'VDD3P3_CPU',18:'VDD_SPI',19:'SPIHD_FLASH',20:'SPIWP_FLASH',21:'SPICS0_FLASH',22:'SPICLK_FLASH',23:'SPID_FLASH',24:'SPIQ_FLASH',25:'GPIO18_USB_DM',26:'GPIO19_USB_DP',27:'GPIO20',28:'GPIO21',29:'XTAL_N',30:'XTAL_P',31:'VDDA',32:'VDDA',33:'EP_GND'}
pin_nets={1:'BLE_CHIP',2:'3V3_RF',3:'3V3_RF',4:'BAT_ADC',5:'PORT_A_IO',6:'LORA_NSS',7:'CHIP_EN',8:'LORA_DIO1',9:'LORA_BUSY',10:'SPI_MISO',11:'3V3',12:'SPI_SCK',13:'SPI_MOSI',14:'I2C_INT_SDA',15:'BOOT_N',16:'DISP_CS',17:'3V3',18:'VDD_SPI',25:'USB_DM_MCU',26:'USB_DP_MCU',27:'PORT_B_IO',28:'I2C_INT_SCL',29:'XTAL_N',30:'XTAL_P',31:'3V3',32:'3V3',33:'GND'}
add('U2','ESP32-C3FH4','QFN32_5X5_EP3_7',{i:(pin_names[i],pin_nets.get(i)) for i in range(1,34)},1,(29,25),note='GPIO12-17 reservados a flash; GPIO11/VDD_SPI alimenta flash. Nenhum deles e GPIO de aplicacao.')
two('L2','24nH >=500mA','3V3','3V3_RF',1,(23,27),note='Filtro ALIMENTACAO, nunca conectar a LNA_IN. Valor inicial sujeito a ensaios EMC.')
for r,v,n,p in [('C6','10uF','3V3_RF',(23,30)),('C7','100nF','3V3_RF',(26,29)),('C8','100nF','3V3',(33,28)),('C9','100nF','3V3',(32,22)),('C10','1uF','VDD_SPI',(33,25)),('C11','1uF','3V3',(28,20)),('C12','100nF','3V3',(25,22))]:cap(r,v,n,1,p)
two('R8','10k','3V3','CHIP_EN',1,(38,27))
cap('C13','1uF','CHIP_EN',1,(38,30))
add('SW2','RESET SPST-NO','BOTAO_A_DEFINIR',{1:('EN','CHIP_EN'),2:('GND','GND')},1,(37,15),note='Botao fisico momentaneo normalmente aberto. Selecionar MPN/footprint na etapa mecanica.')
two('R9','10k','3V3','BOOT_N',1,(43,26))
add('SW3','BOOT SPST-NO','BOTAO_A_DEFINIR',{1:('GPIO9','BOOT_N'),2:('GND','GND')},1,(43,15),note='Botao fisico momentaneo normalmente aberto. Pressionar BOOT durante RESET para ROM download.')
two('R10','10k','3V3','LORA_NSS',1,(36,23),note='GPIO2 e strapping; NSS alto no reset.')
two('R11','4.7k','3V3','I2C_INT_SDA',1,(38,35),note='GPIO8 alto no reset. Escravos internos devem liberar SDA durante boot.')
two('R12','4.7k','3V3','I2C_INT_SCL',1,(38,38),note='GPIO21 pode emitir UART ROM antes do remapeamento; SDA fica alta.')
two('R13','10k','3V3','DISP_CS',1,(50,19))

# 03 RF includes a separate antenna match, with unresolved radiating geometry.
add('Y1','40MHz CL=8pF <=10ppm','XTAL3225',{1:('X1','XTAL_P'),2:('GND','GND'),3:('X2','XTAL_N'),4:('GND','GND')},2,(29,17),note='MPN a selecionar. 10pF iniciais presumem Cparasita ~3pF; verificar ESR, drive e tolerancia total.')
cap('C14','10pF C0G','XTAL_P',2,(26,17),'0402')
cap('C15','10pF C0G','XTAL_N',2,(32,17),'0402')
cap('C16','1.5pF C0G TUNE','BLE_CHIP',2,(22,23),'0201',note='Casamento inicial; exige ajuste VNA e emissao harmonica.')
two('L3','2.7nH TUNE','BLE_CHIP','BLE_50R',2,(20,22),'0201')
cap('C17','1.5pF C0G TUNE','BLE_50R',2,(18,23),'0201')
cap('C18','TUNE DNP','BLE_50R',2,(16,21),'0201','NAO')
two('R14','0R TUNE','BLE_50R','BLE_ANT',2,(14,20),'0201')
cap('C19','TUNE DNP','BLE_ANT',2,(12,21),'0201','NAO')
add('ANT1','Antena impressa BLE 2.4GHz','PENDENTE_ANTENA',{1:('FEED','BLE_ANT'),2:('SHORT_GND','GND')},2,(15,10),note='IFA reservada, GEOMETRIA NAO DEFINIDA. Nao ha cobre de antena neste pre-layout. Short e feed dependem do desenho final.')

# 04 Ebyte manual 2026 section 3.2 (website pin 12 entry is incorrect).
en={i:('GND','GND') for i in [1,2,3,4,5,10,11,12,20,22]}
en.update({6:('RXEN','LORA_RXEN'),7:('TXEN','LORA_TXEN'),8:('DIO2','LORA_DIO2'),9:('VCC','3V3'),13:('DIO1','LORA_DIO1'),14:('BUSY','LORA_BUSY'),15:('NRST','LORA_RST_N'),16:('MISO','SPI_MISO'),17:('MOSI','LORA_MOSI'),18:('SCK','LORA_SCK'),19:('NSS','LORA_NSS'),21:('ANT','LORA_ANT')})
add('U3','E22-900M22S SX1262','E22_900M22S',dict(sorted(en.items())),3,(88,19),note='Sempre populado. Confirmar revisao fisica; p12=GND, p15=NRST no manual 2026. DIO3 interno: TCXO 2.2V.')
two('R15','0R','LORA_DIO2','LORA_TXEN',3,(97,17))
two('R16','100k','LORA_TXEN','GND',3,(99,19))
two('R17','100k','LORA_RXEN','GND',3,(97,21))
two('R18','10k','3V3','LORA_RST_N',3,(78,20))
two('R19','22R','SPI_SCK','LORA_SCK',3,(76,24))
two('R20','22R','SPI_MOSI','LORA_MOSI',3,(76,27))
cap('C20','22uF 10V','3V3',3,(99,14),'0805')
cap('C21','100nF','3V3',3,(99,11))
add('J1','U.FL-R-SMT-1','UFL',{1:('RF','LORA_ANT'),2:('GND','GND'),3:('GND','GND')},3,(76,32),note='Escolher apenas J1 OU IPEX integrado no modulo. Trilha curta 50ohm, sem T aberto; layout final deve eliminar ramal nao usado.')

# 05 Internal control bus, expander and optional display.
add('U4','TCA9534APWR','TSSOP16',{1:('A0','GND'),2:('A1','GND'),3:('A2','GND'),4:('P0','LORA_RST_N'),5:('P1','LORA_RXEN'),6:('P2','LED_N'),7:('P3','DISP_DC'),8:('GND','GND'),9:('P4','DISP_RST_N'),10:('P5','DISP_BUSY'),11:('P6','SENS_EN'),12:('P7','CAN_SHDN'),13:('INT',None),14:('SCL','I2C_INT_SCL'),15:('SDA','I2C_INT_SDA'),16:('VCC','3V3')},4,(46,31),note='Endereco 7-bit 0x38. Portas inicializam entradas; escrever latch antes do registro de direcao.')
cap('C22','100nF','3V3',4,(49,32))
two('R21','2.2k','3V3','LED_A',4,(52,35))
add('D1','LED verde','0603',{1:('A','LED_A'),2:('K','LED_N')},4,(55,35),note='Acende com P2 baixo; manter apagado entre pulsos.')
two('R22','100k','3V3','LED_N',4,(55,38))
two('R23','100k','SENS_EN','GND',4,(52,41))
two('R24','100k','3V3','CAN_SHDN',4,(55,41))
two('R25','100k','3V3','DISP_RST_N',4,(55,22))
two('R26','100k','DISP_DC','GND',4,(58,22))
two('R27','100k','DISP_BUSY','GND',4,(61,22))
add('J2','DISPLAY 8P DNP','HDR8',{1:('VCC','3V3'),2:('GND','GND'),3:('CLK','DISP_CLK'),4:('DATA','DISP_DATA'),5:('CS','DISP_CS'),6:('DC','DISP_DC'),7:('RST','DISP_RST_N'),8:('BUSY','DISP_BUSY')},4,(53,9),'NAO','Header 2.54 mm. Interface de modulo de display 3.3V; nao aciona diretamente painel e-paper cru.')
two('R28','0R SPI','SPI_SCK','DISP_CLK',4,(53,14),fit='NAO')
two('R29','0R SPI','SPI_MOSI','DISP_DATA',4,(56,14),fit='NAO')
two('R30','0R I2C','I2C_INT_SCL','DISP_CLK',4,(59,14),fit='NAO')
two('R31','0R I2C','I2C_INT_SDA','DISP_DATA',4,(62,14),fit='NAO',note='SPI: R28/R29. I2C: R30/R31. Nunca ambos os pares.')
add('J3','SENSOR INTERNO I2C DNP','HDR4',{1:('3V3','3V3'),2:('GND','GND'),3:('SDA','I2C_INT_SDA'),4:('SCL','I2C_INT_SCL')},4,(10,36),'NAO','Reserva para pequena placa SHT40; sensor onboard integrado ainda nao definido pelo cliente.')

# 06 Common RJ bus. Assembly options, not arbitrary firmware-only CAN selection.
add('Q2','AO3401A','SOT23',{1:('G','SENS_GATE'),2:('S','3V3'),3:('D','SENS_PRE')},5,(81,36))
add('Q3','2N7002','SOT23',{1:('G','SENS_EN'),2:('S','GND'),3:('D','SENS_GATE')},5,(85,36))
two('R32','100k','3V3','SENS_GATE',5,(82,40))
two('F2','PTC Ihold 100mA','SENS_PRE','VEXT',5,(89,36),'1206',note='Limite de projeto 100mA TOTAL; escolher curva R/frio, disparo e derating do componente real.')
cap('C23','10uF','VEXT',5,(93,36),'0805')
two('R33','33R DIGITAL','PORT_A_IO','BUS_A',5,(91,40))
two('R34','33R DIGITAL','PORT_B_IO','BUS_B',5,(95,40))
two('R35','4.7k DIGITAL','VEXT','BUS_A',5,(90,43))
two('R36','4.7k I2C','VEXT','BUS_B',5,(94,43),fit='NAO')
for ref,y in [('RJ1',49),('RJ2',66)]:
 add(ref,'R-RJ11M04P-A002','PENDENTE_RJ11',{1:('VCC','VEXT'),2:('GND','GND'),3:('A','BUS_A'),4:('B','BUS_B')},5,(101,y),note='Pinagem LOGICA do contrato; conferir orientacao dos contatos e pinos fisicos pelo desenho C51904501. Sem pads mecanicos inventados.')
add('U5','TCAN330DR','SOIC8',{1:('TXD','CAN_TX'),2:('GND','GND'),3:('VCC','3V3'),4:('RXD','CAN_RX'),5:('SHDN','CAN_SHDN'),6:('CANL','CAN_L'),7:('CANH','CAN_H'),8:('S','GND')},5,(85,47),'NAO','Opcao CAN comum aos dois RJ11; um transceiver pois o ESP32-C3 tem um controlador TWAI. CAN classico, nao CAN FD.')
cap('C24','100nF','3V3',5,(82,47),fit='NAO')
two('R37','0R CAN','PORT_A_IO','CAN_TX',5,(76,47),fit='NAO')
two('R38','0R CAN','CAN_RX','PORT_B_IO',5,(76,50),fit='NAO')
two('R39','0R CAN','CAN_H','BUS_A',5,(87,52),fit='NAO')
two('R40','0R CAN','CAN_L','BUS_B',5,(90,52),fit='NAO')
two('R41','10k CAN','3V3','CAN_TX',5,(79,50),fit='NAO')
two('R42','120R 1% 0.25W','CAN_H','CAN_TERM',5,(86,56),'1206','NAO','Somente em uma extremidade fisica do barramento.')
add('JP1','TERMINACAO CAN','HDR2',{1:('TERM','CAN_TERM'),2:('CANL','CAN_L')},5,(89,60),'NAO')
for ref,y in [('U6',48),('U7',63)]:
 add(ref,'USBLC6-2SC6 DIGITAL','SOT23_6',{1:('IO1','BUS_A'),2:('GND','GND'),3:('IO2','BUS_B'),4:('IO2','BUS_B'),5:('VBUS','VEXT'),6:('IO1','BUS_A')},5,(91,y),note='Protecao DIGITAL; remover na variante CAN. Validar ESD do conjunto com cabo real.')
for ref,y in [('D2',51),('D3',66)]:
 add(ref,'PESD1CAN','SOT23',{1:('LINE1','BUS_A'),2:('LINE2','BUS_B'),3:('GND','GND')},5,(95,y),'NAO','Montar somente variante CAN; verificar pinout no datasheet do sufixo adquirido.')

# 07 Debug/service USB header with no power feed.
add('J4','USB SERVICE 4P','HDR4',{1:('GND','GND'),2:('D-','USB_DM'),3:('D+','USB_DP'),4:('NC_5V_PROIBIDO',None)},6,(40,7),note='Usar adaptador de servico identificado; bateria deve estar ligada. Pino4 sem cobre de alimentacao. Nao e USB-C; nao ha carregador.')
two('R43','22R','USB_DM_MCU','USB_DM',6,(33,33))
two('R44','22R','USB_DP_MCU','USB_DP',6,(30,33))
add('U8','USBLC6-2SC6','SOT23_6',{1:('IO1','USB_DM'),2:('GND','GND'),3:('IO2','USB_DP'),4:('IO2','USB_DP'),5:('VBUS','3V3'),6:('IO1','USB_DM')},6,(38,11),note='Desenhar par diferencial 90ohm; alimentacao local 3.3V. Header de bancada, sem declaracao de conformidade USB de produto.')
for i,(net,pos) in enumerate([('GND',(50,44)),('3V3',(53,44)),('BAT_SW',(57,44)),('CHIP_EN',(40,24)),('PSU_PG',(75,40)),('LORA_BUSY',(75,22))],1):
 add('TP'+str(i),net,'TP',{1:(net,net)},0 if i<4 else 1,pos)

# Final schematic-only revision. GPIO8 is clock (held high), not slave-driven SDA.
U2=next(c for c in COMPS if c['ref']=='U2')
U2['pins']['14']=('GPIO8','I2C_INT_SCL')
U2['pins']['16']=('GPIO10','I2C_INT_SDA')
U2['pins']['28']=('GPIO21','DISP_CS')
next(c for c in COMPS if c['ref']=='R11')['note']='Pull-up SDA interno GPIO10; nao ligado aos conectores RJ11.'
next(c for c in COMPS if c['ref']=='R12')['note']='GPIO8 strapping alto no reset; SCL interno. Nao conectar escravo que mantenha SCL baixo durante boot.'
next(c for c in COMPS if c['ref']=='R13')['note']='GPIO21 pode emitir UART no boot. Display mantido em reset baixo ate inicializar o expansor.'
rr=next(c for c in COMPS if c['ref']=='R25');rr['pins']={'1':('1','DISP_RST_N'),'2':('2','GND')};rr['note']='Mantem display em RESET durante boot.'
for c in COMPS:
 if c['ref'] in ['D2','D3']:
  c['value']='TVS CAN 2 canais TBD';c['package']='TVS_CAN_A_DEFINIR';c['note']='Protecao ainda a selecionar conforme limites absolutos TCAN330 e ensaio requerido. Numeracao logica; nao e MPN nem footprint liberado.'
 # Physical placement is deliberately not part of this deliverable.
 c.pop('pos',None)

ids=iter(range(1,100000))
def gid():return 'gge'+str(next(ids))
def st(x,y,s,mark='L',size=10,color='#1c3550'):
 return f'T~{mark}~{x}~{y}~0~{color}~Arial~{size}pt~~~~comment~{s}~1~start~{gid()}'
def ln(x,y,s,right=True):return f'N~{x}~{y}~0~#064c83~{s}~{gid()}~{ "start" if right else "end"}~{x+(3 if right else -3)}~{y-3}~Arial~8pt'
def pin(n,name,x,y,right=False):
 dx=-20 if right else 20; anchor='end' if right else 'start';tx=x+dx+(-3 if right else 3)
 return f'P~show~0~{n}~{x}~{y}~{0 if right else 180}~{gid()}^^{x}~{y}^^M {x} {y} h {dx}~#800000^^1~{tx}~{y+3}~0~{name}~{anchor}~Arial~7pt^^1~{x+dx/2}~{y-3}~0~{n}~middle~Arial~6pt^^0~{x+dx}~{y}^^0~'

def sch_symbol(c,x,y):
 ps=list(c['pins'].items());is_two=len(ps)==2 and c['ref'][0] in 'RCLF'
 shapes=[];links=[]
 if is_two:
  width=80;h=65
  body=[st(x,y-15,c['ref'],'P',10),st(x,y-2,c['value'],'N',9)]
  for (n,(name,net)),px,right in [(ps[0],x,False),(ps[1],x+80,True)]:
   body.append(pin(n,name,px,y+25,right))
   if net:links.append(ln(px,y+25,net,right))
  if c['ref'][0]=='C':
   body.extend([f'PL~{x+35} {y+15} {x+35} {y+35}~#800000~1~0~none~{gid()}',f'PL~{x+45} {y+15} {x+45} {y+35}~#800000~1~0~none~{gid()}',f'PL~{x+20} {y+25} {x+35} {y+25}~#800000~1~0~none~{gid()}',f'PL~{x+45} {y+25} {x+60} {y+25}~#800000~1~0~none~{gid()}'])
  else:body.append(f'R~{x+20}~{y+18}~~~40~14~#800000~1~0~none~{gid()}')
 else:
  width=210;nleft=(len(ps)+1)//2;h=max(80,nleft*20+25)
  body=[st(x+20,y-18,c['ref'],'P',10),st(x+20,y-4,c['value'],'N',9),f'R~{x+20}~{y+10}~~~170~{h-10}~#800000~1~0~#fffef0~{gid()}']
  for k,(n,(name,net)) in enumerate(ps):
   right=k>=nleft;px=x+width if right else x;py=y+25+(k-nleft if right else k)*20
   body.append(pin(n,name,px,py,right))
   if net:links.append(ln(px,py,net,right))
   else:links.append(f'O~{px}~{py}~{gid()}')
 attrs=f"package`{c['package']}`nameAlias`Value`Value`{c['value']}`pre`{c['ref']}`BOM`{c['fit']}`"
 lib=f"LIB~{x}~{y}~{attrs}~0~0~{c['uid']}"+'#@$'+'#@$'.join(body)
 return [lib]+links,h

SCH=[];section_svgs=[];schematic_cells=[];sheets=[]
for c in COMPS:c['uid']=gid()
for sec,title in enumerate(SECTIONS):
 subset=[c for c in COMPS if c['section']==sec]
 # One large sheet, sections stacked. Four non-overlapping columns.
 base=80
 section_start=len(SCH)
 SCH.extend([st(100,base,title,size=18),st(100,base+22,'EC01 REV0.1 - PROJETO PRELIMINAR - nao liberar fabricacao',size=10,color='#ab4b00')])
 heights=[base+75]*4
 for c in sorted(subset,key=lambda c:-len(c['pins'])):
  col=min(range(4),key=lambda i:heights[i]);x=170+col*510;y=heights[col]
  shapes,h=sch_symbol(c,x,y);SCH+=shapes;schematic_cells.append((c,x,y,h));heights[col]+=h+85
 assert max(heights)<base+1180,(title,max(heights)-base)
 sheets.append({'docType':'1','title':title,'description':'EC01 REV0.1 - Esquematico preliminar sem simulacao','dataStr':{'head':{'docType':'1','editorVersion':'6.5.54','newgId':True,'c_para':{'Prefix Start':'1'},'c_spiceCmd':None},'canvas':'CA~2200~1300~#FFFFFF~yes~#CCCCCC~5~2200~1300~line~5~pixel~5~0~0','shape':SCH[section_start:],'BBox':{'x':10,'y':30,'width':2140,'height':max(heights)-30},'colors':{}}})

sch={'editorVersion':'6.5.54','docType':'5','title':'EC01 REV0.1 ESQUEMATICO','description':'Sete folhas; sem simulacao e sem PCB. Consultar LEIA_ME.','colors':{},'schematics':sheets}
(OUT/'EC01_esquematico_easyeda.json').write_text(json.dumps(sch,ensure_ascii=False,indent=2),encoding='utf-8')

# Electrical source and supporting registers only. No PCB, fabrication or simulation output.
(OUT/'EC01_conexoes.json').write_text(json.dumps(COMPS,ensure_ascii=False,indent=2),encoding='utf-8')
with (OUT/'EC01_BOM_preliminar.csv').open('w',encoding='utf-8-sig',newline='') as f:
 wr=csv.writer(f,delimiter=';');wr.writerow(['Referencia','Valor ou MPN','Encapsulamento proposto','Montar base OneWire','Quantidade','Observacoes'])
 for c in COMPS:wr.writerow([c['ref'],c['value'],c['package'],c['fit'],1,c['note']])
with (OUT/'EC01_lista_de_redes.csv').open('w',encoding='utf-8-sig',newline='') as f:
 wr=csv.writer(f,delimiter=';');wr.writerow(['Referencia','Pino','Nome','Rede'])
 for c in COMPS:
  for n,(name,net) in c['pins'].items():wr.writerow([c['ref'],n,name,net or 'NC'])

# Render a readable SVG of each functional sheet, from the same symbols and pin data.
def svgtext(x,y,s,size=11,anchor='start',color='#173047'):
 return f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" text-anchor="{anchor}" fill="{color}">{html.escape(s)}</text>'
for sec,title in enumerate(SECTIONS):
 base=80;parts=[v for v in schematic_cells if v[0]['section']==sec]
 maxy=max(y+h for c,x,y,h in parts)-base+45
 svg=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2160 {maxy}" style="background:white">',svgtext(50,30,title,22),svgtext(50,51,'EC01 REV0.1 | Esquematico preliminar | Sem simulacao | DNP conforme tabela de montagem',13,color='#a04b12')]
 for c,x,y,h in parts:
  y=y-base+30;ps=list(c['pins'].items());two_pin=len(ps)==2 and c['ref'][0] in 'RCLF';w=80 if two_pin else 210
  svg.extend([svgtext(x+20,y-18,c['ref'],13,color='#a13125'),svgtext(x+20,y-4,c['value'],11)])
  if c['fit']=='NAO':svg.append(svgtext(x+20,y+7,'DNP',8,color='#ab571c'))
  if two_pin:
   if c['ref'].startswith('C'):
    svg.append(f'<path d="M{x+20} {y+25}h15 m0 -10v20 m10 -20v20 m0 -10h15" stroke="#802b20" fill="none"/>')
   else:svg.append(f'<rect x="{x+20}" y="{y+18}" width="40" height="14" fill="none" stroke="#802b20"/>')
  else:svg.append(f'<rect x="{x+20}" y="{y+10}" width="170" height="{h-10}" fill="#fffdf1" stroke="#802b20"/>')
  nl=1 if two_pin else (len(ps)+1)//2
  for k,(n,(name,net)) in enumerate(ps):
   right=k>=nl;px=x+w if right else x;py=y+25+(0 if two_pin else (k-nl if right else k)*20);dx=-20 if right else 20
   svg.append(f'<path d="M{px} {py}h{dx}" stroke="#802b20"/>')
   svg.append(svgtext(px+dx/2,py-3,n,8,'middle','#802b20'))
   if not two_pin:svg.append(svgtext(px+dx+(-3 if right else 3),py+3,name,9,'end' if right else 'start','#802b20'))
   if net:svg.append(svgtext(px+(4 if right else -4),py-4,net,10,'start' if right else 'end','#064c83'))
   else:svg.append(f'<path d="M{px-3} {py-3}l6 6 m-6 0l6 -6" stroke="#149443"/>')
 svg.append('</svg>')
 (OUT/f'EC01_folha_{sec+1:02d}.svg').write_text('\n'.join(svg),encoding='utf-8')

refs=[c['ref'] for c in COMPS];assert len(refs)==len(set(refs))
assert all(U2['pins'][str(i)][1] is None for i in range(19,25))
assert U2['pins']['1'][1]=='BLE_CHIP'
assert next(c for c in COMPS if c['ref']=='U3')['pins']['12'][1]=='GND'
assert next(c for c in COMPS if c['ref']=='U3')['pins']['15'][1]=='LORA_RST_N'
assert next(c for c in COMPS if c['ref']=='U3')['fit']=='SIM'
assert next(c for c in COMPS if c['ref']=='J4')['pins']['4'][1] is None
assert next(c for c in COMPS if c['ref']=='U1')['pins']['1'][1]=='PSU_EN'
nets=collections.defaultdict(list)
for c in COMPS:
 for n,(name,net) in c['pins'].items():
  if net:nets[net].append(c['ref']+'.'+n)
singletons={n:p for n,p in nets.items() if len(p)<2}
assert not singletons,singletons
audit=dict(status='ESQUEMATICO_PRELIMINAR_SEM_SIMULACAO',components=len(COMPS),nets=len(nets),native_shapes=len(SCH),single_node_nets=singletons,checks_passed=['Referencias unicas','Todos os pinos conectados tem rede com >=2 terminais','GPIO12-17 NC externos','LNA_IN em rede RF dedicada','E22 p12 GND e p15 NRST','LoRa montado na base','USB sem 5V para bateria','EN do buck-boost conectado ao divisor UVLO'],not_performed=['Simulacao PSpice cancelada pelo usuario','Testes fisicos','PCB e roteamento adiados','ERC nativo pendente','Validacao de RF'])
(OUT/'EC01_verificacao.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(audit,ensure_ascii=True))
raise SystemExit(0)

# Candidate land patterns. No routing: preserve truthful, auditable pre-layout.
# mm coordinates. Unknown mechanical parts only receive documentary envelopes, not pads.
def pads_for(c):
 p=c['package'];pads=[];w=h=2
 def pad(n,x,y,w,h,drill=0):pads.append((str(n),x,y,w,h,drill))
 if p in ['0201','0402','0603','0805','1206']:
  pitch,pw,ph,bw,bh={'0201':(.6,.35,.35,.6,.3),'0402':(1.0,.6,.65,1.0,.5),'0603':(1.6,.9,.95,1.6,.8),'0805':(2,1.05,1.45,2,1.25),'1206':(3,1.2,1.8,3.2,1.6)}[p]
  pad(1,-pitch/2,0,pw,ph);pad(2,pitch/2,0,pw,ph);w=bw;h=bh
 elif p in ['SOT23','SOT23_6']:
  w=1.3;h=2.9
  if p=='SOT23':
   for n,x,y in [(1,-1,-.95),(2,-1,.95),(3,1,0)]:pad(n,x,y,1,.6)
  else:
   for i in range(3):pad(i+1,-1,i*.95-.95,1,.6);pad(6-i,1,i*.95-.95,1,.6)
 elif p=='TSSOP16':
  w=4.4;h=5
  for i in range(8):pad(i+1,-2.9,(i-3.5)*.65,1.5,.4);pad(16-i,2.9,(i-3.5)*.65,1.5,.4)
 elif p=='SOIC8':
  w=3.9;h=4.9
  for i in range(4):pad(i+1,-2.7,(i-1.5)*1.27,1.5,.6);pad(8-i,2.7,(i-1.5)*1.27,1.5,.6)
 elif p=='QFN32_5X5_EP3_7':
  w=h=5
  for i in range(8):
   pad(1+i,-2.45,(i-3.5)*.5,.7,.25);pad(9+i,(i-3.5)*.5,2.45,.25,.7)
   pad(17+i,2.45,(3.5-i)*.5,.7,.25);pad(25+i,(3.5-i)*.5,-2.45,.25,.7)
  pad(33,0,0,3.7,3.7)
 elif p=='DLA10':
  w=2;h=3
  for i in range(5):pad(i+1,-.9,(i-2)*.5,.6,.25)
  for i in range(5):pad(10-i,.55 if i!=2 else .35,(i-2)*.5,.9 if i!=2 else 1.3,.25)
 elif p=='E22_900M22S':
  w=14;h=20
  for i in range(8):pad(12+i,-6.65,-7.6+i*1.27,1.5,.85);pad(11-i,6.65,-7.6+i*1.27,1.5,.85)
  for i in range(3):pad(20+i,-6.65,6.06+i*1.27,1.5,.85);pad(3-i,6.65,6.06+i*1.27,1.5,.85)
 elif p.startswith('HDR'):
  count=int(p[3:]);w=(count-1)*2.54+2.54;h=2.54
  for i in range(count):pad(i+1,(i-(count-1)/2)*2.54,0,1.8,1.8,1)
 elif p=='XTAL3225':
  w=3.2;h=2.5
  for n,x,y in [(1,-1.1,.85),(2,1.1,.85),(3,1.1,-.85),(4,-1.1,-.85)]:pad(n,x,y,1.2,1)
 elif p=='L4X4':
  w=h=4;pad(1,-1.6,0,1.2,3.2);pad(2,1.6,0,1.2,3.2)
 elif p=='UFL':
  w=3;h=3;pad(1,0,1.5,1,1.05);pad(2,-1.475,0,1.05,2.2);pad(3,1.475,0,1.05,2.2)
 elif p=='TP':w=h=1;pad(1,0,0,1,1)
 elif p=='PENDENTE_BH18650':w=80;h=23
 elif p=='PENDENTE_RJ11':w=h=16
 elif p=='PENDENTE_ANTENA':w=22;h=12
 else:raise ValueError(p)
 return pads,w,h

def unit(x):return round(x/.254,5)
def ptrk(points,layer=12,width=.15,net=''):
 return f'TRACK~{unit(width)}~{layer}~{net}~'+ ' '.join(str(unit(v)) for pt in points for v in pt)+f'~{gid()}'
def ptext(x,y,t,typ='L',layer=3,sz=1):
 return f'TEXT~{typ}~{unit(x)}~{unit(y)}~{unit(.12)}~0~~{layer}~~{unit(sz)}~{t}~~~{gid()}'
PCB=[ptrk([(0,0),(110,0),(110,75),(0,75),(0,0)],10,.1),ptext(3,73,'EC01 REV0.1 PRE-LAYOUT - SEM ROTEAMENTO',layer=12,sz=1.4)]
ALLPADS=[]
for c in COMPS:
 x,y=c['pos'];pads,w,h=pads_for(c);c['width']=w;c['height']=h;c['pad_count']=len(pads)
 body=[ptrk([(x-w/2,y-h/2),(x+w/2,y-h/2),(x+w/2,y+h/2),(x-w/2,y+h/2),(x-w/2,y-h/2)],12 if not pads else 3,.12),ptext(x-w/2,y-h/2-1,c['ref'],'P')]
 if not pads:body.append(ptext(x-w/2,y,c['package'],layer=12,sz=1))
 for n,px,py,pw,ph,drill in pads:
  assert n in c['pins'],(c['ref'],n)
  net=c['pins'][n][1] or '';xx=x+px;yy=y+py
  pts=' '.join(str(unit(v)) for pt in [(xx-pw/2,yy-ph/2),(xx+pw/2,yy-ph/2),(xx+pw/2,yy+ph/2),(xx-pw/2,yy+ph/2)] for v in pt)
  body.append(f'PAD~RECT~{unit(xx)}~{unit(yy)}~{unit(pw)}~{unit(ph)}~{11 if drill else 1}~{net}~{n}~{unit(drill/2)}~{pts}~0~{gid()}~0~~Y')
  ALLPADS.append(dict(ref=c['ref'],pin=n,x=xx,y=yy,w=pw,h=ph,net=net,drill=drill))
 attrs=f"package`{c['package']}`value`{c['value']}`BOM`{c['fit']}`"
 PCB.append(f"LIB~{unit(x)}~{unit(y)}~{attrs}~0~~{c['uid']}~1"+'#@$'+'#@$'.join(body))
layers=['1~TopLayer~#FF0000~true~true~true','2~BottomLayer~#0000FF~true~false~true','3~TopSilkLayer~#FFFF00~true~false~true','4~BottomSilkLayer~#808000~true~false~true','5~TopPasterLayer~#808080~false~false~false','6~BottomPasterLayer~#800000~false~false~false','7~TopSolderLayer~#800080~false~false~false','8~BottomSolderLayer~#AA00FF~false~false~false','9~Ratlines~#6464FF~true~false~true','10~BoardOutline~#FF00FF~true~false~true','11~Multi-Layer~#C0C0C0~true~false~true','12~Document~#FFFFFF~true~false~true','21~Inner1_GND~#800000~true~false~true','22~Inner2_PWR~#008000~true~false~true']
pcb={'head':'3~1.11.3~title`EC01 REV0.1 PRE-LAYOUT`','canvas':'CA~2400~2400~#000000~yes~#FFFFFF~1~1200~1200~line~0.5~mm~1~45~visible~0.5','shape':PCB,'layers':layers,'systemColor':'#000000~#FFFFFF~#FFFFFF~#000000~#FFFFFF','BBox':{'x':0,'y':0,'width':unit(110),'height':unit(75)},'preference':{'hideFootprints':'','hideNets':''},'DRCRULE':{'trackWidth':unit(.15),'track2Track':unit(.15),'pad2Pad':unit(.15),'track2Pad':unit(.15),'hole2Hole':unit(.25),'holeSize':unit(.3),'isRealtime':False}}
(OUT/'EC01_pre_layout_easyeda.json').write_text(json.dumps(pcb,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'EC01_conexoes.json').write_text(json.dumps(COMPS,ensure_ascii=False,indent=2),encoding='utf-8')
with (OUT/'EC01_BOM_preliminar.csv').open('w',encoding='utf-8-sig',newline='') as f:
 wr=csv.writer(f,delimiter=';');wr.writerow(['Referencia','Valor ou MPN','Encapsulamento proposto','Montar base OneWire','Quantidade','Observacoes'])
 for c in COMPS:wr.writerow([c['ref'],c['value'],c['package'],c['fit'],1,c['note']])
with (OUT/'EC01_lista_de_redes.csv').open('w',encoding='utf-8-sig',newline='') as f:
 wr=csv.writer(f,delimiter=';');wr.writerow(['Referencia','Pino','Nome','Rede'])
 for c in COMPS:
  for n,(name,net) in c['pins'].items():wr.writerow([c['ref'],n,name,net or 'NC'])

# Mechanical overview drawn from the actual component coordinates, no pretend traces.
esc=html.escape
svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -8 120 90" role="img" aria-label="Posicionamento preliminar da PCB EC01 110 por 75 milimetros">','<rect x="0" y="0" width="110" height="75" rx="1" fill="#143e34" stroke="#7cd5bc" stroke-width=".3"/>','<rect x="2" y="2" width="26" height="15" fill="#68471f" stroke="#ffd483" stroke-dasharray="1 1" stroke-width=".3"/>','<text x="3" y="5" font-size="1.7" fill="#fff2d6">BLE: RESERVA SEM COBRE</text>']
for c in COMPS:
 x,y=c['pos'];w=c['width'];h=c['height'];unknown=not c['pad_count'];color='#66523a' if unknown else '#202b33' if c['fit']=='SIM' else '#213d3b'
 svg.append(f'<g><title>{esc(c["ref"]+" "+c["value"]+" | "+c["note"])}</title><rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" fill="{color}" stroke="{ "#ffcd75" if unknown else "#9ca9a9"}" stroke-width=".12"/>')
 if len(c['pins'])>7 or unknown:
  svg.append(f'<text x="{x}" y="{y}" fill="#eef5ec" text-anchor="middle" font-family="Arial" font-size="{2 if unknown else 1.5}">{esc(c["ref"])}</text>')
 else:svg.append(f'<text x="{x-w/2}" y="{y-h/2-.4}" fill="#dbdca8" font-family="Arial" font-size="1.25">{c["ref"]}</text>')
 svg.append('</g>')
for p in ALLPADS:
 svg.append(f'<rect x="{p["x"]-p["w"]/2}" y="{p["y"]-p["h"]/2}" width="{p["w"]}" height="{p["h"]}" fill="#caad5c"/>')
 if p['drill']:svg.append(f'<circle cx="{p["x"]}" cy="{p["y"]}" r="{p["drill"]/2}" fill="#101f24"/>')
svg+=['<text x="55" y="-3" fill="#172c3e" text-anchor="middle" font-size="2.4" font-family="Arial">110 mm</text>','<text x="55" y="80" fill="#9a4e0b" text-anchor="middle" font-size="2.2" font-family="Arial">PRE-LAYOUT • sem trilhas • envelopes mecanicos pendentes</text>','</svg>']
(OUT/'EC01_posicionamento.svg').write_text('\n'.join(svg),encoding='utf-8')

# Independent audit of topology and completeness, not an EDA ERC/DRC substitute.
errors=[]
refs=[c['ref'] for c in COMPS]
assert len(refs)==len(set(refs))
mcu=next(c for c in COMPS if c['ref']=='U2')
assert all(mcu['pins'][str(n)][1] is None for n in range(19,25))
assert mcu['pins']['1'][1]=='BLE_CHIP'
assert next(c for c in COMPS if c['ref']=='U3')['pins']['12'][1]=='GND'
assert next(c for c in COMPS if c['ref']=='U3')['fit']=='SIM'
assert next(c for c in COMPS if c['ref']=='J4')['pins']['4'][1] is None
assert next(c for c in COMPS if c['ref']=='U1')['pins']['1'][1]=='PSU_EN'
assert all(0<p['x']<110 and 0<p['y']<75 for p in ALLPADS)
overlaps=[]
for i,a in enumerate(ALLPADS):
 for b in ALLPADS[i+1:]:
  if a['ref']==b['ref']:continue
  if abs(a['x']-b['x'])<(a['w']+b['w'])/2 and abs(a['y']-b['y'])<(a['h']+b['h'])/2:overlaps.append((a['ref'],a['pin'],b['ref'],b['pin']))
audit=dict(status='PRELIMINAR_NAO_FABRICAR',components=len(COMPS),pads=len(ALLPADS),copper_tracks=0,unverified_mechanical_parts=['BT1','RJ1','RJ2','ANT1'],pad_overlaps=overlaps,checks_passed=['GPIO12-17 externos NC','LNA_IN isolado da rede de alimentacao','E22 p12 GND e p15 NRST','LoRa sempre populado','USB sem ligacao de 5V a bateria','EN do buck-boost ligado ao divisor UVLO','Todos os pads gerados dentro do contorno'],not_performed=['ERC nativo','DRC nativo','Verificacao integral dos footprints e MPNs','Roteamento','Preenchimento de planos','Sintonia da antena BLE','Ensaios eletricos, RF e EMC'])
(OUT/'EC01_verificacao.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(audit,ensure_ascii=True))
