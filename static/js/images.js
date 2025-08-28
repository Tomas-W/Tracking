document.addEventListener("DOMContentLoaded", function() {
    var largeScreen = window.innerWidth >= 768; // Example threshold for tablet/PC
    var imageElement = document.getElementById("responsive-image");
    var basePath = imageElement.getAttribute("data-base-path");

    // Append "l" for large screens or "s" for small screens
    var suffix = largeScreen ? "l" : "s";
    imageElement.src = basePath + suffix + ".png";

    console.log("Base Path:", basePath);
    console.log("Suffix:", suffix);
    console.log("Full Image Path:", imageElement.src);
});
