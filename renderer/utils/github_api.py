import os
from typing import List, Dict, Optional, Any
from github import Github, Repository, Issue, Label
import sys

# 添加父目录到路径，以便导入config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class GitHubAPI:
    """GitHub API封装类，使用PyGitHub库"""
    
    def __init__(self, owner: str = None, repo: str = None, token: str = None):
        """
        初始化GitHub API客户端
        
        Args:
            owner: GitHub仓库所有者（默认从环境变量获取）
            repo: GitHub仓库名称（默认从环境变量获取）
            token: GitHub个人访问令牌（默认从环境变量获取）
        """
        self.owner = owner or config.GITHUB_OWNER
        self.repo = repo or config.GITHUB_REPO
        self.token = token or config.GITHUB_TOKEN
        
        if not self.owner or not self.repo:
            raise ValueError("GitHub仓库所有者和名称必须指定")
        
        # 初始化GitHub客户端
        if self.token:
            self.github = Github(self.token)
        else:
            self.github = Github()  # 无令牌，有速率限制
        
        # 获取仓库对象
        try:
            self.repository = self.github.get_repo(f"{self.owner}/{self.repo}")
        except Exception as e:
            print(f"获取仓库失败: {e}")
            raise
    
    def get_issues(self, state: str = "open", labels: List[str] = None, 
                   page: int = 1, per_page: int = 100) -> List[Dict[str, Any]]:
        """
        获取仓库的Issues
        
        Args:
            state: Issue状态（open, closed, all）
            labels: 标签过滤列表
            page: 页码（PyGitHub自动处理分页）
            per_page: 每页数量
            
        Returns:
            Issue数据列表
        """
        try:
            # 构建过滤参数
            kwargs = {"state": state}
            if labels:
                kwargs["labels"] = labels
            
            # 获取Issues
            issues = self.repository.get_issues(**kwargs)
            
            # 转换为字典列表
            issue_list = []
            for i, issue in enumerate(issues):
                if i >= config.MAX_ARTICLES:
                    break
                
                issue_data = self._issue_to_dict(issue)
                issue_list.append(issue_data)
            
            return issue_list
            
        except Exception as e:
            print(f"获取Issues失败: {e}")
            return []
    
    def get_blog_articles(self) -> List[Dict[str, Any]]:
        """
        获取博客文章（带特定标签的Issues）
        
        Returns:
            博客文章列表
        """
        label = config.ARTICLE_LABEL
        return self.get_issues(state="open", labels=[label])
    
    def get_issue(self, issue_number: int) -> Optional[Dict[str, Any]]:
        """
        获取单个Issue详情
        
        Args:
            issue_number: Issue编号
            
        Returns:
            Issue数据字典
        """
        try:
            issue = self.repository.get_issue(issue_number)
            return self._issue_to_dict(issue)
        except Exception as e:
            print(f"获取Issue #{issue_number}失败: {e}")
            return None
    
    def get_labels(self) -> List[Dict[str, Any]]:
        """
        获取仓库所有标签
        
        Returns:
            标签列表
        """
        try:
            labels = self.repository.get_labels()
            label_list = []
            for label in labels:
                label_data = {
                    "name": label.name,
                    "color": label.color,
                    "description": label.description,
                    "url": label.url,
                }
                label_list.append(label_data)
            return label_list
        except Exception as e:
            print(f"获取标签失败: {e}")
            return []
    
    def get_rate_limit(self) -> Dict[str, Any]:
        """
        获取API速率限制信息
        
        Returns:
            速率限制信息
        """
        try:
            rate_limit = self.github.get_rate_limit()
            return {
                "core": {
                    "limit": rate_limit.core.limit,
                    "remaining": rate_limit.core.remaining,
                    "reset": rate_limit.core.reset.isoformat(),
                },
                "search": {
                    "limit": rate_limit.search.limit,
                    "remaining": rate_limit.search.remaining,
                    "reset": rate_limit.search.reset.isoformat(),
                },
            }
        except Exception as e:
            print(f"获取速率限制失败: {e}")
            return {}
    
    def _issue_to_dict(self, issue: Issue) -> Dict[str, Any]:
        """
        将Issue对象转换为字典
        
        Args:
            issue: PyGitHub Issue对象
            
        Returns:
            Issue数据字典
        """
        # 提取标签
        labels = [label.name for label in issue.labels]
        
        # 提取用户信息
        user = {
            "login": issue.user.login,
            "avatar_url": issue.user.avatar_url,
            "html_url": issue.user.html_url,
        }
        
        return {
            "number": issue.number,
            "title": issue.title,
            "body": issue.body or "",
            "state": issue.state,
            "created_at": issue.created_at.isoformat(),
            "updated_at": issue.updated_at.isoformat(),
            "closed_at": issue.closed_at.isoformat() if issue.closed_at else None,
            "labels": labels,
            "user": user,
            "comments": issue.comments,
            "html_url": issue.html_url,
            "url": issue.url,
            "milestone": issue.milestone.title if issue.milestone else None,
            "locked": issue.locked,
            "assignees": [assignee.login for assignee in issue.assignees],
        }
    
    def test_connection(self) -> bool:
        """
        测试GitHub API连接
        
        Returns:
            是否连接成功
        """
        try:
            # 尝试获取仓库信息
            repo_name = self.repository.full_name
            print(f"成功连接到仓库: {repo_name}")
            
            # 显示速率限制
            rate_limit = self.get_rate_limit()
            if rate_limit:
                core_remaining = rate_limit.get("core", {}).get("remaining", 0)
                print(f"API调用剩余次数: {core_remaining}")
            
            return True
        except Exception as e:
            print(f"连接测试失败: {e}")
            return False


def get_github_client() -> GitHubAPI:
    """获取GitHub API客户端实例"""
    return GitHubAPI()


if __name__ == "__main__":
    # 测试GitHub API连接
    print("测试GitHub API连接...")
    
    try:
        client = get_github_client()
        
        if client.test_connection():
            print("\n获取博客文章...")
            articles = client.get_blog_articles()
            print(f"找到 {len(articles)} 篇博客文章")
            
            for article in articles[:3]:  # 显示前3篇
                print(f"  #{article['number']}: {article['title']}")
                print(f"    标签: {', '.join(article['labels'])}")
                print(f"    创建时间: {article['created_at']}")
        else:
            print("连接测试失败")
            
    except Exception as e:
        print(f"错误: {e}")