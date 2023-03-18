let soundplaying = false;

function onScanSuccess(decodedText, decodedResult) {
	const binaryArray = decodedText
  .split('')
  .reduce((acc, next) =>
    [...acc, next.charCodeAt(0)],
    []
  )
	var uncompressed = LZW.decompress(binaryArray);
	var splt = uncompressed.split(";");

	var actions = ["hex","hex","x","ally","bool","bool","bool","bool","hex","x","hex", "bool","hex", "x", "hex"];

	for (i in splt) {
		switch (actions[i]) {
			case "hex":
				splt[i] = parseInt(splt[i], 16);
				break;
			case "bool":
				splt[i] = parseInt(splt[i]);
				break;
			case "ally":
				if (splt[i] == "B") {
					splt[i] = "blue";
				} else {
					splt[i] = "red";
				}
				break;
			case "x": break;
		};
	}

	var data = {
		"match_number": splt[0],
		"linked_team": splt[1],
		"linked_event": splt[2],
		"alliance": splt[3],
		"auto_balance": splt[4],
		"auto_move": splt[5],
		"teleop_balance": splt[6],
		"parked": splt[7],
		"endgame_score": splt[8],
		"endgame_time": splt[9],
		"penalty": splt[10],
		"disabled": splt[11],
		"alliance_final_score": splt[12],
		"scouter_comments": splt[13],
		"recorded_time": splt[14],
	};
	console.log(data);

	for (var key in data) {
		document.getElementById(key).value = data[key];
	}

	const auto_submit_box = document.getElementById('auto_submit');

	if(auto_submit_box.checked) {
		document.getElementById('myForm').submit();
	}
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
