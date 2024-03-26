from torch import nn
import scipy.io as sio 
import numpy as np
import glob
import math, multiprocessing, os
import torch
abspath = os.path.abspath(os.path.dirname(__file__))

class pool_layer(nn.Module):
    """
    The pooling layer on icosahedron discretized sphere using 1-ring filter
    
    Input: 
        N x D tensor
    Return:
        ((N+6)/4) x D tensor
    
    """  

    def __init__(self, neigh_orders, pooling_type='mean'):
        super(pool_layer, self).__init__()

        self.neigh_orders = neigh_orders
        self.pooling_type = pooling_type
        
    def forward(self, x):
        
        num_nodes = int((x.size()[0]+6)/4)
        feat_num = x.size()[1]
        x = x[self.neigh_orders[0:num_nodes*7]].view(num_nodes, 7, feat_num)
        if self.pooling_type == "mean":
            x = torch.mean(x, 1)
        if self.pooling_type == "max":
            x = torch.max(x, 1)
            assert(x[0].size() == torch.Size([num_nodes, feat_num]))
            return x[0], x[1]
        
        # assert x.size() == torch.Size([num_nodes, feat_num]), "assertion error"
                
        return x


def Get_neighs_order(rotated=0):
    neigh_orders_42 = get_neighs_order(42, rotated) #length 294 (42*7)
    neigh_orders_12 = get_neighs_order(12, rotated) #length 84 (12*7)
    
    return neigh_orders_42, neigh_orders_12
  

def get_neighs_order(n_vertex, rotated=0):
    adj_mat_order = sio.loadmat(abspath +'/neigh_indices/adj_mat_order_'+ \
                                str(n_vertex) +'_rotated_' + str(rotated) + '.mat')
    adj_mat_order = adj_mat_order['adj_mat_order']
    neigh_orders = np.zeros((len(adj_mat_order), 7))
    neigh_orders[:,0:6] = adj_mat_order-1
    neigh_orders[:,6] = np.arange(len(adj_mat_order))
    neigh_orders = np.ravel(neigh_orders).astype(np.int64)
    
    return neigh_orders


def Get_upconv_index(rotated=0):
    
    upconv_top_index_163842, upconv_down_index_163842 = get_upconv_index(abspath+'/neigh_indices/adj_mat_order_163842_rotated_' + str(rotated) + '.mat')
    upconv_top_index_40962, upconv_down_index_40962 = get_upconv_index(abspath+'/neigh_indices/adj_mat_order_40962_rotated_' + str(rotated) + '.mat')
    upconv_top_index_10242, upconv_down_index_10242 = get_upconv_index(abspath+'/neigh_indices/adj_mat_order_10242_rotated_' + str(rotated) + '.mat')
    upconv_top_index_2562, upconv_down_index_2562 = get_upconv_index(abspath+'/neigh_indices/adj_mat_order_2562_rotated_' + str(rotated) + '.mat')
    upconv_top_index_642, upconv_down_index_642 = get_upconv_index(abspath+'/neigh_indices/adj_mat_order_642_rotated_' + str(rotated) + '.mat')
    upconv_top_index_162, upconv_down_index_162 = get_upconv_index(abspath+'/neigh_indices/adj_mat_order_162_rotated_' + str(rotated) + '.mat')
    
    #TODO: return tuples of each level
    return upconv_top_index_163842, upconv_down_index_163842, upconv_top_index_40962, upconv_down_index_40962, upconv_top_index_10242, upconv_down_index_10242,  upconv_top_index_2562, upconv_down_index_2562,  upconv_top_index_642, upconv_down_index_642, upconv_top_index_162, upconv_down_index_162


def get_upconv_index(order_path):  
    adj_mat_order = sio.loadmat(order_path)
    adj_mat_order = adj_mat_order['adj_mat_order']
    adj_mat_order = adj_mat_order -1
    nodes = len(adj_mat_order)
    next_nodes = int((len(adj_mat_order)+6)/4)
    upconv_top_index = np.zeros(next_nodes).astype(np.int64) - 1
    for i in range(next_nodes):
        upconv_top_index[i] = i * 7 + 6
    upconv_down_index = np.zeros((nodes-next_nodes) * 2).astype(np.int64) - 1
    for i in range(next_nodes, nodes):
        raw_neigh_order = adj_mat_order[i]
        parent_nodes = raw_neigh_order[raw_neigh_order < next_nodes]
        assert(len(parent_nodes) == 2)
        for j in range(2):
            parent_neigh = adj_mat_order[parent_nodes[j]]
            index = np.where(parent_neigh == i)[0][0]
            upconv_down_index[(i-next_nodes)*2 + j] = parent_nodes[j] * 7 + index
    
    return upconv_top_index, upconv_down_index



class onering_conv_layer(nn.Module):
    """The convolutional layer on icosahedron discretized sphere using 
    1-ring filter
    
    Parameters:
            in_feats (int) - - input features/channels
            out_feats (int) - - output features/channels
            
    Input: 
        N x in_feats tensor
    Return:
        N x out_feats tensor
    """  
    def __init__(self, in_feats, out_feats, neigh_orders, neigh_indices=None, neigh_weights=None):
        super(onering_conv_layer, self).__init__()

        self.in_feats = in_feats
        self.out_feats = out_feats
        self.neigh_orders = neigh_orders

        self.weight = nn.Linear(7 * in_feats, out_feats)
        
    def forward(self, x):
        # import pdb
        # pdb.set_trace()
        mat = x[:,self.neigh_orders:,]  # Select specific neighboring orders
        # batch_size, num_orders, features = mat.size()

        # Reshape mat to [batch_size, 7 * in_feats]
        mat = mat.view(len(x), 7 * self.in_feats)
                
        out_features = self.weight(mat)
        return out_features


class onering_conv_layer_batch(nn.Module):
    """
    The convolutional layer on icosahedron discretized sphere using 1-ring filter

    Parameters:
        in_feats (int) - - input features/channels
        out_feats (int) - - output features/channels
        
    Input: 
        B x N x in_feats tensor
    Return:
        B x N x out_feats tensor
    """  
    def __init__(self, in_feats, out_feats, neigh_orders, neigh_indices=None, neigh_weights=None, drop_rate=None):
        super(onering_conv_layer_batch, self).__init__()

        self.in_feats = in_feats
        self.out_feats = out_feats
        self.neigh_orders = neigh_orders
        
        self.weight = nn.Linear(7 * in_feats, out_feats)
        print(self.weight)
        
    def forward(self, x):
        # import pdb
        # pdb.set_trace()

        x = x.permute(0, 2, 1)
        print(x.shape)
        mat = x[:, :, self.neigh_orders].view(x.shape[0], x.shape[2], 7*self.in_feats)
        # mat = x[:, self.neigh_orders, :]
        print(mat.shape)
        
        # import pdb
        # pdb.set_trace()
        out_features = self.weight(mat)
        # out_features = self.weight(mat).permute(0, 2, 1)

        return out_features