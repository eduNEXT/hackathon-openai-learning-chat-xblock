"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
from django.utils import translation
from xblock.core import XBlock
from xblock.fields import String, Scope, List
from xblock.fragment import Fragment
from xblockutils.resources import ResourceLoader
from xblockutils.settings import XBlockWithSettingsMixin
from xblockutils.studio_editable import StudioEditableXBlockMixin


from .openai_api import OpenaiClient


class OpenAI(XBlock, XBlockWithSettingsMixin, StudioEditableXBlockMixin):
    """
    An XBlock that allows students to interact with the OpenAI language model API through a chat interface
    within the edX course. The XBlock allows the course instructor to set the language and conditions for
    the conversation with the language model, and the students can then enter prompts for the language model
    to respond to. The XBlock stores a history of the conversation between the student and the language model,
    and provides a button for the student to clear the history if desired.
    """

    history = List(
        default=[],
        scope=Scope.user_state,
        help="A history of the conversation with the bot.",
    )
    student_prompt = String(
        default="",
        scope=Scope.user_state,
        help="The last prompt entered by the user.",
    )
    language = String(
        default="spanish",
        scope=Scope.settings,
        help="The language selected by the tutor.",
    )
    conditions = String(
        default="",
        scope=Scope.settings,
        help="The conditions entered by the tutor.",
    )
    editable_fields = (
        "language",
        "conditions",
    )


    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the OpenAI, shown to students
        when viewing courses.
        """
        if context:
            pass  # TO-DO: do something based on the context.
        html = self.resource_string("static/html/openai.html")
        frag = Fragment(html.format(self=self, my_info={"text": "hola mundo"}))
        frag.add_css(self.resource_string("static/css/openai.css"))

        # Add i18n js
        statici18n_js_url = self._get_statici18n_js_url()
        if statici18n_js_url:
            frag.add_javascript_url(self.runtime.local_resource_url(self, statici18n_js_url))

        frag.add_javascript(self.resource_string("static/js/src/openai.js"))
        frag.initialize_js('OpenAI')
        return frag

    def prepare_prompt(self, history, prompt, context):
        """
        Prepares the prompt for the language model by combining the conversation history, the current
        prompt entered by the student, and any additional context specified by the instructor.

        Args:
            history (list): A list of strings representing the previous conversations with the language model.
            prompt (str): The current prompt entered by the student.
            context (str): Additional context specified by the instructor for the conversation with the language model.

        Returns:
            str: The prepared prompt for the language model.
        """
        text = f'{context}\n'
        for line in history:
            text += line
        text += f'{prompt}\n'

        return text

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def ask_client(self, data, suffix=''):
        """
        Handles a request from the student to ask the language model a question.
        The method retrieves the student's prompt from the request data, prepares the prompt for the language model,
        and sends the prompt to the language model using the OpenAI API. The response from the language model
        is then returned to the student.

        Args:
            data (dict): A dictionary containing the request data, including the student's prompt.
            suffix (str, optional): A string that may be used to specify additional information for the request.

        Returns:
            dict: A dictionary containing the response from the language model.
        """
        context = f'You can only speak in {self.language}\n{self.conditions}\n'
        client = OpenaiClient()
        self.student_prompt = data.get('text', "")
        if self.student_prompt == "":
            return {"response": "Please write something in the box"}

        prompt = self.prepare_prompt(self.history, self.student_prompt, context)

        text_created = client.ask(prompt)

        self.history.append(f'{self.student_prompt}\n')
        self.history.append(f'{text_created}\n')

        return {"response": text_created}

    @XBlock.json_handler
    def delete_history(self, data, suffix=''):
        """
        Deletes the chat history.
        """
        self.history = []

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("OpenAI",
             """<openai/>
             """),
            ("Multiple OpenAI",
             """<vertical_demo>
                <openai/>
                <openai/>
                <openai/>
                </vertical_demo>
             """),
        ]

    @staticmethod
    def _get_statici18n_js_url():
        """
        Returns the Javascript translation file for the currently selected language, if any.
        Defaults to English if available.
        """
        locale_code = translation.get_language()
        if locale_code is None:
            return None
        text_js = 'public/js/translations/{locale_code}/text.js'
        lang_code = locale_code.split('-')[0]
        for code in (locale_code, lang_code, 'en'):
            loader = ResourceLoader(__name__)
            if pkg_resources.resource_exists(
                    loader.module_name, text_js.format(locale_code=code)):
                return text_js.format(locale_code=code)
        return None

    @staticmethod
    def get_dummy():
        """
        Dummy method to generate initial i18n
        """
        return translation.gettext_noop('Dummy')
