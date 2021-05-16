// Credit: Mateusz Rybczonec

const FULL_DASH_ARRAY = 283
winner_horse_name = ''
const WARNING_THRESHOLD = 120
const ALERT_THRESHOLD = 60
const countdown = document.querySelector('.countdown')
const horseImages = document.querySelectorAll('.horse-gif img')
const horses = document.querySelectorAll('.horse-gif')

horses.forEach((horse, i) => {
  horse.addEventListener('animationend', (e) => {
    if (i === 1) {
      document.querySelector('.next-race h3').style.opacity = '1'
      var fiveMinutes = 20,
      display = document.querySelector('#time')
      startTimer(fiveMinutes, display)
//      setTimeout(() => {
//        location.href = 'tournaments'
//      }, 20000)
        setResult();
    }
    horseImages[i].src = horse_image
    document.getElementById('confetti').style.display = 'block';
  })
})

setTimeout(() => {
  countdown.style.opacity = '0'

  horseImages.forEach((horseImage, i) => {
    horseImage.src = horse_gif
    horses[i].classList.add(`animation${i + 1}`)
  })
  startRace();
}, milli_sec_left)

const COLOR_CODES = {
  info: {
    color: 'green',
  },
  warning: {
    color: 'orange',
    threshold: WARNING_THRESHOLD,
  },
  alert: {
    color: 'red',
    threshold: ALERT_THRESHOLD,
  },
}

const TIME_LIMIT = second_left
let timePassed = 0
let timeLeft = TIME_LIMIT
let timerInterval = null
let remainingPathColor = COLOR_CODES.info.color

document.getElementById('app').innerHTML = `
<div class="base-timer">
  <svg class="base-timer__svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <g class="base-timer__circle">
      <circle class="base-timer__path-elapsed" cx="50" cy="50" r="45"></circle>
      <path
        id="base-timer-path-remaining"
        stroke-dasharray="283"
        class="base-timer__path-remaining ${remainingPathColor}"
        d="
          M 50, 50
          m -45, 0
          a 45,45 0 1,0 90,0
          a 45,45 0 1,0 -90,0
        "
      ></path>
    </g>
  </svg>
  <span id="base-timer-label" class="base-timer__label">${formatTime(
    timeLeft
  )}</span>
</div>
`

startTimer()

function onTimesUp() {
  clearInterval(timerInterval)
}

function startTimer() {
  timerInterval = setInterval(() => {
    timePassed = timePassed += 1
    timeLeft = TIME_LIMIT - timePassed
    if(timeLeft <= 60 && timeLeft >= 55){
        $('.hide').css('display', "none");
    }
    document.getElementById('base-timer-label').innerHTML = formatTime(timeLeft)
    setCircleDasharray()
    setRemainingPathColor(timeLeft)

    if (timeLeft === 0) {
      onTimesUp()
    }
  }, 1000)
}

function formatTime(time) {
  const minutes = Math.floor(time / 60)
  let seconds = time % 60

  if (seconds < 10) {
    seconds = `0${seconds}`
  }

  return `${minutes}:${seconds}`
}

function setRemainingPathColor(timeLeft) {
  const { alert, warning, info } = COLOR_CODES
  if (timeLeft <= alert.threshold) {
    document
      .getElementById('base-timer-path-remaining')
      .classList.remove(warning.color)
    document
      .getElementById('base-timer-path-remaining')
      .classList.add(alert.color)
  } else if (timeLeft <= warning.threshold) {
    document
      .getElementById('base-timer-path-remaining')
      .classList.remove(info.color)
    document
      .getElementById('base-timer-path-remaining')
      .classList.add(warning.color)
  }
}

function calculateTimeFraction() {
  const rawTimeFraction = timeLeft / TIME_LIMIT
  return rawTimeFraction - (1 / TIME_LIMIT) * (1 - rawTimeFraction)
}

function setCircleDasharray() {
  const circleDasharray = `${(
    calculateTimeFraction() * FULL_DASH_ARRAY
  ).toFixed(0)} 283`
  document
    .getElementById('base-timer-path-remaining')
    .setAttribute('stroke-dasharray', circleDasharray)
}


/*------------------------------------------------
                Set Result
    --------------------------------------------------*/

function setResult(){
	var horse_name = $('#horse_name').val();

	if(horse_name == winner_horse_name){
	    $('#modal_title').html("Congratulations! You've won");
	    $('.imagepreview').attr('src', $(this).find('img').attr('src'));
	    $('#noti').modal('show');
	}else if(horse_name == winner_horse_name){
	    $('#modal_title').html("Congratulations! You've won");
	    $('.imagepreview').attr('src', $(this).find('img').attr('src'));
	    $('#noti').modal('show');
	}else if(horse_name == winner_horse_name){
	    $('#modal_title').html("Congratulations! You've won");
	    $('.imagepreview').attr('src', $(this).find('img').attr('src'));
	    $('#noti').modal('show');
	}else{
	    $('#modal_title').html("Oops! You've Lost this Game, Better Luck next Time!");
	    $('.imagepreview').attr('src', $(this).find('img').attr('src'));
	    $('#noti').modal('show');
	}
	$.ajax({
            type: 'POST',
            url: "set_result",
            data: {"selected": horse_name, "winner": winner_horse_name},
            success: function (response) {
                if(response["msg"] == false){

                }else if(response["msg"] == true){

                }else{

                }
            },
            error: function (response) {
                console.log(response)
            }
    })
}

/*------------------------------------------------
                Start Race
    --------------------------------------------------*/

function startRace(){
    $.ajax({
            type: 'GET',
            url: "start_race",
            data: {},
            success: function (response) {
                if(response["winner"] == false){

                }else{
                    var horse = response['horse'];
                    var winner = response['winner'];
                    winner_horse_name = horse
                    if(horse == 'horse1'){
                        $('.animation1').css("animation", 'run '+winner+'s linear forwards')
                        $('.animation2').css("animation", 'run 35s linear forwards')
                        $('.animation3').css("animation", 'run 38s linear forwards')
                    }else if(horse == 'horse2'){
                        $('.animation2').css("animation", 'run '+winner+'s linear forwards')
                        $('.animation3').css("animation", 'run 35s linear forwards')
                        $('.animation1').css("animation", 'run 37s linear forwards')
                    }else{
                        $('.animation3').css("animation", 'run '+winner+'s linear forwards')
                        $('.animation1').css("animation", 'run 40s linear forwards')
                        $('.animation2').css("animation", 'run 32s linear forwards')
                    }
                }
            },
            error: function (response) {
                console.log(response)
            }
    })
}