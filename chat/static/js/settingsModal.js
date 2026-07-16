const cancelButton = document.querySelector(".cancel-btn");
const crossImg = document.querySelector(".modal-header-cross");
const deleteUserContainer = document.querySelector(".delete-user-container");

function addHideWithClick(button){
    button.addEventListener("click", () => {
        const modalLayout = document.querySelector(".modal-layout");
        modalLayout.classList.add("hidden");
    });
}

deleteUserContainer.addEventListener("click", () => {
    fetch("/chat",
        {
            method: "DELETE",
        }).then(()=> {
            window.location.href = "/authorization";
        }
        );
});

addHideWithClick(cancelButton);
addHideWithClick(crossImg);