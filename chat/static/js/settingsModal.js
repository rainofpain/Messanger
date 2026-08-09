const cancelButtons = document.querySelectorAll(".cancel-btn");
const crossImgs = document.querySelectorAll(".modal-header-cross");
const deleteUserContainer = document.querySelector(".delete-user-container");
const deleteAccount = document.getElementById("delete-account");



function addHideWithClick(button){
    button.addEventListener("click", (event) => {
        const modalLayout = document.querySelector(".modal-layout");
        const modal = event.target.closest('.modal');
        modal.classList.add("hidden");
        modalLayout.classList.add("hidden");
    });
}

deleteUserContainer.addEventListener("click", () => {
    const deleteAccountModal = document.querySelector(".delete-account");
    deleteAccountModal.classList.remove("hidden");
})

deleteAccount.addEventListener("click", () => {
    fetch("/chat",
        {
            method: "DELETE",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action: "delete-account" })
        })
        .then(()=> {
            window.location.href = "/authorization";
        }
        );
});

cancelButtons.forEach(cancelButton => {
    addHideWithClick(cancelButton);
});
crossImgs.forEach(crossImg => {
    addHideWithClick(crossImg);
});