const ratingButtons = document.querySelectorAll(".image-button");
ratingButtons.forEach((button) => {
  button.addEventListener("mouseover", onButtonHover);
  button.addEventListener("mouseout", onButtonMouseOut);
});

function onButtonHover(event) {
  const currentButton = event.target;
  currentButton.classList.add("buttons-on-the-left");
  const allButtons = document.querySelectorAll(".image-button");
  allButtons.forEach((button) => {
    if (button.value < currentButton.value) {
      button.classList.add("buttons-on-the-left");
    }
  });
}
function onButtonMouseOut(event) {
  const currentButton = event.target;
  currentButton.classList.remove("buttons-on-the-left");
  const allButtons = document.querySelectorAll(".image-button");
  allButtons.forEach((button) => {
    if (button.value < currentButton.value) {
      button.classList.remove("buttons-on-the-left");
    }
  });
}
