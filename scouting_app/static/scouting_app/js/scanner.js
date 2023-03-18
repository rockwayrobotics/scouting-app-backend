let soundplaying = false;

function onScanSuccess(decodedText, decodedResult) {
	const binaryArray = decodedText
  .split('')
  .reduce((acc, next) =>
    [...acc, next.charCodeAt(0)],
    []
  )
	var uncompressed = LZW.decompress(binaryArray);
	console.log(uncompressed);
	
	var splt = uncompressed.split(";");

	var actions = ["hex","hex","x","x","bool","bool","bool","bool","hex","x","hex", "bool","hex"];

	for (i in splt) {
		switch (actions[i]) {
			case "hex":
				splt[i] = parseInt(splt[i], 16);
				break;
			case "bool":
				splt[i] = parseInt(splt[i]);
				break;
			case "x": break;
		};
	}
	console.log(splt);
}

function onScanFailure(error) {
  // handle scan failure, usually better to ignore and keep scanning.
  // for example:
  console.warn(`Code scan error = ${error}`);
}

let html5QrcodeScanner = new Html5QrcodeScanner(
  "reader",
  { fps: 10, qrbox: {width: 250, height: 250} },
  /* verbose= */ false);
html5QrcodeScanner.render(onScanSuccess, onScanFailure);
