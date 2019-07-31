import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.preprocessing import OneHotEncoder

if __name__ == "__main__":

    """
    在咱数据工程资源组的 “预测BA带来的收益增长”项目中，除了excel里的数据分析组件做多元线性回归，python的sklearn包也能实现。
    
    在这里简单展示。
    """

    # 读取训练集.xlsx文件，并且拿出两个x一个y
    df = pd.read_excel(r'E:\CETC-BDRI-2019\数据工程资源组\刘芳菱新任务1：数据分析解决业务问题\Business_Analyst_China-'
                       r'master\商业数据分析（入门）\项目二：预测邮寄产品目录带来的收入增长\p1-customers.xlsx',
                       )[["Customer Segment", "Avg Num Products Purchased", "Avg Sale Amount"]]
    print(df.columns)

    # 两个x，即两个特征中，有一个是文本型变量（类型），需要转换成 “one-hot vector”
    ohe = OneHotEncoder()
    cl_cus_seg = ohe.fit_transform(np.array(df['Customer Segment'].values).reshape(-1, 1)).toarray()

    # 把上一步转换好的类型变量x1，和数值变量x2拼在一起，组成X
    features = pd.concat([pd.DataFrame(cl_cus_seg), df['Avg Num Products Purchased']], axis=1)

    # 获取label y
    y = df['Avg Sale Amount']

    # 把 X 和 y 丢进去训练
    regr = linear_model.LinearRegression()
    regr.fit(features, y)

    print('coefficients(b1,b2...):', regr.coef_)
    print('intercept(b0):', regr.intercept_)

    # 训练集上最后正确度
    print(regr.score(features, y))

    # 预测
    test = pd.read_excel(r'E:\CETC-BDRI-2019\数据工程资源组\刘芳菱新任务1：数据分析解决业务问题\Business_Analyst_China-'
                         r'master\商业数据分析（入门）\项目二：预测邮寄产品目录带来的收入增长\p1-mailinglist.xlsx')

    test_set = test[["Customer Segment", "Avg Num Products Purchased"]]
    cl_cus_seg_test = ohe.fit_transform(np.array(test_set['Customer Segment'].values).reshape(-1, 1)).toarray()

    # 把上一步转换好的类型变量x1，和数值变量x2拼在一起，组成X
    X_test = pd.concat([pd.DataFrame(cl_cus_seg_test), test_set['Avg Num Products Purchased']], axis=1)

    test['y_Avg Num Products Purchased'] = regr.predict(X_test)
    test['income'] = test.apply(lambda x: x[12]*x[11]*0.5-6.5, axis=1)
    print(sum(test['income']))
