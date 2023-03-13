let soundplaying = false;

function convertBinaryToObject(str) {
	var newBin = str.split(" ");
	var binCode = [];
	for (i = 0; i < newBin.length; i++) {
		binCode.push(String.fromCharCode(parseInt(newBin[i], 2)));
	}
	let jsonString = binCode.join("");
	return JSON.parse(jsonString);
}

function onScanSuccess(decodedText, decodedResult) {
	console.log(`Code matched = ${decodedText}`, decodedResult);
	
	const binaryArray = decodedText
  .split('')
  .reduce((acc, next) =>
    [...acc, next.charCodeAt(0)],
    []
  )
	console.log(binaryArray);
	var uncompressed = LZW.decompress(binaryArray);
	console.log(uncompressed);
	var b_str = convertBinaryToObject(uncompressed);
	console.log(b_str);
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
