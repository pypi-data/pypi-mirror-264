import streamlit as st
from streamlit_ace import st_ace

from collections.abc import Iterable
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from io import StringIO

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer

from sklearn.decomposition import PCA

from sklearn.pipeline import Pipeline     
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import ShuffleSplit
from sklearn import set_config
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.metrics import confusion_matrix

#from patsy import dmatrix


set_config(display="diagram")
pd.set_option("styler.render.max_elements", 999_999_999_999)


def next_page():
    
    st.session_state.counter += 1


def previous_page():
    
    st.session_state.counter -= 1


@st.cache_data
def to_dataframe(datafile):
    
    if datafile is not None:
        if datafile.name[-4:] == '.csv':
            data = pd.read_csv(datafile)
        elif datafile.name[-4:] == '.xls' or datafile.name[-5:] == '.xlsx':
            data = pd.read_excel(datafile)
        else:
            data = None
    else:
        data = None
    
    return data


def read_data():
    
    st.sidebar.write('## Upload Data')
    
    newfile = st.sidebar.file_uploader('Upload the Data File', type=['csv', 'xlsx', 'xls'], 
                                       disabled=False)
    
    if newfile is not None:
        datafile = newfile
        data = data = to_dataframe(datafile)
        st.session_state.dataset = data
    else:
        if 'dataset' in st.session_state:
            datafile = True
            data = st.session_state.dataset
        else:
            datafile = None
            data = None
    
    if data is not None:
        st.write(data)
        st.write(f'{data.shape[0]} columns x {data.shape[1]} rows')
    
    _, _, col3 = st.sidebar.columns([1, 1, 1])
    disable_next = datafile is None
    
    with col3:
        st.button('Next', key='forward_to_step1', disabled=disable_next, on_click=next_page)


def show_value_counts(this_column):
    
    select_var = this_column.name
    tab1, tab2 = st.tabs(["Preview", "Code"])
    direction = st.sidebar.radio('Plot Direction', options=['Vertical', 'Horizontal'])
    yvalue = st.sidebar.radio('Type of Y-Data', options=['Frequency', 'Density'])
    color = st.sidebar.color_picker('Color', value='#1f77b4')
    with tab1:
        fig = plt.figure(figsize=(8, 5.5))
        if direction == 'Vertical':
            value_counts = this_column.value_counts(normalize=yvalue=='Density')
            plt.bar(value_counts.index, value_counts.values, color=color)
            plt.xticks(rotation=90, fontsize=16)
            plt.ylabel(yvalue, fontsize=16)
        else:
            value_counts = this_column.value_counts(normalize=yvalue=='Density').iloc[::-1]
            plt.barh(value_counts.index, value_counts.values, color=color)
            plt.yticks(fontsize=16)
            plt.xlabel(yvalue, fontsize=16)
        st.pyplot(fig)
            
    with tab2:
        if direction == 'Vertical':
            code_bp = (f"plt.bar(value_counts.index, value_counts.values, color='{color}')\n" 
                       "plt.xticks(rotation=90, fontsize=16)\n"
                       f"plt.ylabel('{yvalue}', fontsize=16)")
        else:
            code_bp = (f"value_counts = value_counts.iloc[::-1]\n"
                       f"plt.barh(value_counts.index, value_counts.values, color='{color}')\n"
                       "plt.yticks(fontsize=16)\n" 
                       f"plt.xlabel('{yvalue}', fontsize=16)")
            
        code_string = ("```python\n" 
                       "import matplotlib.pyplot as plt\n" 
                       "\n" 
                       f"this_column = data['{select_var}']\n" 
                       f"value_counts = this_column.value_counts(normalize={yvalue=='Density'})\n"
                       f"{code_bp}\n" 
                       "plt.show()")
        st.write(code_string)
    

def one_step(step_name, step_call, attributes, defaults, fixed={}):

    step = (step_name, step_call(**fixed))
    fixed_string = ', '.join([f"{p}={v}" for p, v in fixed.items()])
    step_string = f"('{step_name}', {step_call.__name__}({fixed_string}))"

    params = {}
    param_strings = []
    for attr, dv in zip(attributes, defaults):
        with st.sidebar:
            #col1, col2 = st.sidebar.columns([1, 3.1])
            label = f'<p class="small-font" style="margin-bottom:0px">{attr}:</p>'
            st.markdown(label, unsafe_allow_html=True)
            expr = st_ace(value="", placeholder=str(dv), language='python',
                          show_gutter=False, show_print_margin=True, font_size=16,
                          min_lines=1, max_lines=1, key=f'step_name_{attr}')

            if len(expr.strip()) > 0:
                try:
                    values = eval(expr)
                except Exception as e:
                    values = dv
                    st.sidebar.error(str(e) + f' \n\nThe value is reset to {dv}')
            else:
                expr = str(dv) #if not isinstance(dv, str) else f"'{dv}'"
                values = dv
            
            if not isinstance(values, Iterable) or isinstance(values, str):
                values = [values]
                expr = str(values)
            
            params[f"{step_name}__{attr}"] = values
            param_strings.append(f"'{step_name}__{attr}': {expr}")

    return step, params, step_string, param_strings


def variable_analysis():
    
    st.sidebar.write('## Analysis on Variables')
    
    data = st.session_state['dataset']
    
    how = st.sidebar.selectbox('Information on Variables', ['Distribution', 'Correlation'])
    st.sidebar.write('---')
    
    if how == 'Correlation':
        st.write('### Correlation Matrix')
        
        
        num_columns = data.select_dtypes(include='number').columns
        cat_data = data.drop(columns=num_columns)
        col_labels = st.sidebar.multiselect('Select Numerical Variables', 
                                            options=num_columns, default=list(num_columns))
        st.write(data[col_labels].corr())
        
        hue_label = st.sidebar.selectbox('Select a Categorical Varaible', 
                                         options=[None] + list(cat_data.columns))
        kind = st.sidebar.selectbox('Type of Plots', options=['scatter', 'kde', 'hist', 'reg'])
        diag_kind = st.sidebar.selectbox('Type of Diagonal Plots', options=['hist', 'kde'])
        corner = st.sidebar.checkbox('Display Only Corner', value=False)
        
        st.write('### Data Visualization')
        tab1, tab2 = st.tabs(["Preview", "Code"])
        
        with tab1:
            if kind in ['scatter', 'kde']:
                plot_kws=dict(s=20*len(col_labels), linewidth=1, alpha=0.6)
            elif kind == 'reg':
                plot_kws=dict(line_kws=dict(color="r"))
            else:
                plot_kws={}
            pplt = sns.pairplot(data, vars=col_labels, hue=hue_label, 
                                kind=kind, diag_kind=diag_kind, corner=corner,
                                plot_kws=plot_kws)
        
            width = 3*len(col_labels)
            pplt.fig.set_size_inches(width, width)

            st.pyplot(pplt.fig)
            
        with tab2:
            if hue_label is None:
                hue_string = None
            else:
                hue_string = f"'{hue_label}'"
            conf_string = ("import seaborn as sns\n" 
                           "import matplotlib.pyplot as plt\n"
                           "\n"
                           "rc = {'axes.facecolor': 'white',\n" 
                           "      'axes.edgecolor': 'black',\n" 
                           "      'xtick.color': 'black',\n"
                           "      'ytick.color': 'black'}\n"
                           "sns.set_theme(style='ticks', rc=rc)\n")
            
            code_string = ("```python\n" 
                           f"{conf_string}"
                           f"pplt = sns.pairplot(data, vars={col_labels},\n"
                           f"                    hue={hue_string}, corner={corner},\n"
                           f"                    kind='{kind}', diag_kind='{diag_kind}',\n"
                           f"                    plot_kws={plot_kws})\n"
                           f"width = {3*len(col_labels)}\n"
                           "pplt.fig.set_size_inches(width, width)\n"
                           "plt.show()")
            
            st.write(code_string)
        
    elif how == 'Distribution':
        num_columns = data.select_dtypes(include='number').columns
        cat_columns = data.drop(columns=num_columns).columns
        st.write('### Variable Information')
        
        if list(num_columns):
            index = list(data.columns).index(num_columns[0])
        else:
            index = 0
        select_var = st.sidebar.selectbox('Select a Varaible', 
                                          options=data.columns, index=index)
        this_column = data[select_var]
        
            
        if select_var in num_columns:
            this_info = pd.DataFrame(this_column.describe()).T
            this_info['missing count'] = this_column.isnull().sum()
            st.write(this_info)
            
            st.write('### Data Visualization')
            kind = st.sidebar.selectbox('Type of plots', 
                                        options=['hist', 'kde', 'boxplot', 'value counts'])
            
            if kind == 'hist':
                min_val, max_val = this_column.min(), this_column.max()
                bins = st.sidebar.slider('Number of Bins', 
                                         min_value=10, max_value=40, value=25, step=1,)
                yvalue = st.sidebar.radio('Type of Y-Data', options=['Frequency', 'Density'])
                color = st.sidebar.color_picker('Color', value='#1f77b4')
                tab1, tab2 = st.tabs(["Preview", "Code"])    
                with tab1:
                    fig = plt.figure(figsize=(8, 5.5))
                    plt.hist(this_column, bins=bins, color=color, density=yvalue=='Density')
                    plt.xlabel(select_var, fontsize=16)
                    plt.ylabel(yvalue, fontsize=16)
                    plt.title(f'Histogram of {select_var}', fontsize=16)
                    st.pyplot(fig)
                with tab2:
                    code_string = ("```python\n" 
                                   "import matplotlib.pyplot as plt\n"
                                   "\n"
                                   f"this_column = data['{select_var}']\n" 
                                   "fig = plt.figure(figsize=(8, 5.5))\n" 
                                   f"plt.hist(this_column, bins={bins}, density={yvalue=='Density'},\n"
                                   f"         color='{color}') \n"
                                   f"plt.xlabel('{select_var}', fontsize=16)\n" 
                                   f"plt.ylabel('{yvalue}', fontsize=16)\n" 
                                   f"plt.title('Histogram of {select_var}', fontsize=16)\n" 
                                   "plt.show()")

                    st.write(code_string)
            elif kind == 'kde':
                color = st.sidebar.color_picker('Color', value='#1f77b4')
                tab1, tab2 = st.tabs(["Preview", "Code"])    
                with tab1:
                    fig, ax = plt.subplots(1, 1, figsize=(8, 5.5))
                    sns.kdeplot(this_column, fill=True, color=color, ax=ax)
                    ax.set_xlabel(select_var, fontsize=16)
                    ax.set_ylabel('Density', fontsize=16)
                    ax.set_title(f'Kernel Density Estimation of {select_var}', fontsize=16)
                    st.pyplot(fig)
                with tab2:
                    code_string = ("```python\n"
                                   "import seaborn as sns\n" 
                                   "import matplotlib.pyplot as plt\n" 
                                   "\n" 
                                   f"this_column = data['{select_var}']\n" 
                                   "fig, ax = plt.subplots(1, 1, figsize=(8, 5.5))\n" 
                                   f"sns.kdeplot(this_column, fill=True, color='{color}', ax=ax)\n" 
                                   f"ax.set_xlabel('{select_var}', fontsize=16)\n" 
                                   "ax.set_ylabel('Density', fontsize=16)\n" 
                                   f"ax.set_title('Kernel Density Estimation of {select_var}',\n"
                                   "             fontsize=16)\n" 
                                   "plt.show()")
                    st.write(code_string)
            elif kind == 'boxplot':
                direction = st.sidebar.radio('Plot Direction', options=['Vertical', 'Horizontal'])
                tab1, tab2 = st.tabs(["Preview", "Code"])    
                with tab1:
                    fig = plt.figure(figsize=(8, 5.5))
                    plt.boxplot(this_column, vert=direction=='Vertical')
                    if direction == 'Vertical':
                        plt.xticks([1], [select_var], fontsize=16)
                        plt.ylabel('Value', fontsize=16)
                    else:
                        plt.yticks([1], [select_var], fontsize=16)
                        plt.xlabel('Value', fontsize=16)
                    plt.title(f'Boxplot of {select_var}', fontsize=16)
                    st.pyplot(fig)
                with tab2:
                    if direction == 'Vertical':
                        label_string = (f"plt.xticks([1], {[select_var]}, fontsize=16)\n"
                                        "plt.ylabel('Value', fontsize=16)")
                    else:
                        label_string = (f"plt.yticks([1], {[select_var]}, fontsize=16)\n"
                                        "plt.xlabel('Value', fontsize=16)")
                    code_string = ("```python\n"
                                   "import matplotlib.pyplot as plt\n"
                                   "\n"
                                   f"this_column = data['{select_var}']\n" 
                                   "fig = plt.figure(figsize=(8, 5.5))\n" 
                                   f"plt.boxplot(this_column, vert={direction=='Vertical'})\n" 
                                   f"{label_string}\n" 
                                   f"plt.title('Boxplot of {select_var}', fontsize=16)\n"
                                   "plt.show()")
                    st.write(code_string)
            elif kind == 'value counts':
                show_value_counts(this_column)
   
        elif select_var in cat_columns:
            vc = this_column.value_counts()
            this_info = pd.DataFrame({'count': [len(data)],
                                      'categories': [len(vc)],
                                      'largest': [f'{vc.index[0]}: {vc.iloc[0]}'],
                                      'smallest': [f'{vc.index[-1]}: {vc.iloc[-1]}'],
                                      'missing': [this_column.isnull().sum()]}, index=[select_var])
            st.write(this_info)
            
            st.write('### Data Visualization')
            show_value_counts(this_column)
            

    st.sidebar.write('---')
    col1, _, col3 = st.sidebar.columns([1, 1, 1])
    
    with col1:
        st.button('Back', key='back_to_step0', on_click=previous_page)
        
    with col3:
        st.button('Next', key='forward_to_step2', on_click=next_page)
        

def model_variables():
    
    st.sidebar.write('## Variables of the Model')
    st.sidebar.write('---')
    
    data = st.session_state['dataset']
    subset = data.iloc[:20]
    
    dep_var = st.sidebar.selectbox('Dependent Variable', options=data.columns)
    other_var = data.drop(columns=dep_var).columns
    ind_var = st.sidebar.multiselect('Independent Variable', 
                                     options=other_var, default=list(other_var))
    
    def var_highlight(data):
        color = pd.DataFrame('', index=list(data.index), columns=data.columns)
    
        color.loc[:, dep_var] = 'background-color: #BAB3FD'
        color.loc[:, ind_var] = 'background-color: #FFCDB6'
    
        return color
    
    ws = "&nbsp;"
    dvs = f'- <span style="background-color:#BAB3FD">{ws*8}</span>{ws*2}Dependent variable'
    ivs = f'- <span style="background-color:#FFCDB6">{ws*8}</span>{ws*2}Independent variables'
    st.markdown(dvs, unsafe_allow_html=True)
    st.markdown(ivs, unsafe_allow_html=True)
    st.write(subset.style.apply(var_highlight, axis=None))
    
    st.session_state.modelvars = [dep_var] + ind_var
    
    st.sidebar.write('---')
    col1, _, col3 = st.sidebar.columns([1, 1, 1])
    
    with col1:
        st.button('Back', key='back_to_step1', on_click=previous_page)
        
    with col3:
        st.button('Next', key='forward_to_step3', on_click=next_page)


def cat_to_dummies():
    
    st.sidebar.write('## Dummies for Categorical Variables')
    st.sidebar.write('---')
    
    data = st.session_state['dataset']
    ind_columns = st.session_state['modelvars'][1:]
    num_columns = data.select_dtypes(include='number').columns
    default_cats = set(data.drop(columns=num_columns).columns).intersection(set(ind_columns))
    
    cats = st.sidebar.multiselect('Selected Categorical Variables', 
                                  options=ind_columns, default=list(default_cats))
    
    if cats:
        tab1, tab2 = st.tabs(["Preview", "Code"])    
        with tab1:
            ohe = OneHotEncoder(drop='first', sparse_output=False)
            to_dummies = ColumnTransformer(transformers=[("cats", ohe, cats)], 
                                           remainder='passthrough')
    
            st.components.v1.html(to_dummies._repr_html_())
        with tab2:
            code_string = ("```python\n" 
                           "from sklearn.preprocessing import OneHotEncoder\n"
                           "from sklearn.compose import ColumnTransformer\n"
                           f"cats={cats}\n" 
                           "ohe = OneHotEncoder(drop='first', sparse_output=False)\n" 
                           "to_dummies = ColumnTransformer(transformers=[('cats', ohe, cats)],\n" 
                           "                               remainder='passthrough')\n" 
                           "```")
            st.write(code_string)
    else:
        to_dummies = None
        code_string = ''
        
    st.session_state.to_dummies = to_dummies
    st.session_state.dummy_code_string = code_string.split('\n')
    
    st.sidebar.write('---')
    col1, _, col3 = st.sidebar.columns([1, 1, 1])
    
    with col1:
        st.button('Back', key='back_to_step2', on_click=previous_page)
        
    with col3:
        st.button('Next', key='forward_to_step4', on_click=next_page)


def build_model():
    
    data = st.session_state['dataset']
    
    dep_columns = st.session_state['modelvars'][0]
    if np.issubdtype(data[dep_columns].dtype, np.number):
        type_pred = 'Regression'
    else:
        type_pred = 'Classification'
    # st.sidebar.write(f'### {type_pred} Model')
    st.sidebar.write(f'## {type_pred} Model Pipeline')
    
    st.sidebar.write('---')
    
    ind_columns = st.session_state['modelvars'][1:]
    to_dummies = st.session_state['to_dummies']
    
    steps = [('dummy', to_dummies)] if to_dummies is not None else []
    step_strings = ["('dummy', to_dummies)"] if to_dummies is not None else []
    params = {}
    param_strings = []
    import_strings = 'from sklearn.pipeline import Pipeline\n'

    type_scale = st.sidebar.selectbox('Scaling', 
                                      options=[None, 'standard scaler', 'normalizer'], key='1')
    if type_scale is not None:
        if type_scale == 'normalizer':
            step, pa, step_string, pa_strings = one_step('Normalizer', Normalizer, 
                                                         ['norm'], ['l2'])
            for p in pa:
                params[p] = pa[p]
            param_strings.extend(pa_strings)
            import_strings += 'from sklearn.preprocessing import Normalizer\n'
        else:
            step = ('StandardScaler', StandardScaler())
            step_string = "('StandardScaler', StandardScaler())"
            import_strings += 'from sklearn.preprocessing import StandardScaler\n'
        steps.append(step)
        step_strings.append(step_string)
    
    st.sidebar.write('---')
    type_dr = st.sidebar.selectbox('Dimension Reduction', options=[None, 'PCA'], key='2')
    if type_dr is not None:
        step, pa, step_string, pa_strings = one_step('PCA', PCA, 
                                                     ['n_components'], [len(ind_columns)])
        for p in pa:
            params[p] = pa[p]
        param_strings.extend(pa_strings)

        steps.append(step)
        step_strings.append(step_string)

        import_strings += 'from sklearn.decomposition import PCA\n'

    st.sidebar.write('---')
    if type_pred == 'Regression':
        models = {'LinearRegression': LinearRegression,
                  'Ridge': Ridge,
                  'Lasso': Lasso,
                  'DecisionTreeRegressor': DecisionTreeRegressor,
                  'RandomForestRegressor': RandomForestRegressor}
        type_model = st.sidebar.selectbox('Select a Model', options=models.keys(), key='3')
        if type_model == 'LinearRegression':
            step = ('LinearRegression', LinearRegression())
            step_string = "('LinearRegression', LinearRegression())"
            import_strings += f'from sklearn.linear_model import {models[type_model].__name__}\n'
        elif type_model in ['Ridge', 'Lasso']: 
            step, pa, step_string, pa_strings = one_step(type_model, models[type_model], 
                                                         ['alpha', 'max_iter'], [1.0], 
                                                         fixed={'max_iter': 100000000})
            for p in pa:
                params[p] = pa[p]
            param_strings.extend(pa_strings)
            import_strings += f'from sklearn.linear_model import {models[type_model].__name__}\n'
        elif type_model in ['DecisionTreeRegressor', 'RandomForestRegressor']:
            step, pa, step_string, pa_strings = one_step(type_model, models[type_model], 
                                                         ['max_depth', 'max_leaf_nodes',
                                                          'min_samples_split', 'min_samples_leaf',
                                                          'max_features'], 
                                                         [None, None, 2, 1, None])
            for p in pa:
                params[p] = pa[p]
            param_strings.extend(pa_strings)
            if type_model == 'DecisionTreeRegressor':
                import_strings += f'from sklearn.tree import {models[type_model].__name__}\n'
            else:
                import_strings += f'from sklearn.ensemble import {models[type_model].__name__}\n'

        steps.append(step)
        step_strings.append(step_string)
    else:
        models = {'LogisticRegression': LogisticRegression,
                  'DecisionTreeClassifier': DecisionTreeClassifier,
                  'RandomForestClassifier': RandomForestClassifier}
        type_model = st.sidebar.selectbox('Select a Model', options=models.keys(), key='3')
        if type_model == 'LogisticRegression':
            step = ('LogisticRegression', LogisticRegression())
            step_string = "('LogisticRegression', LogisticRegression())"
            import_strings += f'from sklearn.linear_model import {models[type_model].__name__}\n'
        elif type_model in ['DecisionTreeClassifier', 'RandomForestClassifier']:
            step, pa, step_string, pa_strings = one_step(type_model, models[type_model], 
                                                         ['max_depth', 'max_leaf_nodes',
                                                          'min_samples_split', 'min_samples_leaf',
                                                          'max_features'], 
                                                         [None, None, 2, 1, None])
            for p in pa:
                params[p] = pa[p]
            param_strings.extend(pa_strings)
            if type_model == 'DecisionTreeClassifier':
                import_strings += f'from sklearn.tree import {models[type_model].__name__}\n'
            else:
                import_strings += f'from sklearn.ensemble import {models[type_model].__name__}\n'

        steps.append(step)
        step_strings.append(step_string)

    pipe = Pipeline(steps)
    tab1, tab2 = st.tabs(["Preview", "Code"])    
    with tab1:
        st.components.v1.html(pipe._repr_html_(), height=500, scrolling=True)
    with tab2:
        params_code_string = "params = {" + ',\n          '.join(param_strings) + '}\n'
        code_string = ("```python\n" 
                       f"{import_strings}" 
                       "\n" 
                       f"{'' if len(params) == 0 else params_code_string}"
                       "steps = [\n    " + ',\n    '.join(step_strings) + "\n]\n"
                       "pipe = Pipeline(steps)\n"
                       "```")
        st.write(code_string)

    st.session_state.model_pipe = pipe
    st.session_state.model_params = params
    st.session_state.model_code_string = code_string.split('\n')
    st.session_state.type_pred = type_pred

    st.sidebar.write('---')
    col1, _, col3 = st.sidebar.columns([1, 1, 1])
    
    with col1:
        st.button('Back', key='back_to_step3', on_click=previous_page)
        
    with col3:
        st.button('Next', key='forward_to_step5', on_click=next_page)


def assess_model():
    
    st.sidebar.write('## Model Selection and Testing')
    st.sidebar.write('---')
    
    data = st.session_state['dataset']
    dep_columns = st.session_state['modelvars'][0]
    ind_columns = st.session_state['modelvars'][1:]
    pipe = st.session_state.model_pipe
    params = st.session_state.model_params
    type_pred = st.session_state.type_pred
    x = data[ind_columns]
    y = data[dep_columns]
    
    import_strings = "from sklearn.model_selection import ShuffleSplit\n"
    
    cv_test = st.sidebar.checkbox('Save a test dataset')
    if cv_test:
        test_ratio = st.sidebar.slider('Ratio of the test dataset', 
                                       min_value=0.05, max_value=0.50, step=0.05, value=0.30)
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_ratio, 
                                                            random_state=1)  
        import_strings += "from sklearn.model_selection import train_test_split\n"

        var_string = (f"y = data['{dep_columns}']\n" 
                      f"x = data[{ind_columns}]\n" 
                      "x_train, x_test, y_train, y_test = "
                      f"train_test_split(x, y, test_size={test_ratio}, random_state=1)\n")
    else:
        x_train = x
        y_train = y
        x_test, y_test = None, None
        var_string = (f"y_train = data['{dep_columns}']\n" 
                      f"x_train = data[{ind_columns}]\n")
    
    st.session_state.train_date = (x_train, y_train)
    st.session_state.test_data = (x_test, y_test)
    
    cv_folds = st.sidebar.slider('Number of folds', min_value=2, max_value=20, step=1, value=5)
    cv = ShuffleSplit(n_splits=cv_folds, random_state=0)
    cv_string = f"cv = ShuffleSplit(n_splits={cv_folds}, random_state=0)\n"
    
    tab1, tab2 = st.tabs(["Preview", "Code"])
    with tab1:
        if params:
            if type_pred == 'Regression':
                search = GridSearchCV(pipe, params, cv=cv, n_jobs=-1)
            else:
                search = GridSearchCV(pipe, params, scoring='roc_auc_ovr', cv=cv, n_jobs=-1)
            search.fit(x_train, y_train)
            st.write('#### Best Parameter(s):')
            for p in params:
                us_idx = p.index('__')
                st.write(f'- `{p[us_idx+2:]} = {search.best_params_[p]}`')
            st.write('#### Best Cross-Validation Scores:')
            best_index = search.best_index_
            scores = np.array([search.cv_results_[f'split{i}_test_score'][best_index]
                               for i in range(cv_folds)])
            model = search.best_estimator_
            st.write(pd.DataFrame(scores).T)
            st.write(f'Average score: {scores.mean()}')
            
            import_strings += "from sklearn.model_selection import GridSearchCV\n"
            fit_string = ("search = GridSearchCV(pipe, params, cv=cv, n_jobs=-1)\n" 
                          "search.fit(x_train, y_train)\n")
            score_string = ("best_index = search.best_index_\n" 
                            "scores = np.array([search.cv_results_[f'split{i}_test_score'][best_index]\n"
                            f"                   for i in range({cv_folds})])\n")
            best_string = "best_params = {key: search.best_params_[key] for key in params}\n"
            best_string += "model = search.best_estimator_\n"

            st.session_state.model = model
        else:
            st.write('#### Cross-Validation Scores:')
            if type_pred == 'Regression':
                scores = cross_val_score(pipe, x_train, y_train, cv=cv, n_jobs=-1)
            else:
                scores = cross_val_score(pipe, x_train, y_train, 
                                         scoring='roc_auc_ovr', cv=cv, n_jobs=-1)
            model = pipe
            st.write(pd.DataFrame(scores).T)
            st.write(f'Average score: {scores.mean()}')

            import_strings += "from sklearn.model_selection import cross_val_score\n"
            if type_pred == 'Regression':
                fit_string = "scores = cross_val_score(pipe, x_train, y_train, cv=cv, n_jobs=-1)\n"
            else:
                fit_string = ("scores = cross_val_score(pipe, x_train, y_train,\n"
                              "                         scoring='roc_auc_ovr', cv=cv, n_jobs=-1)\n")
            score_string = ""
            best_string = "model = pipe\n"

            model.fit(x_train, y_train)
            st.session_state.model = model

        if cv_test:
            st.write("#### Test the Model")
            # model.fit(x_train, y_train)
            if type_pred == 'Regression':
                test_score = model.score(x_test, y_test)
            else:
                test_score = model.score(x_test, y_test, scoring='roc_auc_ovr')
            st.write(f"Test score: {test_score}")

            test_string = ("model.fit(x_train, y_train)\n"
                           "test_score = model.score(x_test, y_test)\n")
        else:
            test_string = ""

    with tab2:
        code_string = ("```python\n"
                       f"{import_strings}"
                       "\n"
                       f"{var_string}" 
                       f"{cv_string}" 
                       f"{fit_string}" 
                       f"{score_string}"
                       f"{best_string}"
                       f"{test_string}"
                       "```")
        st.write(code_string)

    st.session_state.fit_code_string = code_string.split('\n')
    
    st.sidebar.write('---')
    col1, _, col3 = st.sidebar.columns([1, 1, 1])
    with col1:
        st.button('Back', key='back_to_step4', on_click=previous_page)
    with col3:
        st.button('Next', key='forward_to_step6', on_click=next_page)
        

def analysis():

    pipe = st.session_state.model
    type_pred = st.session_state.type_pred
    x_train, y_train = st.session_state['train_date']
    x_test, y_test = st.session_state['test_data']
    
    st.sidebar.write('## Model Analysis')
    st.sidebar.write('---')

    tab1, tab2 = st.tabs(["Preview", "Code"])
    with tab1:
        if type_pred == 'Regression':
            yhat_cv = cross_val_predict(pipe, x_train, y_train)
            st.write('#### Cross-Validation Results')
            col1, col2 = st.columns([0.55, 0.45])
            with col1:
                fig, ax = plt.subplots(1, 1, figsize=(5.7, 5.7))
                ax.scatter(y_train, yhat_cv, s=20, 
                           facecolor='none', edgecolor='k', alpha=0.7)
                value_max = np.maximum(y_train.max(), yhat_cv.max())
                value_min = np.minimum(y_train.min(), yhat_cv.min())
                ax.plot([value_min, value_max], [value_min, value_max], 
                        color='r', linestyle='--')
                ax.set_xlabel('Actual response', fontsize=16)
                ax.set_ylabel('Predicted response', fontsize=16)
                ax.grid()
                st.pyplot(fig)
            
            if x_test is None:
                test_code_string = ''
            else:
                yhat_test = pipe.predict(x_test)
                st.write('#### Test Results')
                col1, col2 = st.columns([0.55, 0.45])
                with col1:
                    fig, ax = plt.subplots(1, 1, figsize=(5.7, 5.7))
                    ax.scatter(y_test, yhat_test, s=20, 
                               facecolor='none', edgecolor='k', alpha=0.7)
                    value_max = np.maximum(y_test.max(), yhat_test.max())
                    value_min = np.minimum(y_test.min(), yhat_test.min())
                    ax.plot([value_min, value_max], [value_min, value_max], 
                            color='r', linestyle='--')
                    ax.set_xlabel('Actual response', fontsize=16)
                    ax.set_ylabel('Predicted response', fontsize=16)
                    ax.grid()
                    st.pyplot(fig)
                
                test_code_string = ("\n"
                                    "yhat_test = model.predict(x_test)\n"
                                    "fig = plt.figure(figsize=(6.5, 6.5))\n"
                                    "plt.scatter(y_test, yhat_test, s=20,\n"
                                    "            facecolor='none', edgecolor='k', alpha=0.7)\n"
                                    "value_max = np.maximum(y_test.max(), yhat_test.max())\n"
                                    "value_min = np.minimum(y_test.min(), yhat_test.min())\n"
                                    "plt.plot([value_min, value_max], [value_min, value_max],\n"
                                    "         color='r', linestyle='--')\n"
                                    "plt.xlabel('Actual response', fontsize=16)\n"
                                    "plt.ylabel('Predicted response', fontsize=16)\n"
                                    "plt.title('Test Predicted v.s. Actual', fontsize=16)\n"
                                    "plt.grid()\n"
                                    "plt.show()")
        else:
            classes = y_train.unique()
            classes.sort()
            class_labels = st.sidebar.multiselect('Displayed classes', classes, classes)
            proba = pd.DataFrame(cross_val_predict(pipe, x_train, y_train, method='predict_proba'), 
                                 columns=classes)
            
            st.write('#### Cross-Validation Results')
            col1, col2 = st.columns([0.55, 0.45])
            with col1:
                fig, ax = plt.subplots(1, 1, figsize=(5.7, 5.7))
                ax.plot([0, 1], [0, 1], 
                        c='r', linewidth=2, alpha=0.5, linestyle='--', 
                        label='Chance Level (AUC=0.5)')
            
                conf_mats = []
                accuracies = []
                thresholds = []
                for c in class_labels:
                    fpr, tpr, thrds = roc_curve(y_train==c, proba[c])
                    tv = st.sidebar.slider(f'Threshold value for {c}', 0.001, 0.999, 0.5, 0.001, format='%f')
                    thresholds.append(tv)
                    auc_value = auc(fpr, tpr)
                    ax.plot(fpr, tpr, linewidth=2, 
                            label=f"Class '{c}' ROC (AUC={auc_value:.4f})")
                
                    thrds_idx = np.argmin(abs(thrds - tv))
                    ax.scatter(fpr[thrds_idx], tpr[thrds_idx], s=100, color='r')
                    pred_class = (proba[c] > tv).astype(int)
                    
                    cm = pd.DataFrame(confusion_matrix(y_train==c, pred_class, normalize='true'), 
                                      index=[f'True not {c}', f'True {c}'], 
                                      columns=[f'Predicted not {c}', f'Predicted {c}'])
                    conf_mats.append(cm)
                    accuracies.append((pred_class.values == (y_train==c).values).mean())

                    # accuracies.append(((proba[c] > tv).values == (y_train==c).values).mean())
                    js = tpr[thrds_idx] - fpr[thrds_idx]
                    ax.plot([fpr[thrds_idx], fpr[thrds_idx]], [fpr[thrds_idx], tpr[thrds_idx]], 
                            linestyle=':', label=f"Class '{c}' J-statistic ({js:.4f}) ")
        
                ax.legend(fontsize=12)
                ax.set_xlabel('False positive rate', fontsize=16)
                ax.set_ylabel('True positive rate', fontsize=16)
                st.pyplot(fig)

            with col2:
                for c, cm, ac in zip(class_labels, conf_mats, accuracies):
                    st.write(f"**Prediction for class '{c}'**")
                    st.write(f"Overall accuracy: {ac:.4f}")
                    st.write(cm)
                    
            if x_test is None:
                test_code_string = ''
            else:
                proba = pd.DataFrame(pipe.predict_proba(x_test), columns=classes)
                
                st.write('#### Test Results')
                col1, col2 = st.columns([0.55, 0.45])
                with col1:
                    fig, ax = plt.subplots(1, 1, figsize=(5.7, 5.7))
                    ax.plot([0, 1], [0, 1], 
                            c='r', linewidth=2, alpha=0.5, linestyle='--', 
                            label='Chance Level (AUC=0.5)')
                    conf_mats = []
                    accuracies = []
                    for c in class_labels:
                        fpr, tpr, thrds = roc_curve(y_test==c, proba[c])
                        auc_value = auc(fpr, tpr)
                        ax.plot(fpr, tpr, linewidth=2, 
                                label=f"Class '{c}' ROC (AUC={auc_value:.4f})")
                
                        thrds_idx = np.argmin(abs(thrds - tv))
                        ax.scatter(fpr[thrds_idx], tpr[thrds_idx], s=100, color='r')
                        pred_class = (proba[c] > tv).astype(int)
                        cm = pd.DataFrame(confusion_matrix(y_test==c, pred_class, normalize='true'), 
                                          index=[f'True not {c}', f'True {c}'], 
                                          columns=[f'Predicted not {c}', f'Predicted {c}'])
                        conf_mats.append(cm)
                        accuracies.append((pred_class.values == (y_test==c).values).mean())
                
                    ax.legend(fontsize=12)
                    ax.set_xlabel('False positive rate', fontsize=16)
                    ax.set_ylabel('True positive rate', fontsize=16)
                    st.pyplot(fig)
                
                with col2:
                    for c, cm, ac in zip(class_labels, conf_mats, accuracies):
                        st.write(f"**Prediction for class '{c}'**")
                        st.write(f"Overall accuracy: {ac:.4f}")
                        st.write(cm)
                
                test_code_string = ("\n"
                                    "proba = pd.DataFrame(model.predict_proba(x_test), columns=classes)\n"
                                    "confusion_test = {}\n"
                                    "accuracies_test = {}\n"
                                    "fig = plt.figure(figsize=(6.5, 6.5))\n"
                                    "plt.plot([0, 1], [0, 1], c='r', linewidth=2, alpha=0.5, linestyle='--',\n" 
                                    "         label='Chance Level (AUC=0.5)')\n"
                                    "for c, tv in zip(class_labels, thresholds.values()):\n"
                                    "    fpr, tpr, thrds = roc_curve(y_test==c, proba[c])\n"
                                    "    auc_value = auc(fpr, tpr)\n"
                                    "    plt.plot(fpr, tpr, linewidth=2,\n"
                                    "             label=f\"Class '{c}' ROC (AUC={auc_value:.4f})\")\n\n"
                                    #"    thrds_idx = np.argmin(abs(thrds - tv))\n"
                                    #"    plt.scatter(fpr[thrds_idx], tpr[thrds_idx], s=100, color='r')\n"
                                    "    pred_class = (proba[c] > tv).astype(int)\n"
                                    "    cm = pd.DataFrame(confusion_matrix(y_test==c, pred_class, normalize='true'),\n" 
                                    "                      index=[f'True not {c}', f'True {c}'],\n"
                                    "                      columns=[f'Predicted not {c}', f'Predicted {c}'])\n"
                                    "    confusion_test[c] = cm\n"
                                    "    accuracies_test[c] = (pred_class.values == (y_test==c).values).mean()\n"
                                    "plt.legend(fontsize=12)\n"
                                    "plt.xlabel('False positive rate', fontsize=16)\n"
                                    "plt.ylabel('True positive rate', fontsize=16)\n"
                                    "plt.title('Test ROC', fontsize=16)\n"
                                    "plt.show()\n")
                        
    with tab2:
        if type_pred == 'Regression':
            code_string = ("```python\n"
                           "import numpy as np\n"
                           "import matplotlib.pyplot as plt\n"
                           "from sklearn.model_selection import cross_val_score\n"
                           "from sklearn.model_selection import cross_val_predict\n\n"
                           "yhat_cv = cross_val_predict(model, x_train, y_train)\n"
                           "fig = plt.figure(figsize=(6.5, 6.5))\n"
                           "plt.scatter(y_train, yhat_cv, s=20, \n"
                           "            facecolor='none', edgecolor='k', alpha=0.7)\n"
                           "value_max = np.maximum(y_train.max(), yhat_cv.max())\n"
                           "value_min = np.minimum(y_train.min(), yhat_cv.min())\n"
                           "plt.plot([value_min, value_max], [value_min, value_max],\n"
                           "         color='r', linestyle='--')\n"
                           "plt.xlabel('Actual response', fontsize=16)\n"
                           "plt.ylabel('Predicted response', fontsize=16)\n"
                           "plt.title('Cross-Validation Predicted v.s. Actual', fontsize=16)\n"
                           "plt.grid()\n"
                           "plt.show()\n"
                           f"{test_code_string}\n"
                           "```")
        else:
            tv_dict = {c: tv for c, tv in zip(class_labels, thresholds)}
            code_string = ("```python\n"
                           "import numpy as np\n"
                           "import matplotlib.pyplot as plt\n"
                           "from sklearn.model_selection import cross_val_score\n"
                           "from sklearn.model_selection import cross_val_predict\n"
                           "from sklearn.metrics import auc\n"
                           "from sklearn.metrics import roc_curve\n"
                           "from sklearn.metrics import confusion_matrix\n\n"
                           f"class_labels = {class_labels}\n"
                           f"thresholds = {tv_dict}\n\n"
                           "classes = y_train.unique()\n"
                           "classes.sort()\n"
                           "proba = pd.DataFrame(cross_val_predict(model, x_train, y_train,\n" 
                           "                                       method='predict_proba'), columns=classes)\n"
                           "confusion_cv = {}\n"
                           "accuracies_cv = {}\n"
                           "fig = plt.figure(figsize=(6.5, 6.5))\n"
                           "plt.plot([0, 1], [0, 1], c='r', linewidth=2, alpha=0.5, linestyle='--',\n" 
                           "         label='Chance Level (AUC=0.5)')\n"
                           "for c, tv in zip(class_labels, thresholds.values()):\n"
                           "    fpr, tpr, thrds = roc_curve(y_train==c, proba[c])\n"
                           "    auc_value = auc(fpr, tpr)\n"
                           "    plt.plot(fpr, tpr, linewidth=2,\n"
                           "             label=f\"Class '{c}' ROC (AUC={auc_value:.4f})\")\n\n"
                           # "    thrds_idx = np.argmin(abs(thrds - tv))\n"
                           # "    plt.scatter(fpr[thrds_idx], tpr[thrds_idx], s=100, color='r')\n"
                           "    pred_class = (proba[c] > tv).astype(int)\n"
                           "    cm = pd.DataFrame(confusion_matrix(y_train==c, pred_class, normalize='true'),\n" 
                           "                      index=[f'True not {c}', f'True {c}'],\n"
                           "                      columns=[f'Predicted not {c}', f'Predicted {c}'])\n"
                           "    confusion_cv[c] = cm\n"
                           "    accuracies_cv[c] = (pred_class.values == (y_train==c).values).mean()\n"
                           # "    js = tpr[thrds_idx] - fpr[thrds_idx]\n"
                           # "    plt.plot([fpr[thrds_idx], fpr[thrds_idx]], [fpr[thrds_idx], tpr[thrds_idx]],\n" 
                           # "             linestyle=':', label=f\"Class '{c}' J-statistic ({js:.4f}) \")\n"
                           "plt.legend(fontsize=12)\n"
                           "plt.xlabel('False positive rate', fontsize=16)\n"
                           "plt.ylabel('True positive rate', fontsize=16)\n"
                           "plt.title('Cross-Validation ROC', fontsize=16)\n"
                           "plt.show()\n"
                           f"{test_code_string}"
                           "```")

        st.write(code_string)

    st.session_state.analysis_code_string = code_string.split('\n')

    st.sidebar.write('---')
    col1, _, col3 = st.sidebar.columns([1, 1, 1])
    with col1:
        st.button('Back', key='back_to_step5', on_click=previous_page)
    with col3:
        st.button('Next', key='forward_to_step7', on_click=next_page)

def summary():

    st.sidebar.write('## Code Summary')
    st.sidebar.write('---')
    
    state = st.session_state
    code_strings = (state.dummy_code_string + state.model_code_string + 
                    state.fit_code_string + state.analysis_code_string)

    import_lines = []
    from_lines = []
    code_lines = []
    for line in code_strings:
        if line[:3] == '```':
            continue
        if line[:7] == 'import ':
            import_lines.append(line)
        elif line[:5] == 'from ':
            from_lines.append(line)
        else:
            code_lines.append(line)
    
    all_code = '\n'.join(["```python\n"] + import_lines + from_lines + [' '] +
                         code_lines + ["```"])
        
    st.write(all_code)

    col1, _, _ = st.sidebar.columns([1, 1, 1])
    with col1:
        st.button('Back', key='back_to_step5', on_click=previous_page)
    
rc = {'axes.facecolor': 'white',
      'axes.edgecolor': 'black',
      'xtick.color': 'black',
      'ytick.color': 'black'}
sns.set_theme(style="ticks", rc=rc)

list_of_fun = [read_data, 
               variable_analysis, 
               model_variables,
               cat_to_dummies,
               build_model,
               assess_model,
               analysis,
               summary]

if 'counter' not in st.session_state: 
    st.session_state.counter = 0

st.markdown('# C🧉C🧉NU🌴S')
st.markdown('COCONUTS is a user interface for creating and running predictive models.')
st.markdown('---')
if st.session_state.counter == 0:
    st.markdown('- Please upload the dataset for the regression or classification model.')
    st.markdown("- The dataset can be a 'csv', 'xlsx', or 'xls' file.")
    st.markdown(("- Please make sure the the dataset is properly prepared such that:\n"
                 "    - the dependent variables and all independent variables are ready for use; \n"
                 "    - there is no missing value in relavent variables; \n"
                 "    - for categorical variables, the size of each category should be sufficiently large. "))
elif st.session_state.counter == 1:
    msg = ("- The code segments for data visualization will not be included in the final exported code. "
           "Please save them manually.")
    st.markdown(msg)
elif st.session_state.counter == 2:
    msg = ("- COCONUTS determinies the prediction type (regression or classification) according to "
           "the data type of the dependent variable. \n"
           "- If the dependent variable has a numerical type, COCONUTS builds a regression model. \n"
           "- If the type of the dependent variable is boolean or string, COCONUTS builds a classification model.")
    st.markdown(msg)
elif st.session_state.counter == 3:
    st.markdown('- Select the categorical predictor variables to be converted into dummy variables.')
elif st.session_state.counter == 4:
    st.markdown("- Sepcify the steps of the pipeline for the regression/classification model.")
elif st.session_state.counter == 5:
    st.markdown("- This page conduct cross-validation for assessing model performance. ")
    st.markdown("- You may save a randomly selected subset of data as the test dataset. ")
    st.markdown("- The R-squared value is used as the scores for assessing regression models. ")
    st.markdown("- The AUC value is used for assessing the classification models. ")
elif st.session_state.counter == 6:
    st.markdown('- This page displays the predicted v.s. actual responses for regression models.')
    st.markdown('- This page displays the ROC curves for classification models.')
else:
    st.markdown('- This page summarizes the code for running the regression/classificaiton model.')
    if st.session_state['type_pred'] == 'Regression':
        st.markdown('- `best_params` is a dictionary of the best hyperparameter values.')
        st.markdown('- `scores` is the scores in terms of R-squared values calcualted via cross-validation on the training data.')
        st.markdown('- `test_score` is the score in terms of the R-squared value calcualted based on the test data.')
        st.markdown('- `yhat_cv` is the array of predicted response calcualted via cross-validation on the training data.')
        st.markdown('- `yhat_test` is the array of predicted response calculated based on the training data.')
    elif st.session_state['type_pred'] == 'Classification':
        st.markdown('- `accuracies_cv` is the cross-validation accuracies for predicting each selected class.')
        st.markdown('- `accuracies_test` is the test accuracies for predicting each selected class.')
        st.markdown('- `best_params` is a dictionary of the best hyperparameter values.')
        st.markdown('- `confusion_cv` is the confusion matrix calcualted via cross-validation on the training data.')
        st.markdown('- `confusion_test` is the confusion matrix calcualted based on the test data.')
        st.markdown('- `scores` is the scores in terms of AUC values calcualted via cross-validation on the training data.')
        st.markdown('- `test_score` is the score in terms of the AUC value calcualted based on the test data.')
        st.markdown('- `thresholds` is a dictionary of threshold values of selected classes.')

st.markdown('---')
list_of_fun[st.session_state.counter]()
