/* Javascript for OpenAI. */
function OpenAI(runtime, element) {
    var handlerUrl = runtime.handlerUrl(element, 'increment_count');
    var responseUrl = runtime.handlerUrl(element, 'get_response');

    const messageLayout = document.querySelector('.messageContainer')
    const input = document.querySelector(".messageInput")
    const buttonSendMessage = document.querySelector('.buttonSend')

    const updateResponse = (text) => {
        let message = `<div class="messageRecivedWrapper"><p class="messageSend">${text.response}</p><div/>`
        messageLayout.innerHTML += message
    }

    const setUserMessage = (text) => {
        let message = `<div class="messageSendWrapper"><p class="messageSend">${text}</p><div/>`
        messageLayout.innerHTML += message
    }

    const getInputValue = () => {
        const message = input.value

        input.value = '';
        return message
    }

    const sendMessage = () => {
        setUserMessage(getInputValue())

        var handlerUrl = runtime.handlerUrl(element, 'get_response');
        $.ajax({
            type: "POST",
            url: responseUrl,
            data: JSON.stringify({}),
            success: updateResponse
        });
    }


    buttonSendMessage.addEventListener('click', () => {
        sendMessage()
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
