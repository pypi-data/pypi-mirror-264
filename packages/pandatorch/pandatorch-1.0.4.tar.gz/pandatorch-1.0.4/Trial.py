
import numpy as np
import pandas as pd


from pandatorch.data import DataFrame
from pandatorch.model import TorchModel


df=pd.read_csv("notebooks/IRIS.csv")

torch_df=DataFrame(X=df.drop("species",axis=1),y=df['species'])


torch_df.df  


torch_df.features[:5]


torch_df.target[:5]


torch_df.class_to_idx


import torch
from torch import nn
from torch.utils.data import DataLoader


loader=DataLoader(torch_df,batch_size=20)


class Net(TorchModel):
    
    def __init__(self):
        super().__init__()
        self.l1 = nn.Linear(
            in_features=torch_df.get_number_of_columns(torch_df.features),
            out_features=5,
        )
        self.output = nn.Linear(5, 3)
        self.softmax = nn.Softmax(dim=1)
        self.relu = nn.ReLU()

    def loss(self, outputs, targets):
        if targets is None:
            return None
        criterion = nn.CrossEntropyLoss().to(device)
        return criterion(outputs, targets)

    def forward(self, x, targets=None):
        x = self.relu(self.l1(x))
        outputs = self.softmax(self.output(x))
        loss = self.loss(outputs, targets)
        return outputs, loss



# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = 'cuda:0'
print(device)



from sklearn import metrics


model=Net()
optimizer=torch.optim.Adam(model.parameters())
val={"MAE":metrics.mean_absolute_error,"MSE":metrics.mean_squared_error}
losses=model.fit(torch_df,batch_size=1,epochs=30,device="cuda:0",optimizer=optimizer,metrics=val)


print(losses)


from sklearn.metrics import mean_absolute_error


zeros=np.zeros_like(losses)
print(zeros)


mean_absolute_error(zeros,losses)


print(losses)







