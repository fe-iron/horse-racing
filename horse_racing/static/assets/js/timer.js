function startTimer(duration, display) {
  var timer = duration, seconds;
  setInterval(function () {
      seconds = parseInt(timer % 21, 10);

      seconds = seconds < 10 ? "0" + seconds : seconds;

      display.textContent = seconds;

      if (--timer < 0) {
          timer = duration;
      }
  }, 1000);
}

