from TESTING_C_SDK.data_load.read_data.load_data import data_loading


def read_csv(filename):
    obj = data_loading()
    return (obj._load_csv(filename))
    
    #def read_excel(self,filename):
        