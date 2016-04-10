#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
########################################################################
#
#  @file    ezvd.py
#  @authors chrono
#  @date    2016-02-26
#  @version 1.0
#
########################################################################
#  Copyright (c) 2016 Apollo-NG - https://apollo.open-resource.org/
########################################################################
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.
#
########################################################################

import sys, os, math, time, curses

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

def getInput(win, height, width, prompt, default):
    win = win.subwin(height,width,0,0)
    win.border(0)
    win.nodelay(0)
    win.clear()
    curses.curs_set(1)
    win.addstr(2, 3, prompt)
    curses.echo()
    try: uinput = win.getstr(2 + 2, 3, 20)
    except: pass
    curses.curs_set(0)
    curses.noecho()
    win.clear()
    if is_number(uinput):
        return uinput
    else:
        return default

def xterm_title(title):
  if not sys.stdout.isatty():
    return
  sys.stdout.write('\x1b]0;' +  title + '\a')

def screen_title(title):
  if not sys.stdout.isatty():
    return
  sys.stdout.write('\x1bk' + title + '\x1b\\')


def updateR1(win, height, width, R1):
    return getInput(win, height, width, "Enter Value of R1 in Ω", R1)

def updateR2(win, height, width, R2):
    return getInput(win, height, width, "Enter Value of R2 in Ω", R2)

def updateVINMax(win, height, width, VINMax):
    return getInput(win, height, width, "Enter the maximum Voltage you want to measure in V", VINMax)

def updateVRef(win, height, width, VRef):
    return getInput(win, height, width, "Enter your ADC's Voltage Reference in V", VRef)

def toggleRun(run):
    if run == True:
        state = False
    else:
        state = True
    return state

def main():

    ## Input Defaults ##################################################

    R1          = 56000.0
    R2          = 6980.0
    VINMax      = 45
    VRef        = 5.0

    ## Constraints #####################################################

    ADCZMax     = 10000   # Maximum Output Impedance towards ADC < 10k
    ADCResMin   = 0.01    # Minimum required ADC resolution in V

    try:
        try:
            mw = curses.initscr()
            height, width = mw.getmaxyx()

            if height <= 24 or width < 60:
                curses.endwin()
                sys.stdout.write("Your terminal is too small to draw on. Please resize")
                exit(1)

            curses.curs_set(0)
            curses.noecho()
            mw.keypad(1)
            mw.nodelay(1)

            # Define some colors
            try: curses.start_color()
            except: pass
            curses.use_default_colors()
            curses.init_pair(1,curses.COLOR_BLACK,-1)
            curses.init_pair(2,curses.COLOR_GREEN,-1)
            curses.init_pair(3,curses.COLOR_BLUE,-1)
            curses.init_pair(4,curses.COLOR_WHITE,curses.COLOR_RED)
            curses.init_pair(5,curses.COLOR_MAGENTA,-1)
            curses.init_pair(6,curses.COLOR_GREEN, -1)
            curses.init_pair(7,curses.COLOR_RED, -1)
            curses.init_pair(8,curses.COLOR_WHITE, -1)
            curses.init_pair(9,curses.COLOR_WHITE,-1 )
            col1=curses.color_pair(1)
            cgrn=curses.A_BOLD |curses.color_pair(2)
            cgri=curses.A_STANDOUT | curses.A_BOLD | curses.color_pair(6)
            cblu=curses.color_pair(3)
            cred=curses.color_pair(4)
            col5=curses.color_pair(5)
            bred=curses.color_pair(7)
            bwhi=curses.A_STANDOUT | curses.A_BOLD |curses.color_pair(9)


            VIN = 0
            SimDirection = "U"
            SimMode = 3 # 1=R1, 2=R2, 3=V
            SimRate = 0.01
            Run = True

            while 1:

                event = mw.getch()
                if event == ord("q"):
                    break
                elif event == ord("\t"):
                    SimMode = SimMode+1
                    if SimMode > 3:
                        SimMode = 1
                    if SimMode < 3 and SimRate < 1:
                        SimRate = 1
                    if SimMode == 3 and SimRate >= 1:
                        SimRate = 0.1
                elif event == curses.KEY_UP:
                    SimDirection = "U"
                    if Run == False:
                        if SimMode == 1:
                            R1=R1+SimRate
                        if SimMode == 2:
                            R2=R2+SimRate
                        if SimMode == 3:
                            VIN=VIN+SimRate
                elif event == curses.KEY_DOWN:
                    SimDirection = "D"
                    if Run == False:
                        if SimMode == 1:
                            R1=R1-SimRate
                        if SimMode == 2:
                            R2=R2-SimRate
                        if SimMode == 3:
                            VIN=VIN-SimRate
                elif event == ord("+"):
                    if SimMode == 1:
                        if (SimRate * 2) < (1024**3):
                            SimRate = SimRate * 2
                    if SimMode == 2:
                        if (SimRate * 2) < (1024**3):
                            SimRate = SimRate * 2
                    if SimMode == 3:
                        if (SimRate * 2) < (VINMax/4):
                            SimRate = SimRate * 2
                elif event == ord("-"):
                    if (SimRate / 2) > 0.001:
                        SimRate = SimRate / 2
                elif event == ord("p"):
                    Run = toggleRun(Run)
                elif event == ord(" "):
                    Run = toggleRun(Run)
                elif event == ord("1"):
                    R1 = float(updateR1(mw,height,width,R1))
                elif event == ord("2"):
                    R2 = float(updateR2(mw,height,width,R2))
                elif event == ord("m"):
                    VINMax = float(updateVINMax(mw,height,width,VINMax))
                elif event == ord("r"):
                    VRef = float(updateVRef(mw,height,width,VRef))


                if (VINMax * R2 / (R1+R2)) > VRef:
                    ClipV = 0.001
                    while ClipV <= VINMax:
                        if (ClipV * R2 / (R1+R2)) > VRef:
                            break
                        else:
                            ClipV = ClipV + 0.001

                    ClipP = 100-(100/VINMax * ClipV)
                    ClipD = round(20/100 * ClipP)
                else:
                    ClipD = False
                    UC = VRef - (VINMax * R2 / (R1+R2))
                    UP = 100/VRef * UC
                    UD = round(20/100 * UP)


                ########################################################
                ########################################################
                ## Formulas ############################################

                ########################################################
                # Voltage Divider Open-Circuit Output Voltage (Unloaded)

                VdOC        = VIN * R2 / (R1+R2)
                # FIXME: Add some math to estimate the loaded value

                ########################################################
                # Power Loss. Why care? To save power of course, every
                # little mA counts, especially in mobile/autonomous and
                # battery powered devices. If that's not enough of a
                # motivator, knowing how much power will be dissipated
                # helps determining, if the selected resitor's package
                # will be able to handle it. Also, the more power is
                # dissipated into heat, the more you have to fight
                # against temperature rise, which in turn will alter
                # the resistors characteristics and therefore the
                # precision and reliability of your measurement.

                VdI         = VIN / (R1+R2)
                P1          = R1 * (VdI**2)
                P2          = R2 * (VdI**2)

                ########################################################
                # Impedance Matching and "common wisdom":
                #
                # "Seriously? ADC input impedance usually is in the
                # Mega-Ohm Range, so you don't need to bother with
                # the output impedance of your voltage divider"
                #
                # Well, since a majority of projects use ATMega MC's
                # (like the Arduino), let's have a look into some datasheets:
                #
                # http://www.atmel.com/images/atmel-7766-8-bit-avr-atmega16u4-32u4_datasheet.pdf (24.7.1) Page 306
                # http://www.atmel.com/images/Atmel-8271-8-bit-AVR-Microcontroller-ATmega48A-48PA-88A-88PA-168A-168PA-328-328P_datasheet_Complete.pdf (24.6.1) Page 244
                #
                # "The ADC is optimized for analog signals with an output
                # impedance of approximately 10 kΩ or less. If such a
                # source is used, the sampling time will be negligible."
                #
                # Whuut???
                #
                # The problem with high source impedances arises when
                # you are switching the input multiplexer from one pin
                # to another. If you have two inputs, one at 0.5V and
                # one at 4.5V, when you switch from one to the other,
                # the input has to charge (or discharge) that 14 pF
                # capacitor. (See Figure in the datasheets)
                #
                # If the signal source is very high impedance, having to
                # charge the capacitor may cause the input voltage to
                # drop temporarily. If the ADC converts on the input
                # while is is still charging the capacitor, you will
                # get an incorrect value.
                #
                # This can probably be dealt with by letting the ADC
                # input settle for a period of time after switching
                # ADC channels, but the best way to deal with it is to
                # simply ensure that the input source can charge the
                # capacitance fast enough, so that it's not a problem.

                Zin         = R1 + R2
                Zout        = (R1*R2) / (R1+R2)

                ########################################################
                # ADC Resolution (Actual PIN Voltage)

                ADC8Res     = VRef / (2**8)
                ADC10Res    = VRef / (2**10)
                ADC12Res    = VRef / (2**12)
                ADC16Res    = VRef / (2**16)

                ########################################################
                # ADC Resolution (Full-Scale Voltage)

                ADC8FRes    = (R1/R2) * VRef / (2**8)
                ADC10FRes   = (R1/R2) * VRef / (2**10)
                ADC12FRes   = (R1/R2) * VRef / (2**12)
                ADC16FRes   = (R1/R2) * VRef / (2**16)

                ########################################################
                # ADC Decimal Output Prediction

                ADC8Dec     = int((2**8)  / VRef * VdOC)
                ADC10Dec    = int((2**10) / VRef * VdOC)
                ADC12Dec    = int((2**12) / VRef * VdOC)
                ADC16Dec    = int((2**16) / VRef * VdOC)

                ########################################################
                # ADC Clipping Analysis

                if VdOC > VRef:
                    ADCClip = True
                else:
                    ADCClip = False

                # Protect Display from showing clipped values
                if ADC8Dec > (2**8):
                    ADC8Dec = (2**8)

                if ADC10Dec > (2**10):
                    ADC10Dec = (2**10)

                if ADC12Dec > (2**12):
                    ADC12Dec = (2**12)

                if ADC16Dec > (2**16):
                    ADC16Dec = (2**16)

                ########################################################
                # Calculate Pin Voltage from ADC's decimal value and
                # prevent further computation if DEC value is actually 0

                if ADC8Dec > 0:
                    VT8P    = (ADC8Dec  + 0.5) / (2**8 ) * VRef
                else:
                    VT8P = 0

                if ADC10Dec > 0:
                    VT10P   = (ADC10Dec + 0.5) / (2**10) * VRef
                else:
                    VT10P = 0

                if ADC12Dec > 0:
                    VT12P   = (ADC12Dec + 0.5) / (2**12) * VRef
                else:
                    VT12P = 0

                if ADC16Dec > 0:
                    VT16P   = (ADC16Dec + 0.5) / (2**16) * VRef
                else:
                    VT16P = 0

                ########################################################
                # Calculate Full-Scale Voltage, can be copied directly
                # into the AVR/Arduino Firmware as a reference, integrating
                # or alongside the Pin Voltage calculation.

                VT8FS       = VT8P  / (R2/(R1+R2))
                VT10FS      = VT10P / (R2/(R1+R2))
                VT12FS      = VT12P / (R2/(R1+R2))
                VT16FS      = VT16P / (R2/(R1+R2))

                ########################################################
                # Calculate Full-Scale Precision in mV

                VT8Prec      = (VIN - VT8FS ) * 1000
                VT10Prec     = (VIN - VT10FS) * 1000
                VT12Prec     = (VIN - VT12FS) * 1000
                VT16Prec     = (VIN - VT16FS) * 1000

                ########################################################
                # Draw schema

                mw.addstr(  3, 10, "  │  ",cgrn)
                mw.addstr(  4, 10, " ┌┴┐ ",cblu)
                mw.addstr(  5, 10, " │ │ ",cblu)
                mw.addstr(  6, 10, " │ │ ",cblu)
                mw.addstr(  7, 10, " │ │ ",cblu)
                mw.addstr(  8, 10, " └┬┘ ",cblu)
                mw.addstr(  9, 10, "  │  ",cgrn)
                mw.addstr( 10, 10, "  ├─ ",cgrn)
                mw.addstr( 11, 10, "  │  ",cgrn)
                mw.addstr( 12, 10, " ┌┴┐ ",cblu)
                mw.addstr( 13, 10, " │ │ ",cblu)
                mw.addstr( 14, 10, " │ │ ",cblu)
                mw.addstr( 15, 10, " │ │ ",cblu)
                mw.addstr( 16, 10, " └┬┘ ",cblu)
                mw.addstr( 17, 10, "  │  ",cgrn)
                mw.addstr( 18, 10, "╶─┴─╴",cgrn)
                mw.addstr( 19, 10, " ╶─╴ ",cgrn)
                mw.addstr( 20, 10, "  ─  ",cgrn)
                mw.addstr( 10, 25, "─────",cgrn)
                mw.addstr(  1, 35, "┌───────┐",col5)
                mw.addstr(  2, 35, "┤  ADC  │",col5)
                mw.addstr(  3, 35, "│  256  ├▶",col5)
                mw.addstr(  4, 33, "┌─┤ 8 Bit │",col5)
                mw.addstr(  5, 33, "│ └───────┘",col5)
                mw.addstr(  6, 33, "│ ┌───────┐",col5)
                mw.addstr(  7, 35, "┤  ADC  │",col5)
                mw.addstr(  8, 33, "│ │ 1024  ├▶",col5)
                mw.addstr(  9, 33, "├─┤ 10Bit │",col5)
                mw.addstr( 10, 33, "│ └───────┘",col5)
                mw.addstr( 11, 33, "│ ┌───────┐",col5)
                mw.addstr( 12, 35, "┤  ADC  │",col5)
                mw.addstr( 13, 33, "│ │ 4096  ├▶",col5)
                mw.addstr( 14, 33, "├─┤ 12Bit │",col5)
                mw.addstr( 15, 33, "│ └───────┘",col5)
                mw.addstr( 16, 33, "│ ┌───────┐",col5)
                mw.addstr( 17, 35, "┤  ADC  │",col5)
                mw.addstr( 18, 33, "│ │ 65536 ├▶",col5)
                mw.addstr( 19, 33, "├─┤ 16Bit │",col5)
                mw.addstr( 20, 33, "│ └───────┘",col5)
                mw.addstr( 21, 33, "└─",col5)
                mw.addstr(  2, 30, "┌────",cgrn)
                mw.addstr(  3, 30, "│",cgrn)
                mw.addstr(  4, 30, "│",cgrn)
                mw.addstr(  5, 30, "│",cgrn)
                mw.addstr(  6, 30, "│",cgrn)
                mw.addstr(  7, 30, "├────",cgrn)
                mw.addstr(  8, 30, "│",cgrn)
                mw.addstr(  9, 30, "│",cgrn)
                mw.addstr( 10, 30, "┤",cgrn)
                mw.addstr( 11, 30, "│",cgrn)
                mw.addstr( 12, 30, "├────",cgrn)
                mw.addstr( 13, 30, "│",cgrn)
                mw.addstr( 14, 30, "│",cgrn)
                mw.addstr( 15, 30, "│",cgrn)
                mw.addstr( 16, 30, "│",cgrn)
                mw.addstr( 17, 30, "└────",cgrn)
                mw.addstr(  6,  8, "R1",)
                mw.addstr(  5,  15, "R:",)
                mw.addstr( 14,  8, "R2",)
                mw.addstr( 10, 11, "▶",curses.A_BOLD)
                mw.addstr(  2, 12, "▼",curses.A_BOLD)
                mw.addstr( 22, 24, "▼",curses.A_BOLD)
                mw.addstr( 21, 35, "◀",curses.A_BOLD)
                mw.addstr( 23,  4, "░░░░░░░░░░░░░░░░░░░░│░░░░░░░░░░░░░░░░░░░░",curses.A_DIM | curses.color_pair(8))
                mw.addstr( height-1, 1, "R[1] R[2] V[M]ax V[R]ef [+]Rate[-] [ ]Dir[ ] [P]ause [Q]uit")

                if SimDirection == "U":
                    mw.addstr(height-1,37, "▲",cgrn)
                    mw.addstr(height-1,43, "▼")
                else:
                    mw.addstr(height-1,37, "▲")
                    mw.addstr(height-1,43, "▼",cgrn)

                ########################################################
                # Draw values

                if SimMode == 3:
                    mw.addstr( 1, 8, str('  %.2f V  ' % VIN), curses.A_STANDOUT | curses.A_BOLD)
                else:
                    mw.addstr( 1, 8, str('  %.2f V  ' % VIN), curses.A_BOLD)
                
                mw.addstr(21, 36, str(' %.1f V ' % VRef), curses.A_STANDOUT | curses.A_BOLD | col5)
                mw.addstr(21,  9, str('%.3f mA ' % (VdI*1000)))
                
                if SimMode == 1:
                    mw.addstr( 5, 18, str(' %d Ω ' % R1),curses.A_STANDOUT | curses.A_BOLD)
                else:
                    mw.addstr( 5, 18, str(' %d Ω ' % R1))
                
                mw.addstr( 7, 15, str('P: %.3f mW ' % (P1*1000)))
                
                if SimMode == 2:
                    mw.addstr(13, 18, str(' %d Ω ' % R2),curses.A_STANDOUT | curses.A_BOLD)
                else:
                    mw.addstr(13, 18, str(' %d Ω ' % R2))
                
                mw.addstr(15, 15, str('P: %.3f mW ' % (P2*1000)))

                if ClipD:
                    mw.addstr( 24, 10, str('Clipping > %.2f V (%.1f%%) ' % (ClipV,ClipP)), curses.A_BOLD | curses.A_BLINK)
                    mw.addstr( 23, 1, "┌─▶",curses.A_BOLD)
                    mw.addstr( 24, 1, "└────",curses.A_BOLD)
                    #mw.addstr( 23, 45, " ")
                    for i in range(0,ClipD):
                        mw.addstr(23, 23-i, "▓",bred)
                    TDEff = 100-ClipP
                else:
                    mw.addstr(24, 8, str('Wasted Resolution < %.2f V (%.1f%%) ' % (UC,UP)), curses.A_BOLD )
                    mw.addstr( 23, 45, "◀─┐",curses.A_BOLD)
                    mw.addstr( 24, 43, "────┘",curses.A_BOLD)
                    #mw.addstr( 23, 3, " ")
                    for i in range(0,UD):
                        mw.addstr(  23, 25+i, "▓",bred)
                    TDEff = 100-UP

                if TDEff >= 100:
                    mw.addstr( 21,  21, str(' %d%% ' % TDEff),cgri)
                elif TDEff > 95:
                    mw.addstr( 21,  21, str(' %.1f%% ' % TDEff),cgri)
                else:
                    mw.addstr( 21,  21, str(' %.1f%% ' % TDEff),bred)

                if VdOC <= VRef:
                    mw.addstr(10,  2, str(' %.3f V ' % VdOC), curses.A_BOLD | cgri)
                else:
                    mw.addstr(10,  1, str('! %.3f V ' % VdOC), curses.A_BOLD | cred)


                if Zout <= ADCZMax:
                    mw.addstr(10, 15, str('Z: %d Ω' % Zout), curses.A_BOLD | cgrn)
                else:
                    mw.addstr(10, 15, str('Z: %d Ω' % Zout),cred)


                if ADC8FRes <= ADCResMin:
                    mw.addstr( 2, 46, str(' Res: %.2f mV    ' % (ADC8FRes*1000)),cgrn)
                else:
                    mw.addstr( 2, 45, str('! Res: %.2f mV   ' % (ADC8FRes*1000)),cred)

                if not ADCClip:
                    mw.addstr( 3, 46, str(' DEC: %d    ' % ADC8Dec))
                    mw.addstr( 4, 46, str(' %.2f V (%+d mV)    ' % (VT8FS, VT8Prec)), curses.A_BOLD | cgrn)
                else:
                    mw.addstr( 3, 45, str('! DEC: %d   ' % ADC8Dec),cred)
                    mw.addstr( 4, 45, str('! %.2f V (%+d mV)   ' % (VT8FS, VT8Prec)),cred)


                if ADC10FRes <= ADCResMin:
                    mw.addstr( 7, 46, str(' Res: %.2f mV    ' % (ADC10FRes*1000)),cgrn)
                else:
                    mw.addstr( 7, 45, str('! Res: %.2f mV   ' % (ADC10FRes*1000)),cred)

                if not ADCClip:
                    mw.addstr( 8, 46, str(' DEC: %d    ' % ADC10Dec))
                    mw.addstr( 9, 46, str(' %.2f V (%+d mV)    ' % (VT10FS, VT10Prec)), curses.A_BOLD | cgrn)
                else:
                    mw.addstr( 8, 45, str('! DEC: %d   ' % ADC10Dec),cred)
                    mw.addstr( 9, 45, str('! %.2f V (%+d mV)   ' % (VT10FS, VT10Prec)),cred)


                if ADC12FRes <= ADCResMin:
                    mw.addstr(12, 46, str(' Res: %.2f mV    ' % (ADC12FRes*1000)),cgrn)
                else:
                    mw.addstr(12, 45, str('! Res: %.2f mV   ' % (ADC12FRes*1000)),cred)

                if not ADCClip:
                    mw.addstr(13, 46, str(' DEC: %d    ' % ADC12Dec))
                    mw.addstr(14, 46, str(' %.2f V (%+d mV)    ' % (VT12FS, VT12Prec)), curses.A_BOLD | cgrn)
                else:
                    mw.addstr(13, 45, str('! DEC: %d   ' % ADC12Dec),cred)
                    mw.addstr(14, 45, str('! %.2f V (%+d mV)   ' % (VT12FS, VT12Prec)),cred)


                if ADC16FRes <= ADCResMin:
                    mw.addstr(17, 46, str(' Res: %.2f mV    ' % (ADC16FRes*1000)),cgrn)
                else:
                    mw.addstr(17, 45, str('! Res: %.2f mV   ' % (ADC16FRes*1000)),cred)

                if not ADCClip:
                    mw.addstr(18, 46, str(' DEC: %d    ' % ADC16Dec))
                    mw.addstr(19, 46, str(' %.2f V (%+d mV)    ' % (VT16FS, VT16Prec)), curses.A_BOLD | cgrn)
                else:
                    mw.addstr(18, 45, str('! DEC: %d   ' % ADC16Dec),cred)
                    mw.addstr(19, 45, str('! %.2f V (%+d mV)  ' % (VT16FS, VT16Prec)),cred)


                if Run == True:
                    
                    if SimMode == 1:
                        if SimDirection == "U":
                            R1=R1+SimRate
                        elif SimDirection == "D":
                            R1=R1-SimRate

                    if SimMode == 2:
                        if SimDirection == "U":
                            R2=R2+SimRate
                        elif SimDirection == "D":
                            R2=R2-SimRate
                    
                    if SimMode == 3:
                        if SimDirection == "U":
                            VIN=VIN+SimRate
                        elif SimDirection == "D":
                            VIN=VIN-SimRate

                        if VIN > VINMax:
                            SimDirection = "D"
                            VIN = VINMax
                        elif VIN <= 0:
                            VIN = 0
                            SimDirection = "U"

                mw.refresh()
                time.sleep(0.15)

        except KeyboardInterrupt:
            pass
    finally:
        curses.nocbreak()
        curses.echo()
        curses.endwin()

if __name__ == '__main__':
    term = os.getenv('TERM')
    title="EZVD"
    if ('xterm' in term):
        xterm_title(title)
    elif ('screen' in term):
        screen_title(title)
    main()
