"""TO-DO: Write a description of what this XBlock is."""

import json
import pkg_resources
from django.utils import translation
from xblock.core import XBlock
from xblock.fields import String, Scope
from xblock.fragment import Fragment
from xblockutils.resources import ResourceLoader

from .openai_api import OpenaiClient


class OpenAI(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    conditions = String(
        defalut="""
        my student will ask you something, please answer only in spanish, correct any grammar errors and make as much questions as possible to keep the conversation going
        """,
        scope=Scope.user_state,
        help="The initial conditions for the conversation established by the tutor",
    )
    history = String(
        default="",
        scope=Scope.user_state,
        help="A history of the conversation with the bot",
    )
    student_prompt = String(
        default="",
        scope=Scope.user_state,
        help="The last prompt entered by the user",
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

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def ask_client(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        client = OpenaiClient()
        self.student_prompt = data.get('text', None)
        if self.student_prompt is None:
            return {"response": "Please write something in the box"}

        text_created = client.ask(f'{self.conditions}\n\n {self.history}\n\n {self.student_prompt}')

        self.history += f'\n\n{self.student_prompt}\n\n {text_created}\n\n'

        print(self.conditions, self.history, self.student_prompt, text_created)

        return {"response": text_created}

    @XBlock.json_handler
    def delete_history(self, data, suffix=''):
        """
        Deletes history
        """
        self.history = "\n"

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
