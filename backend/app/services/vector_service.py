import os
from app.utils.database import engine
from app.models.knowledge import KnowledgePoint
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, func

# 会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class VectorService:
    @staticmethod
    def generate_embedding(text):
        """生成文本的嵌入向量"""
        # 由于没有pgvector扩展，暂时返回None
        return None
    
    @staticmethod
    def update_knowledge_embeddings():
        """更新所有知识点的嵌入向量"""
        # 由于没有pgvector扩展，暂时返回成功
        return "嵌入向量更新完成（模拟）"
    
    @staticmethod
    def search_similar_knowledge(query, top_k=5):
        """搜索相似的知识点"""
        if not query:
            return []
        
        try:
            print(f"搜索查询: {query}")
            db = SessionLocal()
            try:
                # 使用基于文本的搜索，通过标题和描述的相似度排序
                # 这里使用简单的like查询来模拟搜索
                results = db.query(
                    KnowledgePoint
                ).filter(
                    or_(
                        KnowledgePoint.title.ilike(f"%{query}%"),
                        KnowledgePoint.description.ilike(f"%{query}%")
                    )
                ).limit(top_k).all()
                
                print(f"搜索结果数量: {len(results)}")
                for knowledge in results:
                    print(f"找到知识点: {knowledge.title}")
                
                # 转换结果格式
                search_results = []
                for knowledge in results:
                    search_results.append({
                        "id": knowledge.id,
                        "title": knowledge.title,
                        "description": knowledge.description or "",
                        "similarity": 0.0  # 模拟相似度值
                    })
                return search_results
            finally:
                db.close()
        except Exception as e:
            print(f"搜索失败: {e}")
            return []