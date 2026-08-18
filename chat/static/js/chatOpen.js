const screenWidth = window.screen.width;
if (screenWidth <= 430){
    const chatHeaderName = document.querySelector(".chat-header-name");
    const middleContainer = document.querySelector(".middle-container");
    const leftContainer = document.querySelector(".left-container");
    const rightContainer = document.querySelector(".right-container");
    if (leftContainer.style.display = "flex"){
        leftContainer.style.display = "none";
        middleContainer.style.display = "flex";
        rightContainer.style.display = "none";
    }
    chatHeaderName.addEventListener(
        "click",
        () =>{
            middleContainer.style.display = "none";
            rightContainer.style.display = "block";
        }
    )
}