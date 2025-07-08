# 面试助手 API 接口文档

## 概述

面试助手 API 提供了一套完整的面试评估和可视化功能，包括调用 Dify AI 智能体、解析评分数据、生成雷达图等核心功能。

## 目录

1. [核心功能函数](#核心功能函数)
2. [工具函数](#工具函数)
3. [测试函数](#测试函数)
4. [使用示例](#使用示例)

---

## 核心功能函数

### 1. call_dify_api

调用 Dify API 获取 AI 智能体的面试评估响应。

**函数签名：**
```python
call_dify_api(query, api_url='http://api-dify.sit.vcredit-t.com.local/v1', 
              api_key='app-gee6RMNqRSBLqhx7LnwqUgzL', files=None, 
              user="abc-123", response_mode="streaming", return_chart_base64=False)
```

**参数说明：**

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `query` | str | 是 | - | 面试者回答内容或问题 |
| `api_url` | str | 否 | `http://api-dify.sit.vcredit-t.com.local/v1` | Dify API 的基础 URL |
| `api_key` | str | 否 | `app-gee6RMNqRSBLqhx7LnwqUgzL` | 认证用的 API 密钥 |
| `files` | list | 否 | None | 要上传的文件列表 |
| `user` | str | 否 | "abc-123" | 用户标识符 |
| `response_mode` | str | 否 | "streaming" | 响应模式："streaming"（流式）或"blocking"（阻塞式） |
| `return_chart_base64` | bool | 否 | False | 是否在响应中包含雷达图的 base64 数据 |

**返回值：**

- 当 `return_chart_base64=False` 时：
  - 返回类型：`str` | `dict` | `None`
  - 返回智能体的响应文本（streaming模式）或完整响应对象（blocking模式）

- 当 `return_chart_base64=True` 时：
  - 返回类型：`dict`
  - 返回格式：
    ```python
    {
        "text": "响应文本内容",
        "scores": {"专业能力": 18, "逻辑分析问题能力": 16, ...} | None,
        "chart_base64": "base64编码的图片数据" | None
    }
    ```

**异常处理：**
- 网络错误或API调用失败时返回 `None`
- 自动打印错误信息到控制台

---

### 2. call_dify_api_for_frontend

专门为前端设计的 API 调用函数，自动返回包含 base64 图片的结构化数据。

**函数签名：**
```python
call_dify_api_for_frontend(query, api_url='http://api-dify.sit.vcredit-t.com.local/v1',
                          api_key='app-gee6RMNqRSBLqhx7LnwqUgzL', files=None, 
                          user="abc-123", response_mode="streaming")
```

**参数说明：**

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `query` | str | 是 | - | 面试者回答内容或问题 |
| `api_url` | str | 否 | `http://api-dify.sit.vcredit-t.com.local/v1` | Dify API 的基础 URL |
| `api_key` | str | 否 | `app-gee6RMNqRSBLqhx7LnwqUgzL` | 认证用的 API 密钥 |
| `files` | list | 否 | None | 要上传的文件列表 |
| `user` | str | 否 | "abc-123" | 用户标识符 |
| `response_mode` | str | 否 | "streaming" | 响应模式："streaming"或"blocking" |

**返回值：**
- 返回类型：`dict`
- 返回格式：
  ```python
  {
      "text": "AI智能体的响应文本",
      "scores": {
          "专业能力": 18,
          "逻辑分析问题能力": 16,
          "沟通表达能力": 15,
          "团队协作能力": 17,
          "学习意愿": 19,
          "总分": 85
      } | None,  # 如果响应中包含评分信息
      "chart_base64": "iVBORw0KGgoAAAANSUhEUgAA..." | None  # 雷达图的base64数据
  }
  ```

---

## 工具函数

### 3. parse_scores

解析包含评分信息的文本，提取各项能力分数。

**函数签名：**
```python
parse_scores(text)
```

**参数说明：**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `text` | str | 是 | 包含评分信息的文本 |

**支持的评分格式：**
```
您的总分为：专业能力X分，逻辑分析问题能力X分，沟通表达能力X分，团队协作能力X分，学习意愿X分，总分X分。
```

**返回值：**
- 成功时返回 `dict`：
  ```python
  {
      "专业能力": 18,
      "逻辑分析问题能力": 16,
      "沟通表达能力": 15,
      "团队协作能力": 17,
      "学习意愿": 19,
      "总分": 85
  }
  ```
- 未找到评分信息时返回 `None`

---

### 4. create_radar_chart

根据评分数据创建雷达图可视化。

**函数签名：**
```python
create_radar_chart(scores, save_path='radar_chart.png', return_base64=False)
```

**参数说明：**

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `scores` | dict | 是 | - | 包含各项能力分数的字典 |
| `save_path` | str | 否 | 'radar_chart.png' | 保存雷达图的文件路径 |
| `return_base64` | bool | 否 | False | 是否返回 base64 编码的图片数据 |

**scores 参数格式：**
```python
{
    "专业能力": 18,
    "逻辑分析问题能力": 16,
    "沟通表达能力": 15,
    "团队协作能力": 17,
    "学习意愿": 19,
    "总分": 85
}
```

**返回值：**
- 当 `return_base64=False` 时：返回 `str`（保存的文件路径）
- 当 `return_base64=True` 时：返回 `str`（base64编码的图片数据）

**图表特性：**
- 五个维度：专业能力、逻辑分析问题能力、沟通表达能力、团队协作能力、学习意愿
- 每个维度评分范围：0-20分
- 支持中文标签显示
- 高分辨率输出（300 DPI）

---

## 测试函数

### 5. test_radar_chart

测试雷达图功能的示例函数，用于验证评分解析和图表生成功能。

**函数签名：**
```python
test_radar_chart()
```

**参数：** 无

**返回值：** 无

**功能：**
- 使用模拟评分数据测试解析功能
- 生成测试雷达图文件 `test_radar_chart.png`
- 测试 base64 编码功能
- 输出测试结果到控制台

---

## 使用示例

### 基本使用示例

```python
from api import call_dify_api, call_dify_api_for_frontend

# 1. 基本API调用
response = call_dify_api(
    query="我是计算机专业的应届毕业生，有Python和机器学习项目经验",
    response_mode="streaming"
)
print(response)

# 2. 前端专用API调用
frontend_response = call_dify_api_for_frontend(
    query="我在实习期间主要负责数据分析工作",
    response_mode="streaming"
)

if frontend_response['scores']:
    print("评分结果:", frontend_response['scores'])
    print("总分:", frontend_response['scores']['总分'])
    
if frontend_response['chart_base64']:
    print("已生成雷达图，可直接在前端显示")
```

### 自定义配置示例

```python
# 使用自定义API配置
custom_response = call_dify_api(
    query="描述一下你的团队合作经验",
    api_url="https://your-custom-api.com/v1",
    api_key="your-custom-key",
    user="user-001",
    response_mode="blocking",
    return_chart_base64=True
)
```

### 雷达图生成示例

```python
from api import parse_scores, create_radar_chart

# 解析AI响应中的评分
ai_response = "根据您的回答，您的总分为：专业能力18分，逻辑分析问题能力16分，沟通表达能力15分，团队协作能力17分，学习意愿19分，总分85分。"
scores = parse_scores(ai_response)

if scores:
    # 生成并保存雷达图
    file_path = create_radar_chart(scores, save_path='my_interview_result.png')
    
    # 获取base64数据
    base64_data = create_radar_chart(scores, return_base64=True)
```

---

## 错误处理

### 常见错误类型

1. **网络连接错误**
   - API调用函数会捕获 `requests.exceptions.RequestException`
   - 返回 `None` 并输出错误信息

2. **评分解析失败**
   - `parse_scores` 函数在无法匹配评分格式时返回 `None`
   - 这是正常行为，表示文本中不包含标准格式的评分信息

3. **图表生成失败**
   - 通常由于字体问题或数据格式错误
   - 函数会使用备用字体配置

### 最佳实践

1. **API调用前检查网络连接**
2. **使用前端专用函数 `call_dify_api_for_frontend` 获得结构化返回**
3. **始终检查返回值是否为 `None`**
4. **在生产环境中使用自定义的API密钥和URL**

---

## 配置说明

### 默认配置

```python
# 默认API配置
DEFAULT_API_URL = "http://api-dify.sit.vcredit-t.com.local/v1"
DEFAULT_API_KEY = "app-gee6RMNqRSBLqhx7LnwqUgzL"
DEFAULT_USER = "abc-123"

# 雷达图配置
RADAR_DIMENSIONS = ["专业能力", "逻辑分析问题能力", "沟通表达能力", "团队协作能力", "学习意愿"]
MAX_SCORE_PER_DIMENSION = 20
```

### 字体配置

系统自动配置中文字体支持：
- 优先使用 `SimHei`（黑体）
- 备用字体 `Microsoft YaHei`（微软雅黑）

---

## 版本信息

- **当前版本**: v1.0
- **Python要求**: >= 3.6
- **主要依赖**:
  - `requests`
  - `matplotlib`
  - `numpy`
  - `json`（标准库）
  - `re`（标准库）
  - `base64`（标准库）
  - `io`（标准库） 