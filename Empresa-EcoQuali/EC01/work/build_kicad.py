from pathlib import Path
import json,uuid,math,csv,collections,re,subprocess,os,shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs'/'EC01_KiCad_REV0_2';OUT.mkdir(exist_ok=True,parents=True)
PROJ=OUT/'KiCad';PROJ.mkdir(exist_ok=True)
COMPS=json.loads((ROOT/'outputs/EC01_ESQUEMATICO_REV0_1/EC01_conexoes.json').read_text(encoding='utf8'))
SECTIONS=['01_Alimentacao_Bateria','02_ESP32_Inicializacao','03_BLE_Cristal','04_LoRa_915MHz','05_Expansao_Display','06_Sensores_CAN','07_USB_Servico']
TITLES=['Alimentacao e bateria','ESP32 e inicializacao','BLE e cristal','Radio LoRa 915 MHz','Expansao e display','Sensores externos e CAN','USB de servico']
NOTES=[
 ['Celula 1S protegida e removivel. Sem carregador. USB nao alimenta o circuito.', 'TPS63802: 3,308 V nominal. EN: liga em ~3,30 V; desliga em ~3,00 V.', 'F1, F2, suporte e chave exigem selecao mecanica e coordenacao de protecao.'],
 ['GPIO12 a GPIO17 reservados a flash: NC externos. VDD_SPI somente desacoplado.', 'GPIO2 e GPIO8 altos no boot. GPIO9 baixo durante RESET para gravacao.', 'GPIO21 pode emitir UART no boot; display fica em reset ate configurar U4.'],
 ['LNA_IN isolado de 3V3. C16/L3/C17 sao valores iniciais para ajuste de RF.', 'ANT1 representa a IFA futura: geometria e casamento dependem da PCB e carcaca.', 'Cristal 40 MHz CL=8 pF: C14/C15=10 pF pressupoe ~3 pF de parasitas.'],
 ['E22-900M22S sempre montado. Manual 2026: p12=GND, p15=NRST.', 'Firmware: DIO2 controla TXEN; TCXO interno por DIO3 a 2,2 V. RXEN via U4.', 'Usar somente J1 ou o IPEX integrado; evitar derivacao RF em aberto na PCB.'],
 ['U4 TCA9534A: endereco I2C de 7 bits 0x38. Inicializa com portas em entrada.', 'Display SPI: R28/R29. Display I2C: R30/R31. Nunca montar ambos os pares.', 'J2/J3 DNP. Interface 3,3 V para MODULO; nao aciona painel e-paper diretamente.'],
 ['RJ1/RJ2 compartilham barramento. Pinagem LOGICA 1=VEXT 2=GND 3=A 4=B.', 'Base OneWire: R33/R34/R35 e U6/U7. I2C: acrescentar R36. Cabos a definir.', 'CAN: remover R33-R36 e U6/U7; montar U5/C24/R37-R41. TVS D2/D3 pendentes.', 'CAN usa um TWAI comum. 120R por R42/JP1 somente na extremidade fisica.', 'VEXT 3,3 V nominal; orcamento 100 mA total. PTC nao e limitador preciso.', 'Com VEXT desligada, colocar GPIO1/20 em alta impedancia para evitar realimentacao.'],
 ['J4 e header de servico, nao USB-C. Pino 4 NC. Nunca conectar 5 V a 3V3.', 'Gravar com bateria ligada. D-/D+ por R43/R44 e ESD U8.', 'USB Serial/JTAG nativo: GPIO18 D- e GPIO19 D+. Verificar cabo e polaridade.']]
def U(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'EC01-REV02-'+s))
def q(s):return json.dumps(str(s),ensure_ascii=False)
def f(n):return f'{n:.4f}'.rstrip('0').rstrip('.') if n else '0'
def fx(sz=1.27,justify='',hide=False):return f'(effects (font (size {sz} {sz}))'+(f' (justify {justify})' if justify else '')+(' (hide yes)' if hide else '')+')'
def prop(k,v,x=0,y=0,hide=False,size=1.27):return f'(property {q(k)} {q(v)} (at {f(x)} {f(y)} 0) {fx(size,hide=hide)})'
def text(s,x,y,size=1.27):return f'(text {q(s)} (at {f(x)} {f(y)} 0) {fx(size,"left")} (uuid {q(U(s+str(x)+str(y)))}) )'
ST='(stroke (width 0.254) (type default)) (fill (type none))'
def line(points):return '(polyline (pts '+' '.join(f'(xy {f(x)} {f(y)})' for x,y in points)+') '+ST+')'
def rect(x1,y1,x2,y2):return f'(rectangle (start {f(x1)} {f(y1)}) (end {f(x2)} {f(y2)}) {ST})'
def pin_type(c,n,name):
 r=c['ref'];n=int(n)
 if r=='U1':return {1:'input',2:'input',3:'power_in',4:'input',5:'open_collector',6:'power_out',7:'passive',8:'power_in',9:'passive',10:'power_in'}[n]
 if r=='U2':
  if n in [2,3,11,17,31,32,33]:return 'power_in'
  if n==18:return 'power_out'
  if n==7:return 'input'
  if 19<=n<=24:return 'no_connect'
  return 'bidirectional' if n not in [1,29,30] else 'passive'
 if r=='U3':
  if name in ['GND','VCC']:return 'power_in'
  return 'output' if name in ['DIO1','DIO2','BUSY','MISO'] else ('passive' if name=='ANT' else 'input')
 if r=='U4':
  if n in [8,16]:return 'power_in'
  if n==13:return 'open_collector'
  if n in [1,2,3,14]:return 'input'
  return 'bidirectional'
 if r=='U5':return {1:'input',2:'power_in',3:'power_in',4:'output',5:'input',6:'bidirectional',7:'bidirectional',8:'input'}[n]
 return 'passive'

# Logical schematic only: no unverified package name is a PCB footprint assignment.
for c in COMPS:
 c['note']=c['note'].replace('pre-layout','esquematico').replace('Envelope reservado 80x23 mm; NAO e footprint verificado. ','')
 if c['ref']=='BT1':c['note']='Celula 18650 1S protegida, removivel; confirmar comprimento e compatibilidade com suporte antes de escolher MPN final.'
 if c['ref']=='ANT1':c['note']='Representacao funcional de IFA impressa; geometria, feed e short dependem da PCB e carcaca futuras.'

ROOT_ID=U('root');SHEET_IDS=[U('sheet'+str(i)) for i in range(7)]
def make_lib(c):
 ref=c['ref'];name='EC01_'+ref;ps=list(c['pins'].items());tw=len(ps)==2 and (ref[0] in 'RCLF' or ref in ['BT1','SW1','SW2','SW3','D1'])
 pins=[];graphics=[]
 if tw:
  xx=7.62;hh=2.54
  pins=[(ps[0][0],ps[0][1],-xx,0,0),(ps[1][0],ps[1][1],xx,0,180)]
  if ref[0]=='C':graphics=[line([(-2.54,-2.54),(-2.54,2.54)]),line([(2.54,-2.54),(2.54,2.54)]),line([(-5.08,0),(-2.54,0)]),line([(2.54,0),(5.08,0)])]
  elif ref[0]=='L':
   for a in [-5.08,-2.54,0,2.54]:graphics.append(f'(arc (start {f(a)} 0) (mid {f(a+1.27)} 1.27) (end {f(a+2.54)} 0) {ST})')
  elif ref.startswith('SW'):
   graphics=[line([(-5.08,0),(-2.54,0)]),line([(2.54,0),(5.08,0)]),line([(-2.54,0),(2.54,2.54)])]
   for a in [-2.54,2.54]:graphics.append(f'(circle (center {f(a)} 0) (radius 0.5) {ST})')
   if ref!='SW1':graphics.append(line([(0,1.27),(0,3.81),(-1.27,3.81),(1.27,3.81)]))
  elif ref=='BT1':
   graphics=[line([(-5.08,0),(-1.27,0)]),line([(1.27,0),(5.08,0)]),line([(-1.27,-3.81),(-1.27,3.81)]),line([(1.27,-1.905),(1.27,1.905)])]
   hh=3.81
  elif ref=='D1':
   graphics=[line([(-5.08,0),(-2.54,0)]),line([(2.54,0),(5.08,0)]),line([(-2.54,-2.54),(-2.54,2.54),(2.54,0),(-2.54,-2.54)]),line([(2.54,-2.54),(2.54,2.54)]),line([(0,3.81),(2.54,6.35),(1.27,6.35)]),line([(2.54,3.81),(5.08,6.35),(3.81,6.35)])]
   hh=6.35
  else:
   graphics=[rect(-5.08,-1.27,5.08,1.27)]
   if ref[0]=='F':graphics.append(line([(-5.08,0),(5.08,0)]))
 elif ref.startswith('TP'):
  xx=0;hh=2.54;pins=[(ps[0][0],ps[0][1],0,0,90)]
  graphics=[line([(0,2.54),(0,3.81)]),f'(circle (center 0 5.08) (radius 1.27) {ST})']
 else:
  xx=33.02 if ref=='U2' else 25.4
  nl=(len(ps)+1)//2;hh=max(5.08,(nl-1)*1.905+3.81)
  graphics=[rect(-xx+2.54,hh,xx-2.54,-hh)]
  for i,(n,p) in enumerate(ps):
   right=i>=nl;j=i-nl if right else i
   yy=(nl-1)*1.905-j*3.81
   pins.append((n,p,xx if right else -xx,yy,180 if right else 0))
 # Custom component symbols carry explicit pin names and numbers, including MOSFET G/S/D.
 pre=''.join(x for x in ref if x.isalpha())
 body=f'(symbol {q(name)} (pin_names (offset 0.635)'+(' (hide yes)' if tw else '')+') (in_bom yes) (on_board yes) '
 body+=prop('Reference',pre,0,hh+3.81)+prop('Value',c['value'],0,hh+1.27)+prop('Footprint','',hide=True)+prop('Datasheet','',hide=True)
 body+=f'(symbol {q(name+"_0_1")} '+''.join(graphics)+')'
 body+=f'(symbol {q(name+"_1_1")} '
 for n,(pn,net),x,y,a in pins:
  body+=f'(pin {pin_type(c,n,pn)} line (at {f(x)} {f(y)} {a}) (length 2.54) (name {q(pn)} {fx(1.016)}) (number {q(n)} {fx(1.016)}))'
 return body+'))',pins,hh,xx

LIBS={c['ref']:make_lib(c) for c in COMPS}
FLAG='(symbol "EC01_PWR_FLAG" (power) (pin_names (offset 0) (hide yes)) (in_bom no) (on_board no) '+prop('Reference','#FLG',hide=True)+prop('Value','PWR_FLAG',0,3.81)+'(symbol "EC01_PWR_FLAG_0_1" '+line([(0,0),(0,1.27),(-1.27,2.54),(0,3.81),(1.27,2.54),(0,1.27)])+')(symbol "EC01_PWR_FLAG_1_1" (pin power_out line (at 0 0 90) (length 0) (name "pwr" '+fx()+') (number "1" '+fx()+'))))'
def header(uid,title):return f'(kicad_sch (version 20250114) (generator "ec01_engineering") (uuid {q(uid)}) (paper "A3") (title_block (title {q("EC01 Sensor Universal - "+title)}) (date "2026-10-04") (rev "0.2") (comment 1 "ESQUEMATICO PRELIMINAR - SEM SIMULACAO - SEM PCB") (comment 2 "Footprints e partes TBD ainda nao liberados"))'
def glabel(net,x,y,ang,key):
 return f'(global_label {q(net)} (shape bidirectional) (at {f(x)} {f(y)} {ang}) {fx(1.016,"left" if ang==0 else "right")} (uuid {q(U(key))}) '+prop('Intersheetrefs','${INTERSHEET_REFS}',x,y,True)+')'
def wire(x1,y1,x2,y2,key):return f'(wire (pts (xy {f(x1)} {f(y1)}) (xy {f(x2)} {f(y2)})) (stroke (width 0) (type default)) (uuid {q(U(key))}))'

for sec,title in enumerate(TITLES):
 cs=[c for c in COMPS if c['section']==sec];body=header(U('file'+str(sec)),title)
 body+='(lib_symbols '+''.join(LIBS[c['ref']][0].replace('(symbol "EC01_','(symbol "EC01:EC01_',1) for c in cs)+(FLAG.replace('(symbol "EC01_PWR_FLAG"','(symbol "EC01:EC01_PWR_FLAG"',1) if sec in [0,1] else '')+')'
 body+=text(f'{sec+1:02d}  {title.upper()}',15,15,2.54)
 heights=[35.56]*3
 for c in sorted(cs,key=lambda x:-len(x['pins'])):
  lib,pins,hh,xx=LIBS[c['ref']];col=min(range(3),key=lambda i:heights[i]);x=71.12+col*129.54;y=heights[col]+hh+5.08
  heights[col]=y+hh+10.16
  ref=c['ref'];dnp=c['fit']=='NAO'
  body+=f'(symbol (lib_id {q("EC01:EC01_"+ref)}) (at {f(x)} {f(y)} 0) (unit 1) (in_bom yes) (on_board yes) (dnp {"yes" if dnp else "no"}) (uuid {q(U(ref))})'
  body+=prop('Reference',ref,x,y-hh-5.08)+prop('Value',c['value'],x,y-hh-2.54,size=1.016)+prop('Footprint','',x,y,True)+prop('Datasheet','',x,y,True)
  body+=prop('Encapsulamento_proposto',c['package'],x,y,True)+prop('Decisao',c['note'],x,y,True)+prop('Montagem_base','DNP' if dnp else 'SIM',x,y,True)
  for n,p,px,py,a in pins:body+=f'(pin {q(n)} (uuid {q(U(ref+"-pin-"+n))}))'
  body+=f'(instances (project "EC01" (path {q("/"+ROOT_ID+"/"+SHEET_IDS[sec])} (reference {q(ref)}) (unit 1)))))'
  for n,(pn,net),px,py,a in pins:
   ax=x+px;ay=y-py
   if not net:body+=f'(no_connect (at {f(ax)} {f(ay)}) (uuid {q(U(ref+"-nc-"+n))}))'
   else:
    ex=ax+(-5.08 if px<0 else 5.08)
    body+=wire(ax,ay,ex,ay,ref+'-w-'+n)+glabel(net,ex,ay,180 if px<0 else 0,ref+'-label-'+n)
 note_y=max(heights)+2.54
 assert note_y+len(NOTES[sec])*4.5<264,(sec,note_y)
 for i,n in enumerate(NOTES[sec]):body+=text(n,15,note_y+i*4.5,1.27)
 if sec in [0,1]:
  for i,net in enumerate(['BAT_SW','GND'] if sec==0 else ['3V3_RF']):
   x=40.64+i*50.8;y=round((note_y+22)/1.27)*1.27;ref='#FLG'+str(sec*2+i+1)
   body+=f'(symbol (lib_id "EC01:EC01_PWR_FLAG") (at {x} {f(y)} 0) (unit 1) (in_bom no) (on_board no) (dnp no) (uuid {q(U(ref))})'+prop('Reference',ref,x,y,True)+prop('Value','PWR_FLAG',x,y-5.08,size=1.016)+f'(pin "1" (uuid {q(U(ref+"pin"))}))(instances (project "EC01" (path {q("/"+ROOT_ID+"/"+SHEET_IDS[sec])} (reference {q(ref)}) (unit 1)))))'
   body+=wire(x,y,x+5.08,y,ref+'wire')+glabel(net,x+5.08,y,0,ref+'net')
 body+='(embedded_fonts no))'
 (PROJ/(SECTIONS[sec]+'.kicad_sch')).write_text(body,encoding='utf8')

body=header(ROOT_ID,'Arquitetura e navegacao')+'(lib_symbols)'
body+=text('EC01 SENSOR UNIVERSAL',20,20,4)+text('Esquematico nativo KiCad | REV 0.2 | 04 outubro 2026',20,29,2)
body+=text('Duplo clique em cada folha para abrir o circuito. Redes com o mesmo nome sao globais.',20,38,1.524)
for i,title in enumerate(TITLES):
 x=25+(i%3)*127;y=60+(i//3)*52
 body+=f'(sheet (at {x} {y}) (size 105 32) (stroke (width 0.254) (type solid)) (fill (color 0 0 0 0)) (uuid {q(SHEET_IDS[i])}) '
 body+=prop('Sheetname',f'{i+1:02d} - {title}',x+52.5,y+9)+prop('Sheetfile',SECTIONS[i]+'.kicad_sch',x+52.5,y+23,size=1.016)
 body+=f'(instances (project "EC01" (path {q("/"+ROOT_ID)} (page {q(str(i+2))})))))'
for j,t in enumerate(['BASE: 1S protegida -> buck-boost 3V3 -> ESP32-C3FH4 + E22-900M22S + sensores.', 'RJ1/RJ2 sao um barramento comum. CAN exige alteracao de montagem; nao basta firmware.', 'DNP = nao montar na base OneWire. Conectores e TVS TBD exigem selecao antes da PCB.', 'Simulacoes PSpice e testes fisicos cancelados por solicitacao do cliente.', 'Este projeto nao inclui PCB, antena final, firmware ou liberacao para fabricacao.', 'Consultar EC01_Documento_de_Engenharia.pdf e BOM para decisoes, limites e pendencias.']):body+=text(t,20,218+j*5,1.524)
body+='(sheet_instances (path "/" (page "1"))) (embedded_fonts no))'
(PROJ/'EC01.kicad_sch').write_text(body,encoding='utf8')
(PROJ/'EC01.kicad_pro').write_text(json.dumps({'meta':{'filename':'EC01.kicad_pro','version':1}},indent=2))
(PROJ/'EC01.kicad_sym').write_text('(kicad_symbol_lib (version 20250114) (generator "ec01_engineering") '+''.join(v[0] for v in LIBS.values())+FLAG+')',encoding='utf8')
(PROJ/'sym-lib-table').write_text('(sym_lib_table (version 7) (lib (name "EC01") (type "KiCad") (uri "${KIPRJMOD}/EC01.kicad_sym") (options "") (descr "Simbolos EC01 revisados por pinagem; footprints ainda nao atribuidos")))',encoding='utf8')
(OUT/'EC01_conexoes.json').write_text(json.dumps(COMPS,ensure_ascii=False,indent=2),encoding='utf8')
for fn in ['EC01_BOM_preliminar.csv','EC01_lista_de_redes.csv']:shutil.copy2(ROOT/'outputs/EC01_ESQUEMATICO_REV0_1'/fn,OUT/fn)
print(f'{len(COMPS)} componentes; 8 folhas KiCad criadas em {PROJ}')

