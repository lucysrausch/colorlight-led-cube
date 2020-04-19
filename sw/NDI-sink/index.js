const grandiose = require('grandiose');
const argv = require('minimist')(process.argv.slice(2));
const chunks = require('buffer-chunks');
const udp = require('dgram');

const client = udp.createSocket('udp4');

const framebuffer = [
	Buffer.alloc(64*64),
];

const cube = {
	ip: '192.168.178.50',
	port_1: 26208,
	port_2: 26209,
	port_3: 26210,
	port_4: 26212,
	port_5: 26216,
	port_6: 26224,
	//ports: [26208, 26209, 26210, 26212, 26216, 26224],
	ports: [26177, 26178, 26180, 26184, 26192, 26208],
	x: 64,
	y: 64,
};

const main = async () => {
	const sources = await grandiose.find({
		showLocalSources: true,
		extraIPs: [ "127.0.0.1", "100.124.200.70" ]
	});

	if(argv.source === undefined){
		console.log(`please select a source by appending --source <id>`);
		for(const [i, el] of sources.entries()){
			console.log(`--source ${i} :: ${el.name}`);
		}

		return;
	}

	let receiver = await grandiose.receive({
		source: sources[argv.source],
		colorFormat: grandiose.COLOR_FORMAT_RGBX_RGBA,
		name: "led_cube",
	});

	let timeout = 10000;

	if(argv.timout !== undefined)
		timeout = argv.timout;

	let ip_address = cube.ip;

	if(argv.ip !== undefined)
		ip_address = argv.ip;

	// allocate buffer
	const buffer = Buffer.alloc(cube.x * cube.y * 4 * 6);

	while (1) {
		try {
			let videoFrame = await receiver.video(timeout);
			framebuffer[0] = videoFrame.data;

			const size = {
				x: videoFrame.xres,
				y: videoFrame.yres,
			};

			// iterate over lines
			const lines = chunks(videoFrame.data, cube.x * 4).slice(0, size.y);

			for([y, line] of lines.entries()){
				const pixels = chunks(line, 4).slice(0, size.x);

				// parse all pixels
				for([x, pixel] of pixels.entries()){
					const addr = ((y & 0x3F) << 6) | (x & 0x3F);

					const r = pixel[0];
					const b = pixel[1];
					const g = pixel[2];
					const a = pixel[3];

					const alpha = a / 255;

					const pixeldata = (addr << 18) | (((parseInt(r * alpha))&0xFC) << 10)
											       | (((parseInt(g * alpha))&0xFC) << 4)
											       | (((parseInt(b * alpha))&0xFC) >> 2);
					
					buffer.writeUInt32BE(pixeldata, (y * size.x + x) * 4);
				}
			}

			for([i, port] of cube.ports.entries()){
				const panels = chunks(buffer, 64*64*4);

				//if(i == 0){
					for([y, chunk] of chunks(panels[i], 2**10).entries()){
						// send udp packet
						client.send(chunk, port, cube.ip, error => {
							if(error) console.error(error)
						});
					}
				//}
			}
		} catch (e) {
			console.log(e);
		}
	}
};

main();
