# EC01 — entrada do projeto

Transferido para este computador em 04/10/2026 e movido, a pedido do usuário, para `C:/Users/User/OneDrive/Documents/GitHub/KiCad/Empresa-EcoQuali/EC01`.

Na mudança de pasta, os 72 arquivos foram conferidos por tamanho e SHA-256, sem divergências. Este guia foi atualizado depois dessa conferência para registrar o novo local.

## Abrir o projeto

No KiCad, abra [EC01.kicad_pro](outputs/EC01_KiCad_REV0_2/KiCad/EC01.kicad_pro).
Mantenha juntas todas as folhas e a biblioteca dessa pasta.

O [resumo de continuidade](RESUMO_EC01.md) registra o contexto recebido do notebook, as decisões e as pendências. Ele não contém o histórico integral da conversa original. Recomendações e próximos passos descritos nele são contexto para planejamento, não execução automática de novas etapas de engenharia.

## Organização preservada

- `outputs/EC01_KiCad_REV0_2/`: esquemático atual, biblioteca e exportações existentes.
- `outputs/EC01_ESQUEMATICO_REV0_1/`: revisão anterior e dados usados pelos geradores.
- `referencias/`: especificação original.
- `work/`: scripts e referências técnicas recebidos.
- `INVENTARIO_EC01.csv`: relação dos arquivos originais e seus hashes SHA-256.

A estrutura interna foi mantida para preservar caminhos relativos e dependências dos scripts. Os originais em Downloads permanecem intactos.

## Conferência da transferência

O ZIP contém 71 arquivos. Os 68 arquivos relacionados no inventário foram conferidos por tamanho e SHA-256 antes da extração e por SHA-256 após a extração, sem divergências. Resumo e inventário dentro do ZIP coincidem com os anexos avulsos. As sete folhas auxiliares existem; a biblioteca EC01 usa caminho relativo ao projeto.

SHA-256 do ZIP recebido: `45de7165bb3904f02443dd95bcdaa832311cc69ef92eb62df710157f5b7ae43a`.

Há instalações do KiCad nas pastas 9.0 e 10.0 deste computador. A consulta de versão da instalação 10.0 encontrou restrição de escrita em `Documents/KiCad`; a versão exata e a abertura do projeto não foram validadas nesta transferência.

## Estado recebido

Existe um esquemático REV 0.2 com oito folhas. Não há PCB nem firmware do EC01 neste pacote. Segundo o resumo recebido, o PDF e a netlist precedem a última edição do esquemático; a BOM também requer revisão. Nenhum circuito foi alterado e nenhum gerador foi executado nesta transferência.

## Continuidade entre computadores

A pasta está dentro do OneDrive, mas a sincronização, a conta e a disponibilidade no notebook ainda não foram verificadas. O acesso remoto também não foi configurado.

O projeto agora está dentro do repositório local `C:/Users/User/OneDrive/Documents/GitHub/KiCad`, cujo remoto `origin` é `https://github.com/MurilloHorvath/KiCad.git`. Após a transferência, o Git identificou `Empresa-EcoQuali/EC01/` como arquivos novos, ainda não incluídos em commit. Esta operação não enviou arquivos ao GitHub; é necessário fazer commit e push para disponibilizar essa versão no remoto.

Antes de alternar de computador usando sincronização de arquivos, feche o projeto no primeiro e confirme o término da sincronização nos dois. Evite editar o mesmo projeto simultaneamente. O ZIP original é o ponto de recuperação desta transferência; ele não constitui um backup periódico.

Para escolher o fluxo definitivo, falta confirmar se o fixo poderá ficar ligado e conectado quando você estiver fora. O acesso remoto permite centralizar o ambiente no fixo; trabalhar com cópias locais requer combinar como registrar e transferir as alterações.

## Ordem dos esquemáticos — organização de 04/10/2026

Abra `EC01.kicad_pro`; a folha principal `EC01.kicad_sch` apresenta a arquitetura e os atalhos numerados para as folhas abaixo. A numeração indica a ordem de leitura dos blocos, não uma classificação de risco elétrico.

| Ordem | Arquivo | Conteúdo |
|---|---|---|
| Principal | `EC01.kicad_sch` | Arquitetura e navegação |
| 01 | `01_Alimentacao_Bateria.kicad_sch` | Bateria e alimentação |
| 02 | `02_ESP32_Inicializacao.kicad_sch` | Microcontrolador, reset e boot |
| 03 | `03_BLE_Cristal.kicad_sch` | BLE e cristal |
| 04 | `04_LoRa_915MHz.kicad_sch` | Rádio LoRa |
| 05 | `05_Expansao_Display.kicad_sch` | Expansão e display |
| 06 | `06_Sensores_CAN.kicad_sch` | Sensores externos e CAN |
| 07 | `07_USB_Servico.kicad_sch` | USB de serviço |

Os arquivos estão em `outputs/EC01_KiCad_REV0_2/KiCad/`. Os nomes das folhas na hierarquia receberam os mesmos prefixos. A ordem e os números de página existentes foram mantidos: arquitetura na página 1 e blocos 01–07 nas páginas 2–8.

As folhas de circuito foram somente renomeadas, com conteúdo preservado. O gerador `work/build_kicad.py` foi ajustado para usar esses nomes e não foi executado. O resumo, inventário e exportações recebidos do notebook permanecem registros históricos e podem citar os nomes antigos. O inventário original serve para o pacote recebido, não para os nomes atuais. Há uma cópia anterior à organização em `work/organizacao_schematicos_antes_*.zip`.