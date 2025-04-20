# Clebsch-Gordan系数计算
# 绘图部分
# copyright@pifuyuini
# version: 1.0.2
# 20241204更新：基于已完成的cgc_funtion_adjusted.py

# 导入必要的库
import cgc_function_adjusted as cgcfa
import pandas as pd
import matplotlib.pyplot as plt

# 表格生成函数
def cg_table_generator(cg):
    '''
    Generate a corresponding CG coefficient table based on a CG class.

    Parameters:
    cg: cgc_function_adjusted.CG

    Return:
    pandas.DataFrame
    '''
    # 值的提取
    m_col = cg.m_set()[0:cg.number_of_half_of_m()]
    j_row = cg.j_set()
    table_of_CG = cg.cg_table()
    # 表头
    header = ['M', 'm1', 'm2', f'J={j_row[0]}'] + [''] * (len(j_row) - 1)
    # M，m1和m2列
    m1_col = []
    m2_col = []
    m_norm_col = []
    for m in m_col:
        m1m2 = cg.m1m2(m)
        m1_col_this_m = []
        m2_col_this_m = []
        for group in m1m2:
            m1_col_this_m.append(group[0])
            m2_col_this_m.append(group[1])
        m1_col = m1_col + m1_col_this_m
        m2_col = m2_col + m2_col_this_m
        m_norm_col = m_norm_col + [f'{m}'] + [''] * (len(m1_col_this_m) - 1)
    # 表格的生成
    df = pd.DataFrame(columns=header)
    df.iloc[:, 0] = m_norm_col
    df.iloc[:, 1] = m1_col
    df.iloc[:, 2] = m2_col
    for i in range(len(j_row)):
        if i == 0:
            df.iloc[:, 3+i] = table_of_CG[i]
        else:
            cg_norm_row = (len(table_of_CG[0]) - len(table_of_CG[i]) - 1) * [''] + [f'J={j_row[i]}'] + table_of_CG[i]
            df.iloc[:, 3+i] = cg_norm_row
    return df

def cg_df_plot(df):
    '''
    Plot the table.

    Parameters:
    df: pandas.DataFrame

    Return:
    None
    '''
    # FireFly!
    '''
    #3e324a（紫黑）
    #475d7b（灰蓝）
    #97c6c0（灰绿）
    #e5802e（橘黄）
    #e26e1b（深橘黄）
    #e6e4e0（银白）
    #4df8e8（蓝绿）
    '''
    colors = ['#3e324a', '#475d7b', '#97c6c0', '#e26e1b', '#4df8e8', '#e6e4e0'] # FireFly!
    # Adjusting the table styling as per the new requirements
    fig, ax = plt.subplots(dpi=300)
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
    # Styling the table
    for (row, col), cell in table.get_celld().items():
        if col == 0:  # Highlight M column
            cell.set_facecolor(colors[2])
        elif col == 1 or col == 2:  # Highlight m1 and m2 columns
            cell.set_facecolor(colors[4])
        if row == 0 and col < 4:  # First four header columns
            cell.set_facecolor(colors[0])
            cell.set_text_props(color=colors[5], weight='bold')
        elif row == 0 and col >= 4:  # Remaining header columns with no border and white background
            cell.set_facecolor('white')
            cell.set_edgecolor('white')  # Remove border
        elif row > 0 and col == 3 + row:  # Diagonal cells starting from (0,3), (1,4), etc.
            cell.set_facecolor(colors[0])
            cell.set_text_props(color=colors[5], weight='bold')
        # Special styling for cells containing 'J'
        if 'J' in str(cell.get_text().get_text()):
            cell.set_facecolor(colors[0])
            cell.set_text_props(color=colors[5], weight='bold')        
        # Styling for empty cells
        if cell.get_text().get_text() == '':
            cell.set_facecolor('white')
            cell.set_edgecolor('white')
        # Retain normal border for non-empty cells
        if cell.get_text().get_text() != '':
            cell.set_edgecolor('black')
        # Since the above function fails, remove all borders
        cell.set_edgecolor('white')
        if (col > 2) and (cell.get_text().get_text() != '') and ('J' not in str(cell.get_text().get_text())):
            cell.set_facecolor(colors[5])
    # Adding the title
    j1 = df['m1'].iloc[0]
    j2 = df['m2'].iloc[0]
    plt.title(f"Clebsch-Gordan Coefficients for j1 = {j1}, j2 = {j2}", weight='bold', color=colors[1])

    # Display the updated table
    plt.show()
    return None


