import pyGHDL.libghdl     as libghdl
libghdl.initialize()
libghdl.analyze_init()
libghdl.analyze_file("pwm_conditioning_state_machine.vhd")