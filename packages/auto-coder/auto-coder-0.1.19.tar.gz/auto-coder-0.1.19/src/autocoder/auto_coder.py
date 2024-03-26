import byzerllm
from typing import List,Dict,Any,Optional
import argparse 
from autocoder.common import AutoCoderArgs
from autocoder.dispacher import Dispacher 
import yaml   
import locale
import os
from autocoder.common import git_utils
from jinja2 import Template
import hashlib

lang_desc = {
    "en": {
        "parser_desc": "Auto-implement missing methods in a Python script.",
        "source_dir": "Path to the project source code directory",
        "git_url": "URL of the git repository to clone the source code from",
        "target_file": "The file path to write the generated source code to",
        "query": "The user query or instruction to handle the source code",
        "template": "The template to use for generating the source code. Default is 'common'",
        "project_type": "The type of the project. Options: py, ts, py-script, translate, or file suffix. Default is 'py'",
        "execute": "Whether to execute the generated code. Default is False",
        "package_name": "Only works for py-script project type. The package name of the script. Default is empty.",
        "script_path": "Only works for py-script project type. The path to the Python script. Default is empty.",
        "model": "The name of the model to use. Default is empty",
        "model_max_length": "The maximum length of the generated code by the model. Default is 1024. This only works when model is specified.",
        "file": "Path to the YAML configuration file",
        "anti_quota_limit": "Time to wait in seconds after each API request. Default is 1s",
        "skip_build_index": "Whether to skip building the source code index. Default is False",
        "print_request": "Whether to print the request sent to the model. Default is False",
        "cmd_args_title": "Command Line Arguments:",
        "py_packages": "The Python packages added to context, only works for py project type. Default is empty.",
        "human_as_model": "Use human as model or not. Default is False",
        "urls": "The urls to crawl and extract text from, separated by comma",
        "search_engine": "The search engine to use. Supported engines: bing, google. Default is empty",
        "search_engine_token": "The token for the search engine API. Default is empty",
        "model_max_input_length": "The maximum length of the generated code by the model. Default is 6000. This only works when model is specified.",
        "auto_merge": "Whether to automatically merge the generated code into the existing file. Default is False",
        "revert_desc": "Revert the changes made by the specified file",
        
    },
    "zh": {
        "parser_desc": "自动为Python脚本实现缺失的方法。",
        "source_dir": "项目源代码目录路径",
        "git_url": "用于克隆源代码的Git仓库URL",
        "target_file": "生成的源代码的输出文件路径",
        "query": "用户查询或处理源代码的指令",
        "template": "生成源代码使用的模板。默认为'common'",
        "project_type": "项目类型。可选值:py、ts、py-script、translate或文件后缀名。默认为'py'",
        "execute": "是否执行生成的代码。默认为False",
        "package_name": "仅适用于py-script项目类型。脚本的包名。默认为空。",
        "script_path": "仅适用于py-script项目类型。Python脚本路径。默认为空。",
        "model": "使用的模型名称。默认为空",
        "model_max_length": "模型生成代码的最大长度。默认为1024。仅在指定模型时生效。",
        "file": "YAML配置文件路径",
        "anti_quota_limit": "每次API请求后等待的秒数。默认为1秒",
        "skip_build_index": "是否跳过构建源代码索引。默认为False",
        "print_request": "是否打印发送到模型的请求。默认为False",
        "cmd_args_title": "命令行参数:",
        "py_packages": "添加到上下文的Python包,仅适用于py项目类型。默认为空。",
        "human_as_model": "是否使用人工作为模型。默认为False",
        "urls": "要爬取并提取文本的URL,多个URL以逗号分隔",
        "search_engine": "要使用的搜索引擎。支持的引擎:bing、google。默认为空",
        "search_engine_token": "搜索引擎API的令牌。默认为空",
        "model_max_input_length": "模型的最大输入长度。默认为6000。仅在指定模型时生效。",
        "auto_merge": "是否自动将生成的代码合并到现有文件中。默认为False。",
        "revert_desc": "撤销指定文件所做的更改",
    }
}

def parse_args() -> AutoCoderArgs:
    system_lang, _ = locale.getdefaultlocale()
    lang = "zh" if system_lang and system_lang.startswith("zh") else "en"
    desc = lang_desc[lang]

    parser = argparse.ArgumentParser(description=desc["parser_desc"])
    subparsers = parser.add_subparsers(dest="command")
    
    parser.add_argument("--source_dir", required=False, help=desc["source_dir"])
    parser.add_argument("--git_url", help=desc["git_url"])
    parser.add_argument("--target_file", required=False, help=desc["target_file"])
    parser.add_argument("--query", help=desc["query"])
    parser.add_argument("--template", default="common", help=desc["template"])
    parser.add_argument("--project_type", default="py", help=desc["project_type"])
    parser.add_argument("--execute", action='store_true', help=desc["execute"])
    parser.add_argument("--package_name", default="", help=desc["package_name"])  
    parser.add_argument("--script_path", default="", help=desc["script_path"])
    parser.add_argument("--model", default="", help=desc["model"])
    parser.add_argument("--model_max_length", type=int, default=2000, help=desc["model_max_length"])
    parser.add_argument("--model_max_input_length", type=int, default=6000, help=desc["model_max_input_length"])
    parser.add_argument("--file", default=None, required=False, help=desc["file"])
    parser.add_argument("--anti_quota_limit", type=int, default=1, help=desc["anti_quota_limit"])
    parser.add_argument("--skip_build_index", action='store_false', help=desc["skip_build_index"])
    parser.add_argument("--print_request", action='store_true', help=desc["print_request"])
    parser.add_argument("--py_packages", required=False, default="", help=desc["py_packages"])
    parser.add_argument("--human_as_model", action='store_true', help=desc["human_as_model"])
    parser.add_argument("--urls", default="", help=desc["urls"])
    parser.add_argument("--search_engine", default="", help=desc["search_engine"])
    parser.add_argument("--search_engine_token", default="",help=desc["search_engine_token"])
    parser.add_argument("--auto_merge", action='store_true', help=desc["auto_merge"])

    revert_parser = subparsers.add_parser("revert", help=desc["revert_desc"])
    revert_parser.add_argument("--file", help=desc["revert_desc"])
    
    args = parser.parse_args()

    return AutoCoderArgs(**vars(args)),args


def main():
    args,raw_args = parse_args()
    
    if args.file:
        with open(args.file, "r") as f:
            config = yaml.safe_load(f)
            for key, value in config.items():
                if key != "file":  # 排除 --file 参数本身   
                    ## key: ENV {{VARIABLE_NAME}}
                    if isinstance(value, str) and value.startswith("ENV"):  
                        template = Template(value.removeprefix("ENV").strip())                  
                        value = template.render(os.environ)                        
                    setattr(args, key, value)

    if raw_args.command == "revert":        
        repo_path = args.source_dir

        file_content = open(args.file).read()
        md5 = hashlib.md5(file_content.encode('utf-8')).hexdigest()        
        file_name = os.path.basename(args.file)
        
        revert_result = git_utils.revert_changes(repo_path, f"auto_coder_{file_name}_{md5}")
        if revert_result:
            print(f"Successfully reverted changes for {args.file}")
        else:
            print(f"Failed to revert changes for {args.file}")
        return                  
    
    print("Command Line Arguments:")
    print("-" * 50)
    for arg, value in vars(args).items():
        print(f"{arg:20}: {value}")
    print("-" * 50)                
        
    from byzerllm.utils.client import EventCallbackResult,EventName
    from prompt_toolkit import prompt
    from prompt_toolkit.formatted_text import FormattedText
    def intercept_callback(llm,model: str, input_value: List[Dict[str, Any]]) -> EventCallbackResult:
                
        if input_value[0].get("embedding",False) or input_value[0].get("tokenizer",False) or input_value[0].get("apply_chat_template",False) or input_value[0].get("meta",False):
              return True,None
        if not input_value[0].pop("human_as_model",None):
            return True, None
        
        print(f"Intercepted request to model: {model}")        
        instruction = input_value[0]["instruction"] 
        history = input_value[0]["history"]
        final_ins = instruction + "\n".join([item["content"] for item in history])                    

        with open(args.target_file, "w") as f:
            f.write(final_ins)

        print(f'''\033[92m {final_ins[0:100]}....\n\n(The instruction to model have be saved in: {args.target_file})\033[0m''')    
        
        lines = []
        while True:
            line = prompt(FormattedText([("#00FF00", "> ")]), multiline=False)
            if line.strip() == "EOF":
                break
            lines.append(line)
        
        result = "\n".join(lines)

        with open(args.target_file, "w") as f:
            f.write(result)

        if result.lower() == 'c':
            return True, None
        else:            
            v = [{
              "predict":result,
              "input":input_value[0]["instruction"],
              "metadata":{}
            }]
            return False, v
        
    
    if args.model:
        byzerllm.connect_cluster()        
        llm = byzerllm.ByzerLLM(verbose=args.print_request)
        
        if args.human_as_model:
            llm.add_event_callback(EventName.BEFORE_CALL_MODEL, intercept_callback)

        llm.setup_template(model=args.model,template="auto")
        llm.setup_default_model_name(args.model)
        llm.setup_max_output_length(args.model,args.model_max_length)
        llm.setup_extra_generation_params(args.model, {"max_length": args.model_max_length})
    else:
        llm = None

    dispacher = Dispacher(args, llm)
    dispacher.dispach()

if __name__ == "__main__":
    main()
