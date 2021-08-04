# @Time   : 2020/11/22
# @Author : Kun Zhou
# @Email  : francis_kun_zhou@163.com

# UPDATE:
# @Time   : 2020/11/24, 2020/12/29, 2020/12/17, 2021/8/4
# @Author : Kun Zhou, Xiaolei Wang, Yuanhang Zhou, Chenzhan Shang
# @Email  : francis_kun_zhou@163.com, wxl1999@foxmail.com, sdzyh002@gmail.com, czshang@outlook.com

from crslab.agent.supervised import *
from crslab.agent.interactive import *

agent_register_table = {
    'KGSF': KGSFAgent,
    'KBRD': KBRDAgent,
    'TGReDial': TGReDialAgent,
    'TGRec': TGReDialAgent,
    'TGConv': TGReDialAgent,
    'TGPolicy': TGReDialAgent,
    'TGRec_TGConv': TGReDialAgent,
    'TGRec_TGConv_TGPolicy': TGReDialAgent,
    'ReDialRec': ReDialAgent,
    'ReDialConv': ReDialAgent,
    'ReDialRec_ReDialConv': ReDialAgent,
    'InspiredRec_InspiredConv': InspiredAgent,
    'BERT': TGReDialAgent,
    'SASREC': TGReDialAgent,
    'TextCNN': TGReDialAgent,
    'GRU4REC': TGReDialAgent,
    'Popularity': TGReDialAgent,
    'Transformer': KGSFAgent,
    'GPT2': TGReDialAgent,
    'ConvBERT': TGReDialAgent,
    'TopicBERT': TGReDialAgent,
    'ProfileBERT': TGReDialAgent,
    'MGCG': TGReDialAgent,
    'PMI': TGReDialAgent,
    'SCPR': SCPRAgent,
    'EAR': EARAgent
}


def get_agent(opt, dataset, vocab):
    """get supervised to batchify dataset

    Args:
        opt (Config or dict): config for supervised or the whole system.
        dataset: processed raw data, no side data.
        vocab (dict): all kinds of useful size, idx and map between token and idx.

    Returns:
        supervised

    """
    model_name = opt['model_name']
    if model_name in agent_register_table:
        return agent_register_table[model_name](opt, dataset, vocab)
    else:
        raise NotImplementedError(f'The supervised [{model_name}] has not been implemented')

