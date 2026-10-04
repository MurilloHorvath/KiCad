# EC01 — revisão do método e dos circuitos

04/10/2026 · REV 0.2-R1 · revisão de esquemático; não é liberação para fabricação.

## Método observado e aplicado

Nas folhas 01 e 02, você substituiu componentes dispersos, ligados quase exclusivamente por rótulos globais, por circuitos visíveis: fios entre componentes próximos, capacitores ao lado da alimentação, resistores de polarização junto aos sinais e símbolos de GND. Essa direção melhora a leitura e facilita conferir o caminho da corrente.

O mesmo critério foi aplicado às folhas 03–07. O desenho foi dividido por função, mantendo os nomes e a hierarquia. Ligações internas próximas usam fios; conexões entre blocos da mesma folha podem usar rótulos locais; sinais que atravessam folhas usam rótulos globais. Rotacionar ou deslocar um componente exige conferir os pontos de conexão, pois um nome escrito no valor de um testpoint não nomeia sua rede.

As folhas 01 e 02 conservaram sua organização manual. Foram feitos reparos pontuais de conexão, ajuste de grade e espaçamento de resistores para acomodar os nomes dos sinais.

## Erros identificados nos arquivos recebidos

| Folha | Situação encontrada | Correção |
|---|---|---|
| 01 | R3 terminava em PSU_EN, mas o pino EN de U1 e R4 estavam em outra rede. EN ficava apenas com o caminho a GND por R4. | Reconectado o topo de R4 e EN a PSU_EN; preservados 200k/100k. |
| 01 | Saída PG e R5 não alcançavam o rótulo PSU_PG de TP5. | Restabelecida a rede PSU_PG. |
| 01 | BAT_SW aparecia no valor de TP3, mas o circuito havia perdido o nome da rede. | Reposto o rótulo de rede BAT_SW. |
| 01 | Pontos de C1/C2/R3 e alguns símbolos de terra fora da grade de conexão. | Alinhamento de componentes e fios correspondentes. |
| 02 | CHIP_EN não alcançava o botão RESET; BOOT_N não alcançava GPIO9. | Restabelecidas as duas redes. |
| 02 | GPIO2, GPIO4, GPIO8, GPIO10 e GPIO21 perderam, respectivamente, LORA_NSS, LORA_BUSY, I2C_INT_SCL, I2C_INT_SDA e DISP_CS. | Restabelecidos os rótulos nas redes corretas. |
| 02 | A saída de L2 e os pinos VDD3P3 não estavam unidos à rede 3V3_RF do PWR_FLAG. | Restabelecida a identificação da alimentação filtrada. |
| Projeto | GND dependia de uma biblioteca global não declarada no projeto. | Incluída a biblioteca padrão `power` na tabela do projeto via variável do KiCad 10. |

A inversão dos números IN/OUT da chave SPST SW1 foi preservada: para esse componente passivo de dois terminais, a orientação é eletricamente equivalente. A verificação considera essa equivalência explicitamente.

## Discussão das sugestões

### 1. Corrente de repouso e divisores

Sua conta está correta para 4,2 V e para os divisores originalmente pretendidos: 4,2/300k = 14 µA no EN e 4,2/200k = 21 µA no ADC, totalizando 35 µA. A 3,7 V, o total seria aproximadamente 30,8 µA. Isso se refere à chave geral ligada e não é o consumo total do equipamento.

**ADC:** 1M/1M reduziria a corrente a 2,1 µA a 4,2 V. Porém, a resistência de Thévenin passaria de 50k para 500k. Com 100nF, a constante de tempo passaria de 5ms para 50ms. Após um degrau, 250ms deixa cerca de 0,67% de erro de acomodação; 350ms, cerca de 0,09%, no modelo RC ideal. A espera não precisa necessariamente se repetir ao acordar se C5 continuar carregado. Fugas DC e perturbações de amostragens sucessivas ainda precisam de avaliação. Cada 10nA de fuga em 500k provoca 5mV no ADC, equivalentes a 10mV na bateria. C5 não elimina esse erro DC. **Mantidos 100k/100k nesta revisão; 1M/1M é uma opção a validar.**

**EN:** a TI especifica limiares nominais de 1,1V/1,0V e fuga de entrada de até 0,2µA. Para uma corrente de entrada I, o deslocamento do limiar referido à bateria tem magnitude I × R superior: aproximadamente 40mV com 200k e 400mV com 2M, além das tolerâncias. Por isso, 2M/1M economiza corrente, mas prejudica a precisão do corte. **Mantidos 200k/100k.** [TPS63802, características elétricas e habilitação](https://www.ti.com/lit/ds/symlink/tps63802.pdf).

Também entram no orçamento o consumo quiescente do regulador, o divisor de feedback, o rádio, o expansor, a proteção da célula e resistores que ficam polarizados em estados ativos. O divisor de FB sozinho consome aproximadamente 3,308/602k = 5,50µA na saída de 3,3V; esse valor não é diretamente igual à corrente da bateria.

### 2. Dependência do expansor

Concordo com a preocupação, mas nem toda falha I2C derruba o rádio imediatamente: o efeito depende dos estados já retidos nas saídas. O TCA9534A parte com portas como entradas e pode voltar ao estado inicial por ciclo de alimentação. Antes de habilitar saídas, o firmware deve escrever os estados seguros, configurar direções e só então iniciar rádio/display. Documentados timeout, tentativa de recuperação do barramento e tratamento de falha persistente. O componente não oferece um pino externo dedicado de reset; recuperação por software não garante resolver todo travamento. [TCA9534A](https://www.ti.com/lit/ds/symlink/tca9534a.pdf).

### 3. L2 e cristal

Sua observação procede: a recomendação inicial de **24nH é para um componente série no XTAL_P**. Foi acrescentado **L4=24nH TUNE** na folha 03, entre XTAL_P e o nó de Y1/C14. L2 foi marcado **FILTRO RF TBD >=500mA**, removendo a aparência de que 24nH já estivesse validado para a alimentação.

O guia também pede filtro LC para VDD3P3, mas a fonte consultada não sustenta fechar automaticamente L2 em 1,7nH. Esse valor e o MPN ficam pendentes. C14/C15 de 10pF dão CL=8pF somente se os parasitas equivalerem a aproximadamente 3pF; não é garantia de frequência ou partida. Valores do cristal e das redes RF continuam iniciais. [Guia de hardware ESP32-C3](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/schematic-checklist.html).

### 4. Homologação

A revisão não declara o EC01 nem o E22-900M22S homologados. A identificação exata do módulo e seu certificado/código precisam ser conferidos; um componente empregado no produto não comprova por si só a conformidade do conjunto. A definição dos ensaios e do enquadramento deve integrar a etapa de produto. Não foi realizada uma consulta conclusiva de certificado específico. [Portal de certificação da Anatel](https://www.gov.br/anatel/pt-br/regulado/certificacao-de-produtos).

### 5. Queda de VEXT

O alerta é pertinente, mas a queda não pode ser quantificada apenas por “PTC de 100mA”. Ihold não é uma resistência e depende das condições térmicas. É necessário escolher a peça, obter sua resistência máxima nas condições de uso e somar Q2, cabo e contatos. O DS18B20 exige pelo menos 3,0V em alimentação local. [DS18B20](https://www.analog.com/media/en/technical-documentation/data-sheets/ds18b20.pdf).

Como ilustração, com 3,308V ideais na origem, a margem até 3,0V é 308mV: a 100mA, toda a resistência de ida/retorno teria que ficar abaixo de 3,08Ω. Na prática, a margem será menor após tolerâncias e transientes. Essa conta não seleciona F2 e não substitui a medição no sensor. Q2 deve ser avaliado pelo RDS(on) garantido na tensão real de gate, não apenas pelo valor típico. [AO3401A](https://www.aosmd.com/sites/default/files/res/datasheets/AO3401A.pdf).

### 6. Footprints, proteção e PCB

Continuam pendentes os footprints, os MPNs em aberto, TVS compatíveis com CAN, pinagem mecânica dos RJ11 e escolha da saída de antena do rádio. A pinagem lógica dos símbolos próprios não comprova o footprint. A especificação de 50Ω refere-se à impedância da trilha e depende do empilhamento real da placa; não determina uma largura universal. Revisão manual de RF e retorno de terra permanece necessária. Não foram executados simulações nem testes físicos nesta revisão.

## Verificação entregue

- Exportação e análise com KiCad CLI 10.0.3, instalado neste computador.
- 107 componentes elétricos, incluindo L4 novo; 321 pinos em 63 redes conferidos por conjuntos de conexões.
- Comparação por conectividade, independentemente dos nomes automáticos de redes do KiCad.
- ERC final: **0 erros e 0 avisos**. Antes da revisão: 2 erros e 36 avisos no mesmo ambiente de conferência.
- As quatro regras já ignoradas foram mantidas: `single_global_label`, `four_way_junction`, `simulation_model_issue` e `footprint_filter`. Nenhuma nova regra foi silenciada.
- PDF de oito páginas exportado e inspecionado visualmente. Netlist, BOM preliminar e dados de conexões atualizados a partir dos esquemáticos revisados.
- Valores originais preservados, exceto L2 marcado como pendente; L4 adicionado como valor inicial para ajuste. Os dados refletem a revisão, não uma seleção final para compra.

O ERC e a comparação de redes verificam consistência estática, não desempenho elétrico, RF, fabricação ou certificação. A conectividade de referência provém do projeto anterior, com as correções descritas acima; não equivale a uma validação independente de todos os requisitos do produto.

## Continuidade

Os arquivos nativos KiCad editados são a fonte principal desta revisão. O antigo `work/build_kicad.py` gera o desenho anterior e pode sobrescrever suas alterações manuais: não o execute sobre a pasta de trabalho. O resumo e o inventário da transferência original permanecem históricos.

Abra `KiCad/EC01.kicad_pro`. Consulte `EC01_VALIDACAO_R1.json` para a conferência e o registro de aplicação para saber se esta cópia foi instalada na pasta original. Não foi feito commit nem push nesta revisão.
