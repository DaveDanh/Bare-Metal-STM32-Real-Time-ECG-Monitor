# Bare-Metal STM32 Real-Time ECG Monitor 

## Overview
This project implements a real-time Electrocardiogram (ECG) monitoring system utilizing an **STM32G0B1RE** microcontroller and the **AD8232** ECG sensor (Nursing Eng Lab V1.0 board). 

Built entirely using **bare-metal C programming** (register-level, no HAL/LL libraries), the system emphasizes high-performance data acquisition through Hardware Timers and Direct Memory Access (DMA). The captured physiological data, along with real-time Leads-Off Detection (LOD) statuses, is transmitted via a custom UART packet protocol to a PC, where a Python-based Matplotlib dashboard renders the live waveforms.

## Dashboard Preview
*(Real-time plotting of PA0 analog signal and PA8/PA9 digital LOD states)*

## Key Features
* **Bare-Metal Implementation:** Direct manipulation of STM32 hardware registers for GPIO, RCC, ADC, TIM, DMA, and USART for maximum efficiency and execution speed.
* **DMA-Driven ADC:** ADC sampling is triggered autonomously by Hardware Timer 2 (TIM2) at a precise rate, with data transferred directly to memory via DMA (Channel 1) without CPU intervention.
* **Custom UART Protocol:** A robust 6-byte header packet structure ensures synchronized data transmission between the MCU and the PC.
* **Leads-Off Detection (LOD):** Real-time monitoring of electrode connectivity status (LOD+ and LOD-) to instantly alert users of loose or disconnected sensors.
* **Live Python Dashboard:** A multi-pane Matplotlib GUI that dynamically plots the ECG waveform and visually indicates the LOD states.

**Header (6 Bytes):**
* `Byte 0`: `0xF1` (Sync Byte 1)
* `Byte 1`: `0xF1` (Sync Byte 2)
* `Byte 2`: `Length LSB` (Buffer Size lower byte)
* `Byte 3`: `Length MSB` (Buffer Size upper byte)
* `Byte 4`: `LOD+ State` (0 = Normal, 1 = Leads Off)
* `Byte 5`: `LOD- State` (0 = Normal, 1 = Leads Off)
