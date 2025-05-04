
(function() {
    const app = document.querySelector(".app");
    const socket = io();

    let uname;

    // Joining the chat
    app.querySelector(".join-screen #join-user").addEventListener("click", function() {
        let username = app.querySelector(".join-screen #user-name").value;
        if (username.length == 0) {
            return;
        }
        socket.emit("newuser", username);
        uname = username;
        app.querySelector(".join-screen").classList.remove("active");
        app.querySelector(".chat-screen").classList.add("active");
    });

    // Sending message
    app.querySelector(".chat-screen #send-message").addEventListener("click", function() {
        let message = app.querySelector(".chat-screen #message-input").value;
        if (message.length == 0) {
            return;
        }
        renderMessage("my", {
            username: uname,
            text: message
        });
        socket.emit("chat", {
            username: uname,
            text: message
        });
        app.querySelector(".chat-screen #message-input").value = "";
    });

    // Emoji picker functionality
    document.querySelector("#emoji-picker").addEventListener("click", function() {
        let emojiList = ['😀', '😂', '😍', '😎', '👍', '❤️', '🎉'];
        let emojiPicker = document.createElement('div');
        emojiPicker.classList.add('emoji-list');
        
        emojiList.forEach(emoji => {
            let emojiButton = document.createElement('button');
            emojiButton.textContent = emoji;
            emojiButton.addEventListener('click', function() {
                let messageInput = document.querySelector("#message-input");
                messageInput.value += emoji; 
                emojiPicker.remove(); 
            });
            emojiPicker.appendChild(emojiButton);
        });

        document.body.appendChild(emojiPicker); 
    });

    
    document.querySelector("#file-upload").addEventListener("click", function() {
        document.querySelector("#file-input").click();
    });

    document.querySelector("#file-input").addEventListener("change", function() {
        let file = this.files[0];
        if (file) {
            let formData = new FormData();
            formData.append("file", file);

            fetch("/upload", {
                method: "POST",
                body: formData
            }).then(response => response.json())
              .then(data => {
                  if (data.success) {
                      let message = {
                          username: uname,
                          text: `File: <a href="${data.filePath}" download>${file.name}</a>`
                      };
                      renderMessage("my", message);
                      socket.emit("chat", message); 
                  }
              });
        }
    });

    
    app.querySelector(".chat-screen #exit-chat").addEventListener("click", function() {
        socket.emit("exituser", uname);
        window.location.reload();
    });

    
    socket.on("update", function(update) {
        renderMessage("update", update);
    });

    socket.on("chat", function(message) {
        renderMessage("other", message);
    });

    
    function renderMessage(type, message) {
        let messageContainer = app.querySelector(".chat-screen .messages");
        if (type === "my") {
            let el = document.createElement("div");
            el.setAttribute("class", "message my-message");
            el.innerHTML = `
                <div>
                    <div class="name">You</div>
                    <div class="text">${message.text}</div>
                </div>
            `;
            messageContainer.appendChild(el);
        } else if (type === "other") {
            let el = document.createElement("div");
            el.setAttribute("class", "message other-message");
            el.innerHTML = `
                <div>
                    <div class="name">${message.username}</div>
                    <div class="text">${message.text}</div>
                </div>
            `;
            messageContainer.appendChild(el);
        } else if (type === "update") {
            let el = document.createElement("div");
            el.setAttribute("class", "update");
            el.innerHTML = message;
            messageContainer.appendChild(el);
        }
        messageContainer.scrollTop = messageContainer.scrollHeight - messageContainer.clientHeight;
    }

})();
