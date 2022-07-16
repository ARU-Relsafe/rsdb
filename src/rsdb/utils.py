import rsdb_.orm as orm
from scipy.stats import beta, gamma, lognorm, norm
import numpy as np

def up_while_or(node: orm.FTNode) -> orm.FTNode|None:
    """Поднимаемся наверх по дереву пока встречаются ИЛИ гейты или начало дерева отказов"""
    gate = node.Event
    if gate.Symbol == orm.SymbolEnum.OR.value:
        if node.Transfer == orm.TransferEnum.Yes.value or node.FatherNode is None:
            return node
        else:
            result = up_while_or(node.FatherNode)
            if result is None:
                return node
            return result
    return None

def et_propagate(event_tree: orm.EventTree, back_propagate=False, recursive=False):
    pass

def get_distribution(param: orm.Param):
    """
    The function returns the distribution object of scipy
    """
    if param.DistType==orm.DistributionEnum.Gamma.value:
        # для гамма распределения
        # a-shape (k)
        # scale-theta scale (mean=shape*scale)
        return gamma(a=param.DistPar1, scale=param.DistPar1/param.Mean)
    elif param.DistType==orm.DistributionEnum.Beta.value:
        # для бета распределения
        # a-alpha shape
        # b-beta shape (mean=alpha/(alpha-beta)
        return beta(a=param.DistPar1, b=param.DistPar1/param.Mean-param.DistPar1)
    elif param.DistType==orm.DistributionEnum.Lognormal.value:
        # для лог-нормлаьного распределения
        # s-среднеквадратическое отклонение (EF=p95/p50) (sigma=log(EF)/CI90)
        # scale-медиана (scale=exp(mu))
        ef = param.DistPar1
        m = param.Mean
        ci90 = 1.64485363
        sigma = np.log(ef)/ci90
        med = m*np.exp(-(sigma**2)/2)
        return lognorm(s=sigma, scale = med)
    elif param.DistType==orm.DistributionEnum.Normal.value:
        return norm(loc=param.Mean, scale=param.DistPar1)
    else:
        return None