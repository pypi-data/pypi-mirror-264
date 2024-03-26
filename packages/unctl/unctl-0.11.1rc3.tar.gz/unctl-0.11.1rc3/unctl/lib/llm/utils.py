from unctl.lib.utils import GlobalVar

llm = GlobalVar.make("LLMInstance", default=None)


def set_llm_instance(llm_instance):
    llm.set(llm_instance)


def get_llm_instance():
    return llm.get()
