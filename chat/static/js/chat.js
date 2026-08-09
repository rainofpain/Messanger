const deleteChat = document.getElementById('delete-chat');
const blueTrash = document.getElementById("blue-trash");
const addedChatsContainer = document.querySelector(".added-chats-container");
const searchInput = document.querySelector(".search-input");
const userChatContainerContent = document.querySelector(".user-chat-container-content");
const messageInput= document.getElementById("message_input");
const sendMessageBtn = document.getElementById("send_message");
const enterChatBtn = document.getElementById("enter-chat");
const joinChatModal = document.querySelector(".join-chat");
const modalLayout = document.querySelector(".modal-layout");

let userChatName = "";
const socketApp = io();

const url = window.location.href
const urlSplit = url.split('/');
let currentChatId = "";

function enterToChat(chatId){
    fetch("/chat",
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                action: "enter-chat",
                chatId: chatId
             })
        })
        .then(
            response => {
                return response.json()
            })
        .then(data => {
            console.log(data.is_member)
            if(data.is_member === true){
                window.location.href = `/chat/${chatId}`;
            }
            else{
                modalLayout.classList.remove("hidden");
                joinChatModal.classList.remove("hidden");
                enterChatBtn.dataset.chatId = chatId;
            }

        }
    );
}


socketApp.on("connect", (data) => {
    console.log("Connected");
});

socketApp.on("new_message", (data) => {
    const chatContentContainer = document.querySelector(".chat-content-container");
    const userEmail = sendMessageBtn.dataset.userEmail;
    const messageContainer = document.createElement("div");
    messageContainer.classList.add("chat-message");
    messageContainer.innerHTML = `
            <div>
                <p>${data.user_email}: ${data.message}</p>
            </div>    
        `;
    chatContentContainer.appendChild(messageContainer);
});

if (urlSplit.length == 5){
    currentChatId = urlSplit.pop();
    socketApp.emit("join", { chat: `chat_${currentChatId}` });
    console.log("connected");
}

if (enterChatBtn){
    enterChatBtn.addEventListener(
        "click",
        () =>{
        let chatId = enterChatBtn.dataset.chatId;
        fetch("/chat",
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ 
                    action: "add-user-to-chat",
                    chatId: chatId
                 })
            })
            .then(()=> {
               window.location.href = `/chat/${chatId}`;
            }
        );
        window.location.href = `/chat/${chatId}`;
        }
    );
}
sendMessageBtn.addEventListener("click", () => {
    let message = messageInput.value.trim();
    messageInput.value = "";
    console.log(currentChatId);
    if (message && message != "" && currentChatId != ""){
        fetch(`/chat/${currentChatId}`,
                {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ 
                        action: "send_message",
                        message: message
                     })
                })
                .then(()=> {
                    socketApp.emit("send_to_chat", {
                        chat: `chat_${currentChatId}`,
                        message: message
                    });
                }
            );  
    }
    
})


if (userChatContainerContent){
    userChatName = userChatContainerContent.dataset.userChatName;
}

if (blueTrash){
    blueTrash.addEventListener("click", () => {
        const deleteChatModal = document.querySelector(".delete-chat");
        const modalLayout = document.querySelector(".modal-layout");
        modalLayout.classList.remove("hidden");
        deleteChatModal.classList.remove("hidden");
    });
}

deleteChat.addEventListener("click", () => {
    fetch("/chat",
        {
            method: "DELETE",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action: "delete-chat" })
        })
        .then(()=> {
            window.location.href = "/authorization";
        }
        );
});

if(addedChatsContainer){
    const chats = JSON.parse(addedChatsContainer.dataset.chats);
    const chatsArray = chats.map(chat => ({ id: chat.id, name: chat.name }));
    
    searchInput.addEventListener('input', (event) =>{
        addedChatsContainer.innerHTML = "";
        const input_value = event.target.value.trim(); 
        if (input_value != ""){
            chatsArray.forEach(chat => {
                if(chat.name.includes(input_value) && chat.name[0] === input_value[0] && chat.name != userChatName){
                    const chat_container = document.createElement("div");
                    chat_container.classList.add("chat-container");
                    chat_container.dataset.chatId = chat.id;
                    chat_container.innerHTML = `
                            <div>
                                <p>${chat.name}</p>
                            </div>    
                        `;
                    chat_container.addEventListener("click", () => {
                        const chatId = chat_container.dataset.chatId;
                        enterToChat(chatId);
                    });
                    addedChatsContainer.appendChild(chat_container);
                }
            });
        }
    });
    
    const chatContainers = document.querySelectorAll(".chat-container");

    if(chatContainers){
        chatContainers.forEach(chat => {
            chat.addEventListener("click", () =>{
                const chatId = chat.dataset.chatId;
                enterToChat(chatId);
            });
        });
    }
}

