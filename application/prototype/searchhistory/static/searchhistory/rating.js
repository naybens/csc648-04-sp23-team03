const maxRating = 5;

// html class tag
const class_list_lightning_foreground = "lightning-foreground";
const class_list_lightning_background = "lightning-background";

// Image link
const image_background_energy =
  "https://csc648whereweeatinmeow.s3.us-west-2.amazonaws.com/background_energy.svg";
const image_foreground_energy =
  "https://csc648whereweeatinmeow.s3.us-west-2.amazonaws.com/energy.svg";

const ratingDivs = document.querySelectorAll(".rating");
ratingDivs.forEach((element) => {
  let rating = element.getAttribute("data-value");
  for (let i = 0; i < rating; i++) {
    let img = document.createElement("img");
    img.classList.add(class_list_lightning_foreground);
    img.src = image_foreground_energy;
    element.appendChild(img);
  }
  for (let i = 0; i < maxRating - rating; i++) {
    let img = document.createElement("img");
    img.classList.add(class_list_lightning_background);
    img.src = image_background_energy;
    element.appendChild(img);
  }
});
