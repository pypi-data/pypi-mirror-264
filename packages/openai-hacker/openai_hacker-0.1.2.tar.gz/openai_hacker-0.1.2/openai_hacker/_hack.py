import json
import os
import tarfile
import time
from collections import defaultdict
from io import BytesIO
from typing import Optional, Callable

import yaml
from joblib import Memory

from openai_hacker import conf

try:
    from openai.api_resources import Completion, ChatCompletion
except ImportError:
    from openai.resources.completions import Completions as Completion
    from openai.resources.chat.completions import Completions as ChatCompletion

fn_chat_create_original = ChatCompletion.create
fn_text_create_original = Completion.create

fn_chat_create_cached: Optional[Callable] = None
fn_text_create_cached: Optional[Callable] = None

counters = defaultdict(int)


def yaml_str_presenter(dumper, data):
    lines = data.splitlines()
    if len(lines) > 1:  # check for multiline string
        output = '\n'.join(map(lambda s: s.rstrip(), lines))
        return dumper.represent_scalar('tag:yaml.org,2002:str', output, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


yaml.add_representer(str, yaml_str_presenter)
yaml.representer.SafeRepresenter.add_representer(str, yaml_str_presenter)


def json_default(obj):
    try:
        return obj.__dict__
    except:
        return None


def init_cache():
    assert conf.cache_dir

    global fn_text_create_cached, fn_chat_create_cached

    if conf.cache_dir:
        mem = Memory(location=conf.cache_dir, verbose=0)
        fn_chat_create_cached = mem.cache(fn_chat_create_original)
        fn_text_create_cached = mem.cache(fn_text_create_original)
    else:
        fn_chat_create_cached = None
        fn_text_create_cached = None


def get_next_dump_file(chat: bool):
    counters[conf.stage] += 1
    n_counter = counters[conf.stage]
    suffix = conf.suffix_chat if chat else conf.suffix_completion
    dump_file = f'{conf.stage}_{n_counter:03d}{suffix}'
    return dump_file


def dump_data(file_name: str, data):
    if file_name.endswith('.json'):
        content = json.dumps(data, ensure_ascii=False, indent=2, default=json_default)
    else:  # default as yaml
        js_str = json.dumps(data, ensure_ascii=False, indent=2, default=json_default)
        js_data = json.loads(js_str)
        content = yaml.dump(js_data, allow_unicode=True)

    content = content.encode('utf-8')
    work_dir = os.path.abspath(os.path.expanduser(conf.dump_dir))
    if work_dir.endswith('.tar'):  # dump as tarball
        base_dir = os.path.split(work_dir)[0]
        os.makedirs(base_dir, exist_ok=True)

        with tarfile.open(work_dir, 'a') as tar:
            tar_info = tarfile.TarInfo(file_name)
            tar_info.size = len(content)
            tar_info.mtime = time.time()
            tar_info.uid = os.getuid()
            tar_info.gid = os.getgid()
            tar.addfile(tar_info, BytesIO(content))
    else:  # dump as multi-files
        os.makedirs(work_dir, exist_ok=True)
        file_path = os.path.join(work_dir, file_name)
        with open(file_path, 'wb') as f:
            f.write(content)


def hacked_text_create(*args, **kwargs):
    log_file = get_next_dump_file(False)
    r = None
    try:
        if fn_text_create_cached is not None:
            r = fn_text_create_cached(*args, **kwargs)
        else:
            r = fn_text_create_original(*args, **kwargs)

        log_data = dict(request=kwargs, response=r)
        dump_data(log_file, log_data)
        return r
    except KeyboardInterrupt:
        raise
    except AttributeError:
        return r  # ignore
    except Exception as e:
        log_data = dict(request=kwargs, response=str(e))
        dump_data(log_file, log_data)
        raise


def hacked_chat_create(*args, **kwargs):
    log_file = get_next_dump_file(True)
    r = None
    try:
        if fn_chat_create_cached is not None:
            r = fn_chat_create_cached(*args, **kwargs)
        else:
            r = fn_chat_create_original(*args, **kwargs)

        log_data = dict(request=kwargs, response=r.__dict__)
        dump_data(log_file, log_data)
        return r
    except KeyboardInterrupt:
        raise
    except AttributeError:
        return r  # ignore
    except Exception as e:
        log_data = dict(request=kwargs, response=str(e))
        dump_data(log_file, log_data)
        raise


def hack(stage: str = None, dump_dir: str = None, cache_dir: str = None,
         suffix_chat: str = None, suffix_completion: str = None,
         hack_chat: bool = True, hack_completion: bool = True):
    if stage:
        conf.stage = stage

    if dump_dir:
        if dump_dir.endswith('.tar') and os.path.exists(dump_dir):
            os.remove(dump_dir)
        conf.dump_dir = dump_dir

    if cache_dir is not None:
        conf.cache_dir = cache_dir

    if conf.cache_dir:
        init_cache()

    if suffix_chat:
        conf.suffix_chat = suffix_chat

    if suffix_completion:
        conf.suffix_completion = suffix_completion

    if hack_chat:
        ChatCompletion.create = hacked_chat_create

    if hack_completion:
        Completion.create = hacked_text_create


def foo_tar():
    from io import BytesIO
    buf = BytesIO()
    buf.write(b'hihi,hasdfaha\n')
    data = buf.getvalue()

    tar = tarfile.open('foo.tar', 'a')
    tar.close()
    print('done')


if __name__ == '__main__':
    foo_tar()
