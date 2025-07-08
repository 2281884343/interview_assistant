import requests
import json
import re
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
import base64
import io

def parse_scores(text):
    """
    解析评分文本，提取各项能力分数
    参数:
    - text: 包含评分信息的文本
    返回:
    - dict: 包含各项能力分数的字典，如果未找到评分信息则返回None
    """
    # 匹配评分格式的正则表达式
    pattern = r'您的总分为：专业能力(\d+)分，逻辑分析问题能力(\d+)分，沟通表达能力(\d+)分，团队协作能力(\d+)分，学习意愿(\d+)分，总分(\d+)分。'
    
    match = re.search(pattern, text)
    if match:
        scores = {
            '专业能力': int(match.group(1)),
            '逻辑分析问题能力': int(match.group(2)),
            '沟通表达能力': int(match.group(3)),
            '团队协作能力': int(match.group(4)),
            '学习意愿': int(match.group(5)),
            '总分': int(match.group(6))
        }
        return scores
    return None

def create_radar_chart(scores, save_path='radar_chart.png', return_base64=False):
    """
    根据评分创建雷达图
    参数:
    - scores: 包含各项能力分数的字典
    - save_path: 保存雷达图的路径
    - return_base64: 是否返回base64编码的图片数据
    """
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    
    # 能力维度标签
    categories = ['专业能力', '逻辑分析问题能力', '沟通表达能力', '团队协作能力', '学习意愿']
    
    # 获取各维度分数
    values = [scores[cat] for cat in categories]
    
    # 计算角度
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    
    # 闭合雷达图
    values += values[:1]
    angles += angles[:1]
    
    # 创建图形和极坐标轴
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    # 绘制雷达图
    ax.plot(angles, values, 'o-', linewidth=2, label=f'总分: {scores["总分"]}分', color='#1f77b4')
    ax.fill(angles, values, alpha=0.25, color='#1f77b4')
    
    # 设置标签
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12)
    
    # 设置径向轴
    ax.set_ylim(0, 20)  # 每个维度最大20分
    ax.set_yticks([5, 10, 15, 20])
    ax.set_yticklabels(['5分', '10分', '15分', '20分'], fontsize=10)
    ax.grid(True)
    
    # 添加标题和图例
    plt.title('面试评分雷达图', size=16, fontweight='bold', pad=20)
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1.0))
    
    # 保存图片
    plt.tight_layout()
    
    if return_base64:
        # 保存到内存缓冲区
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        
        # 转换为base64
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # 关闭缓冲区
        buffer.close()
        plt.close()  # 关闭图形以释放内存
        
        print("雷达图已生成为base64数据")
        return image_base64
    else:
        # 保存到文件
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        plt.close()  # 关闭图形以释放内存
        
        print(f"雷达图已保存到: {save_path}")
        return save_path

def call_dify_api(query, api_url = 'http://api-dify.sit.vcredit-t.com.local/v1', api_key = 'app-gee6RMNqRSBLqhx7LnwqUgzL', files=None,  user="abc-123", response_mode="streaming", return_chart_base64=False):
    """
    调用Dify API获取智能体响应
    参数:
    - api_url: Dify API的基础URL
    - api_key: 认证用的API密钥
    - query: 面试者回答内容
    - files: 要上传的文件列表，默认为None
    - user: 用户标识
    - response_mode: 响应模式，"streaming"或"blocking",默认"streaming"流式输出
    - return_chart_base64: 是否在响应中包含雷达图的base64数据
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "inputs": {},
        "query": query,
        "response_mode": response_mode,
        "user": user
    }
    
    if files:
        data["files"] = files
    
    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=data,
            stream=response_mode == "streaming"
        )
        
        response.raise_for_status()
        
        # 流式响应处理
        if response_mode == "streaming":
            full_answer = []
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8').lstrip('data: ')
                    if line == '[DONE]':
                        break
                    try:
                        json_data = json.loads(line)
                        if "answer" in json_data:
                            full_answer.append(json_data["answer"])
                    except json.JSONDecodeError:
                        continue
            # 拼接完整回答
            result = ''.join(full_answer)
            
            # 检查是否包含评分信息，如果有则生成雷达图
            scores = parse_scores(result)
            chart_base64 = None
            
            if scores:
                print("检测到评分信息，正在生成雷达图...")
                if return_chart_base64:
                    chart_base64 = create_radar_chart(scores, return_base64=True)
                else:
                    create_radar_chart(scores)
            
            # 根据参数决定返回格式
            if return_chart_base64:
                return {
                    "text": result,
                    "scores": scores,
                    "chart_base64": chart_base64
                }
            else:
                return result
        # 阻塞式响应处理
        else:
            result = response.json()
            chart_base64 = None
            scores = None
            
            # 对于阻塞式响应，也检查评分信息
            if isinstance(result, dict) and 'answer' in result:
                scores = parse_scores(result['answer'])
                if scores:
                    print("检测到评分信息，正在生成雷达图...")
                    if return_chart_base64:
                        chart_base64 = create_radar_chart(scores, return_base64=True)
                    else:
                        create_radar_chart(scores)
            
            # 根据参数决定返回格式
            if return_chart_base64:
                return {
                    "text": result,
                    "scores": scores,
                    "chart_base64": chart_base64
                }
            else:
                return result
            
    except requests.exceptions.RequestException as e:
        print(f"API调用失败: {e}")
        return None

def test_radar_chart():
    """
    测试雷达图功能的示例函数
    """
    # 模拟一个包含评分的响应
    test_response = "根据您的回答，您的总分为：专业能力18分，逻辑分析问题能力16分，沟通表达能力15分，团队协作能力17分，学习意愿19分，总分85分。这是一个不错的表现！"
    
    print("测试解析评分功能:")
    scores = parse_scores(test_response)
    if scores:
        print("成功解析评分:", scores)
        print("正在生成雷达图文件...")
        create_radar_chart(scores, 'test_radar_chart.png')
        
        print("正在生成base64雷达图...")
        base64_data = create_radar_chart(scores, return_base64=True)
        print(f"base64数据长度: {len(base64_data)} 字符")
        print(f"base64数据前50字符: {base64_data[:50]}...")
    else:
        print("未检测到评分信息")

def call_dify_api_for_frontend(query, api_url = 'http://api-dify.sit.vcredit-t.com.local/v1', api_key = 'app-gee6RMNqRSBLqhx7LnwqUgzL', files=None, user="abc-123", response_mode="streaming"):
    """
    专门为前端设计的API调用函数，自动返回结构化数据包含base64图片
    返回格式:
    {
        "text": "响应文本",
        "scores": {"专业能力": 18, ...} 或 None,
        "chart_base64": "base64图片数据" 或 None
    }
    """
    return call_dify_api(
        query=query,
        api_url=api_url,
        api_key=api_key,
        files=files,
        user=user,
        response_mode=response_mode,
        return_chart_base64=True
    )

# 使用示例
if __name__ == "__main__":
    # 配置参数
    API_URL = "http://api-dify.sit.vcredit-t.com.local/v1/chat-messages"
    API_KEY = "app-gee6RMNqRSBLqhx7LnwqUgzL" 
    USER_QUERY = "你好，我是人工智能专业应届毕业生"
    
    print("=== 面试助手API调用工具 ===")
    print("功能说明：")
    print("1. 调用Dify API获取面试评价")
    print("2. 自动检测评分信息并生成雷达图")
    print("3. 雷达图包含五个维度：专业能力、逻辑分析问题能力、沟通表达能力、团队协作能力、学习意愿")
    print("4. 支持返回base64图片数据供前端使用")
    print()
    
    # 测试雷达图功能
    print("测试雷达图功能：")
    test_radar_chart()
    print()
    
    # 调用API（传统模式，保存图片文件）
    print("调用Dify API（传统模式）：")
    response = call_dify_api(
        api_url=API_URL,
        api_key=API_KEY,
        query=USER_QUERY,
        response_mode="streaming"
    )
    
    if response:
        print("API响应成功")
        print("响应内容:", response[:200] + "..." if len(response) > 200 else response)
    else:
        print("API调用失败")
    
    print("\n" + "="*50)
    
    # 调用API（前端模式，返回结构化数据）
    print("调用Dify API（前端模式）：")
    frontend_response = call_dify_api_for_frontend(
        api_url=API_URL,
        api_key=API_KEY,
        query=USER_QUERY,
        response_mode="streaming"
    )
    
    if frontend_response:
        print("前端API响应成功")
        print("响应结构:")
        print(f"- 文本内容: {str(frontend_response.get('text', ''))[:100]}...")
        print(f"- 评分数据: {frontend_response.get('scores')}")
        print(f"- 图片数据: {'有' if frontend_response.get('chart_base64') else '无'}")
        if frontend_response.get('chart_base64'):
            print(f"- 图片base64长度: {len(frontend_response['chart_base64'])} 字符")
    else:
        print("前端API调用失败")
