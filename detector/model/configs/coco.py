from .base import commen, data, model, train, test

data.scale = None

model.heads['ct_hm'] = 3

train.batch_size = 4
train.epoch = 150
train.dataset = 'smoke_train'

test.dataset = 'smoke_val'

class config(object):
    commen = commen
    data = data
    model = model
    train = train
    test = test