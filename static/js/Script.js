/*global $*/
const formOpenBtn = document.querySelector("#form-open");
const home = document.querySelector(".home");
const formContainer = document.querySelector(".form_container");
const formCloseBtn = document.querySelector(".form_close");
const signupBtn = document.querySelector("#signup");
const loginBtn = document.querySelector("#login");
const pwShowHide = document.querySelectorAll(".pw_hide");
const successMessage = document.querySelector("#successMessage");


formOpenBtn.addEventListener("click", () => home.classList.add("show"));
formCloseBtn.addEventListener("click", () => home.classList.remove("show"));

pwShowHide.forEach((icon) => {
  icon.addEventListener("click", () => {
    let getPwInput = icon.parentElement.querySelector("input");
    if (getPwInput.type === "password") {
      getPwInput.type = "text";
      icon.classList.replace("uil-eye-slash", "uil-eye");
    } else {
      getPwInput.type = "password";
      icon.classList.replace("uil-eye", "uil-eye-slash");
    }
  });
});

// Function to show the success message
function showSuccessMessage() {
  successMessage.style.display = "block";

  // Automatically hide the message after 3 seconds
  setTimeout(() => {
    successMessage.style.display = "none";
  }, 3000);
}

// Update the signupBtn event listener
signupBtn.addEventListener("click", (e) => {
  e.preventDefault();
  formContainer.classList.add("active");
  document.querySelector(".login_form").style.display = "none";
  document.querySelector(".signup_form").style.display = "block";

  // Call the showSuccessMessage function
  showSuccessMessage();
  // Add a click event listener to the document to hide the message when clicking outside
  const clickOutsideListener = (event) => {
    const targetElement = event.target;

    // Check if the clicked element is outside the success message and the signup button
    if (!successMessage.contains(targetElement) && targetElement !== signupBtn) {
      successMessage.style.display = "none";
      document.removeEventListener("click", clickOutsideListener); // Remove the event listener once the message is hidden
    }
  };

  document.addEventListener("click", clickOutsideListener);
});



loginBtn.addEventListener("click", (e) => {
  e.preventDefault();
  formContainer.classList.remove("active");
  
  // Call the showSuccessMessage function
  // Add a click event listener to the document to hide the message when clicking outside
  const clickOutsideListener = (event) => {
    const targetElement = event.target;

    // Check if the clicked element is outside the success message and the login button
    if (!successMessage.contains(targetElement) && targetElement !== loginBtn) {
      successMessage.style.display = "none";
      document.removeEventListener("click", clickOutsideListener); // Remove the event listener once the message is hidden
    }
  };

  document.addEventListener("click", clickOutsideListener);
});

// Slider initialization
var imgs = document.querySelectorAll('.slider img');
var dots = document.querySelectorAll('.dot');
var currentImg = 0; // index of the first image 
const interval = 3000; // duration(speed) of the slide


function changeSlide(n) {
  for (var i = 0; i < imgs.length; i++) { // reset
    imgs[i].style.opacity = 0;
    dots[i].className = dots[i].className.replace(' active', '');
  }

  currentImg = (currentImg + 1) % imgs.length; // update the index number

  if (n != undefined) {
      clearInterval(timer);
      timer = setInterval(changeSlide, interval);
      currentImg = n;
  }

  imgs[currentImg].style.opacity = 1;
  dots[currentImg].className += ' active';
}

var timer = setInterval(changeSlide, interval);
