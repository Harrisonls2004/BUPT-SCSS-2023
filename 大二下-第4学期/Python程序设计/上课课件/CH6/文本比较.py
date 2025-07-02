'''
import jieba
from collections import Counter

def read_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_ngrams(text, n=2):
    words = [word for word in jieba.lcut(text) if len(word) > 1]
    words = [word.strip() for word in words if word.strip()]
    ngrams = zip(*[words[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]

def compare_books(file1, file2, n=2):
    # 处理第一本书
    text1 = read_text(file1)
    ngrams1 = get_ngrams(text1, n)
    counter1 = Counter(ngrams1)
    
    # 处理第二本书
    text2 = read_text(file2)
    ngrams2 = get_ngrams(text2, n)
    counter2 = Counter(ngrams2)
    
    # 获取共同n-gram
    common_ngrams = counter1.keys() & counter2.keys()
    
    # 整理结果并按总频次排序
    results = []
    for ng in common_ngrams:
        results.append((ng, counter1[ng], counter2[ng]))
    
    # 按总出现次数降序排序
    results.sort(key=lambda x: x[1]+x[2], reverse=True)
    return results

if __name__ == "__main__":
    n = 2  # 可修改n-gram长度
    common_words = compare_books('C:/Users/1/Desktop/sanguo.txt', 'C:/Users/1/Desktop/bailuyuan.txt', n)
    
    # 打印完整结果
    print(f"共发现 {len(common_words)} 个共同{n}-gram")
    print("="*40)
    print(f"{'n-gram':<10} | 《三国》次数 | 《白鹿原》次数")
    print("-"*40)
    
    # 遍历所有结果（移除切片限制）
    for word, cnt1, cnt2 in common_words:  # 已移除[:20]切片
        print(f"{word:<10} | {cnt1:<10} | {cnt2:<10}")
    
    # 添加结束分隔线
    print("="*40)
    print("全部结果输出完成")

'''

import jieba
from collections import Counter
import os

def read_text(file_path):
    """读取文本文件内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_two_character_words(text):
    """提取文本中所有二字词语"""
    # 精确模式分词
    words = jieba.lcut(text)
    # 过滤：保留长度=2的中文词语，且非纯符号
    return [word for word in words 
            if len(word) == 2 
            and '\u4e00' <= word[0] <= '\u9fff'  # 确保是中文
            and '\u4e00' <= word[1] <= '\u9fff']

def compare_two_character_words(file1, file2):
    """比较两本书的二字词语共现情况"""
    # 处理第一本书
    text1 = read_text(file1)
    words1 = get_two_character_words(text1)
    counter1 = Counter(words1)
    
    # 处理第二本书
    text2 = read_text(file2)
    words2 = get_two_character_words(text2)
    counter2 = Counter(words2)
    
    # 获取共同词语（使用集合交集）
    common_words = counter1.keys() & counter2.keys()
    
    # 整理结果并按总频次排序
    results = []
    for word in common_words:
        results.append((word, counter1[word], counter2[word]))
    
    # 按总出现次数降序排序
    results.sort(key=lambda x: x[1]+x[2], reverse=True)
    return results

if __name__ == "__main__":
    # 文件路径处理（使用原始字符串避免转义问题）
    file1 = r'C:/Users/1/Desktop/sanguo.txt'  # 替换实际路径
    file2 = r'C:/Users/1/Desktop/bailuyuan.txt'
    

    # 检查文件是否存在
    if not os.path.exists(file1) or not os.path.exists(file2):
        print("错误：文件路径不存在！")
        exit()
    
    # 执行比较
    common_words = compare_two_character_words(file1, file2)
    
    # 打印完整结果
    print(f"共发现 {len(common_words)} 个共同二字词语")
    print("="*45)
    print(f"{'词语':<8} | 《三国》出现次数 | 《白鹿原》出现次数")
    print("-"*45)
    for word, cnt1, cnt2 in common_words[0:20]:  # 仅打印前20个结果
        print(f"{word:<8} | {cnt1:<14} | {cnt2:<14}")
    print("="*45)


