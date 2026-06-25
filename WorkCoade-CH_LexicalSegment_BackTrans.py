"""
20260625
The examples were translated from English to Chinese. In order to back translate
the translated Chinese text, we have to do the following steps:
1. Input the Chinese text.
2. Segment the texts into words by words. This code employed the database Jieba to segment the Chinese text.
3. Translating the words.
4. Marking the words' with Chinese Pinyin.
5. Back translating the Chinese text into English. 
The work via the API of Deepseek. 

"""


import os
import jieba
from openai import OpenAI
from pypinyin import pinyin, Style

# ------------------ 配置 ------------------
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "你的API密钥")
BASE_URL = "https://api.deepseek.com/v1"
MODEL = "deepseek-chat"

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=BASE_URL)

def call_deepseek(prompt, temperature=0.2):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=1024
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        # 这里会打印具体的错误类型和描述
        print(f"❌ API 调用出错：{type(e).__name__} - {e}")
        return ""

def word_by_word_translation(word_list):
    """
    将分词列表逐词翻译成英文（词级对应）。
    返回与输入顺序一致的英文词列表，英文短语用下划线连接。
    """
    words_str = "[" + ", ".join(word_list) + "]"
    prompt = f"""任务：把以下中文词语列表中的每一个词都翻译成英文。
要求：
- 严格词级对应，忽略语法。
- 如果某个中文词的英文翻译包含多个单词，请用下划线连接（例如 New_York）。
- 输出只保留英文词序列，用空格分隔，顺序与输入完全一致。
- 不要添加任何解释或额外文字。

输入：{words_str}"""

    result = call_deepseek(prompt)
    if not result:
        return ["[error]"] * len(word_list)

    translated = result.split()
    if len(translated) != len(word_list):
        print("警告：逐词翻译数量不匹配，已做填充处理。")
        while len(translated) < len(word_list):
            translated.append("[?]")
        translated = translated[:len(word_list)]
    return translated

def overall_translation(paragraph):
    """翻译整个段落，得到准确流畅的英文"""
    prompt = f"请将以下中文段落翻译成准确、地道的英文：\n{paragraph}"
    return call_deepseek(prompt, temperature=0.1)

def main():
    # 1. 输入汉语文段
    print("请输入要处理的汉语文段（输入完成后按回车）：")
    paragraph = input().strip()
    if not paragraph:
        print("输入为空，程序退出。")
        return

    # 2. jieba 分词
    words = list(jieba.cut(paragraph, cut_all=False))
    words = [w.strip() for w in words if w.strip()]
    segmented = " / ".join(words)

    # 2.5 获取每个词的拼音（带声调）
    pinyin_list = [p[0] for p in pinyin(words, style=Style.TONE)]
    pinyin_str = " / ".join(pinyin_list)

    # 3. 逐词翻译（词级对应）
    print("正在进行词级翻译……")
    word_trans = word_by_word_translation(words)
    word_trans_str = " / ".join(word_trans)

    # 4. 整体翻译
    print("正在进行整体翻译……")
    full_trans = overall_translation(paragraph)

    # 5. 保存结果到 txt 文件
    output_filename = "translation_output.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("原始文本：\n")
        f.write(paragraph + "\n\n")
        f.write("分词结果（jieba）：\n")
        f.write(segmented + "\n\n")
        f.write("分词拼音：\n")
        f.write(pinyin_str + "\n\n")
        f.write("逐词翻译（词级对应）：\n")
        f.write(word_trans_str + "\n\n")
        f.write("整体译文（准确英文）：\n")
        f.write(full_trans + "\n")

    print(f"处理完成！结果已保存至 {output_filename}")
    print("=" * 40)
    print("原始文本:", paragraph)
    print("分词结果:", segmented)
    print("分词拼音:", pinyin_str)
    print("逐词翻译:", word_trans_str)
    print("整体译文:", full_trans)

if __name__ == "__main__":
    main()
