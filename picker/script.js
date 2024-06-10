"use strict";
(() => {
	/*[ Util ]***********************************************************************************/

	/**
	$() streamlines creating and getting elements.

	Arguments:
		str: String
			Query selector or HTML to create.

	Returns: HTMLElement | Array(HTMLElement)
		The created or found element(s).
	**/
	function $(str) {
		let res;
		if (/</u.test(str)) {
			res = document.createElement(null);
			res = [...((res.innerHTML = str), res.children)];
		} else {
			res = [...document.querySelectorAll(str)];
		}

		return res.length < 2 ? res[0] : res;
	}

	/**
	toast() displays a message in the toast bar for a period of time.

	Arguments:
		text: String
			Text to display.
		showMS: Number
			Number of milliseconds to display the toast for.
	**/
	function toast(text, showMS = 3000) {
		const msg = $(`<p aria-role="alert">${text}</p>`);
		$("#toast-bar").appendChild(msg);
		setTimeout(msg.remove.bind(msg), showMS);
	}

	/*[ Main ]***********************************************************************************/

	const HTML = $("html");
	HTML.classList.add("js");
	HTML.appendChild($('<aside id="toast-bar"></aside>'));
	$("img").forEach((elm) => {
		elm.onclick = () => {
			navigator.clipboard.writeText(elm.alt).then(
				() => {
					toast(`Copied ${elm.alt} To Clipboard`);
				},
				() => {
					toast(`Failed To Copy ${elm.alt} To Clipboard`);
				}
			);
		};
	});

})();
