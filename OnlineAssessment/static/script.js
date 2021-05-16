function getTimeRemaining(endtime) {
	const total = Date.parse(endtime) - Date.parse(new Date());
	const seconds = Math.floor((total / 1000) % 60);

	return {
		seconds, total
	};
}

function initializeClock(id, endtime) {
	const clock = document.getElementById(id);
	const secondsSpan = clock.querySelector('.seconds');

	function updateClock() {
		const nextBtn = document.querySelector('.next-btn');
		const t = getTimeRemaining(endtime);
		secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);

		if (t.total <= 0) {
			clearInterval(timeinterval);
			alert('time has expired!')
			nextBtn.click()
		}
	}

	updateClock();
	const timeinterval = setInterval(updateClock, 1000);
}

const deadline = new Date(Date.parse(new Date()) + 60 * 1000);
initializeClock('timer', deadline);