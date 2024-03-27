import math
import timeit

import numpy as np
import matplotlib.pyplot as plt
import torch





def cal_dEdxyz_ddp(aevs, E, daev, inds):
        dEdxyz = [[] for b in range(E.shape[0])]
        fa = torch.autograd.grad(outputs=E.sum(), inputs=aevs, create_graph=True)
        for i in range(E.shape[0]):
                t1 = timeit.default_timer()
                dE = torch.zeros((len(daev[0][0][0])), device=E.device)
                for t in range(len(inds)):
                    #print(inds[t])
                    for j in torch.nonzero(sum([inds[t] == i]), as_tuple=True)[0]:
                        dE = dE + torch.matmul(fa[t][j], daev[t][j])

                #for j in torch.nonzero(sum([inds[0] == i]), as_tuple=True)[0]:
                #        dE = dE + torch.matmul(fa[0][j], daev[0][j])
                #for j in torch.nonzero(sum([inds[1] == i]), as_tuple=True)[0]:
                #        dE = dE + torch.matmul(fa[1][j], daev[1][j])

                dEdxyz[i] = dE

        return dEdxyz



