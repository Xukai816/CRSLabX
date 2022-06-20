# @Time   : 2020/11/22
# @Author : Kun Zhou
# @Email  : francis_kun_zhou@163.com

# UPDATE:
# @Time   : 2020/11/23, 2021/1/9
# @Author : Kun Zhou, Xiaolei Wang
# @Email  : francis_kun_zhou@163.com, wxl1999@foxmail.com

import json
import os
import time
from pprint import pprint

import yaml
from loguru import logger
from tqdm import tqdm


class Config:
    """Configurator module that load the defined parameters."""

    def __init__(self, config_file, gpu='-1', debug=False):
        """Load parameters and set log level.

        Args:
            config_file (str): path to the config file, which should be in ``yaml`` format.
                You can use default config provided in the `Github repo`_, or write it by yourself.
            debug (bool, optional): whether to enable debug function during running. Defaults to False.

        .. _Github repo:
            https://github.com/RUCAIBox/CRSLab

        """

        # self.opt保存yaml文件解析为字典，保存各参数。
        self.opt = self.load_yaml_configs(config_file)
        print('self.opt:', self.opt)
        print('=======self.opt end=======')

        # gpu
        os.environ['CUDA_VISIBLE_DEVICES'] = gpu
        #os.environ['CUDA_VISIBLE_DEVICES'] = '1'
        self.opt['gpu'] = [i for i in range(len(gpu.split(',')))]
        #print(self.opt['gpu'])
        # dataset 选择数据集
        dataset = self.opt['dataset']
        tokenize = self.opt['tokenize']
        if isinstance(tokenize, dict):
            print('tokenize is a dict type')
            tokenize = ', '.join(tokenize.values())
        # model
        model = self.opt.get('model', None)
        rec_model = self.opt.get('rec_model', None) #推荐模型
        conv_model = self.opt.get('conv_model', None) #对话模型
        policy_model = self.opt.get('policy_model', None) #策略模型
        # 三个模型模型可以分开指定，也可以用一个参数指定
        if model:
            model_name = model
        else:
            models = []
            if rec_model:
                models.append(rec_model)
            if conv_model:
                models.append(conv_model)
            if policy_model:
                models.append(policy_model)
            model_name = '_'.join(models)
        self.opt['model_name'] = model_name
        # log 设置log名字
        log_name = self.opt.get("log_name",
                                dataset+'_'+model_name+'_'+time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime()))+".log"
        #设置保存日志的文件夹
        if not os.path.exists("log"):
            os.makedirs("log")
        logger.remove()
        if debug:
            level = 'DEBUG'
        else:
            level = 'INFO'
        logger.add(os.path.join("log", log_name), level=level)
        logger.add(lambda msg: tqdm.write(msg, end=''), colorize=True, level=level)

        logger.info(f"[Dataset: {dataset} tokenized in {tokenize}]")
        if model:
            logger.info(f'[Model: {model}]')
        if rec_model:
            logger.info(f'[Recommendation Model: {rec_model}]')
        if conv_model:
            logger.info(f'[Conversation Model: {conv_model}]')
        if policy_model:
            logger.info(f'[Policy Model: {policy_model}]')
        logger.info("[Config]" + '\n' + json.dumps(self.opt, indent=4))

    @staticmethod #修饰类中的方法,使其可以在不创建类实例的情况下调用方法
    def load_yaml_configs(filename):
        """This function reads ``yaml`` file to build config dictionary
        Args:
            filename (str): path to ``yaml`` config
        Returns:
            dict: config
        """
        config_dict = dict()
        with open(filename, 'r', encoding='utf-8') as f:
            config_dict.update(yaml.safe_load(f.read()))
        return config_dict

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError("index must be a str.")
        self.opt[key] = value

    def __getitem__(self, item):
        if item in self.opt:
            return self.opt[item]
        else:
            return None

    def get(self, item, default=None):
        """Get value of corrsponding item in config

        Args:
            item (str): key to query in config
            default (optional): default value for item if not found in config. Defaults to None.

        Returns:
            value of corrsponding item in config

        """
        if item in self.opt:
            return self.opt[item]
        else:
            return default

    def __contains__(self, key):
        #print('__contains__:using')
        if not isinstance(key, str):
            raise TypeError("index must be a str.")
        return key in self.opt

    def __str__(self):
        return str(self.opt)

    def __repr__(self):
        return self.__str__()

if __name__ == '__main__':
    opt_dict = Config('../../config/crs/kbrd/redial.yaml')
    print('=====')
    pprint(opt_dict)

    #print('datasets' in opt_dict)
    #print(opt_dict.__contains__('das'))
    #print(opt_dict['dataset'])
    #pprint(repr(opt_dict))
