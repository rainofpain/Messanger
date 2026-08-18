const stepBackArrows = document.querySelectorAll(".step-back-arrow");

if (stepBackArrows){
    stepBackArrows.forEach(stepBackArrow => {
        stepBackArrow.addEventListener(
            "click",
            (event) => {
                const section = event.target.closest(".section");
                section.style.display = "none";
                if (section.classList.contains('right-container')){
                    const middleContainer = document.querySelector(".middle-container");
                    middleContainer.style.display = "flex";
                }
                if (section.classList.contains('middle-container')){
                    const leftContainer = document.querySelector(".left-container");
                    leftContainer.style.display = "flex";
                }
            }
        );
    });
}