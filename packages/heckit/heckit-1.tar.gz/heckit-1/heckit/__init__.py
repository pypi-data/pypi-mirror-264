import pyperclip as pc
    
def imports():
    s = '''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy.stats as sts
import warnings
warnings.filterwarnings("ignore")
    '''
    return pc.copy(s)
    
def analiz():
    s = '''data1 = pd.read_excel(r'C:\kr.xlsx', sheet_name='1.1')
print(data1.head())
print(data1.shape)
print(data1.info())

plt.figure(figsize=(10, 6))
plt.plot(data1['T'], data1['Y'], color='blue', marker='o', linestyle='-')
plt.title('Временной ряд')
plt.xlabel('Год')
plt.ylabel('Значение')
plt.grid(True)
plt.show()
    '''
    return pc.copy(s)
    
def irvin():
    s = '''result = pd.DataFrame()  
y = data1['Y']
n = len(y)
result['y'] = y

# Вычисляем среднеквадратическое отклонение
S_y = np.sqrt(sum([(y[i] - y.mean()) ** 2 for i in range(n)]) / (n - 1))

# Вычисляем величину l_t для наблюдений
l_t = [0] + [abs(y[i] - y[i - 1]) / S_y for i in range(1, n)]
result['lambda'] = l_t

# Если величина l_t превышает табличный уровень, то значение y_t считается аномальным
difference = data1['Y'].diff()
lamb = np.abs(difference)/S_y
l_kririch = 1.478*(n/10)**(-0.1767)

result_normal = result[result['lambda'] <= l_kririch]  # Убираем аномалии из таблицы

# Проводим анализ по методу Ирвина
anomalies = result[result['lambda'] > l_kririch]
num_anomalies = len(anomalies)

if num_anomalies == 0:
    print("Аномалий не обнаружено.")
else:
    print(f"Обнаружено {num_anomalies} аномалий:")
    print(anomalies)

# Отобразим таблицу без аномалий
print("\nТаблица без аномалий:")
print(result_normal)

#Используя метод Ирвина проанализировани датасет на аномальные значения. Таких не оказалось => Датасет оставляем без изменений.
    '''
    return pc.copy(s)

def foster():
    s = '''from scipy.stats import t
def foster_stuart(y):
n = len(y)
k = [1] + [0]*(n - 1)
l = [1] + [0]*(n - 1)
for t in range(1, n):
    if y[t] > max(y[:t]): k[t] = 1 
    if y[t] < min(y[:t]): l[t] = 1 
k = np.array(k)
l = np.array(l)
s = sum(k[1:]+l[1:])
d = sum(k[1:]-l[1:])
mu_s = (1.693872*np.log(n) - 0.299015)/(1 - 0.035092*np.log(n) + 0.002705*np.log(n)**2)
mu_d = 0
sigma_s = np.sqrt(2*np.log(n)-3.4253)
sigma_d = np.sqrt(2*np.log(n)-0.8456)
t_s = np.abs(s - mu_s)/sigma_s
t_d = np.abs(d - mu_d)/sigma_d
trend = "Тренд отсутствует"
if t_s > t_kr and t_d > t_kr:
    trend = "Есть тренд и тренд дисперсии"
elif t_s > t_kr:
    trend = "Есть тренд"
elif t_d > t_kr:
    trend = "Есть тренд дисперсии"
return trend, t_s, t_d
alpha = 0.05
t_kr = t.ppf(1 - alpha/2, df = len(y) - 1)
result = foster_stuart(y)
print("Результаты теста Фостера-Стьюарта:", result)
    '''
    return pc.copy(s)
    
def prognoz5():
    s = '''from sklearn.linear_model import LinearRegression
x = data1.drop(columns=['Y'])
X_train = x[:-5]
X_test = x[-5:]
y_train = y[:-5]
y_test = y[-5:]
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
linear_pred = linear_model.predict(X_test)
linear_mse = mean_squared_error(y_test, linear_pred)
print(linear_mse)
y_pred = linear_model.predict(x)
plt.plot(y)
plt.plot(y_pred)
plt.show()

from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
degree = 2 
polynomial_model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
polynomial_model.fit(X_train, y_train)
polynomial_pred = polynomial_model.predict(X_test)
polynomial_mse = mean_squared_error(y_test, polynomial_pred)
print(polynomial_mse)
y_pred = polynomial_model.predict(x)
plt.plot(y)
plt.plot(y_pred)
plt.show()

# Выбор оптимальной модели
if linear_mse < polynomial_mse:
    optimal_model = linear_model
    print("Выбрана линейная модель")
else:
    optimal_model = polynomial_mse
    print("Выбрана полиномиальная модель")
# Построение прогноза для следующих 5 точек
future_data = x[-5:]    
forecast = optimal_model.predict(future_data)
forecast
#Выбрана линейная модель тк в ней MSE наименьшее. По ней сделаны прогнозные значения.
    '''
    return pc.copy(s)
    
def predobr():
    s = '''data2 = pd.read_excel(r'C:\kr.xlsx', sheet_name='3.1')
print(data2.head())
print(data2.info())
#Все данные числовые, нет пропущенных значений => не проводим доп обработку данных.
#Распределение признаков и целевой переменной
data2.hist(figsize=(10, 10))
plt.show()
# Определение и устранение выбросов
# Использую межквартильный размах
Q1 = data2.quantile(0.25)
Q3 = data2.quantile(0.75)
IQR = Q3 - Q1
data_no_outliers = data2[~((data2 < (Q1 - 1.5 * IQR)) | (data2 > (Q3 + 1.5 * IQR))).any(axis=1)]
data_no_outliers
# Посмотреть на соотношение классов
class_counts = data2['Class'].value_counts()
print(class_counts)
# Гистограмма классов
plt.bar(class_counts.index, class_counts.values)
plt.xlabel('Class')
plt.ylabel('Count')
plt.title('Class Distribution')
plt.show()
#Классы несбалансированы, это может повлиять на обучение модели, тк классов 0 больше, она может быть более склонна к его прогнозированию с большей точностью.
#Но терять данные мы не хотим, поэтому оставлим так.
    '''
    return pc.copy(s)

def imports2():
    s = '''import pandas as pd
import numpy as np
import seaborn as sns
import statsmodels.api as sm
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix, precision_score, recall_score
import matplotlib.pyplot as plt
from scipy.stats import *
from sklearn.metrics import r2_score, explained_variance_score
from sympy import *
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.model_selection import train_test_split
    '''
    return pc.copy(s)
   
def sredn():
    s = '''import numpy as np
from scipy.stats import ttest_ind
from scipy.stats import f,t
def check_trend_sr(data):
    alpha = 0.01
    split_index = len(data) // 2
    first_half = data[:split_index]
    second_half = data[split_index:]
    # Вычисляем средние значения для двух половин
    mean_first = np.mean(first_half)
    mean_second = np.mean(second_half)
    var_first = np.var(first_half)
    var_second = np.var(second_half)
    f_value = var_first / var_second if var_first > var_second else var_second / var_first
    critical_value_f = f.ppf(1 - alpha, len(first_half)-1, len(second_half)-1)
    n1 = len(first_half)
    n2 = len(second_half)
    sigma = np.sqrt(((n1-1)*var_first + (n2-1)*var_second)/((n1+n2-2)))
    t_value = abs((mean_first - mean_second))/sigma*np.sqrt(1/len(first_half)+1/len(second_half))
    crit_t = t.ppf(1-alpha,len(first_half)+len(second_half)-2)
    if t_value<crit_t and f_value >= critical_value_f:
        print("Тренд не обнаружен")
    else:
        print("Обнаружен тренд в данных")
    print(t_value,f_value,crit_t,critical_value_f)
check_trend_sr(data['IP2_CEA_M'])
    '''
    return pc.copy(s)

def logit_probit():
    s = '''X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=3)
X0 = sm.add_constant(X_train) #строим логит модель
log_reg0 = sm.Logit(y_train, X0)
result = log_reg0.fit()
result.summary()

X0 = sm.add_constant(X_train) #строим пробит модель
prob = sm.Probit(y_train, X0)
result_prob = prob.fit()
result_prob.summary()
    '''
    return pc.copy(s)

def metriki():
    s = '''X0 = sm.add_constant(X_test)
y_pred = result.predict(X0) #for logit
y_pred = result_prob.predict(X0) #for probit
y_pred[y_pred > 0.5] = 1
y_pred[y_pred < 0.5] = 0
print(accuracy_score(y_test, y_pred))
print(f1_score(y_test, y_pred))
print(precision_score(y_test, y_pred))
print(recall_score(y_test, y_pred))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True)
    '''
    return pc.copy(s)

def procent():
    s = '''#logit
X0 = sm.add_constant(X_train) 
prob = sm.Logit(y_train, X0) # строим Логит модель
result_prob = prob.fit()
X0 = sm.add_constant(X_test)
y_pred = result_prob.predict(X0)
y_pred[y_pred >= 0.7] = 1 # Стало
y_pred[y_pred < 0.7] = 0
y_pred.value_counts()
#probit
X0 = sm.add_constant(X_train) 
prob = sm.Probit(y_train, X0) # строим пробит модель
result_prob = prob.fit()
X0 = sm.add_constant(X_test)
y_pred = result_prob.predict(X0)
y_pred[y_pred >= 0.7] = 1 # Стало
y_pred[y_pred < 0.7] = 0
y_pred.value_counts()
    '''
    return pc.copy(s)
    
def holt():
    s = '''from statsmodels.tsa.api import ExponentialSmoothing
model = ExponentialSmoothing(Y_new, seasonal_periods=12, trend='add', seasonal='add').fit()
model.params
# Предсказанные значения на 4 периода вперёд
pred = model.forecast(4)
print(pred)
ax = Y_new.plot(title='Прогноз методом Хольта Уинтерса', label='Данные')
model.fittedvalues.plot(ax=ax, style='--', c='g', label='Предсказанные значения')
model.forecast(4).plot(ax=ax, c='r', label='Прогноз на 4 периода')
plt.legend()
plt.show()
    '''
    return pc.copy(s)