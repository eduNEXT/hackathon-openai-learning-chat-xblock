/* Javascript for OpenAI. */
function OpenAI(runtime, element) {

    const askClientHandler = runtime.handlerUrl(element, 'ask_client');
    const deleteHistoryHandler = runtime.handlerUrl(element, 'delete_history');
    const messageLayout = document.querySelector('.messageContainer')
    const input = document.querySelector(".messageInput")
    const buttonSendMessage = document.querySelector('.buttonSend')
    const buttonClear = document.querySelector('.buttonClear')

    const clearChat = () => {
        messageLayout.innerHTML = ''

        $.ajax({
            type: "POST",
            url: deleteHistoryHandler,
            data: JSON.stringify({}),
            success: (response) => {
            }
        });
    }

    const setLoader = () => messageLayout.innerHTML += `
       <div id="loader-chat" class="messageSendWrapper"><div class="lds-ellipsis"><div></div><div></div><div></div><div></div></div><div/>
    `

    const removeLoader = () => {
        const loader = document.querySelector('#loader-chat')
        loader.remove()
    }

    const updateResponse = (text) => {
        removeLoader()
        let message = `<div class="messageRecivedWrapper"><p class="messageRecived">${text.response}</p><div/>`
        messageLayout.innerHTML += message
        messageLayout.scrollTo(0, '100%');
    }

    const setUserMessage = (text) => {
        let message = `<div class="messageSendWrapper"><p class="messageSend">${text}</p><div/>`
        messageLayout.innerHTML += message
    }

    const getInputValue = () => {
        const message = input.value

        input.value = ''
        return message
    }

    const sendMessage = () => {
        let userInput = getInputValue()
        setUserMessage(userInput)

        $.ajax({
            type: "POST",
            url: askClientHandler,
            data: JSON.stringify({"text": userInput}),
            success: (response) => {
                setLoader()
                setTimeout(updateResponse(response), 100)
            }
        });
    }


    buttonSendMessage.addEventListener('click', () => {
        sendMessage()
    })

    buttonClear.addEventListener('click', () => {
        clearChat()
    })

    input.addEventListener('keypress', (key) => {
        if(key.key === 'Enter') {
            sendMessage()
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
