var config = {
    apiKey: 'AIzaSyAVoCvlXSDlY49LyQAkZeWhNjzp2VWV1Os',
    authDomain: 'tokyo-kingdom-299513.firebaseapp.com',
    projectId: 'tokyo-kingdom-299513',
    storageBucket: 'tokyo-kingdom-299513.appspot.com',
    messagingSenderId: '585339205310',
    appId: '1:585339205310:web:055d44f7a9ef0eee22d0ef',
    measurementId: 'G-HC4JTP0D9N',
    databaseURL: '',
  }
  
  
console.log('Anurag'); 
firebase.initializeApp(config)

window.onload = function () {
  render()
  document.getElementById('otp-input-block').style.display = 'none'
  document.getElementById('signup-btn').style.display = 'none'
}
function render() {
  window.recaptchaVerifier = new firebase.auth.RecaptchaVerifier(
    'recaptcha-container',
    {
      size: 'invisible',
      callback: (response) => {
        // reCAPTCHA solved, allow signInWithPhoneNumber.
        onSignInSubmit()
      },
    }
  )
}

function phoneAuth() {
  var number = document.getElementById('mob').value
  number = '+91' + number

  firebase
    .auth()
    .signInWithPhoneNumber(number, recaptchaVerifier)
    .then((confirmationResult) => {
      // SMS sent. Prompt user to type the code from the message, then sign the
      // user in with confirmationResult.confirm(code).
      window.confirmationResult = confirmationResult
      codeResult = confirmationResult
      console.log(codeResult)
      alert('message sent check your phone!')
    })
    .catch((error) => {
      // Error; SMS not sent
      // ...
      document.getElementById('msg').innerHTML =
        'Enter only 10 digit Number without +91'
      console.log(error)
    })
}

function codeVerify() {
  var otp = document.getElementById('verificationCode').value
  codeResult
    .confirm(otp)
    .then((result) => {
      // User signed in successfully.
      const user = result.user
      document.forms['register'].submit()
    })
    .catch((error) => {
      // User couldn't sign in (bad verification code?)
      // ...
      document.getElementById('msg').innerHTML =
        'Something went wrong! Try again'
    })
}

function enable() {
  document.getElementById('otp-input-block').style.display = 'block'
  document.getElementById('get-otp').disabled = false
}

function enable_signup() {
  document.getElementById('get-otp').disabled = true
  document.getElementById('signup-btn').style.display = 'block'
}
