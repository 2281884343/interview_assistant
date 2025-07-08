from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import sys
import os

# 导入我们的API函数
from api import call_dify_api_for_frontend

app = Flask(__name__)
CORS(app)  # 允许跨域请求

@app.route('/')
def index():
    """返回前端页面"""
    try:
        with open('frontend_example.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return """
        <h1>面试助手API服务器</h1>
        <p>前端文件未找到，请确保 frontend_example.html 文件存在</p>
        <p>您可以直接访问 <a href="/api/interview-evaluation">/api/interview-evaluation</a> 接口进行测试</p>
        """

@app.route('/api/interview-evaluation', methods=['POST'])
def interview_evaluation():
    """面试评价API接口"""
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({
                'error': '请求数据格式错误',
                'message': '请发送JSON格式的数据'
            }), 400
        
        query = data.get('query', '').strip()
        if not query:
            return jsonify({
                'error': '参数错误',
                'message': '请提供query参数'
            }), 400
        
        # 可选参数
        api_url = data.get('api_url', 'http://api-dify.sit.vcredit-t.com.local/v1/chat-messages')
        api_key = data.get('api_key', 'app-gee6RMNqRSBLqhx7LnwqUgzL')
        files = data.get('files')
        user = data.get('user', 'web-user')
        response_mode = data.get('response_mode', 'streaming')
        
        # 调用面试评价API
        result = call_dify_api_for_frontend(
            query=query,
            api_url=api_url,
            api_key=api_key,
            files=files,
            user=user,
            response_mode=response_mode
        )
        
        if result is None:
            return jsonify({
                'error': 'API调用失败',
                'message': '无法连接到Dify服务'
            }), 500
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': '服务器错误',
            'message': str(e)
        }), 500

@app.route('/api/test', methods=['GET'])
def test_api():
    """测试API接口"""
    test_query = "你好，我是人工智能专业应届毕业生，具有扎实的机器学习理论基础"
    
    try:
        result = call_dify_api_for_frontend(
            query=test_query,
            response_mode="streaming"
        )
        
        return jsonify({
            'status': 'success',
            'test_query': test_query,
            'result': result
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'service': '面试助手API服务',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print("🚀 面试助手API服务器启动中...")
    print("📍 访问地址: http://localhost:5000")
    print("📋 API文档:")
    print("   GET  /              - 前端页面")
    print("   POST /api/interview-evaluation - 面试评价接口")
    print("   GET  /api/test      - 测试接口")
    print("   GET  /health        - 健康检查")
    print()
    print("📊 API使用示例:")
    print("curl -X POST http://localhost:5000/api/interview-evaluation \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{\"query\": \"我是AI专业学生，请评价我的能力\"}'")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000) 