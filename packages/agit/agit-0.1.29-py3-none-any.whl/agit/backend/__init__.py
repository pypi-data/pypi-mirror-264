# import agit.backend.openai_bk as openai_bk
# import agit.backend.zhipuai_bk as zhipuai_bk
import agit

def call_llm_api(prompt: str, model: str, **kwargs):
    if "chatglm" in model or "glm" in model: 
        if model == "chatglm3-6b":
            return agit.backend.openai_bk.call_llm_api(prompt=prompt, model=model, **kwargs)
        return agit.backend.zhipuai_bk.call_llm_api(prompt=prompt, model=model, **kwargs)
    else:
        return agit.backend.openai_bk.call_llm_api(prompt=prompt, model=model, **kwargs)
