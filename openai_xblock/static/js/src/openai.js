/* Javascript for OpenAI. */
function OpenAI(runtime, element) {

    const askClientHandler = runtime.handlerUrl(element, 'ask_client');
    const deleteHistoryHandler = runtime.handlerUrl(element, 'delete_history');
    const messageLayout = document.querySelector('.messageContainer');
    const input = document.querySelector(".messageInput");
    const buttonSendMessage = document.querySelector('.buttonSend');
    const buttonClear = document.querySelector('.buttonClear');

    const scrollToBottom = () => {
        messageLayout.scrollTop = messageLayout.scrollTopMax;
    }

    const clearChat = () => {
        messageLayout.innerHTML = '';

        $.ajax({
            type: "POST",
            url: deleteHistoryHandler,
            data: JSON.stringify({}),
            success: (response) => {
            }
        });
    }

    const removeLoader = () => {
        const loader = document.querySelector('#loader-chat');
        loader.remove();
    }

    const updateResponse = (text) => {
        removeLoader()
        let message = `<div class="messageRecivedWrapper"><p class="messageRecived">${text.response}</p><div/>`;
        messageLayout.innerHTML += message;
        scrollToBottom();
    }

    const setUserMessage = (text) => {
        let message = `<div class="messageSendWrapper"><p class="messageSend">${text}</p><div/>`;
        let ellipsis = `<div id="loader-chat" class="messageRecivedWrapper"><div class="lds-ellipsis messageRecived"><div></div><div></div><div></div></div><div/>`
        messageLayout.innerHTML += message;
        messageLayout.innerHTML += ellipsis;
        scrollToBottom();
    }

    const getInputValue = () => {
        const message = input.value;

        input.value = '';
        return message;
    }

    const sendMessage = () => {
        let userInput = getInputValue();
        setUserMessage(userInput);

        $.ajax({
            type: "POST",
            url: askClientHandler,
            data: JSON.stringify({"text": userInput}),
            success: (response) => {
                updateResponse(response)
            }
        });
    }

    buttonSendMessage.addEventListener('click', () => {
        sendMessage();
    });

    buttonClear.addEventListener('click', () => {
        clearChat();
    });

    input.addEventListener('keypress', e => {
        if (e.key === 'Enter') {
            if (!e.shiftKey)
            {
                e.preventDefault()
                sendMessage();
                return;
            }
            
            if (input.rows < 6)
                input.rows += 1;
        }
    })


    $(function ($) {
        /*
        Use `gettext` provided by django-statici18n for static translations

        var gettext = OpenAIi18n.gettext;


        $('p.info', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: responseUrl,
            data: JSON.stringify({}),
            success: updateResponse
        });
    });
        */

        /* Here's where you'd do things on page load. */
    });
}
