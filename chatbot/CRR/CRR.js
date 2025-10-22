<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Chatbot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
        }
        #chatbox {
            width: 300px;
            height: 400px;
            border: 1px solid #ccc;
            overflow-y: auto;
            margin: auto;
            padding: 10px;
        }
        #userInput {
            width: 80%;
            padding: 10px;
        }
    </style>
</head>
<body>
    <h2>Simple Chatbot</h2>
    <div id="chatbox"></div>
    <input type="text" id="userInput" placeholder="Ask a question...">
    <button id="sendButton">Send</button>
    
    <script>
        const dataset = {
            "hello": "Hi there! How can I help you?",
            "how are you": "I'm just a bot, but I'm doing great!",
            "what is your name": "I'm a simple chatbot.",
            "bye": "Goodbye! Have a great day!"
        };

        document.addEventListener("DOMContentLoaded", () => {
            document.getElementById("sendButton").addEventListener("click", sendMessage);
        });

        function sendMessage() {
            let inputElement = document.getElementById("userInput");
            let input = inputElement.value.toLowerCase().trim();
            let chatbox = document.getElementById("chatbox");
            
            if (input === "") return;
            
            chatbox.innerHTML += `<p><strong>You:</strong> ${input}</p>`;
            
            let response = dataset[input] || "I'm sorry, I don't understand that.";
            chatbox.innerHTML += `<p><strong>Bot:</strong> ${response}</p>`;
            
            inputElement.value = "";
            chatbox.scrollTop = chatbox.scrollHeight;
        }
    </script>
</body>
</html>
