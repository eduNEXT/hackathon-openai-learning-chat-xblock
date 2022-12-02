/* Javascript for OpenAI. */
function OpenAI(runtime, element) {
    var handlerUrl = runtime.handlerUrl(element, 'ask');

    $('#promptForm').onSubmit(function(eventObject) {
        eventObject.preventDefault();
        console.log(eventObject)
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"text": "fdsfdsf"}),
            success: updateCount
        });
    });

    $(function ($) {
        /*
        Use `gettext` provided by django-statici18n for static translations

        var gettext = OpenAIi18n.gettext;
        */

        /* Here's where you'd do things on page load. */
    });
}
