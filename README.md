# 面试助手雷达图系统

## 🎯 项目简介

这是一个集成了Dify AI评价和雷达图可视化的面试助手系统。当AI返回包含特定格式的评分信息时，系统会自动生成美观的雷达图，展示面试者在各个维度的能力评分。

## 🌟 主要功能

- **智能评分检测**：自动识别AI返回的评分信息
- **雷达图生成**：根据评分自动创建五维度雷达图
- **前端集成**：支持base64图片数据返回，便于前端展示
- **Web服务**：提供完整的Web服务器和前端界面
- **多种使用方式**：支持命令行、API调用、Web界面等多种使用方式

## 📊 评分维度

系统支持以下五个维度的评分（每个维度最高20分，总分100分）：

1. **专业能力** - 技术知识和专业技能
2. **逻辑分析问题能力** - 思维逻辑和问题分析
3. **沟通表达能力** - 语言表达和沟通技巧
4. **团队协作能力** - 团队合作和协调能力
5. **学习意愿** - 学习态度和成长意识

## 🔧 安装依赖

```bash
pip install -r requirements.txt
```

### 依赖包说明

- `requests` - HTTP请求库，用于调用Dify API
- `matplotlib` - 图表绘制库，用于生成雷达图
- `numpy` - 数值计算库，用于雷达图数据处理
- `flask` - Web框架，用于构建API服务器
- `flask-cors` - 跨域支持，用于前端调用API

## 🚀 使用方法

### 1. 命令行测试

直接运行主程序：

```bash
python api.py
```

这将执行测试功能，包括：
- 雷达图功能测试
- Dify API调用测试
- base64图片生成测试

### 2. 作为库使用

```python
from api import call_dify_api_for_frontend, parse_scores, create_radar_chart

# 前端友好的API调用（返回结构化数据）
result = call_dify_api_for_frontend(
    query="请评价我的技术能力",
    response_mode="streaming"
)

# 检查结果
if result and result.get('scores'):
    print("评分数据:", result['scores'])
    print("是否包含雷达图:", '有' if result.get('chart_base64') else '无')

# 独立使用雷达图功能
scores = {
    '专业能力': 18,
    '逻辑分析问题能力': 16,
    '沟通表达能力': 15,
    '团队协作能力': 17,
    '学习意愿': 19,
    '总分': 85
}

# 保存为文件
create_radar_chart(scores, 'my_radar.png')

# 获取base64数据
base64_data = create_radar_chart(scores, return_base64=True)
```

### 3. Web服务器模式

启动完整的Web服务器：

```bash
python web_server_example.py
```

服务器将在 `http://localhost:5000` 启动，提供：

- `GET /` - 前端界面
- `POST /api/interview-evaluation` - 面试评价API
- `GET /api/test` - 测试接口
- `GET /health` - 健康检查

### 4. API接口调用

#### 请求示例

```bash
curl -X POST http://localhost:5000/api/interview-evaluation \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "我是人工智能专业应届毕业生，具有机器学习基础"
  }'
```

#### 响应格式

```json
{
  "text": "AI评价文本内容...",
  "scores": {
    "专业能力": 16,
    "逻辑分析问题能力": 15,
    "沟通表达能力": 14,
    "团队协作能力": 16,
    "学习意愿": 18,
    "总分": 79
  },
  "chart_base64": "iVBORw0KGgoAAAANSUhEUgAAA..."
}
```

## 🎨 前端集成

### HTML显示示例

```html
<img src="data:image/png;base64,{chart_base64}" alt="能力雷达图" />
```

### JavaScript处理示例

```javascript
async function getInterviewEvaluation(query) {
    const response = await fetch('/api/interview-evaluation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query })
    });
    
    const result = await response.json();
    
    // 显示文本内容
    document.getElementById('response').textContent = result.text;
    
    // 显示雷达图
    if (result.chart_base64) {
        const img = document.getElementById('radar-chart');
        img.src = `data:image/png;base64,${result.chart_base64}`;
        img.style.display = 'block';
    }
}
```

## 📋 评分格式要求

系统会自动检测以下格式的评分信息：

```
您的总分为：专业能力XX分，逻辑分析问题能力XX分，沟通表达能力XX分，团队协作能力XX分，学习意愿XX分，总分XX分。
```

**注意**：格式必须完全匹配，包括标点符号和措辞。

## ⚙️ 配置说明

### API配置

在 `api.py` 中修改默认配置：

```python
# 默认API配置
API_URL = "http://api-dify.sit.vcredit-t.com.local/v1/chat-messages"
API_KEY = "app-gee6RMNqRSBLqhx7LnwqUgzL"
```

### 雷达图样式

在 `create_radar_chart` 函数中可以自定义：

- 图表尺寸
- 颜色主题
- 字体设置
- 坐标轴范围

## 🐛 故障排除

### 常见问题

1. **中文字体显示问题**
   - 确保系统安装了中文字体（SimHei或Microsoft YaHei）
   - 可以修改 `plt.rcParams['font.sans-serif']` 设置

2. **API连接失败**
   - 检查网络连接
   - 验证API地址和密钥是否正确
   - 确认Dify服务是否可访问

3. **图片生成失败**
   - 检查matplotlib是否正确安装
   - 确认有足够的内存空间
   - 检查文件写入权限

### 调试模式

启用详细日志：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📁 文件结构

```
interview_assistant/
├── api.py                    # 主要API和雷达图功能
├── web_server_example.py     # Flask Web服务器
├── frontend_example.html     # 前端界面示例
├── requirements.txt          # 依赖包列表
├── README.md                # 项目说明文档
└── *.png                    # 生成的雷达图文件
```

## 🔜 后续计划

- [ ] 支持更多图表类型（柱状图、饼图等）
- [ ] 添加历史评分记录功能
- [ ] 支持批量评价处理
- [ ] 增加评分趋势分析
- [ ] 优化移动端显示效果

## 📄 许可证

本项目采用 MIT 许可证，详情请参阅 LICENSE 文件。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！ 