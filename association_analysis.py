# 基于中国网购数据的购物车关联性分析

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mlxtend.frequent_patterns import apriori, association_rules
import seaborn as sns
from matplotlib.font_manager import FontProperties
import warnings
warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 1. 创建模拟的中国网购交易数据
def create_transaction_data():
    # 根据任务中提供的10笔交易数据
    transactions = [
        [1, '手机壳', '充电宝', '数据线'],
        [2, '手机壳', '数据线'],
        [3, '充电宝', '耳机'],
        [4, '手机壳', '耳机', '数据线'],
        [5, '充电宝', '手机壳'],
        [6, '数据线', '耳机'],
        [7, '手机壳', '充电宝', '数据线'],
        [8, '手机壳', '耳机'],
        [9, '充电宝', '数据线'],
        [10, '手机壳', '数据线']
    ]
    
    # 转换为DataFrame格式
    df = pd.DataFrame(transactions)
    df.rename(columns={0: '交易ID'}, inplace=True)
    
    # 将交易数据转换为适合关联规则挖掘的格式
    return df

# 2. 将交易数据转换为one-hot编码格式
def convert_to_onehot(df):
    # 创建一个空的DataFrame，列为所有可能的商品
    unique_items = set()
    for i in range(1, len(df.columns)):
        unique_items.update(df[i].dropna().values)
    
    # 创建one-hot编码的DataFrame
    onehot_df = pd.DataFrame(index=df['交易ID'], columns=list(unique_items))
    
    # 填充one-hot编码
    for idx, row in df.iterrows():
        for i in range(1, len(df.columns)):
            if pd.notna(row[i]):
                onehot_df.at[row['交易ID'], row[i]] = 1
    
    # 将NaN替换为0
    onehot_df.fillna(0, inplace=True)
    
    return onehot_df

# 3. 计算支持度
def calculate_support(onehot_df):
    # 使用apriori算法计算频繁项集
    frequent_itemsets = apriori(onehot_df, min_support=0.1, use_colnames=True)
    
    # 按支持度排序
    frequent_itemsets.sort_values('support', ascending=False, inplace=True)
    
    return frequent_itemsets

# 4. 计算关联规则（置信度和提升度）
def calculate_association_rules(frequent_itemsets):
    # 使用association_rules函数计算关联规则
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1)
    
    # 按置信度排序
    rules.sort_values('confidence', ascending=False, inplace=True)
    
    return rules

# 5. 可视化支持度
def visualize_support(frequent_itemsets):
    plt.figure(figsize=(10, 6))
    
    # 只显示前10个频繁项集
    top_itemsets = frequent_itemsets.head(10)
    
    # 将frozenset转换为字符串
    top_itemsets['itemsets_str'] = top_itemsets['itemsets'].apply(lambda x: ', '.join(list(x)))
    
    # 绘制条形图
    sns.barplot(x='support', y='itemsets_str', data=top_itemsets)
    plt.title('商品组合的支持度')
    plt.xlabel('支持度')
    plt.ylabel('商品组合')
    plt.tight_layout()
    plt.savefig('support_visualization.png')
    plt.close()

# 6. 可视化关联规则
def visualize_rules(rules):
    plt.figure(figsize=(10, 8))
    
    # 只显示前10条规则
    top_rules = rules.head(10).copy()
    
    # 将frozenset转换为字符串
    top_rules['antecedents_str'] = top_rules['antecedents'].apply(lambda x: ', '.join(list(x)))
    top_rules['consequents_str'] = top_rules['consequents'].apply(lambda x: ', '.join(list(x)))
    top_rules['rule'] = top_rules['antecedents_str'] + ' → ' + top_rules['consequents_str']
    
    # 绘制散点图
    plt.scatter(top_rules['support'], top_rules['confidence'], alpha=0.5, s=top_rules['lift']*100)
    
    # 添加标签
    for i, row in top_rules.iterrows():
        plt.annotate(row['rule'], 
                     (row['support'], row['confidence']),
                     xytext=(5, 5),
                     textcoords='offset points')
    
    plt.title('关联规则的支持度、置信度和提升度')
    plt.xlabel('支持度')
    plt.ylabel('置信度')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('rules_visualization.png')
    plt.close()

# 7. 分析和解释关联规则
def analyze_rules(rules):
    print("\n关联规则分析结果：")
    print("="*50)
    
    # 选择前3条规则进行详细分析
    top_rules = rules.head(3)
    
    for i, rule in top_rules.iterrows():
        antecedents = ', '.join(list(rule['antecedents']))
        consequents = ', '.join(list(rule['consequents']))
        support = rule['support']
        confidence = rule['confidence']
        lift = rule['lift']
        
        print(f"\n规则 {i+1}: {antecedents} → {consequents}")
        print(f"支持度: {support:.2f} (即{support*100:.1f}%的交易中同时包含{antecedents}和{consequents})")
        print(f"置信度: {confidence:.2f} (即购买{antecedents}的顾客中有{confidence*100:.1f}%会购买{consequents})")
        print(f"提升度: {lift:.2f} (")
        
        if lift > 1:
            print(f"  提升度>1，表明购买{antecedents}会增加购买{consequents}的可能性")
            print(f"  具体而言，购买{antecedents}的顾客购买{consequents}的可能性是随机购买的{lift:.1f}倍")
        elif lift == 1:
            print(f"  提升度=1，表明购买{antecedents}与购买{consequents}相互独立")
        else:
            print(f"  提升度<1，表明购买{antecedents}会降低购买{consequents}的可能性")
    
    print("\n电商应用建议：")
    print("="*50)
    print("1. 捆绑销售策略：对于提升度高的商品组合，可以考虑打包销售或促销活动")
    print("2. 商品布局优化：在网页设计中，将关联性强的商品放在相近位置")
    print("3. 个性化推荐：基于用户已购买的商品，推荐置信度高的关联商品")
    print("4. 库存管理：关联性强的商品应当保持同步的库存水平")
    print("5. 促销活动设计：可以针对提升度高的商品组合设计'买A送B'或'A+B打折'等促销活动")

# 主函数
def main():
    print("基于中国网购数据的购物车关联性分析\n")
    
    # 1. 创建交易数据
    df = create_transaction_data()
    print("交易数据示例：")
    print(df.head())
    
    # 2. 转换为one-hot编码
    onehot_df = convert_to_onehot(df)
    print("\nOne-hot编码后的数据：")
    print(onehot_df.head())
    
    # 3. 计算支持度
    frequent_itemsets = calculate_support(onehot_df)
    print("\n频繁项集及其支持度：")
    print(frequent_itemsets)
    
    # 4. 计算关联规则
    rules = calculate_association_rules(frequent_itemsets)
    print("\n关联规则（包含支持度、置信度和提升度）：")
    print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])
    
    # 5. 可视化支持度
    visualize_support(frequent_itemsets)
    print("\n已生成商品组合支持度可视化图表: support_visualization.png")
    
    # 6. 可视化关联规则
    visualize_rules(rules)
    print("已生成关联规则可视化图表: rules_visualization.png")
    
    # 7. 分析和解释关联规则
    analyze_rules(rules)

if __name__ == "__main__":
    main()