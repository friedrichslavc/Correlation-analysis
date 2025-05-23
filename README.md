# 基于中国网购数据的购物车关联性分析

## 项目简介

本项目通过分析模拟的中国网购交易数据，挖掘商品之间的关联规则，理解支持度、置信度和提升度的计算，并探讨其在电商中的应用。

## 数据集说明

使用模拟的中国网购交易数据（10笔交易），包含以下商品：
- 手机壳
- 充电宝
- 数据线
- 耳机

这些商品是中国电商平台上常见的数码配件，反映了中国消费者的购物习惯。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

运行关联性分析脚本：

```bash
python association_analysis.py
```

## 分析内容

1. **支持度计算**：计算单品和商品组合的支持度
2. **置信度计算**：计算关联规则的置信度
3. **提升度计算**：计算关联规则的提升度并分析其意义
4. **可视化**：生成支持度和关联规则的可视化图表
5. **应用建议**：基于分析结果提供电商应用建议

## 输出结果

- 控制台输出：详细的分析结果和解释
- 图表输出：
  - `support_visualization.png`：商品组合支持度可视化
  - `rules_visualization.png`：关联规则可视化

## 电商应用价值

- 捆绑销售策略优化
- 商品布局优化
- 个性化推荐系统改进
- 库存管理优化
- 促销活动设计
