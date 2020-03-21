SOURCE :=../liteeth_core.v \
         ../udp_panel_writer.v \
         ../ledpanel.v \
         ../pll.v \
         ../phy_io.v \
         ../top.v

YOSYS_SCRIPT:=syn.ys

all : top.svf

../pll.v :
	ecppll -i 25 --clkout0_name clock --clkout0 125 --clkout1_name panel_clock --clkout1 52 -f ../pll.v

../liteeth_core.v : ../liteeth.yml
	liteeth_gen --gateware-dir ../ --no-compile-software ../liteeth.yml

top.json : $(YOSYS_SCRIPT) $(SOURCE)
	yosys -s $< -o $@

top.config : top.json
	nextpnr-ecp5 --pre-pack clocks.py --25k --freq 125 --timing-allow-fail --package CABGA256 --speed 6 --json top.json --lpf top.lpf --write top-post-route.json --textcfg top.config

top.bit : top.config
	ecppack top.config top.bit

top.svf : top.bit
	./bit_to_svf.py top.bit top.svf

flash.svf : top.bit
	./bit_to_flash.py top.bit flash.svf


prog : top.svf
	~/opt/openocd/bin/openocd -f openocd.cfg -c "transport select jtag; init; scan_chain; svf top.svf; shutdown; quit"
