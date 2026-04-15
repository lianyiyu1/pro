import os
import time
import urllib.request
from urllib.error import HTTPError, URLError


def list_files(directory):
    """
    列出某个目录下有哪些文件（包括文件的基本属性、大小等信息）
    
    Args:
        directory (str): 目录路径
    
    Returns:
        dict: 包含文件信息的字典
    """
    try:
        if not os.path.exists(directory):
            return {"error": f"目录不存在: {directory}"}
        
        if not os.path.isdir(directory):
            return {"error": f"路径不是目录: {directory}"}
        
        files = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            is_dir = os.path.isdir(item_path)
            size = os.path.getsize(item_path) if not is_dir else 0
            mtime = os.path.getmtime(item_path)
            mtime_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
            
            files.append({
                "name": item,
                "path": item_path,
                "is_directory": is_dir,
                "size": size,  # 字节
                "last_modified": mtime_str
            })
        
        return {
            "success": True,
            "directory": directory,
            "file_count": len(files),
            "files": files
        }
    except Exception as e:
        return {"error": str(e)}


def rename_file(directory, old_name, new_name):
    """
    修改某个目录下某个文件的名字
    
    Args:
        directory (str): 目录路径
        old_name (str): 旧文件名
        new_name (str): 新文件名
    
    Returns:
        dict: 操作结果
    """
    try:
        old_path = os.path.join(directory, old_name)
        new_path = os.path.join(directory, new_name)
        
        if not os.path.exists(old_path):
            return {"error": f"文件不存在: {old_path}"}
        
        if os.path.exists(new_path):
            return {"error": f"新文件名已存在: {new_path}"}
        
        os.rename(old_path, new_path)
        
        return {
            "success": True,
            "old_path": old_path,
            "new_path": new_path
        }
    except Exception as e:
        return {"error": str(e)}


def delete_file(directory, filename):
    """
    删除某个目录下的某个文件
    
    Args:
        directory (str): 目录路径
        filename (str): 文件名
    
    Returns:
        dict: 操作结果
    """
    try:
        file_path = os.path.join(directory, filename)
        
        if not os.path.exists(file_path):
            return {"error": f"文件不存在: {file_path}"}
        
        if os.path.isdir(file_path):
            return {"error": f"路径是目录，不能直接删除: {file_path}"}
        
        os.remove(file_path)
        
        return {
            "success": True,
            "deleted_path": file_path
        }
    except Exception as e:
        return {"error": str(e)}


def create_file(directory, filename, content):
    """
    在某个目录下新建1个文件，并且写入内容
    
    Args:
        directory (str): 目录路径
        filename (str): 文件名
        content (str): 文件内容
    
    Returns:
        dict: 操作结果
    """
    try:
        if not os.path.exists(directory):
            return {"error": f"目录不存在: {directory}"}
        
        if not os.path.isdir(directory):
            return {"error": f"路径不是目录: {directory}"}
        
        file_path = os.path.join(directory, filename)
        
        if os.path.exists(file_path):
            return {"error": f"文件已存在: {file_path}"}
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "success": True,
            "file_path": file_path,
            "content_length": len(content)
        }
    except Exception as e:
        return {"error": str(e)}


def read_file(directory, filename):
    """
    读取某个目录下的某个文件的内容
    
    Args:
        directory (str): 目录路径
        filename (str): 文件名
    
    Returns:
        dict: 包含文件内容的字典
    """
    try:
        file_path = os.path.join(directory, filename)
        
        if not os.path.exists(file_path):
            return {"error": f"文件不存在: {file_path}"}
        
        if os.path.isdir(file_path):
            return {"error": f"路径是目录，无法读取: {file_path}"}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        size = os.path.getsize(file_path)
        
        return {
            "success": True,
            "file_path": file_path,
            "size": size,
            "content": content
        }
    except Exception as e:
        return {"error": str(e)}


def curl(url, timeout=30):
    """
    通过curl访问网页并返回网页内容
    
    Args:
        url (str): 网页URL
        timeout (int): 超时时间（秒），默认30秒
    
    Returns:
        dict: 包含网页内容的字典
    """
    try:
        # Clean URL - remove backticks and whitespace
        url = url.strip().strip('`')
        
        # Encode URL properly, including path with non-ASCII characters
        from urllib.parse import quote, urlparse, urlunparse
        
        # Parse the URL
        parsed = urlparse(url)
        
        # Encode the path if it contains non-ASCII characters
        encoded_path = quote(parsed.path, safe='/:')
        
        # Encode the query string
        if parsed.query:
            # Split query into components
            query_parts = parsed.query.split('&')
            encoded_parts = []
            for part in query_parts:
                if '=' in part:
                    key, value = part.split('=', 1)
                    # Encode the value
                    encoded_value = quote(value, safe='')
                    encoded_parts.append(f"{key}={encoded_value}")
                else:
                    encoded_parts.append(part)
            # Reconstruct the query
            encoded_query = '&'.join(encoded_parts)
        else:
            encoded_query = ''
        
        # Reconstruct the URL with encoded parts
        encoded_url = urlunparse((
            parsed.scheme,
            parsed.netloc,
            encoded_path,
            parsed.params,
            encoded_query,
            parsed.fragment
        ))
        
        # Create request with headers
        req = urllib.request.Request(encoded_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        req.add_header('Accept-Language', 'zh-CN,zh;q=0.9,en;q=0.8')
        
        # Open URL with timeout
        with urllib.request.urlopen(req, timeout=timeout) as response:
            # Get response status and headers
            status_code = response.getcode()
            headers = dict(response.getheaders())
            
            # Read content
            content = response.read().decode('utf-8', errors='replace')
            content_length = len(content)
        
        return {
            "success": True,
            "url": url,
            "encoded_url": encoded_url,
            "status_code": status_code,
            "content_length": content_length,
            "headers": headers,
            "content": content[:10000]  # Limit content to 10KB to avoid excessive output
        }
    except HTTPError as e:
        return {
            "error": f"HTTP Error {e.code}: {e.reason}",
            "url": url,
            "status_code": e.code
        }
    except URLError as e:
        return {
            "error": f"URL Error: {e.reason}",
            "url": url
        }
    except Exception as e:
        return {"error": str(e), "url": url}
