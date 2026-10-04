# EC01 Sensor Universal — Resumo para continuidade

Registro de 04 de outubro de 2026. Este arquivo descreve o estado encontrado no disco nesta conversa. É um resumo de transferência, não o relatório completo de engenharia nem uma liberação para fabricação.

## Onde retomar

O trabalho mais recente é o **esquemático KiCad REV 0.2**, com oito folhas, 106 componentes lógicos e três símbolos de indicação de alimentação para o ERC. Abra `outputs/EC01_KiCad_REV0_2/KiCad/EC01.kicad_pro` após extrair o pacote inteiro. O arquivo principal do circuito é `EC01.kicad_sch`, na mesma pasta.

Pasta original da conversa:

`C:\Users\Skydrones\Documents\Codex\2026-10-03\pro`

Todos os caminhos relativos abaixo partem dessa pasta, ou da raiz do ZIP depois de extraído. Nenhum original foi movido, excluído ou regravado nesta organização. O pacote é uma cópia do estado atual, não uma sincronização entre computadores.

## Objetivo e escopo autorizado

Desenvolver o EC01 como nó sensor alimentado por uma célula 18650, com ESP32-C3FH4, BLE, LoRa em 915 MHz, dois conectores RJ11 de sensores, leitura de bateria, programação por USB nativo e reserva para display. A especificação original é uma fonte de requisitos a revisar; suas recomendações não equivalem a decisões técnicas validadas.

O pedido começou com EasyEDA e PCB. Posteriormente foram solicitadas simulações em PSpice antes da PCB; em seguida, o usuário cancelou os testes e simulações por enquanto e limitou o escopo ao esquemático. A decisão mais recente é usar **KiCad** e documentar as decisões em um documento de engenharia. As dimensões da placa continuam livres. O pedido atual é organizar os arquivos para continuar também no computador fixo.

## Inventário principal e caminhos

| Item | Caminho relativo | Uso e estado |
|---|---|---|
| Projeto KiCad | `outputs/EC01_KiCad_REV0_2/KiCad/EC01.kicad_pro` | Ponto de entrada; configuração de projeto mínima |
| Esquemático raiz | `outputs/EC01_KiCad_REV0_2/KiCad/EC01.kicad_sch` | Navegação para sete folhas de circuito |
| Folhas | `Alimentacao.kicad_sch`, `ESP32.kicad_sch`, `BLE_e_cristal.kicad_sch`, `LoRa.kicad_sch`, `Expansao_e_display.kicad_sch`, `Sensores_e_CAN.kicad_sch`, `USB_servico.kicad_sch` | Todas na mesma pasta `KiCad`; copiar juntas |
| Biblioteca local | `outputs/EC01_KiCad_REV0_2/KiCad/EC01.kicad_sym` | Símbolos específicos do projeto |
| Tabela de bibliotecas | `outputs/EC01_KiCad_REV0_2/KiCad/sym-lib-table` | Aponta para `${KIPRJMOD}/EC01.kicad_sym` |
| Preferências locais | `outputs/EC01_KiCad_REV0_2/KiCad/EC01.kicad_prl` | Estado local do editor; não é requisito elétrico |
| PDF existente | `outputs/EC01_KiCad_REV0_2/EC01_Esquematico.pdf` | Exportação anterior à última alteração dos símbolos |
| ERC mais recente | `outputs/EC01_KiCad_REV0_2/EC01_ERC.json` | KiCad 10.0.6; 0 violações registradas; ver limites abaixo |
| Netlist exportada | `outputs/EC01_KiCad_REV0_2/EC01_netlist.xml` | Exportação anterior à última edição; regenerar |
| BOM preliminar | `outputs/EC01_KiCad_REV0_2/EC01_BOM_preliminar.csv` | Valores, opções de montagem e peças pendentes; copiada da REV 0.1 |
| Dados de conexão | `outputs/EC01_KiCad_REV0_2/EC01_conexoes.json` | Representação de 106 componentes gerada pelo script |
| Lista de redes | `outputs/EC01_KiCad_REV0_2/EC01_lista_de_redes.csv` | Registro de pinos e redes copiado da REV 0.1 |
| Gerador KiCad | `work/build_kicad.py` | Código Python; lê dados da revisão EasyEDA e escreve a REV 0.2 |
| Gerador inicial | `work/build_ec01.py` | Gera os arquivos EasyEDA e dados elétricos intermediários |
| Revisão anterior | `outputs/EC01_ESQUEMATICO_REV0_1/` | JSON EasyEDA, SVGs por seção, BOM, redes e verificação inicial |
| Especificação extraída | `work/spec.txt` | Texto extraído do documento fornecido pelo usuário |

Especificação original, fora da pasta da conversa:

`C:\Users\Skydrones\Downloads\EC01 - Sensor Universal — Especificação de Projeto.docx`

Uma cópia está incluída em `referencias/` no ZIP. O inventário CSV registra o caminho absoluto original, o caminho no pacote, tamanho, data UTC e SHA-256 de cada arquivo. Não foi localizado firmware do EC01 (`.ino`, projeto ESP-IDF ou PlatformIO) na pasta desta conversa nem nos resultados pertinentes da busca em `Documents/Codex` e `Downloads`. O caminho convencional `C:/Users/Skydrones/Desktop` não existe neste ambiente. Essa busca não constitui uma varredura de todos os discos ou serviços em nuvem.

## Bibliotecas e dependências

| Finalidade | Necessário | Observação |
|---|---|---|
| Abrir e editar o projeto | KiCad 10, preferencialmente 10.0.6 para reproduzir o ambiente | Versão registrada no ERC; executável local em `C:/Program Files/KiCad/10.0/bin/kicad-cli.exe` |
| Resolver os símbolos | `EC01.kicad_sym` e `sym-lib-table` junto aos esquemas | Caminho relativo; símbolos também estão embutidos nas folhas |
| Abrir os PDFs | Leitor de PDF | Não exige Python ou PSpice |
| Consultar BOM e redes | Editor CSV ou planilha | UTF-8 com BOM; delimitador ponto e vírgula |
| Executar os dois geradores | Python 3 | Usam apenas biblioteca padrão; não há pacotes pip obrigatórios nos imports atuais |
| Entrada do gerador KiCad | `outputs/EC01_ESQUEMATICO_REV0_1/EC01_conexoes.json` e os dois CSVs dessa pasta | Dependência importante mesmo após migrar para KiCad |
| Exportar PDF, netlist e ERC | `kicad-cli` do KiCad | Não depende de EasyEDA nem de sua conta |
| Renderização auxiliar usada anteriormente | `pypdfium2`, e ferramentas de PDF do ambiente | Opcionais para inspeção por imagens; não são requisitos dos geradores nem do projeto |

O Python utilizado nesta máquina fica em `C:/Users/Skydrones/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`. Esse caminho é específico desta instalação e não precisa existir no computador fixo. Os scripts calculam a raiz com base no próprio arquivo; mantenha a estrutura `work/` e `outputs/` do pacote.

Não há footprints atribuídos, biblioteca `.pretty`, tabela `fp-lib-table`, modelos 3D, PCB `.kicad_pcb`, Gerbers ou projeto de firmware do EC01 nesse conjunto. As bibliotecas padrão de footprints do KiCad serão úteis na etapa futura de PCB, mas nenhum footprint foi liberado nesta revisão. Não foi detectada dependência de biblioteca global para os símbolos usados no esquemático atual.

PSpice não é necessário para continuar o escopo atual. Há material do fabricante em `work/pspice_vendor/` (modelo TPS63802, `.LIB`, `.OLB`, `.DSN`, `.OPJ` e perfis de exemplo); ele está preservado apenas como referência. Esses arquivos não são uma simulação executada do EC01. RadioLib foi sugerida para o futuro firmware, mas não há integração, dependência instalada ou versão fixada no projeto.

## Referências técnicas existentes

| Arquivo no pacote | Conteúdo |
|---|---|
| `work/esp.pdf` e `work/esp.txt` | Datasheet ESP32-C3 |
| `work/ebyte.pdf` e `work/ebyte.txt` | Manual E22-900M22S |
| `work/psu.pdf` e `work/psu.txt` | Datasheet TPS63802 |
| `work/io.pdf` e `work/io.txt` | Datasheet TCA9534A |
| `work/can.pdf` e `work/can.txt` | Datasheet família TCAN33x |
| `work/ebyte-pcb.zip` e imagens E22 | Arquivo e desenhos do fabricante; não são PCB do EC01 |
| `work/format*`, `work/schex`, `work/pcbex` | Referências de formato EasyEDA; `pcbex` é exemplo de formato |
| `work/pspice_vendor/` | Modelo e projeto de exemplo fornecidos pela TI, não executados |

## Decisões e propostas registradas no esquemático

As decisões de ferramenta e escopo acima vieram do usuário. As escolhas de circuito abaixo foram incorporadas como **propostas de engenharia preliminares** e ainda exigem revisão; não houve aprovação individual de cada alteração em relação à especificação.

| Tema | Escolha atual e justificativa | Pendência ou limite |
|---|---|---|
| MCU | ESP32-C3FH4 com flash interna | Pinos GPIO12–17 reservados à flash ficam NC externamente; não disponibilizam seis GPIOs adicionais |
| GPIOs escassos | TCA9534APWR no I2C interno, endereço de 7 bits 0x38 | Controles lentos via expansor; firmware e adaptação do controle do rádio não implementados |
| Alimentação | TPS63802DLAR buck-boost no lugar do LDO TLV75733 | Mantém possibilidade de 3,3 V quando a célula cai abaixo de 3,3 V; estabilidade, perdas e carga ainda não validadas |
| Tensão nominal | R1=511 kΩ e R2=91 kΩ, aproximadamente 3,308 V | Tolerâncias, transientes e dimensionamento completo ainda pendentes |
| Habilitação | Divisor 200 kΩ/100 kΩ no EN; limiares nominais ~3,30 V para ligar e ~3,00 V para desligar | Não substitui proteção da célula; conferir tolerâncias e partida com bateria descarregada |
| Bateria | Uma 18650 protegida, substituível, com chave geral, fusível e PMOS de inversão | Sem carregador; confirmar compatibilidade mecânica da célula protegida com o suporte |
| Medição da bateria | Divisor 100 kΩ/100 kΩ de 0,1% e 100 nF no ADC GPIO0 | Escala metade da tensão; consome ~21 µA a 4,2 V; calibração e tempo de aquisição pendentes |
| Reset e boot | EN com 10 kΩ/1 µF; botões RESET e BOOT GPIO9 | MPNs dos botões não escolhidos; preservar níveis de strapping |
| BLE | LNA_IN isolado da alimentação; CLC inicial 1,5 pF / 2,7 nH / 1,5 pF e reserva de casamento da antena | Valores iniciais, dependentes de ajuste de RF; IFA sem geometria de PCB definida |
| Cristal | 40 MHz, CL alvo 8 pF, capacitores iniciais 10 pF | MPN, ESR, tolerância total e parasitas ainda devem ser fechados |
| LoRa | E22-900M22S SX1262 montado em todas as unidades | Manual consultado: pino 12 GND e pino 15 NRST; confirmar revisão física adquirida |
| Controle LoRa | DIO2 ligado a TXEN; RXEN e reset via expansor; DIO1 e BUSY diretamente no MCU | Configuração do TCXO interno e sequência de controle devem ser implementadas no firmware |
| Antena LoRa | Reserva U.FL J1 | Escolher J1 ou IPEX do módulo, evitando ramal RF aberto; antena externa e carcaça pendentes |
| Sensores externos | RJ1/RJ2 no mesmo barramento, pinagem lógica 1 VEXT, 2 GND, 3 A, 4 B | Conferir numeração física do conector; não são duas portas independentes |
| Protocolos | Base OneWire; I2C com pull-up adicional; SPI reduzido apenas para sensores compatíveis | Um protocolo por montagem/uso do barramento; SPI sem CS não é universal |
| CAN opcional | Um TCAN330 comum aos dois RJ11, associado ao único TWAI | Alteração de montagem obrigatória; remover rede digital/ESD incompatível, TVS CAN ainda TBD |
| Terminação CAN | 120 Ω por R42/JP1, opcional | Montar somente em extremidade física; não habilitar em toda unidade indiscriminadamente |
| Energia externa | VEXT comutado por PMOS/NMOS e PTC; orçamento preliminar de 100 mA total | PTC não limita precisamente a corrente; selecionar peça e evitar realimentação pelos GPIOs |
| Display | Header 8 vias DNP, seleção SPI ou I2C por pares de resistores 0 Ω mutuamente exclusivos | Módulo 3,3 V ainda não escolhido; não é acionamento direto de painel e-paper |
| Sensor interno | Header I2C DNP para expansão | SHT40/SHTC3 onboard não incorporado sem definição do requisito |
| LED | Controle ativo baixo pelo expansor | Consumo e cadência dependem do firmware |
| USB | Header de serviço GND/D−/D+/NC, resistores série de 22 Ω e ESD | Bateria deve estar ligada; não fornece 5 V, não carrega bateria e não é USB-C |
| PCB | Adiada | Dimensões, posicionamento, footprints, antenas e roteamento ainda não definidos |

### Mapeamento do MCU implementado

| GPIO | Rede ou função |
|---|---|
| 0 | BAT_ADC |
| 1 | PORT_A_IO |
| 2 | LORA_NSS, pull-up de boot |
| 3 | LORA_DIO1 |
| 4 | LORA_BUSY |
| 5 | SPI_MISO |
| 6 | SPI_SCK |
| 7 | SPI_MOSI |
| 8 | I2C_INT_SCL, manter alto durante boot |
| 9 | BOOT_N |
| 10 | I2C_INT_SDA |
| 18 e 19 | USB D− e D+ |
| 20 | PORT_B_IO |
| 21 | DISP_CS; display mantido em reset durante boot |

O VDD_SPI é desacoplado e não é GPIO de aplicação. Os GPIO12–17 não são utilizados externamente.

## Estado real e limitações

1. Os arquivos nativos KiCad foram gerados e o KiCad 10.0.6 conseguiu exportar o circuito. O relatório ERC existente, datado internamente `2026-10-04T13:44:44` (sem fuso registrado), contém **zero violações** nas regras executadas. Isso não comprova funcionamento, dimensionamento, conformidade RF ou adequação à fabricação.
2. O ERC lista como ignoradas as verificações `single_global_label`, `four_way_junction`, `simulation_model_issue` e `footprint_filter`. Há símbolos funcionais próprios e três PWR_FLAG para declarar fontes de alimentação através de elementos passivos; esses indicadores não simulam as fontes. A revisão independente da pinagem e das escolhas elétricas permanece necessária.
3. **PDF e netlist existentes são anteriores à última gravação dos esquemas.** Foram preservados como encontrados e não devem ser apresentados como exportações da revisão final. Regenerá-los a partir dos `.kicad_sch` é o primeiro passo técnico.
4. A BOM e o CSV de redes na pasta KiCad foram copiados da REV 0.1. Revisar sua correspondência com o projeto atual antes de compras ou qualquer montagem; há notas históricas e MPNs/encapsulamentos indefinidos.
5. O documento completo `EC01_Documento_de_Engenharia.pdf`, citado na folha raiz, **ainda não existe**. Essa referência é uma pendência; este resumo de continuidade não deve ser confundido com o relatório prometido.
6. A revisão visual de todas as folhas após a última alteração não foi concluída. O trabalho foi interrompido durante acabamento de símbolos e conferências. Não há testes físicos, simulações PSpice, firmware funcional, PCB ou liberação de fabricação.
7. A abertura/importação da revisão EasyEDA não foi concluída de forma verificável. Ela é mantida como histórico e como entrada dos geradores; o alvo atual é KiCad.

## Como continuar no computador fixo

1. Copiar o ZIP para o computador fixo e extrair todo o conteúdo em uma pasta de trabalho gravável. Não abrir o projeto diretamente dentro do ZIP.
2. Instalar ou usar KiCad 10.0.6, preservando `EC01.kicad_sym`, `sym-lib-table` e todas as folhas na pasta `KiCad`. Abrir `outputs/EC01_KiCad_REV0_2/KiCad/EC01.kicad_pro`.
3. Conferir a biblioteca local EC01. Seu caminho `${KIPRJMOD}/EC01.kicad_sym` acompanha a pasta, dispensando copiar as configurações pessoais desta máquina.
4. Ler este resumo e o inventário. Se continuar com outro assistente, fornecer o resumo e a especificação, pois o ZIP não transporta o histórico integral deste chat.
5. Escolher uma cópia de trabalho como principal e registrar revisões. O pacote não cria Git remoto, sincronização ou acesso ao computador fixo; evitar editar a mesma revisão em dois computadores sem reconciliar as mudanças.

### Regeneração por código

Os geradores **sobrescrevem** arquivos nas pastas de saída. Não são necessários para abrir o esquemático. Depois de editar manualmente no KiCad, executar um gerador pode perder essas alterações. Só os executar em uma cópia separada e com uma estratégia clara sobre qual arquivo é a fonte principal.

Fluxo atual: `work/build_ec01.py` → dados da REV 0.1 → `work/build_kicad.py` → arquivos KiCad REV 0.2. O gerador KiCad não lê o JSON de conexões da própria REV 0.2 como entrada. As datas, alguns textos de revisão e nomes de pastas estão fixados no código e devem ser atualizados em uma revisão futura.

O arquivo `build_ec01.py` contém um trecho antigo de geração de PCB **inativo depois de `raise SystemExit(0)`**. Não remover essa interrupção para “completar” a placa: esse trecho não representa trabalho de PCB autorizado ou validado na fase atual.

## Próximos passos técnicos

1. Regenerar PDF e netlist do estado atual; revisar visualmente as oito folhas e repetir ERC após qualquer modificação. Comparar a netlist do KiCad com a lista de conexões, sem tratar o ERC como validação funcional.
2. Definir se a manutenção continuará diretamente no KiCad ou nos geradores; eliminar a dependência histórica da REV 0.1 somente após reconciliar os dados e preservar uma revisão.
3. Concluir o documento de engenharia solicitado: rastreabilidade dos requisitos, justificativas, cálculos e tolerâncias, orçamento de corrente/consumo, variantes de montagem, interfaces e pendências. Atualizar a referência ao documento na folha raiz.
4. Fechar MPNs de cristal, indutor, fusíveis/PTC, TVS CAN, botões, suporte da célula e conectores; conferir pinagens físicas. Selecionar display e confirmar necessidade de sensor onboard.
5. Revisar partida e desligamento do buck-boost, strapping, comportamento do expansor no boot, controle de LoRa, alimentação dos sensores e limitações dos protocolos. Essas análises ainda não autorizam retomar simulações ou testes cancelados.
6. Somente após fechar o esquemático e receber orientação para avançar, iniciar a PCB: dimensões/carcaça, footprints, posicionamento de conectores e rádios, alimentação e plano de terra, RF e antenas. Sintonia RF e ensaios deverão ser planejados quando o escopo de testes for retomado.

## O que foi preservado no pacote

Incluídos: KiCad atual completo, exportações e relatórios existentes, revisão EasyEDA anterior, dois geradores Python, especificação original e extraída, datasheets e referências técnicas, modelo de fornecedor PSpice e inventário com hashes. A origem de cada arquivo é rastreável no CSV.

As pastas `work/kicad_config`, `work/kicad_user` e `work/kicad_qa` ficaram no computador original: são configurações locais e imagens intermediárias de inspeção, não dependências do circuito. Os executáveis do KiCad, runtimes Python/Node, caches do Codex e dados de conta não foram copiados. Nenhum original foi removido.
